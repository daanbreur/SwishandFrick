import pygame
from enums import Skills, Gems
from utils import getFontAtSize, set_layer_visibilty, check_gem, add_gem
from constants import PAUSE_BLINK_TIME_MS

from MenuButton import MenuButton

import logging

class Ingame:
  def __init__(self, game) -> None:
    self.game = game

    self.walls = []
    for obj in self.game.tmx_data.get_layer_by_name("walls")[:]: 
      logging.debug(f"Created Wall at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.shallowwater = []
    for obj in self.game.tmx_data.get_layer_by_name("shallowwater")[:]:
      logging.debug(f"Created Shallowwater at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.shallowwater.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    
    self.blue_gem_collider = self.game.tmx_data.get_layer_by_name("blue_gem_collider")[0]
    self.red_gem_collider = self.game.tmx_data.get_layer_by_name("red_gem_collider")[0]
    self.purple_gem_collider = self.game.tmx_data.get_layer_by_name("purple_gem_collider")[0]
    self.green_gem_collider = self.game.tmx_data.get_layer_by_name("green_gem_collider")[0]
    self.orange_gem_collider = self.game.tmx_data.get_layer_by_name("orange_gem_collider")[0]
    self.pink_gem_collider = self.game.tmx_data.get_layer_by_name("pink_gem_collider")[0]
    self.lemon_gem_collider = self.game.tmx_data.get_layer_by_name("lemon_gem_collider")[0]

  def draw(self, screen) -> None:
    self.game.group.center(self.game.player.rect.center)
    self.game.group.draw(screen)

  def update(self, dt: float) -> None:
    self.game.group.update(dt)

    def add_and_hide_gem(layername: str, gem: Gems) -> None:
      set_layer_visibilty(self.game.tmx_data, self.game.map_layer, layername, False)
      add_gem(sprite, gem)

    
    for sprite in self.game.group.sprites():
      if sprite.feet.collidelist(self.walls) > -1: sprite.move_back(dt)
      if sprite.feet.collidelist(self.shallowwater) > -1 and not Skills.SWIM in sprite.skills: sprite.move_back(dt)
      
      if sprite.feet.colliderect(self.blue_gem_collider.x, self.blue_gem_collider.y, self.blue_gem_collider.width, self.blue_gem_collider.height) and not check_gem(sprite, Gems.BLUE): add_and_hide_gem("blue_gem", Gems.BLUE)
      if sprite.feet.colliderect(self.red_gem_collider.x, self.red_gem_collider.y, self.red_gem_collider.width, self.red_gem_collider.height) and not check_gem(sprite, Gems.RED): add_and_hide_gem("red_gem", Gems.RED)
      if sprite.feet.colliderect(self.purple_gem_collider.x, self.purple_gem_collider.y, self.purple_gem_collider.width, self.purple_gem_collider.height) and not check_gem(sprite, Gems.PURPLE): add_and_hide_gem("purple_gem", Gems.PURPLE)
      if sprite.feet.colliderect(self.green_gem_collider.x, self.green_gem_collider.y, self.green_gem_collider.width, self.green_gem_collider.height) and not check_gem(sprite, Gems.GREEN): add_and_hide_gem("green_gem", Gems.GREEN)
      if sprite.feet.colliderect(self.orange_gem_collider.x, self.orange_gem_collider.y, self.orange_gem_collider.width, self.orange_gem_collider.height) and not check_gem(sprite, Gems.ORANGE): add_and_hide_gem("orange_gem", Gems.ORANGE)
      if sprite.feet.colliderect(self.pink_gem_collider.x, self.pink_gem_collider.y, self.pink_gem_collider.width, self.pink_gem_collider.height) and not check_gem(sprite, Gems.PINK): add_and_hide_gem("pink_gem", Gems.PINK)
      if sprite.feet.colliderect(self.lemon_gem_collider.x, self.lemon_gem_collider.y, self.lemon_gem_collider.width, self.lemon_gem_collider.height) and not check_gem(sprite, Gems.LEMON): add_and_hide_gem("lemon_gem", Gems.LEMON)
