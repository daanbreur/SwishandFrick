"""main_menu module: contains MainMenu class"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

import pygame

from constants import RESOURCES_DIR
from enums import GameState
from utils import resource_path, get_font_at_size

from menu_button import MenuButton

if TYPE_CHECKING:
    from game import Game


class MainMenu:
    """This class handles logic for the MainMenu Screen."""

    def __init__(self, game: Game) -> None:
        self.game: Game = game
        self.background: pygame.Surface = pygame.image.load(
            resource_path(RESOURCES_DIR / "background.png")
        )
        self.font: pygame.font.Font = get_font_at_size(font_size=30)

        def start_game() -> None:
            self.game.gameState = GameState.IN_GAME

        def close_game() -> None:
            self.game.running = False

        width, height = pygame.display.get_surface().get_size()
        self.buttons: List[MenuButton] = [
            MenuButton(
                (width / 2, height / 2),
                (200, 50),
                color=(220, 220, 220),
                cb_=start_game,
                text="Start Game",
            ),
            MenuButton(
                (width / 2, height / 2 + 50 + 10),
                (200, 50),
                color=(220, 220, 220),
                cb_=close_game,
                text="Exit",
            ),
        ]

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the buttons and paused text to the specified screen

        Args:
            screen (pygame.Surface): screen to draw to.
        """
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))

        text_surface = self.font.render("Swish and Frick", False, (255, 255, 255))
        screen.blit(
            text_surface,
            (
                screen.get_width() / 2 - text_surface.get_width() / 2,
                screen.get_height() / 2 - text_surface.get_height() / 2 - 50,
            ),
        )

        for btn in self.buttons:
            btn.draw(screen)

    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handles the clicks for the buttons

        Args:
            pos (Tuple[int,int]): current mouse position
        """
        for btn in self.buttons:
            if btn.rect.collidepoint(pos):
                btn.callback()
