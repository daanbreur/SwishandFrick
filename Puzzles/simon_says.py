"""simon_says module: contains SimonSaysButtons enum and SimonSays class"""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import enum
import logging
import random
import pygame

from constants import SIMON_SAYS_BLINK_TIME_MS
from enums import UserEvents
from utils import tile_object_to_rect

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)


class SimonSaysButtons(enum.Enum):
    """This class contains the SimonSaysButtons enum.
    """
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'


class SimonSays:
    """This class handles logic for the SimonSays puzzle.
    """
    def __init__(self, game: Game) -> None:
        self.active: bool = False
        self.solved: bool = False
        self.game: Game = game

        self.sequence: List[SimonSaysButtons] = [random.choice(list(SimonSaysButtons))]
        self.entered_sequence: List[SimonSaysButtons] = []

        self.show_color_index: int = 0
        self.show_color: bool = False

        pygame.time.set_timer(UserEvents.SIMON_SAYS_BLINK.value, SIMON_SAYS_BLINK_TIME_MS)

        self.red_button_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_red_range")[0]
        )
        self.blue_button_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_blue_range")[0]
        )
        self.green_button_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_green_range")[0]
        )
        self.yellow_button_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_yellow_range")[0]
        )
        self.reset_button_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_reset_range")[0]
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Handles the drawing for the simon_says puzzle, to the specified screen

        Args:
            screen (pygame.Surface): screen to draw to.
        """
        if self.show_color:
            if not self.show_color_index > len(self.sequence)-1:
                logger.info(
                    "Sequence: {} | Index: {} | Show Color: {}",
                    self.sequence,
                    self.show_color_index,
                    self.sequence[self.show_color_index]
                )
                if self.sequence[self.show_color_index] == SimonSaysButtons.RED:
                    screen.fill((255, 0, 0))
                if self.sequence[self.show_color_index] == SimonSaysButtons.BLUE:
                    screen.fill((0, 0, 255))
                if self.sequence[self.show_color_index] == SimonSaysButtons.GREEN:
                    screen.fill((0, 255, 0))
                if self.sequence[self.show_color_index] == SimonSaysButtons.YELLOW:
                    screen.fill((255, 255, 0))

    def update(self, dt_: float) -> None:
        """Handles the update cycle for the puzzle

        Args:
            dt_ (float): frame timedelta
        """
        if self.active:
            if len(self.sequence) == len(self.entered_sequence):
                if self.sequence == self.entered_sequence:
                    if len(self.entered_sequence) < 5:
                        self.sequence.append(random.choice(list(SimonSaysButtons)))
                        logger.info("New Sequence: {}", str(self.sequence))
                        self.entered_sequence = []
                        self.show_color_index = 0
                        self.show_color = True
                    else:
                        self.game.toast_manager.add_toast("Simon Says Solved", 17)
                        self.game.door_manager.open_door_by_id("button_door_two")
                        self.game.door_manager.open_door_by_id("puzzle_door_one")
                        self.solved = True
                        self.active = False
                else:
                    self.reset()

    def next_color(self) -> None:
        """Next color event, called on interval
        Updates show_color_index to next color
        """
        if self.active:
            if self.show_color_index == len(self.sequence)-1:
                self.show_color = False
            else:
                self.show_color_index += 1
                self.show_color = True

    def reset(self) -> None:
        """Resets puzzle to default state.
        """
        if not self.solved:
            self.game.toast_manager.add_toast("Simon Says Reset", 17)
            self.game.door_manager.close_door_by_id("button_door_two")
            self.game.door_manager.close_door_by_id("puzzle_door_one")
            self.show_color = True
            self.sequence = [random.choice(list(SimonSaysButtons))]
            self.entered_sequence = []

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handles user input, checks for collision with buttons and plays sounds

        Args:
            event (pygame.event.Event): pygame event object
        """
        if event.key == pygame.K_f:
            for sprite in self.game.group.sprites():
                if self.active:
                    if sprite.feet.colliderect(self.red_button_collider):
                        self.entered_sequence.append(SimonSaysButtons.RED)
                    if sprite.feet.colliderect(self.blue_button_collider):
                        self.entered_sequence.append(SimonSaysButtons.BLUE)
                    if sprite.feet.colliderect(self.green_button_collider):
                        self.entered_sequence.append(SimonSaysButtons.GREEN)
                    if sprite.feet.colliderect(self.yellow_button_collider):
                        self.entered_sequence.append(SimonSaysButtons.YELLOW)
                    if sprite.feet.colliderect(self.reset_button_collider):
                        self.reset()
                else:
                    if sprite.feet.colliderect(self.reset_button_collider):
                        self.active = True
                        self.reset()
