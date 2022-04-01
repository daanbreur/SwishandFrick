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
  logging.info("Initialized screen with size %s", screen.get_size())
  return screen

def load_image(filename: str) -> pygame.Surface:
  return pygame.image.load(str(RESOURCES_DIR / filename))

def getFontAtSize(fontName="Level Up Level Up.otf", fontSize=16) -> pygame.font.Font:
  return pygame.font.Font(RESOURCES_DIR / "fonts" / fontName, fontSize)

def set_layer_visibilty(tmx_data: pytmx.TiledMap, map_layer: pyscroll.BufferedRenderer, layerName: str, visible: bool) -> None:
  tmx_data.get_layer_by_name(layerName).visible = visible
  map_layer.data.tmx = tmx_data
  map_layer.redraw_tiles(map_layer._buffer)
  # logging.info(f"Set {layerName} visible to {visible}")
  return

def get_layer_visibility(tmx_data: pytmx.TiledMap, layerName: str) -> bool:
  return tmx_data.get_layer_by_name(layerName).visible

def add_skill(player, skill) -> None:
  if not check_skill(player, skill):
    player.game.toastManager.addToast(f"You now have {skill}!")
    logging.info(f"add_skill {skill} to {player.skills}")
    player.skills.append(skill)
  return

def check_skill(player, skill) -> bool:
  return skill in player.skills

def add_gem(player, gem) -> None:
  if not check_gem(player, gem):
    player.game.toastManager.addToast(f"You found a {gem}!")
    logging.info(f"add_gem {gem} to {player.inventory}")
    player.inventory.append(gem)
  return
  
def remove_gem(player, gem) -> None:
  if not check_gem(player, gem):
    player.game.toastManager.addToast(f"You lost a {gem}!")
    logging.info(f"remove_gem {gem} from {player.inventory}")
    player.inventory.remove(gem)
  return

def check_gem(player, gem) -> bool:
  return gem in player.inventory

def tile_object_to_rect(tile_object: pytmx.TiledObject) -> pygame.Rect:
  return pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)