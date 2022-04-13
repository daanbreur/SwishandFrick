"""paused_menu module: contains PausedMenu class"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

import pygame

from enums import GameState, UserEvents
from utils import get_font_at_size
from constants import PAUSE_BLINK_TIME_MS
from menu_button import MenuButton

if TYPE_CHECKING:
    from game import Game


class PausedMenu:
    """This class handles logic for the PausedMenu Screen.
    """
    def __init__(self, game: Game) -> None:
        self.game: Game = game
        self.font: pygame.font.Font = get_font_at_size(font_size=20)
        self.draw_paused: bool = False

        pygame.time.set_timer(UserEvents.PAUSE_BLINK.value, PAUSE_BLINK_TIME_MS)

        def resume_game() -> None:
            self.game.game_state = GameState.IN_GAME

        def settings() -> None:
            self.game.game_state = GameState.SETTINGS

        def main_menu() -> None:
            self.game.game_state = GameState.MAIN_MENU

        width, height = pygame.display.get_surface().get_size()
        self.buttons: List[MenuButton] = [
            MenuButton(
                (width / 2, height / 2),
                (200, 50),
                color=(220, 220, 220),
                cb_=resume_game,
                text="Resume Game",
            ),
            MenuButton(
                (width / 2, height / 2 + 50 + 10),
                (200, 50),
                color=(220, 220, 220),
                cb_=settings,
                text="Settings",
            ),
            MenuButton(
                (width / 2, height / 2 + 100 + 20),
                (200, 50),
                color=(220, 220, 220),
                cb_=main_menu,
                text="Main Menu",
            ),
        ]

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the buttons and paused text to the specified screen

        Args:
            screen (pygame.Surface): screen to draw to.
        """
        self.game.menus["ingame"].draw(screen)

        if self.draw_paused:
            text_surface = self.font.render("Paused", False, (255, 255, 255))
            screen.blit(
                text_surface,
                (
                    screen.get_width() / 2 - text_surface.get_width() / 2,
                    screen.get_height() / 2 - text_surface.get_height() / 2 - 50,
                ),
            )

        for btn in self.buttons:
            btn.draw(screen)

    def blink(self) -> None:
        """Event function that toggles the text
        """
        self.draw_paused = not self.draw_paused

    def handle_click(self, pos: Tuple[int, int]) -> None:
        """Handles the clicks for the buttons

        Args:
            pos (Tuple[int, int]): current mouse position
        """
        for btn in self.buttons:
            if btn.rect.collidepoint(pos):
                btn.callback()
