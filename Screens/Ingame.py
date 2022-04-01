from re import S
import pygame
from enums import Skills, Gems
from utils import add_skill, check_skill, get_layer_visibility, getFontAtSize, resource_path, set_layer_visibilty, check_gem, add_gem, tile_object_to_rect
from constants import PAUSE_BLINK_TIME_MS, RESOURCES_DIR

from MenuButton import MenuButton

import logging
f_key = False
class Ingame:
  def __init__(self, game) -> None:
    self.game = game
    self.font = getFontAtSize(fontSize=20)
    
    self.f_key_pressed = False
    
    self.door_one_time = 0
    self.door_lever_water_enabled = False
    self.door_lever_one_enabled = False

    self.lever_lever_one_enabled = False
    self.lever_lever_two_enabled = False
    self.lever_lever_three_enabled = False
    self.lever_lever_four_enabled = False
    self.lever_lever_five_enabled = False
    self.lever_lever_six_enabled = False
    
    self.gem_door_opened = False
    self.music_door_opened = False
    self.gear_wall_opened = False
    self.water_wall_opened = False 


    self.walls = []
    for obj in self.game.tmx_data.get_layer_by_name("walls")[:]: 
      logging.info(f"Created Wall at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.shallowwater = []
    for obj in self.game.tmx_data.get_layer_by_name("shallowwater")[:]:
      logging.info(f"Created Shallowwater at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.shallowwater.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    
    self.soft_wall_low_range = []
    for obj in self.game.tmx_data.get_layer_by_name("soft_wall_low_range")[:]:
      logging.info(f"Created Soft Wall Low Range at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.soft_wall_low_range.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.soft_wall_high_range = []
    for obj in self.game.tmx_data.get_layer_by_name("soft_wall_high_range")[:]:
      logging.info(f"Created Soft Wall High Range at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.soft_wall_high_range.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.soft_wall_low_collider = []
    for obj in self.game.tmx_data.get_layer_by_name("soft_wall_low_collider")[:]:
      logging.info(f"Created Soft Wall Low Collider at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.soft_wall_low_collider.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.soft_wall_high_collider = []
    for obj in self.game.tmx_data.get_layer_by_name("soft_wall_high_collider")[:]:
      logging.info(f"Created Soft Wall High Collider at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.soft_wall_high_collider.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    
    self.gear_wall_collider = []
    for obj in self.game.tmx_data.get_layer_by_name("gear_wall_collider")[:]:
      logging.info(f"Created Gear Wall Collider at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.gear_wall_collider.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.shallow_water_finish = []
    for obj in self.game.tmx_data.get_layer_by_name("shallow_water_finish")[:]:
      logging.info(f"Created Shallow Water Finish at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.shallow_water_finish.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    
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
    self.lever_water_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_water_range")[0])
    self.house_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("house_door_collider")[0])
    self.lever_spawn_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_spawn_range")[0])
    self.lever_door_one_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_door_one_collider")[0])
    self.button_house_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("button_house_range")[0])
    self.simon_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_door_collider")[0])
    self.puzzle_door_one = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("levers_door_collider")[0])
    self.simon_sign_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_sign_range")[0])
    self.beach_sign_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("beach_sign_range")[0])
    self.lever_complete_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_complete_range")[0])
    self.music_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_door_collider")[0])
    self.gem_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("gem_door_collider")[0])
    self.beach_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("beach_door_collider")[0])

    self.hamer_lever_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("hamer_lever_range")[0])

    self.music_button_green_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_green_range")[0])
    self.music_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_one_range")[0])
    self.music_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_two_range")[0])
    self.music_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_three_range")[0])
    self.music_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_four_range")[0])
    self.music_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_red_range")[0])

    self.math_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_red_range")[0])
    self.math_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_one_range")[0])
    self.math_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_two_range")[0])
    self.math_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_three_range")[0])
    self.math_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_button_four_range")[0])

    self.lever_lever_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_one_range")[0])
    self.lever_lever_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_two_range")[0])
    self.lever_lever_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_three_range")[0])
    self.lever_lever_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_four_range")[0])
    self.lever_lever_five_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_five_range")[0])
    self.lever_lever_six_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_six_range")[0])

    self.mors_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_door_collider")[0])
    self.math_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("math_door_collider")[0])
    self.beach_button_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("beach_button_range")[0])

    self.mors_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_red_range")[0])
    self.mors_button_blue_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_blue_range")[0])
    self.mors_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_one_range")[0])
    self.mors_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_two_range")[0])
    self.mors_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_three_range")[0])
    self.mors_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_four_range")[0])
    self.mors_button_five_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_five_range")[0])
    self.mors_button_six_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("mors_button_six_range")[0])

    self.final_gem_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("final_gem_door_collider")[0])
    self.final_gem_button_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("final_gem_button_range")[0])

    self.gear_wall_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("gear_wall_range")[0])

    self.konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
    self.komani_code_entered = []
    self.konami_code_index = 0
    self.komani_code_completed = False

    self.konami_text_show = False
    self.simon_text_show = False
    self.math_text_show = False
    
    self.music_required = [1,2,3,2,1,2,3,2,1,3,4,4,4,4,4,3]
    self.music_entered = []
    self.music_index = 0
    self.music_completed = False

    self.math_required = [3, 4, 1, 2]
    self.math_entered = []
    self.math_completed = False

    self.morse_required = [4,3,6,5,1,2]
    self.morse_entered = []
    self.morse_completed = False
    
  def draw(self, screen) -> None:
    self.game.group.center(self.game.player.rect.center)
    self.game.group.draw(screen)
    sign_one = self.font.render("Do the konami code", False, (255, 255, 255))
    if self.konami_text_show: screen.blit(sign_one, (screen.get_width()/2, screen.get_height()/2 - sign_one.get_height()/2 - 50))
    sign_two = self.font.render("RRLLLR", False, (255, 255, 255))
    if self.simon_text_show: screen.blit(sign_two, (screen.get_width()/2, screen.get_height()/2 - sign_two.get_height()/2 - 50))
    sign_three = self.font.render("(((wortel van 6.512.704) + 7)/3)*4", False, (255, 255, 255))
    if self.math_text_show: screen.blit(sign_three, (screen.get_width()/2, screen.get_height()/2 - sign_three.get_height()/2 - 50))



  def handle_input(self, event) -> None:
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_f:
        self.f_key_pressed = True
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

      if sprite.feet.collidelist(self.soft_wall_low_range) > -1 and check_skill(sprite, Skills.HAMMER): hide_layer("soft_wall_low")
      if sprite.feet.collidelist(self.soft_wall_low_collider) > -1 and not check_skill(sprite, Skills.HAMMER): sprite.move_back(dt)
      if sprite.feet.collidelist(self.soft_wall_high_range) > -1 and check_skill(sprite, Skills.HAMMER): hide_layer("soft_wall_high")
      if sprite.feet.collidelist(self.soft_wall_high_collider) > -1 and not check_skill(sprite, Skills.HAMMER): sprite.move_back(dt)

      if sprite.feet.colliderect(self.gear_wall_range) and check_gem(sprite, Gems.GEAR):
        self.gear_wall_opened = True
        hide_layer("gear_wall")
      if sprite.feet.collidelist(self.gear_wall_collider) > -1 and not self.gear_wall_opened: sprite.move_back(dt)

      if sprite.feet.colliderect(self.gem_door_range) and check_gem(sprite, Gems.BLUE) and check_gem(sprite, Gems.RED) and check_gem(sprite, Gems.GREEN): 
        self.gem_door_opened = True
        hide_layer("gem_door_one")
      if sprite.feet.colliderect(self.gem_door_collider) and not self.gem_door_opened: sprite.move_back(dt)

      if sprite.feet.colliderect(self.final_gem_button_range) and check_gem(sprite, Gems.ORANGE) and check_gem(sprite, Gems.LEMON) and check_gem(sprite, Gems.PURPLE) and check_gem(sprite, Gems.PINK) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.water_wall_opened = True
        hide_layer("water_empty")
      if sprite.feet.collidelist(self.shallow_water_finish) > -1 and not self.water_wall_opened: sprite.move_back(dt)

      if sprite.feet.colliderect(self.lever_complete_range) and self.lever_lever_one_enabled and self.lever_lever_two_enabled and not self.lever_lever_three_enabled and not self.lever_lever_four_enabled and not self.lever_lever_five_enabled and self.lever_lever_six_enabled:
        add_skill(sprite, Skills.HAMMER)
      
      if sprite.feet.colliderect(self.music_door_collider) and not self.music_door_opened: sprite.move_back(dt)
      if sprite.feet.colliderect(self.final_gem_door_collider) and not self.morse_completed: sprite.move_back(dt)

      if sprite.feet.colliderect(self.konami_sign): self.konami_text_show = True 
      else: self.konami_text_show = False
      if sprite.feet.colliderect(self.simon_sign_range): self.simon_text_show = True 
      else: self.simon_text_show = False
      if sprite.feet.colliderect(self.beach_sign_range): self.math_text_show = True
      else: self.math_text_show = False

      if sprite.feet.colliderect(self.button__one_range) and self.f_key_pressed == True:
        hide_layer("button_door_one")
        self.door_one_time = pygame.time.get_ticks() + 2000
      if sprite.feet.colliderect(self.button_door_one_collider) and pygame.time.get_ticks() > self.door_one_time: sprite.move_back(dt)
      if pygame.time.get_ticks() > self.door_one_time: show_layer("button_door_one")


      if sprite.feet.colliderect(self.button_house_range) and self.f_key_pressed == True:
        hide_layer("button_door_two")
        self.door_one_time = pygame.time.get_ticks() + 4000
      if sprite.feet.colliderect(self.simon_door_collider): 
        if self.game.puzzles['simonsays'].solved: pass
        elif pygame.time.get_ticks() > self.door_one_time: sprite.move_back(dt)
      if self.game.puzzles['simonsays'].solved: hide_layer("button_door_two")
      elif pygame.time.get_ticks() > self.door_one_time: show_layer("button_door_two")


      if sprite.feet.colliderect(self.house_door_collider) and not self.door_lever_water_enabled: sprite.move_back(dt)
      if sprite.feet.colliderect(self.lever_water_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.door_lever_water_enabled = not self.door_lever_water_enabled
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_water", not get_layer_visibility(self.game.tmx_data, "lever_water"))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_door_two", not get_layer_visibility(self.game.tmx_data, "lever_door_two"))


      if sprite.feet.colliderect(self.lever_door_one_collider) and not self.door_lever_one_enabled: sprite.move_back(dt)
      if sprite.feet.colliderect(self.lever_spawn_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.door_lever_one_enabled = not self.door_lever_one_enabled
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_spawn", not get_layer_visibility(self.game.tmx_data, "lever_spawn"))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_door_one", not get_layer_visibility(self.game.tmx_data, "lever_door_one"))
      
      if sprite.feet.colliderect(self.puzzle_door_one) and not self.game.puzzles['simonsays'].solved: sprite.move_back(dt)
      if self.game.puzzles['simonsays'].solved: hide_layer("puzzle_door_one")

      if sprite.feet.colliderect(self.lever_lever_one_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.lever_lever_one_enabled = not self.lever_lever_one_enabled
        logging.info("Levers Enabled: %s %s %s %s %s %s" % (self.lever_lever_one_enabled, self.lever_lever_two_enabled, self.lever_lever_three_enabled, self.lever_lever_four_enabled, self.lever_lever_five_enabled, self.lever_lever_six_enabled))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_one", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_one"))

      if sprite.feet.colliderect(self.lever_lever_two_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.lever_lever_two_enabled = not self.lever_lever_two_enabled
        logging.info("Levers Enabled: %s %s %s %s %s %s" % (self.lever_lever_one_enabled, self.lever_lever_two_enabled, self.lever_lever_three_enabled, self.lever_lever_four_enabled, self.lever_lever_five_enabled, self.lever_lever_six_enabled))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_two", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_two"))

      if sprite.feet.colliderect(self.lever_lever_three_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.lever_lever_three_enabled = not self.lever_lever_three_enabled
        logging.info("Levers Enabled: %s %s %s %s %s %s" % (self.lever_lever_one_enabled, self.lever_lever_two_enabled, self.lever_lever_three_enabled, self.lever_lever_four_enabled, self.lever_lever_five_enabled, self.lever_lever_six_enabled))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_three", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_three"))

      if sprite.feet.colliderect(self.lever_lever_four_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.lever_lever_four_enabled = not self.lever_lever_four_enabled
        logging.info("Levers Enabled: %s %s %s %s %s %s" % (self.lever_lever_one_enabled, self.lever_lever_two_enabled, self.lever_lever_three_enabled, self.lever_lever_four_enabled, self.lever_lever_five_enabled, self.lever_lever_six_enabled))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_four", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_four"))

      if sprite.feet.colliderect(self.lever_lever_five_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.lever_lever_five_enabled = not self.lever_lever_five_enabled
        logging.info("Levers Enabled: %s %s %s %s %s %s" % (self.lever_lever_one_enabled, self.lever_lever_two_enabled, self.lever_lever_three_enabled, self.lever_lever_four_enabled, self.lever_lever_five_enabled, self.lever_lever_six_enabled))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_five", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_five"))

      if sprite.feet.colliderect(self.lever_lever_six_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.lever_lever_six_enabled = not self.lever_lever_six_enabled
        logging.info("Levers Enabled: %s %s %s %s %s %s" % (self.lever_lever_one_enabled, self.lever_lever_two_enabled, self.lever_lever_three_enabled, self.lever_lever_four_enabled, self.lever_lever_five_enabled, self.lever_lever_six_enabled))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_puzzle_six", not get_layer_visibility(self.game.tmx_data, "lever_puzzle_six"))

      if sprite.feet.colliderect(self.hamer_lever_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.music_door_opened = not self.music_door_opened
        logging.info("Music Door: %s" % self.music_door_opened)
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_hamer", not get_layer_visibility(self.game.tmx_data, "lever_hamer"))
        set_layer_visibilty(self.game.tmx_data, self.game.map_layer, "lever_door_three", not get_layer_visibility(self.game.tmx_data, "lever_door_three"))


      if sprite.feet.colliderect(self.music_button_green_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        logging.info("Playing music for musicgame")
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/songlevel.wav" ))
        pygame.mixer.music.play()

      if sprite.feet.colliderect(self.music_button_red_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        show_layer("puzzle_door_two")
        logging.info("Resetting musicgame")
        self.music_entered = []
        self.music_completed = False
      
      if sprite.feet.colliderect(self.music_button_one_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.music_entered.append(1)
        logging.info("Music Notes Entered: %s" % self.music_entered)
        if self.music_required == self.music_entered:
          self.music_completed = True
          hide_layer("puzzle_door_two")
          logging.info("Music Completed, Opening Door")	
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes1.wav" ))
        pygame.mixer.music.play()
      if sprite.feet.colliderect(self.music_button_two_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.music_entered.append(2)
        logging.info("Music Notes Entered: %s" % self.music_entered)
        if self.music_required == self.music_entered:
          self.music_completed = True
          hide_layer("puzzle_door_two")
          logging.info("Music Completed, Opening Door")	
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes2.wav" ))
        pygame.mixer.music.play()
      if sprite.feet.colliderect(self.music_button_three_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.music_entered.append(3)
        logging.info("Music Notes Entered: %s" % self.music_entered)
        if self.music_required == self.music_entered:
          self.music_completed = True
          hide_layer("puzzle_door_two")
          logging.info("Music Completed, Opening Door")	
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes3.wav" ))
        pygame.mixer.music.play()
      if sprite.feet.colliderect(self.music_button_four_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.music_entered.append(4)
        logging.info("Music Notes Entered: %s" % self.music_entered)
        if self.music_required == self.music_entered:
          self.music_completed = True
          hide_layer("puzzle_door_two")
          logging.info("Music Completed, Opening Door")	
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes4.wav" ))
        pygame.mixer.music.play() 
      if self.music_required == self.music_entered:
          self.music_completed = True
      else: 
        self.music_completed = False
        show_layer("puzzle_door_two")

      if sprite.feet.colliderect(self.beach_door_collider) and not self.music_completed: sprite.move_back(dt)
      if sprite.feet.colliderect(self.beach_button_range) and self.f_key_pressed == True:
        hide_layer("puzzle_door")
        self.door_one_time = pygame.time.get_ticks() + 12000
      if sprite.feet.colliderect(self.math_door_collider):
        if self.morse_completed:
          pass
        elif pygame.time.get_ticks() > self.door_one_time: sprite.move_back(dt)
      if pygame.time.get_ticks() > self.door_one_time and not self.morse_completed: show_layer("puzzle_door")

      if sprite.feet.colliderect(self.mors_door_collider) and not self.math_entered: sprite.move_back(dt)

      if sprite.feet.colliderect(self.math_button_red_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        show_layer("puzzle_door_three")
        logging.info("Resetting mathgame")
        self.math_entered = []
        self.math_completed = False
      
      if sprite.feet.colliderect(self.math_button_one_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.math_entered.append(1)
        logging.info("Math Entered: %s" % self.math_entered)
        if self.math_required == self.math_entered:
          self.math_completed = True
          hide_layer("puzzle_door_three")
          logging.info("Math Completed, Opening Door")	
      if sprite.feet.colliderect(self.math_button_two_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.math_entered.append(2)
        logging.info("Math Entered: %s" % self.math_entered)
        if self.math_required == self.math_entered:
          self.math_completed = True
          hide_layer("puzzle_door_three")
          logging.info("Math Completed, Opening Door")	
      if sprite.feet.colliderect(self.math_button_three_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.math_entered.append(3)
        logging.info("Math Entered: %s" % self.math_entered)
        if self.math_required == self.math_entered:
          self.math_completed = True
          hide_layer("puzzle_door_three")
          logging.info("Math Completed, Opening Door")
      if sprite.feet.colliderect(self.math_button_four_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.math_entered.append(4)
        logging.info("Math Entered: %s" % self.math_entered)
        if self.math_required == self.math_entered:
          self.math_completed = True
          hide_layer("puzzle_door_three")
          logging.info("Math Completed, Opening Door")	
      if self.math_required == self.math_entered: self.math_completed = True
      else: self.math_completed = False

      if sprite.feet.colliderect(self.mors_button_blue_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        logging.info("Playing music for morsegame")
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/morselevel.wav" ))
        pygame.mixer.music.play()

      if sprite.feet.colliderect(self.mors_button_red_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        show_layer("puzzle_door")
        show_layer("puzzle_door_four")
        logging.info("Resetting morsegame")
        self.morse_entered = []
        self.morse_completed = False
      
      if sprite.feet.colliderect(self.mors_button_one_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.morse_entered.append(1)
        logging.info("morse Notes Entered: %s" % self.morse_entered)
        if self.morse_required == self.morse_entered:
          self.morse_completed = True
          hide_layer("puzzle_door_four")
          hide_layer("puzzle_door")
          logging.info("Morse Completed, Opening Door")	
      if sprite.feet.colliderect(self.mors_button_two_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.morse_entered.append(2)
        logging.info("morse Notes Entered: %s" % self.morse_entered)
        if self.morse_required == self.morse_entered:
          self.morse_completed = True
          hide_layer("puzzle_door_four")
          hide_layer("puzzle_door")
          logging.info("Morse Completed, Opening Door")
      if sprite.feet.colliderect(self.mors_button_three_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.morse_entered.append(3)
        logging.info("morse Notes Entered: %s" % self.morse_entered)
        if self.morse_required == self.morse_entered:
          self.morse_completed = True
          hide_layer("puzzle_door_four")
          hide_layer("puzzle_door")
          logging.info("Morse Completed, Opening Door")
      if sprite.feet.colliderect(self.mors_button_four_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.morse_entered.append(4)
        logging.info("morse Notes Entered: %s" % self.morse_entered)
        if self.morse_required == self.morse_entered:
          self.morse_completed = True
          hide_layer("puzzle_door_four")
          hide_layer("puzzle_door")
          logging.info("Morse Completed, Opening Door")
      if sprite.feet.colliderect(self.mors_button_five_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.morse_entered.append(5)
        logging.info("Morse Notes Entered: %s" % self.morse_entered)
        if self.morse_required == self.morse_entered:
          self.morse_completed = True
          hide_layer("puzzle_door_four")
          hide_layer("puzzle_door")
          logging.info("Morse Completed, Opening Door")
      if sprite.feet.colliderect(self.mors_button_six_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        self.morse_entered.append(6)
        logging.info("Morse Notes Entered: %s" % self.morse_entered)
        if self.morse_required == self.morse_entered:
          self.morse_completed = True
          hide_layer("puzzle_door_four")
          hide_layer("puzzle_door")
          logging.info("Morse Completed, Opening Door")
      