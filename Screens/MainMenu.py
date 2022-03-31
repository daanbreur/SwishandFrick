import pygame
import logging

from constants import *
from enums import GameState
from utils import resource_path, getFontAtSize

from MenuButton import MenuButton

class MainMenu:
  def __init__(self, game) -> None:
    self.game = game
    self.background = pygame.image.load(resource_path(RESOURCES_DIR / "background.png"))
    self.font = getFontAtSize(fontSize=30)
  
    def startGame() -> None: self.game.gameState = GameState.IN_GAME
    def closeGame() -> None: self.game.running = False
    w, h = pygame.display.get_surface().get_size()
    self.buttons = [MenuButton((w/2, h/2), (200, 50), color=(220, 220, 220), cb=startGame, text='Start Game'), MenuButton((w/2, h/2+50+10), (200, 50), color=(220, 220, 220), cb=closeGame, text='Exit')]

  def draw(self, screen) -> None:
    screen.fill((0, 0, 0))
    screen.blit(self.background, (0, 0))

    textSurface = self.font.render("Swish and Frick", False, (255, 255, 255))
    screen.blit(textSurface, (screen.get_width()/2 - textSurface.get_width()/2, screen.get_height()/2 - textSurface.get_height()/2 - 50))

    for btn in self.buttons:
      btn.draw(screen)
  
  def handle_click(self, pos) -> None:
    for btn in self.buttons:
      if btn.rect.collidepoint(pos):
        btn.callback()