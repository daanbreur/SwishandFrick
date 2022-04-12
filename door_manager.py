"""door_manager module: contains the DoorManager and Door class."""

from __future__ import annotations
from typing import TYPE_CHECKING

import logging
import pygame
from utils import tile_object_to_rect, set_layer_visibilty

if TYPE_CHECKING:
    from Player import Player
    from game import Game

logger = logging.getLogger(__name__)

class Door:
    """ This class implements all door logic. Used inside the DoorManager class
    """
    def __init__(self, game: Game, collider_layer: str, sprite_layer: str):
        """Constructs all necessary attributes for the door object

        Args:
            game (Game): the game class instance for the running game
            collider_layer (str): the layer name for the collider
            sprite_layer (str): the layer name with the closed state sprite
        """
        self.game: Game = game
        self.opened: bool = False
        self.opened_until = None
        self.collider_layer: str = collider_layer
        self.sprite_layer: str = sprite_layer
        self.collider: pygame.Rect = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name(self.collider_layer)[0]
        )

    def open(self) -> None:
        """Opens the door indefinitely until manually closed
        """
        self.opened = True
        set_layer_visibilty(
            self.game.tmx_data, self.game.map_layer, self.sprite_layer, False
        )

    def close(self) -> None:
        """Closes the door indefinitely until manually opened
        """
        self.opened = False
        set_layer_visibilty(
            self.game.tmx_data, self.game.map_layer, self.sprite_layer, True
        )

    def open_for_millis(self, millis: int) -> None:
        """Opens the door for a set amount of milliseconds

        Args:
            millis (int): amount of milliseconds to open the door for
        """
        self.opened = True
        self.opened_until = pygame.time.get_ticks() + millis
        set_layer_visibilty(
            self.game.tmx_data, self.game.map_layer, self.sprite_layer, False
        )

    def set_opened(self, opened: bool) -> None:
        """Set the door's open state manually

        Args:
            opened (bool): open/true or closed/false the state to set the door to
        """
        self.opened = opened
        set_layer_visibilty(
            self.game.tmx_data, self.game.map_layer, self.sprite_layer, not opened
        )

    def get_opened(self) -> bool:
        """Get the current state of the door

        Returns:
            bool: the state of the door (open/true or closed/false)
        """
        return self.opened

    def update(self, sprite: Player, dt: float) -> None:
        """Handles the colliding with the door for the player

        Args:
            sprite (Player): the player object to check the collision with
            dt (float): dt
        """
        if self.opened_until is not None and pygame.time.get_ticks() > self.opened_until:
            self.opened = False
            self.opened_until = None
            set_layer_visibilty(
                self.game.tmx_data, self.game.map_layer, self.sprite_layer, True
            )
        if sprite.feet.colliderect(self.collider) and not self.opened:
            sprite.move_back(dt)


class DoorManager:
    """ This class handles doors and the update cycle for each of them.
    """
    def __init__(self, game: Game):
        """Constructs all necessary attributes for the doormanager object

        Args:
            game (Game): the game class instance for the running game
        """
        self.game: Game = game
        self.doors: dict[str, Door] = {}

    def new_door(self, id_: str, collider_layer: str, sprite_layer: str) -> None:
        """Creates a new door object and adds it to the manager

        Args:
            id_ (str): a unique id for the door to be used for accessing it
            collider_layer (str): the layer name for the collider
            sprite_layer (str): the layer name with the closed state sprite
        """
        if id_ in self.doors:
            logger.warning("DoorManager: Door with id {} already exists", id_)
            return
        logger.info(
            "DoorManager: Creating new door (id {}, collider {}, sprite {})",
            id_,
            collider_layer,
            sprite_layer,
        )
        self.doors[id_] = Door(self.game, collider_layer, sprite_layer)

    def get_door(self, id_: str) -> Door:
        """Gets the door instance for the unique id specified

        Args:
            id_ (str): unique id for the door to be returned

        Returns:
            Door: door associated with the unique id
        """
        if id_ not in self.doors:
            logger.warning("DoorManager: Door with id {} does not exist", id_)
            return None
        return self.doors[id_]

    def open_door_by_id(self, id_: str) -> None:
        """Opens the door associated with the unique id specified

        Args:
            id_ (str): door id to select
        """
        if id_ not in self.doors:
            logger.warning("DoorManager: Door with id {} does not exist", id_)
            return
        if self.doors[id_].get_opened():
            return
        logger.info("DoorManager: Opening door with id {}", id_)
        self.doors[id_].open()

    def open_door_for_millis_by_id(self, id_: str, millis: int) -> None:
        """Opens the door associated with the unique id specified for a set amount of milliseconds

        Args:
            id_ (str): door id to select
            millis (int): amount of milliseconds to open the door for
        """
        if id_ not in self.doors:
            logger.warning("DoorManager: Door with id {} does not exist", id_)
            return
        if self.doors[id_].get_opened():
            return
        logger.info(
            "DoorManager: Opening door with id {} for {} milliseconds", id_, millis
        )
        self.doors[id_].open_for_millis(millis)

    def close_door_by_id(self, id_: str) -> None:
        """Closes the door associated with the unique id specified

        Args:
            id_ (str): door id to select
        """
        if id_ not in self.doors:
            logger.warning("DoorManager: Door with id {} does not exist", id_)
            return
        if not self.doors[id_].get_opened():
            return
        logger.info("DoorManager: Closing door with id {}", id_)
        self.doors[id_].close()

    def update(self, sprite: Player, dt: float) -> None:
        """Handles the colliding with all doors and the player

        Args:
            sprite (Player): the player object to check the collision with
            dt (float): dt
        """
        for door in self.doors.values():
            door.update(sprite, dt)
