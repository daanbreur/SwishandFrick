import pygame
import logging
from utils import set_layer_visibilty, tile_object_to_rect

class Math():
  def __init__(self, game) -> None:
    self.active = True
    self.solved = False
    self.game = game

    self.sequence = [3, 4, 1, 2]
    self.enteredSequence = []

    self.math_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_red_range")[0])

    self.math_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_one_range")[0])
    self.math_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_two_range")[0])
    self.math_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_three_range")[0])
    self.math_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_four_range")[0])

  def draw(self, screen: pygame.Surface) -> None:
    return
  
  def update(self, df: float) -> None:
    if self.active:
      if len(self.enteredSequence) >= len(self.sequence):
        if self.sequence == self.enteredSequence:
          if not self.solved:
            logging.info("Math Solved")
            self.solved = True
            self.game.toastManager.addToast("Math Challange Solved", 17)
            set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "puzzle_door_three", False)
        else:
          self.reset()

  def reset(self) -> None:
    logging.info("Resetting Math")
    self.game.toastManager.addToast("Math Challange Reset", 17)
    self.solved = False
    self.sequence = [3, 4, 1, 2]
    self.enteredSequence = []
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "puzzle_door_three", True)

  def handle_input(self, event) -> None:
    if event.key == pygame.K_f:
      for sprite in self.game.group.sprites():
        if sprite.feet.colliderect(self.math_button_one_range): self.enteredSequence.append(1)
        if sprite.feet.colliderect(self.math_button_two_range): self.enteredSequence.append(2)
        if sprite.feet.colliderect(self.math_button_three_range): self.enteredSequence.append(3)
        if sprite.feet.colliderect(self.math_button_four_range): self.enteredSequence.append(4)

        if sprite.feet.colliderect(self.math_button_red_range): self.reset()