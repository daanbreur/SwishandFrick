"""sign_manager module: contains the SignManager and Sign class."""

from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
import pygame
from utils import tile_object_to_rect

if TYPE_CHECKING:
    from player import Player
    from game import Game

logger = logging.getLogger(__name__)


class Sign:
    def __init__(self, game: Game, range_layer: str, text: str):
        self.game: Game = game
        self.range_layer: str = range_layer
        self.collider: pygame.Rect = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name(self.range_layer)[0]
        )
        self._text: str = text
        self._showing: bool = False
        self._previous_showing: bool = False

    def update(self, sprite: Player, dt_: float) -> None:
        pass

class SignManager:
    """ This class handles drawing of the signs whenever the Player is in its range.
    """
    def __init__(self, game: Game):
        self.game: Game = game
        self.signs: dict[str, Sign] = {}

    def new_sign(self, id_: str, range_layer: str, text: str) -> None:
        """

        Args:
            id_ (str): a unique id for the sign to be used for accessing it
            range_layer (str): the layer name for the range to show the text in
            text (str): the string to be displayed

        Returns:
            None
        """
        if id_ in self.signs:
            logger.warning("SignManager: Sign with id {} already exists", id_)
            return
        logger.info(
            "SignManager: Creating new sign (id {}, range {}, text {})",
            id_,
            range_layer,
            text
        )
        self.signs[id_] = Sign(self.game, range_layer, text)

    def get_sign(self, id_: str) -> Sign:
        if id_ not in self.signs:
            logger.warning("SignManager: Sign with id {} does not exist", id_)
            raise KeyError
        return self.signs[id_]

    def update(self, sprite: Player, dt_: float) -> None:
        for sign in self.signs.values():
            sign.update(sprite, dt_)

    def draw(self, screen: pygame.Surface):
        for sign in self.signs.values():
            sign.draw()
