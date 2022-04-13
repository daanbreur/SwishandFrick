"""music module: contains the Music class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
import pygame

from constants import RESOURCES_DIR
from utils import resource_path, tile_object_to_rect

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)

class Music():
    """This class handles logic for the Music puzzle.
    """
    def __init__(self, game: Game) -> None:
        self.active = True
        self.solved = False
        self.game: Game = game

        self.sequence: List[int] = [1,2,3,2,1,2,3,2,1,3,4,4,4,4,4,3]
        self.entered_sequence: List[int] = []

        self.music_button_green_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_button_green_range")[0]
        )
        self.music_button_red_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_button_red_range")[0]
        )
        self.music_button_one_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_button_one_range")[0]
        )
        self.music_button_two_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_button_two_range")[0]
        )
        self.music_button_three_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_button_three_range")[0]
        )
        self.music_button_four_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_button_four_range")[0]
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
                        logger.info("Music Solved")
                        self.solved = True
                        self.game.toastManager.add_toast("Music Challenge Solved", 17)
                        self.game.doorManager.open_door_by_id("beach_door")
                else:
                    self.reset()

    def reset(self) -> None:
        """Resets puzzle to default state.
        """
        logger.info("Resetting Music")
        pygame.mixer.music.stop()
        self.game.toastManager.add_toast("Music Challenge Reset", 17)
        self.game.doorManager.close_door_by_id("beach_door")
        self.solved = False
        self.sequence = [1,2,3,2,1,2,3,2,1,3,4,4,4,4,4,3]
        self.entered_sequence = []

    def handle_input(self, event) -> None:
        """Handles user input, checks for collision with buttons and plays sounds

        Args:
            event (pygame.event.Event): pygame event object
        """
        if event.key == pygame.K_f:
            for sprite in self.game.group.sprites():
                if sprite.feet.colliderect(self.music_button_one_range):
                    pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes1.wav" ))
                    pygame.mixer.music.play()
                    self.entered_sequence.append(1)
                if sprite.feet.colliderect(self.music_button_two_range):
                    pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes2.wav" ))
                    pygame.mixer.music.play()
                    self.entered_sequence.append(2)
                if sprite.feet.colliderect(self.music_button_three_range):
                    pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes3.wav" ))
                    pygame.mixer.music.play()
                    self.entered_sequence.append(3)
                if sprite.feet.colliderect(self.music_button_four_range):
                    pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes4.wav" ))
                    pygame.mixer.music.play()
                    self.entered_sequence.append(4)

                if sprite.feet.colliderect(self.music_button_green_range):
                    logger.info("Playing music for Music Challenge")
                    self.game.toastManager.add_toast("Playing audio for Music Challenge", 15)
                    pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/songlevel.wav" ))
                    pygame.mixer.music.play()
                if sprite.feet.colliderect(self.music_button_red_range):
                    self.reset()
