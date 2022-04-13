"""konami_code module: contains the KonamiCode class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
import pygame

from enums import Skills
from utils import add_skill, check_skill

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)


class KonamiCode:
    """ This class handles logic for the KonamiCode puzzle.
    """
    def __init__(self, game: Game) -> None:
        self.active: bool = True
        self.solved: bool = False
        self.game: Game = game

        self.sequence: List[int] = [
            pygame.K_UP,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_b,
            pygame.K_a
        ]
        self.entered_sequence: List[int] = []
        self.index: int = 0

    def update(self, dt_: float) -> None:
        """Handles update cycle

        Args:
            dt_ (float): time framedelta
        """

    def draw(self, screen: pygame.Surface) -> None:
        """Handles the drawing

        Args:
            screen (pygame.Surface): screen to draw to.
        """

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle input from the main game

        Args:
            event (pygame.event.Event): pygame event object
        """
        if not self.solved:
            if event.key == self.sequence[self.index]:
                self.entered_sequence.append(event.key)
                self.index += 1
                logger.debug(
                    "Konamicode input: {} / {} | {}",
                    self.index,
                    len(self.sequence),
                    pygame.key.name(self.sequence[self.index-1])
                )
                if self.sequence == self.entered_sequence:
                    self.solved = True
                    logger.info("Konamicode entered correctly")
                    self.game.toast_manager.add_toast("Konamicode Solved", 17)
                    if not check_skill(self.game.player, Skills.SWIM):
                        logger.info("Konamicode entered correctly, adding swim skill")
                        add_skill(self.game.player, Skills.SWIM)
