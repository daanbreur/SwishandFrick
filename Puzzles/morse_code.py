"""morse_code module: contains the MorseCode class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
import pygame

from constants import RESOURCES_DIR
from utils import resource_path, tile_object_to_rect

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)


class MorseCode:
    """This class handles logic for the MorseCode puzzle.
    """
    def __init__(self, game: Game) -> None:
        self.active: bool = True
        self.solved: bool = False
        self.game: Game = game

        self.sequence: List[int] = [4, 3, 6, 5, 1, 2]
        self.entered_sequence: List[int] = []

        self.mors_button_red_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_red_range")[0]
        )
        self.mors_button_blue_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_blue_range")[0]
        )
        self.mors_button_one_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_one_range")[0]
        )
        self.mors_button_two_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_two_range")[0]
        )
        self.mors_button_three_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_three_range")[0]
        )
        self.mors_button_four_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_four_range")[0]
        )
        self.mors_button_five_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_five_range")[0]
        )
        self.mors_button_six_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("mors_button_six_range")[0]
        )

    def update(self, dt_: float) -> None:
        """Handles the update cycle for the puzzle

        Args:
            dt_ (float): frame timedelta
        """
        if self.active:
            if len(self.entered_sequence) >= len(self.sequence):
                if self.sequence == self.entered_sequence:
                    if not self.solved:
                        logger.info("Morse Code Solved")
                        self.solved = True
                        self.game.toast_manager.add_toast("Morse Code Solved", 17)
                        self.game.door_manager.open_door_by_id("math_door")
                        self.game.door_manager.open_door_by_id("final_gem_door")
                else:
                    self.reset()

    def draw(self, screen: pygame.Surface) -> None:
        """Handles the drawing

        Args:
            screen (pygame.Surface): screen to draw to.
        """

    def reset(self) -> None:
        """Resets puzzle to default state.
        """
        logger.info("Resetting Morse Code")
        self.game.door_manager.close_door_by_id("final_gem_door")
        self.game.door_manager.close_door_by_id("math_door")
        self.game.toast_manager.add_toast("Morse Code Reset", 17)
        self.solved = False
        self.sequence = [4, 3, 6, 5, 1, 2]
        self.entered_sequence = []
        pygame.mixer.music.stop()

    def handle_input(self, event) -> None:
        """Handles user input, checks for collision with button

        Args:
            event (pygame.event.Event): pygame event object
        """
        if event.key == pygame.K_f:
            for sprite in self.game.group.sprites():
                if sprite.feet.colliderect(self.mors_button_one_range):
                    self.entered_sequence.append(1)
                if sprite.feet.colliderect(self.mors_button_two_range):
                    self.entered_sequence.append(2)
                if sprite.feet.colliderect(self.mors_button_three_range):
                    self.entered_sequence.append(3)
                if sprite.feet.colliderect(self.mors_button_four_range):
                    self.entered_sequence.append(4)
                if sprite.feet.colliderect(self.mors_button_five_range):
                    self.entered_sequence.append(5)
                if sprite.feet.colliderect(self.mors_button_six_range):
                    self.entered_sequence.append(6)

                if sprite.feet.colliderect(self.mors_button_red_range):
                    self.reset()
                if sprite.feet.colliderect(self.mors_button_blue_range):
                    logger.info("Playing sound for Morse Code")
                    self.game.toast_manager.add_toast("Playing audio for Morse Code Challenge", 15)
                    pygame.mixer.music.load(
                        resource_path(RESOURCES_DIR / "sounds/morselevel.wav")
                    )
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play()
