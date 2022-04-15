"""settings_menu module: contains SettingsMenu class"""

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

import pygame

if TYPE_CHECKING:
    from game import Game


class SettingsMenu:
    """This class handles logic for the SettingsMenu Screen.
    """
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the buttons and paused text to the specified screen

        Args:
            screen (pygame.Surface): screen to draw to.
        """

    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handles the clicks for the buttons

        Args:
            pos (Tuple[int, int]): current mouse position
        """
