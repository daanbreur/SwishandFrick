import pygame
from enums import Skills, Gems
from utils import add_skill, check_skill, getFontAtSize, set_layer_visibilty, check_gem, add_gem, tile_object_to_rect
from constants import PAUSE_BLINK_TIME_MS

from MenuButton import MenuButton

import logging
f_key = False
class Ingame:
  def __init__(self, game) -> None:
    self.game = game
    self.font = getFontAtSize(fontSize=20)
    
    self.f_key_pressed = False
    
    self.door_one_time = 0

    self.walls = []
    for obj in self.game.tmx_data.get_layer_by_name("walls")[:]: 
      logging.debug(f"Created Wall at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.shallowwater = []
    for obj in self.game.tmx_data.get_layer_by_name("shallowwater")[:]:
      logging.debug(f"Created Shallowwater at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.shallowwater.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    
    self.blue_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("blue_gem_collider")[0])
    self.red_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("red_gem_collider")[0])
    self.purple_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("purple_gem_collider")[0])
    self.green_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("green_gem_collider")[0])
    self.orange_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("orange_gem_collider")[0])
    self.pink_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("pink_gem_collider")[0])
    self.lemon_gem_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lemon_gem_collider")[0])
    self.gear_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("gear_collider")[0])
    self.boots_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("boots_collider")[0])
    self.red_key_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("red_key_collider")[0])
    self.red_key_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("red_key_range")[0])
    self.red_key_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("red_key_door_collider")[0])
    self.gem_door_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("gem_door_range")[0])
    self.konami_sign = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("konami_sign")[0])
    self.button_door_one_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("button_door_one_collider")[0])
    self.button__one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("button__one_range")[0])
    
    self.konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
    self.komani_code_entered = []
    self.konami_code_index = 0
    self.komani_code_completed = False
    self.konami_text_show = False

    
  def draw(self, screen) -> None:
    self.game.group.center(self.game.player.rect.center)
    self.game.group.draw(screen)
    sign_one = self.font.render("Do the konami code", False, (255, 255, 255))
    if self.konami_text_show: screen.blit(sign_one, (screen.get_width()/2 - sign_one.get_width()/2, screen.get_height()/2 - sign_one.get_height()/2 - 50))

  def handle_input(self, event) -> None:
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_f:
        self.f_key_pressed = True
        logging.info("f down")
      
      elif not self.komani_code_completed:
        if event.key == self.konami_code[self.konami_code_index]:
          self.komani_code_entered.append(event.key)
          self.konami_code_index += 1

          logging.info(f"Konami code index: {self.konami_code_index} / {len(self.konami_code)} | {self.konami_code[self.konami_code_index-1]}")
          if self.konami_code == self.komani_code_entered:
            logging.info("Konami code entered correctly")
            self.komani_code_completed = True
            if not check_skill(self.game.player, Skills.SWIM):
              logging.info("Komani code entered correctly, adding swim skill")
              add_skill(self.game.player, Skills.SWIM)

    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_f:
        self.f_key_pressed = False
        logging.info("f up")
      
  def update(self, dt: float) -> None:
    self.game.group.update(dt)

    def add_and_hide_skill(layername: str, skill: Skills) -> None:
      set_layer_visibilty(self.game.tmx_data, self.game.map_layer, layername, False)
      add_skill(sprite, skill)

    def add_and_hide_gem(layername: str, gem: Gems) -> None:
      set_layer_visibilty(self.game.tmx_data, self.game.map_layer, layername, False)
      add_gem(sprite, gem)
      
    def hide_layer(layername: str) -> None:
      set_layer_visibilty(self.game.tmx_data, self.game.map_layer, layername, False)
      
    def show_layer(layername: str) -> None:
      set_layer_visibilty(self.game.tmx_data, self.game.map_layer, layername, True)

    
    for sprite in self.game.group.sprites():
      if sprite.feet.collidelist(self.walls) > -1: sprite.move_back(dt)
      if sprite.feet.collidelist(self.shallowwater) > -1 and not Skills.SWIM in sprite.skills: sprite.move_back(dt)
      
      if sprite.feet.colliderect(self.blue_gem_collider) and not check_gem(sprite, Gems.BLUE): add_and_hide_gem("blue_gem", Gems.BLUE)
      if sprite.feet.colliderect(self.red_gem_collider) and not check_gem(sprite, Gems.RED): add_and_hide_gem("red_gem", Gems.RED)
      if sprite.feet.colliderect(self.purple_gem_collider) and not check_gem(sprite, Gems.PURPLE): add_and_hide_gem("purple_gem", Gems.PURPLE)
      if sprite.feet.colliderect(self.green_gem_collider) and not check_gem(sprite, Gems.GREEN): add_and_hide_gem("green_gem", Gems.GREEN)
      if sprite.feet.colliderect(self.orange_gem_collider) and not check_gem(sprite, Gems.ORANGE): add_and_hide_gem("orange_gem", Gems.ORANGE)
      if sprite.feet.colliderect(self.pink_gem_collider) and not check_gem(sprite, Gems.PINK): add_and_hide_gem("pink_gem", Gems.PINK)
      if sprite.feet.colliderect(self.lemon_gem_collider) and not check_gem(sprite, Gems.LEMON): add_and_hide_gem("lemon_gem", Gems.LEMON)
      if sprite.feet.colliderect(self.gear_collider) and not check_gem(sprite, Gems.GEAR): add_and_hide_gem("gear", Gems.GEAR)
      if sprite.feet.colliderect(self.boots_collider) and not check_skill(sprite, Skills.RUN): add_and_hide_skill("boots", Skills.RUN)
      if sprite.feet.colliderect(self.red_key_collider) and not check_gem(sprite, Gems.KEY): add_and_hide_gem("red_key", Gems.KEY)
      if sprite.feet.colliderect(self.red_key_door_collider) and not check_gem(sprite, Gems.KEY): sprite.move_back(dt)
      if sprite.feet.colliderect(self.red_key_range) and check_gem(sprite, Gems.KEY): hide_layer("red_key_door")
      if sprite.feet.colliderect(self.gem_door_range) and check_gem(sprite, Gems.BLUE) and check_gem(sprite, Gems.RED) and check_gem(sprite, Gems.GREEN): hide_layer("gem_door_one")
      if sprite.feet.colliderect(self.konami_sign): self.konami_text_show = True 
      else: self.konami_text_show = False
      
      if sprite.feet.colliderect(self.button__one_range) and self.f_key_pressed == True:
        hide_layer("button_door_one")
        self.door_one_time = pygame.time.get_ticks() + 2000
      if sprite.feet.colliderect(self.button_door_one_collider) and pygame.time.get_ticks() > self.door_one_time: sprite.move_back(dt)
      # if pygame.time.get_ticks() > self.door_one_time: show_layer("button_door_one")
