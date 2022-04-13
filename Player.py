"""player module: contains Player class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List
import pygame

from utils import load_image

if TYPE_CHECKING:
    from game import Game
    from enums import Gems, Skills

class Player(pygame.sprite.Sprite):
    """ This class is the main player object.
    Stores location data, inventory and skills.
    """
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.image = load_image("player.png").convert_alpha()
        self.velocity = [0, 0]
        self._position = [0.0, 0.0]
        self._old_position = self._position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)
        self.skills: List[Skills] = []
        self.inventory: List[Gems] = []

    @property
    def position(self) -> List[float]:
        """Get player position information

        Returns:
            List[float]: player coordinates
        """
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        """Set player instance position

        Args:
            value (List[float]): coordinates to set player position to
        """
        self._position = list(value)

    def update(self, dt_: float) -> None:
        """Player update cycle, uses velocity and frame timedelta to calculate distance to move

        Args:
            dt_ (float): frame timedelta
        """
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt_
        self._position[1] += self.velocity[1] * dt_
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt_: float) -> None:
        """Move back player to previous location

        Args:
            dt_ (float): frame timedelta
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
