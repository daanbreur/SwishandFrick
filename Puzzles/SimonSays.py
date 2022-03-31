import pygame
import enum
import logging
import random

from utils import tile_object_to_rect

class SimonSaysButtons(enum.Enum):
  RED = 'red'
  GREEN = 'green'
  YELLOW = 'yellow'
  BLUE = 'blue'

class SimonSays():
  def __init__(self, game) -> None:
    self.active = False
    self.solved = False
    self.game = game

    self.sequence = []
    self.enteredSequence = []

    self.red_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("x")[0])
    self.blue_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("x")[0])
    self.green_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("x")[0])
    self.yellow_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("x")[0])
    self.reset_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("x")[0])

    return

  def draw(self, screen: pygame.Surface) -> None:
    screen.fill((255, 0, 0))
    return
  
  def update(self, df: float) -> None:
    self.sequence.append(random.choice(list(SimonSaysButtons)))

  def reset(self) -> None:
    self.sequence = []
    self.enteredSequence = []

  def handle_input(self, event) -> None:
    if event.key == pygame.K_f:
      for sprite in self.game.group.sprites():
        if sprite.feet.colliderect(self.red_button_collider): self.enteredSequence.append(SimonSaysButtons.RED)
        if sprite.feet.colliderect(self.blue_button_collider): self.enteredSequence.append(SimonSaysButtons.BLUE)
        if sprite.feet.colliderect(self.green_button_collider): self.enteredSequence.append(SimonSaysButtons.GREEN)
        if sprite.feet.colliderect(self.yellow_button_collider): self.enteredSequence.append(SimonSaysButtons.YELLOW)
        if sprite.feet.colliderect(self.reset_button_collider): self.reset()