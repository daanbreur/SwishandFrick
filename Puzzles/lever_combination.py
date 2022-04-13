"""lever_combination module: contains the LeverCombination class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
import pygame

from enums import Skills
from utils import add_skill, get_layer_visibility, set_layer_visibility, tile_object_to_rect

if TYPE_CHECKING:
    from game import Game

class LeverCombination():
    """ This class handles logic for the LeverCombination puzzle.
    """
    def __init__(self, game: Game) -> None:
        self.active: bool = True
        self.solved: bool = False
        self.game: Game = game

        self.sequence: List[bool] = [True, True, False, False, False, True]
        self.entered_sequence: List[bool] = [False, False, False, False, False, False]

        self.lever_complete_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_complete_range")[0]
        )
        self.lever_lever_one_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_lever_one_range")[0]
        )
        self.lever_lever_two_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_lever_two_range")[0]
        )
        self.lever_lever_three_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_lever_three_range")[0]
        )
        self.lever_lever_four_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_lever_four_range")[0]
        )
        self.lever_lever_five_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_lever_five_range")[0]
        )
        self.lever_lever_six_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_lever_six_range")[0]
        )

    def update(self, dt_: float) -> None:
        """Handles the update cycle for the puzzle

        Args:
            dt_ (float): frame timedelta
        """
        if self.active:
            if self.game.player.feet.colliderect(self.lever_complete_range):
                if self.sequence == self.entered_sequence:
                    if not self.solved:
                        logging.info("LeverCombination Solved")
                        self.solved = True
                        self.game.toastManager.addToast("Lever Combination Solved", 17)
                        add_skill(self.game.player, Skills.HAMMER)

    def reset(self) -> None:
        """Resets puzzle to default state.
        """
        logging.info("Resetting LeverCombination")
        self.game.toastManager.addToast("Lever Combination Reset", 17)
        self.solved = False
        self.sequence = [True, True, False, False, False, True]
        self.entered_sequence = [False, False, False, False, False, False]

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles user input, checks for collision with lever and turns it on or of

        Args:
            event (pygame.event.Event): pygame event object
        """
        if event.key == pygame.K_f:
            for sprite in self.game.group.sprites():
                if sprite.feet.colliderect(self.lever_lever_one_range):
                    self.entered_sequence[0] = not self.entered_sequence[0]
                    set_layer_visibility(
                        self.game.tmx_data,
                        self.game.map_layer,
                        "lever_puzzle_one",
                        not get_layer_visibility(self.game.tmx_data, "lever_puzzle_one")
                    )
                if sprite.feet.colliderect(self.lever_lever_two_range):
                    self.entered_sequence[1] = not self.entered_sequence[1]
                    set_layer_visibility(
                        self.game.tmx_data,
                        self.game.map_layer,
                        "lever_puzzle_two",
                        not get_layer_visibility(self.game.tmx_data, "lever_puzzle_two")
                    )
                if sprite.feet.colliderect(self.lever_lever_three_range):
                    self.entered_sequence[2] = not self.entered_sequence[2]
                    set_layer_visibility(
                        self.game.tmx_data,
                        self.game.map_layer,
                        "lever_puzzle_three",
                        not get_layer_visibility(self.game.tmx_data, "lever_puzzle_three")
                    )
                if sprite.feet.colliderect(self.lever_lever_four_range):
                    self.entered_sequence[3] = not self.entered_sequence[3]
                    set_layer_visibility(
                        self.game.tmx_data,
                        self.game.map_layer,
                        "lever_puzzle_four",
                        not get_layer_visibility(self.game.tmx_data, "lever_puzzle_four")
                    )
                if sprite.feet.colliderect(self.lever_lever_five_range):
                    self.entered_sequence[4] = not self.entered_sequence[4]
                    set_layer_visibility(
                        self.game.tmx_data,
                        self.game.map_layer,
                        "lever_puzzle_five",
                        not get_layer_visibility(self.game.tmx_data, "lever_puzzle_five")
                    )
                if sprite.feet.colliderect(self.lever_lever_six_range):
                    self.entered_sequence[5] = not self.entered_sequence[5]
                    set_layer_visibility(
                        self.game.tmx_data,
                        self.game.map_layer,
                        "lever_puzzle_six",
                        not get_layer_visibility(self.game.tmx_data, "lever_puzzle_six")
                    )
