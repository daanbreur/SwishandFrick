import pygame
import enum
import logging
import random
from constants import SIMON_SAYS_BLINK_TIME_MS
from enums import UserEvents

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

    self.sequence = [random.choice(list(SimonSaysButtons))]
    self.enteredSequence = []

    self.showColorIndex = 0
    self.showColor = False

    self.blinkTimer = pygame.time.set_timer(UserEvents.SIMON_SAYS_BLINK.value, SIMON_SAYS_BLINK_TIME_MS)

    self.red_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_red_range")[0])
    self.blue_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_blue_range")[0])
    self.green_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_green_range")[0])
    self.yellow_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_yellow_range")[0])
    self.reset_button_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_reset_range")[0])

    return

  def draw(self, screen: pygame.Surface) -> None:
    if self.showColor:
      logging.info(f"Sequence: {self.sequence} | Index: {self.showColorIndex} | Show Color: {self.sequence[self.showColorIndex]}")
      if self.sequence[self.showColorIndex] == SimonSaysButtons.RED: screen.fill((255, 0, 0))
      if self.sequence[self.showColorIndex] == SimonSaysButtons.BLUE: screen.fill((0, 0, 255))
      if self.sequence[self.showColorIndex] == SimonSaysButtons.GREEN: screen.fill((0, 255, 0))
      if self.sequence[self.showColorIndex] == SimonSaysButtons.YELLOW: screen.fill((255, 255, 0))
  
  def update(self, df: float) -> None:
    logging.info(f"Simon Says: {self.sequence} | Submitted: {self.enteredSequence}")
    if self.active:
      if len(self.sequence) == len(self.enteredSequence):
        if self.sequence == self.enteredSequence:
          if len(self.enteredSequence) < 5:
            self.sequence.append(random.choice(list(SimonSaysButtons)))
            self.enteredSequence = []
            self.showColorIndex = 0
            self.showColor = True
          else:
            self.solved = True
            self.active = False
        else:
          self.reset()
    pass

  def nextColor(self) -> None:
    if self.active:
      if self.showColorIndex == len(self.sequence)-1: 
        self.showColor = False
      else: 
        self.showColorIndex += 1
        self.showColor = True

  def reset(self) -> None:
    if not self.solved:
      self.sequence = [random.choice(list(SimonSaysButtons))]
      self.enteredSequence = []

  def handle_input(self, event) -> None:
    if event.key == pygame.K_f:
      for sprite in self.game.group.sprites():
        if self.active:
          if sprite.feet.colliderect(self.red_button_collider): self.enteredSequence.append(SimonSaysButtons.RED)
          if sprite.feet.colliderect(self.blue_button_collider): self.enteredSequence.append(SimonSaysButtons.BLUE)
          if sprite.feet.colliderect(self.green_button_collider): self.enteredSequence.append(SimonSaysButtons.GREEN)
          if sprite.feet.colliderect(self.yellow_button_collider): self.enteredSequence.append(SimonSaysButtons.YELLOW)
          if sprite.feet.colliderect(self.reset_button_collider): self.reset()
        else:
          if sprite.feet.colliderect(self.reset_button_collider): self.active = True