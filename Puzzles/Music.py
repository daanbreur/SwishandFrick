from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from game import Game

import pygame
import logging
from constants import RESOURCES_DIR
from utils import resource_path, set_layer_visibilty, tile_object_to_rect

class Music():
  def __init__(self, game: Game) -> None:
    self.active = True
    self.solved = False
    self.game: Game = game

    self.sequence = [1,2,3,2,1,2,3,2,1,3,4,4,4,4,4,3]
    self.enteredSequence = []

    self.music_button_green_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_green_range")[0])
    self.music_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_red_range")[0])

    self.music_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_one_range")[0])
    self.music_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_two_range")[0])
    self.music_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_three_range")[0])
    self.music_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_four_range")[0])

  def draw(self, screen: pygame.Surface) -> None:
    return
  
  def update(self, df: float) -> None:
    if self.active:
      if len(self.enteredSequence) >= len(self.sequence):
        if self.sequence == self.enteredSequence:
          if not self.solved:
            logging.info("Music Solved")
            self.solved = True
            self.game.toastManager.addToast("Music Challange Solved", 17)
            self.game.doorManager.openDoorById("beach_door")
        else:
          self.reset()

  def reset(self) -> None:
    logging.info("Resetting Music")
    pygame.mixer.music.stop()
    self.game.toastManager.addToast("Music Challange Reset", 17)
    self.game.doorManager.closeDoorById("beach_door")
    self.solved = False
    self.sequence = [1,2,3,2,1,2,3,2,1,3,4,4,4,4,4,3]
    self.enteredSequence = []

  def handle_input(self, event) -> None:
    if event.key == pygame.K_f:
      for sprite in self.game.group.sprites():
        if sprite.feet.colliderect(self.music_button_one_range):
          pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes1.wav" ))
          pygame.mixer.music.play()
          self.enteredSequence.append(1)
        if sprite.feet.colliderect(self.music_button_two_range):
          pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes2.wav" ))
          pygame.mixer.music.play()
          self.enteredSequence.append(2)
        if sprite.feet.colliderect(self.music_button_three_range):
          pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes3.wav" ))
          pygame.mixer.music.play()
          self.enteredSequence.append(3)
        if sprite.feet.colliderect(self.music_button_four_range):
          pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes4.wav" ))
          pygame.mixer.music.play()
          self.enteredSequence.append(4)

        if sprite.feet.colliderect(self.music_button_green_range):
          logging.info("Playing music for Music Challenge")
          self.game.toastManager.addToast("Playing audio for Music Challange", 15)
          pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/songlevel.wav" ))
          pygame.mixer.music.play()
        if sprite.feet.colliderect(self.music_button_red_range): self.reset()