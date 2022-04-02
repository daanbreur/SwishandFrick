import pygame
import logging
from constants import RESOURCES_DIR

from utils import resource_path, set_layer_visibilty, tile_object_to_rect

class MorseCode():
  def __init__(self, game) -> None:
    self.active = True
    self.solved = False
    self.game = game

    self.sequence = [4,3,6,5,1,2]
    self.enteredSequence = []

    self.mors_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_red_range")[0])
    self.mors_button_blue_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_blue_range")[0])

    self.mors_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_one_range")[0])
    self.mors_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_two_range")[0])
    self.mors_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_three_range")[0])
    self.mors_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_four_range")[0])
    self.mors_button_five_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_five_range")[0])
    self.mors_button_six_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_six_range")[0])

  def draw(self, screen: pygame.Surface) -> None:
    return
  
  def update(self, df: float) -> None:
    if self.active:
      if len(self.enteredSequence) >= len(self.sequence):
        if self.sequence == self.enteredSequence and not self.solved:
          logging.info("Morse Code Solved")
          self.solved = True
          self.game.toastManager.addToast("Morse Code Solved", 17)
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "puzzle_door", False)
          set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "puzzle_door_four", False)
        else:
          self.reset()

  def reset(self) -> None:
    logging.info("Resetting Morse Code")
    self.game.toastManager.addToast("Morse Code Reset", 17)
    self.solved = False
    self.sequence = [4,3,6,5,1,2]
    self.enteredSequence = []
    pygame.mixer.music.stop()
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "puzzle_door", True)
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "puzzle_door_four", True)

  def handle_input(self, event) -> None:
    if event.key == pygame.K_f:
      for sprite in self.game.group.sprites():
        if sprite.feet.colliderect(self.mors_button_one_range): self.enteredSequence.append(1)
        if sprite.feet.colliderect(self.mors_button_two_range): self.enteredSequence.append(2)
        if sprite.feet.colliderect(self.mors_button_three_range): self.enteredSequence.append(3)
        if sprite.feet.colliderect(self.mors_button_four_range): self.enteredSequence.append(4)
        if sprite.feet.colliderect(self.mors_button_five_range): self.enteredSequence.append(5)
        if sprite.feet.colliderect(self.mors_button_six_range): self.enteredSequence.append(6)

        if sprite.feet.colliderect(self.mors_button_red_range): self.reset()
        if sprite.feet.colliderect(self.mors_button_blue_range):
          logging.info("Playing sound for Morse Code")
          self.game.toastManager.addToast("Playing audio for Morse Code Challange", 15)
          pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/morselevel.wav" ))
          pygame.mixer.music.set_volume(0.7)
          pygame.mixer.music.play()