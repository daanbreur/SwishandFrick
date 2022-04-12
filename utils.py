"""Utilities for handling inventory, layers, screen, pyinstaller and more"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union

import os
import sys
import logging
import pygame

from constants import RESOURCES_DIR

if TYPE_CHECKING:
    import pytmx
    import pyscroll
    from pathlib import Path
    from Player import Player
    from enums import Skills, Gems

logger = logging.getLogger(__name__)

def resource_path(relative_path: Union[Path, str]) -> str:
    """Get absolute path to resource, for dev and for PyInstaller

    Args:
        relative_path (Union[Path, str]): relative path to resource

    Returns:
        str: full path to resource
    """
    try:
        base_path = sys._MEIPASS # pylint: disable=W0212 disable=E1101
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def initialize_screen(width: int, height: int) -> pygame.Surface:
    """Initialize new screen with given width and height

    Args:
        width (int): width of screen
        height (int): height of screen

    Returns:
        pygame.Surface: new screen instance
    """
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    logger.info("Initialized screen with size {}", screen.get_size())
    return screen

def load_image(filename: str) -> pygame.Surface:
    """Load image from file

    Args:
        filename (str): relative path to image file

    Returns:
        pygame.Surface: image surface loaded from file
    """
    return pygame.image.load(resource_path(RESOURCES_DIR / filename))

def get_font_at_size(font_name="Level Up Level Up.otf", font_size=16) -> pygame.font.Font:
    """Get font at given size

    Args:
        font_name (str, optional): filename for the font. Defaults to "Level Up Level Up.otf".
        font_size (int, optional): fontsize for the font. Defaults to 16.

    Returns:
        pygame.font.Font: font instance at given size and font
    """
    return pygame.font.Font(resource_path(RESOURCES_DIR / "fonts" / font_name), font_size)

def set_layer_visibility(
    tmx_data: pytmx.TiledMap,
    map_layer: pyscroll.BufferedRenderer,
    layer_name: str,
    visible: bool
) -> None:
    """Set the visibility of the specified layer

    Args:
        tmx_data (pytmx.TiledMap): TileMap data instance to modify
        map_layer (pyscroll.BufferedRenderer): maplayer instance to modify
        layer_name (str): name of the layer to change visibility of
        visible (bool): the new visibility of the layer
    """
    tmx_data.get_layer_by_name(layer_name).visible = visible
    map_layer.data.tmx = tmx_data
    map_layer.redraw_tiles(map_layer._buffer) # pylint: disable=W0212
    logger.debug("Set {} visible to {}", layer_name, visible)

def get_layer_visibility(tmx_data: pytmx.TiledMap, layer_name: str) -> bool:
    """Get the visibility of the specified layer

    Args:
        tmx_data (pytmx.TiledMap): TileMap data instance to get visibility from
        layer_name (str): name of the layer to get visibility from

    Returns:
        bool: visibility of the layer
    """
    return tmx_data.get_layer_by_name(layer_name).visible

def add_skill(player: Player, skill: Skills) -> None:
    """Add skill to players inventory

    Args:
        player (Player): player instance to add skill to
        skill (Skills): skill to add to player
    """
    if not check_skill(player, skill):
        player.game.toastManager.addToast(f"You now have {skill.name}!")
        logger.info("add_skill {} to {}", skill, player.skills)
        player.skills.append(skill)

def check_skill(player: Player, skill: Skills) -> bool:
    """Check if player has skill

    Args:
        player (Player): player instance to check skills of
        skill (Skills): skill to check for

    Returns:
        bool: True if player has skill, False otherwise
    """
    return skill in player.skills

def add_gem(player: Player, gem: Gems) -> None:
    """Add gem to players inventory

    Args:
        player (Player): player instance to add gem to
        gem (Gems): gem to add to player
    """
    if not check_gem(player, gem):
        player.game.toastManager.addToast(f"You found a {gem.name} Gem!")
        logger.info("add_gem {} to {}", gem, player.inventory)
        player.inventory.append(gem)

def remove_gem(player: Player, gem: Gems) -> None:
    """Remove gem from players inventory

    Args:
        player (Player): player instance to remove gem from
        gem (Gems): gem to remove from player
    """
    if not check_gem(player, gem):
        player.game.toastManager.addToast(f"You lost a {gem.name} Gem!")
        logger.info("remove_gem {} from {}", gem, player.inventory)
        player.inventory.remove(gem)

def check_gem(player: Player, gem: Gems) -> bool:
    """Check if player has gem

    Args:
        player (Player): player instance to check gems of
        gem (Gems): gem to check for

    Returns:
        bool: True if player has gem, False otherwise
    """
    return gem in player.inventory

def tile_object_to_rect(tile_object: pytmx.TiledObject) -> pygame.Rect:
    """Convert a pytmx.TiledObject to a pygame.Rect

    Args:
        tile_object (pytmx.TiledObject): pytmx.TileObject to convert

    Returns:
        pygame.Rect: converted pytmx.TileObject to pygame.Rect
    """
    return pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
