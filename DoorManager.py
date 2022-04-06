from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from Player import Player
  from game import Game

import pygame
import logging

from utils import tile_object_to_rect, get_layer_visibility, set_layer_visibilty

class Door():
  def __init__(self, game: Game, collider_layer: str, sprite_layer: str):
    self.game: Game = game
    self.opened: bool = False
    self.openedUntil = None
    self.collider_layer: str = collider_layer
    self.sprite_layer: str = sprite_layer
    self.collider: pygame.Rect = tile_object_to_rect(self.game.tmx_data.get_layer_by_name(self.collider_layer)[0])

  def open(self) -> None:
    self.opened = True
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, self.sprite_layer, False)
  
  def close(self) -> None:
    self.opened = False
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, self.sprite_layer, True)

  def openForMillis(self, millis: int) -> None:
    self.opened = True
    self.openedUntil = pygame.time.get_ticks() + millis
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, self.sprite_layer, False)

  def setOpened(self, opened: bool) -> None:
    self.opened = opened
    set_layer_visibilty(self.game.tmx_data, self.game.map_layer, self.sprite_layer, not opened)

  def getOpened(self) -> bool:
    return self.opened

  def update(self, sprite: Player, dt: float) -> None:
    if self.openedUntil != None and pygame.time.get_ticks() > self.openedUntil:
      self.opened = False
      self.openedUntil = None
      set_layer_visibilty(self.game.tmx_data, self.game.map_layer, self.sprite_layer, True)
    if sprite.feet.colliderect(self.collider) and not self.opened: sprite.move_back(dt)

class DoorManager():
  def __init__(self, game: Game):
    self.game: Game = game
    self.doors: dict[str, Door] = {}

  def newDoor(self, id: str, collider_layer: str, sprite_layer: str) -> None:
    if id in self.doors:
      logging.warning(f"DoorManager: Door with id {id} already exists")
      return
    logging.info(f"DoorManager: Creating new door (id {id}, collider {collider_layer}, sprite {sprite_layer})")
    self.doors[id] = Door(self.game, collider_layer, sprite_layer)
  
  def getDoor(self, id: str) -> Door:
    if id not in self.doors:
      logging.warning(f"DoorManager: Door with id {id} does not exist")
      return None
    return self.doors[id]

  def openDoorById(self, id: str) -> None:
    if id not in self.doors:
      logging.warning(f"DoorManager: Door with id {id} does not exist")
      return
    if self.doors[id].getOpened(): return
    logging.info(f"DoorManager: Opening door with id {id}")
    self.doors[id].open()
  
  def openDoorForMillisById(self, id: str, millis: int) -> None:
    if id not in self.doors:
      logging.warning(f"DoorManager: Door with id {id} does not exist")
      return
    if self.doors[id].getOpened(): return
    logging.info(f"DoorManager: Opening door with id {id} for {millis} milliseconds")
    self.doors[id].openForMillis(millis)

  def closeDoorById(self, id: str) -> None:
    if id not in self.doors:
      logging.warning(f"DoorManager: Door with id {id} does not exist")
      return
    if not self.doors[id].getOpened(): return
    logging.info(f"DoorManager: Closing door with id {id}")
    self.doors[id].close()

  def update(self, sprite: Player, dt: float) -> None:
    for door in self.doors.values():
      door.update(sprite, dt)