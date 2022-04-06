import pygame
import logging
from constants import RESOURCES_DIR
from enums import Skills
from utils import add_skill, get_layer_visibility, resource_path, set_layer_visibilty, tile_object_to_rect

class LeverCombination():
  def __init__(self, game) -> None:
    self.active = True
    self.solved = False
    self.game = game

    self.sequence = [True, True, False, False, False, True]
    self.enteredSequence = [False, False, False, False, False, False]

    self.lever_complete_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_complete_range")[0])

    self.lever_lever_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_one_range")[0])
    self.lever_lever_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_two_range")[0])
    self.lever_lever_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_three_range")[0])
    self.lever_lever_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_four_range")[0])
    self.lever_lever_five_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_five_range")[0])
    self.lever_lever_six_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_six_range")[0])

  def draw(self, screen: pygame.Surface) -> None:
    return
  
  def update(self, df: float) -> None:
    if self.active:
      if self.game.player.feet.colliderect(self.lever_complete_range):
        if self.sequence == self.enteredSequence:
          if not self.solved:
            logging.info("LeverCombination Solved")
            self.solved = True
            self.game.toastManager.addToast("Lever Combination Solved", 17)
            add_skill(self.game.player, Skills.HAMMER)

  def reset(self) -> None:
    logging.info("Resetting LeverCombination")
    self.game.toastManager.addToast("Lever Combination Reset", 17)
    self.solved = False
    self.sequence = []
    self.enteredSequence = []

  def handle_input(self, event) -> None:
    if event.key == pygame.K_f:
      for sprite in self.game.group.sprites():
        if sprite.feet.colliderect(self.lever_lever_one_range):
          self.enteredSequence[0] = not self.enteredSequence[0]
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_one", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_one"))
        if sprite.feet.colliderect(self.lever_lever_two_range):
          self.enteredSequence[1] = not self.enteredSequence[1]
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_two", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_two"))
        if sprite.feet.colliderect(self.lever_lever_three_range):
          self.enteredSequence[2] = not self.enteredSequence[2]
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_three", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_three"))
        if sprite.feet.colliderect(self.lever_lever_four_range):
          self.enteredSequence[3] = not self.enteredSequence[3]
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_four", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_four"))
        if sprite.feet.colliderect(self.lever_lever_five_range):
          self.enteredSequence[4] = not self.enteredSequence[4]
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_five", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_five"))
        if sprite.feet.colliderect(self.lever_lever_six_range):
          self.enteredSequence[5] = not self.enteredSequence[5]
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_six", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_six"))
