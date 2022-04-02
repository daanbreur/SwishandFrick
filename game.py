from __future__ import annotations
from distutils.spawn import spawn

import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pathlib import Path
from turtle import Screen
from typing import List

import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_MINUS, K_EQUALS, K_ESCAPE, K_r, K_0
from pygame.locals import KEYDOWN, VIDEORESIZE, QUIT

import pytmx
from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from enums import GameState, Skills, UserEvents

from Screens.MainMenu import MainMenu
from Screens.PausedMenu import PausedMenu
from Screens.Ingame import Ingame
from Screens.SettingsMenu import SettingsMenu

from Puzzles.SimonSays import SimonSays
from Puzzles.MorseCode import MorseCode

from ToastManager import ToastManager

from Player import Player
from utils import *
from constants import *

class Game:
  map_path = resource_path(RESOURCES_DIR / "map.tmx")

  def __init__(self, screen: pygame.Surface) -> None:
    self.screen = screen
    self.running = False
    self.gameState = GameState.MAIN_MENU
    
    self.tmx_data = load_pygame(self.map_path)

    self.player = Player(self)
    spawnObj = self.tmx_data.get_layer_by_name("spawn")[0]
    self.player.position = (spawnObj.x-spawnObj.width/2, spawnObj.y)

    # Create new renderer
    self.map_layer = pyscroll.BufferedRenderer(
      data=pyscroll.data.TiledMapData(self.tmx_data),
      size=screen.get_size(),
      clamp_camera=False,
      zoom=2,
    )

    # Make Pyscroll group
    self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=50)
    self.group.add(self.player)

    self.toastManager = ToastManager(self.screen)

    self.puzzles = {
      'simonsays': SimonSays(self),
      'morsecode': MorseCode(self),
    }

    self.menus = {
      'mainmenu': MainMenu(self),
      'ingame': Ingame(self),
      'settings': SettingsMenu(self),
      'pausemenu': PausedMenu(self),
    }

  def draw(self) -> None:
    if self.gameState == GameState.MAIN_MENU: self.menus['mainmenu'].draw(self.screen)
    if self.gameState == GameState.SETTINGS: self.menus['settings'].draw(self.screen)
    if self.gameState == GameState.PAUSE_MENU: self.menus['pausemenu'].draw(self.screen)
    if self.gameState == GameState.IN_GAME: 
      self.menus['ingame'].draw(self.screen)
      for puzzle in self.puzzles.values():
        if puzzle.active:
          puzzle.draw(self.screen)
      self.toastManager.draw(self.screen)

  def handle_input(self) -> None:
    for event in pygame.event.get():
      if event.type == QUIT:
        self.running = False
        break

      elif event.type == UserEvents.PAUSE_BLINK.value:
        self.menus['pausemenu'].blink()
      elif event.type == UserEvents.SIMON_SAYS_BLINK.value:
        self.puzzles['simonsays'].nextColor()

      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and self.gameState == GameState.MAIN_MENU: self.menus['mainmenu'].handle_click(event.pos)
        if event.button == 1 and self.gameState == GameState.PAUSE_MENU: self.menus['pausemenu'].handle_click(event.pos)

      elif event.type == KEYDOWN:
        if event.key == K_ESCAPE and self.gameState == GameState.MAIN_MENU:
          self.running = False
          break
        elif event.key == K_ESCAPE and self.gameState == GameState.IN_GAME: self.gameState = GameState.PAUSE_MENU
        elif event.key == K_ESCAPE and self.gameState == GameState.PAUSE_MENU: self.gameState = GameState.MAIN_MENU
        elif event.key == K_0: self.puzzles['simonsays'].active = not self.puzzles['simonsays'].active
        else:
          if self.gameState == GameState.IN_GAME:
            self.menus['ingame'].handle_input(event)
          for puzzle in self.puzzles.values():
            puzzle.handle_input(event)
        
      elif event.type == VIDEORESIZE:
        logging.info("Resizing screen to %sx%s", event.w, event.h)
        self.screen = initialize_screen(event.w, event.h)
        self.map_layer.set_size((event.w, event.h))
        
      else:
        if self.gameState == GameState.IN_GAME: self.menus['ingame'].handle_input(event)
       

    if self.gameState == GameState.IN_GAME:
      pressed = pygame.key.get_pressed()
      mods = pygame.key.get_mods()

      if pressed[pygame.K_w]: self.player.velocity[1] = -PLAYER_RUN_SPEED if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills else -PLAYER_MOVE_SPEED
      elif pressed[pygame.K_s]: self.player.velocity[1] = PLAYER_RUN_SPEED if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills else PLAYER_MOVE_SPEED
      else: self.player.velocity[1] = 0

      if pressed[pygame.K_a]: self.player.velocity[0] = -PLAYER_RUN_SPEED if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills else -PLAYER_MOVE_SPEED
      elif pressed[pygame.K_d]: self.player.velocity[0] = PLAYER_RUN_SPEED if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills else PLAYER_MOVE_SPEED
      else: self.player.velocity[0] = 0

  def update(self, dt: float) -> None:
    self.menus['ingame'].update(dt)
    for puzzle in self.puzzles.values():
      if puzzle.active:
        puzzle.update(dt)

  def run(self) -> None:
    """
    Run 👏 The 👏 Game 👏 Loop 👏
    """
    clock = pygame.time.Clock()
    self.running = True

    try:
      while self.running:
        dt = clock.tick() / 1000.0
        self.handle_input()
        self.update(dt)
        self.draw()
        pygame.display.flip()

        sys.stdout.write("FPS: %s\r" % str(float(clock.get_fps())))
        sys.stdout.flush()
    except KeyboardInterrupt:
      self.running = False

def main() -> None:
  logging.info("Python version: " + str(sys.version))
  logging.info("Pygame version: " + str(pygame.version.ver))
  logging.info("Pytmx version: " + str(pytmx.__version__))
  logging.info("Pyscroll version: " + str(pyscroll.__version__))
  logging.info("Current Process ID: " + str(os.getpid()))
  logging.info("Current Parent Process ID: " + str(os.getppid()))

  pygame.init()
  logging.info("Pygame initialized")

  pygame.font.init()
  logging.info("Pygame font module initialized")

  pygame.mixer.init()
  logging.info("Pygame mixer module initialized")

  screen = initialize_screen(1280, 720)
  logging.info("Initialized screen")

  pygame.display.set_caption('Swish and Frick')
  logging.info("Set window title to: " + str(pygame.display.get_caption()[0]))

  try:
    game = Game(screen)
    game.run()
  except KeyboardInterrupt:
    pass
  finally:
    pygame.quit()


if __name__ == "__main__":
  main()