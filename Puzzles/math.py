"""math module: contains the Math class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
import pygame

from utils import tile_object_to_rect

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)


class Math:
    """This class handles logic for the Math puzzle.
    """
    def __init__(self, game: Game) -> None:
        self.active: bool = True
        self.solved: bool = False
        self.game: Game = game

        self.sequence: List[int] = [3, 4, 1, 2]
        self.entered_sequence: List[int] = []

        self.math_button_red_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("math_button_red_range")[0]
        )
        self.math_button_one_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("math_button_one_range")[0]
        )
        self.math_button_two_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("math_button_two_range")[0]
        )
        self.math_button_three_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("math_button_three_range")[0]
        )
        self.math_button_four_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("math_button_four_range")[0]
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
                        logger.info("Math Solved")
                        self.solved = True
                        self.game.toast_manager.add_toast("Math Challenge Solved", 17)
                        self.game.door_manager.open_door_by_id("morse_door")
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
        logger.info("Resetting Math")
        self.game.toast_manager.add_toast("Math Challenge Reset", 17)
        self.game.door_manager.close_door_by_id("morse_door")
        self.solved = False
        self.sequence = [3, 4, 1, 2]
        self.entered_sequence = []

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles user input, checks for collision with button

        Args:
            event (pygame.event.Event): pygame event object
        """
        if event.key == pygame.K_f:
            for sprite in self.game.group.sprites():
                if sprite.feet.colliderect(self.math_button_one_range):
                    self.entered_sequence.append(1)
                if sprite.feet.colliderect(self.math_button_two_range):
                    self.entered_sequence.append(2)
                if sprite.feet.colliderect(self.math_button_three_range):
                    self.entered_sequence.append(3)
                if sprite.feet.colliderect(self.math_button_four_range):
                    self.entered_sequence.append(4)

                if sprite.feet.colliderect(self.math_button_red_range):
                    self.reset()
