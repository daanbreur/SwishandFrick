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

    self.walls = []
    for obj in self.game.tmx_data.get_layer_by_name("walls")[:]: 
      logging.info(f"Created Wall at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
      self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    self.shallowwater = []
    for obj in self.game.tmx_data.get_layer_by_name("shallowwater")[:]:
      logging.info(f"Created Shallowwater at {obj.x}, {obj.y} with dimensions {obj.width}, {obj.height}")
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
    self.lever_water_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_water_range")[0])
    self.house_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("house_door_collider")[0])
    self.lever_spawn_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_spawn_range")[0])
    self.lever_door_one_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_door_one_collider")[0])
    self.button_house_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("button_house_range")[0])
    self.simon_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_door_collider")[0])
    self.puzzle_door_one = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("levers_door_collider")[0])
    self.simon_sign_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("simon_sign_range")[0])
    self.lever_complete_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_complete_range")[0])
    self.music_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_door_collider")[0])
    self.gem_door_collider = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("gem_door_collider")[0])

    self.music_button_green_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_green_range")[0])
    self.music_button_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_one_range")[0])
    self.music_button_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_two_range")[0])
    self.music_button_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_three_range")[0])
    self.music_button_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_four_range")[0])
    self.music_button_red_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("music_button_red_range")[0])


    self.lever_lever_one_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_one_range")[0])
    self.lever_lever_two_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_two_range")[0])
    self.lever_lever_three_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_three_range")[0])
    self.lever_lever_four_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_four_range")[0])
    self.lever_lever_five_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_five_range")[0])
    self.lever_lever_six_range = tile_object_to_rect(self.game.tmx_data.get_layer_by_name("lever_lever_six_range")[0])

    self.konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
    self.komani_code_entered = []
    self.konami_code_index = 0
    self.komani_code_completed = False
    self.konami_text_show = False
    self.simon_text_show = False
    
  def draw(self, screen) -> None:
    self.game.group.center(self.game.player.rect.center)
    self.game.group.draw(screen)
    sign_one = self.font.render("Do the konami code", False, (255, 255, 255))
    if self.konami_text_show: screen.blit(sign_one, (screen.get_width()/2, screen.get_height()/2 - sign_one.get_height()/2 - 50))
    sign_two = self.font.render("RRLLLR", False, (255, 255, 255))
    if self.simon_text_show: screen.blit(sign_two, (screen.get_width()/2, screen.get_height()/2 - sign_two.get_height()/2 - 50))

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

      if sprite.feet.colliderect(self.gem_door_range) and check_gem(sprite, Gems.BLUE) and check_gem(sprite, Gems.RED) and check_gem(sprite, Gems.GREEN): 
        self.gem_door_opened = True
        hide_layer("gem_door_one")
      if sprite.feet.colliderect(self.gem_door_collider) and not self.gem_door_opened: sprite.move_back(dt)

      if sprite.feet.colliderect(self.lever_complete_range) and self.lever_lever_one_enabled and self.lever_lever_two_enabled and not self.lever_lever_three_enabled and not self.lever_lever_four_enabled and not self.lever_lever_five_enabled and self.lever_lever_six_enabled:
        self.music_door_opened = True
        hide_layer("lever_door_three")
      if sprite.feet.colliderect(self.music_door_collider) and not self.music_door_opened: sprite.move_back(dt)

      if sprite.feet.colliderect(self.konami_sign): self.konami_text_show = True 
      else: self.konami_text_show = False
      if sprite.feet.colliderect(self.simon_sign_range): self.simon_text_show = True 
      else: self.simon_text_show = False

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


      if sprite.feet.colliderect(self.music_button_green_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/songlevel.wav" ))
        pygame.mixer.music.play()
      
      if sprite.feet.colliderect(self.music_button_one_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes1.wav" ))
        pygame.mixer.music.play()
      if sprite.feet.colliderect(self.music_button_two_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes2.wav" ))
        pygame.mixer.music.play()
      if sprite.feet.colliderect(self.music_button_three_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes3.wav" ))
        pygame.mixer.music.play()
      if sprite.feet.colliderect(self.music_button_four_range) and self.f_key_pressed == True:
        self.f_key_pressed = False
        pygame.mixer.music.load(resource_path( RESOURCES_DIR / "sounds/notes4.wav" ))
        pygame.mixer.music.play() 