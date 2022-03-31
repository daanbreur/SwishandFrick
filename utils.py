import logging
import pygame
import os
import sys
import pytmx
import pyscroll
from constants import RESOURCES_DIR

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

def initialize_screen(width: int, height: int) -> pygame.Surface:
  screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
  logging.debug("Initialized screen with size %s", screen.get_size())
  return screen

def load_image(filename: str) -> pygame.Surface:
  return pygame.image.load(str(RESOURCES_DIR / filename))

def getFontAtSize(fontName="Level Up Level Up.otf", fontSize=16) -> pygame.font.Font:
  return pygame.font.Font(RESOURCES_DIR / "fonts" / fontName, fontSize)

def set_layer_visibilty(tmx_data: pytmx.TiledMap, map_layer: pyscroll.BufferedRenderer, layerName: str, visible: bool) -> None:
  tmx_data.get_layer_by_name(layerName).visible = visible
  map_layer.data.tmx = tmx_data
  map_layer.redraw_tiles(map_layer._buffer)
  return

def add_gem(player, gem) -> None:
  if not check_gem(player, gem):
    logging.info(f"add_gem {gem} to {player.inventory}")
    player.inventory.append(gem)
  return

def check_gem(player, gem) -> bool:
  return gem in player.inventory