from __future__ import annotations
from typing import TYPE_CHECKING

import logging
import pygame
from enums import Skills, Gems
from utils import add_skill, check_skill, get_layer_visibility, get_font_at_size, set_layer_visibility, check_gem, add_gem, tile_object_to_rect

if TYPE_CHECKING:
    from game import Game

logger = logging.getLogger(__name__)
class Ingame:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.font = get_font_at_size(font_size=20)

        self.f_key_pressed = False

        self.door_one_time = 0
        self.door_lever_water_enabled = False
        self.door_lever_one_enabled = False

        self.music_door_opened = False
        self.gear_wall_opened = False
        self.water_wall_opened = False


        self.walls = []
        for obj in self.game.tmx_data.get_layer_by_name("walls")[:]:
            logger.info(
                "Created Wall at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.shallowwater = []
        for obj in self.game.tmx_data.get_layer_by_name("shallowwater")[:]:
            logger.info(
                "Created Shallowwater at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.shallowwater.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.soft_wall_low_range = []
        for obj in self.game.tmx_data.get_layer_by_name("soft_wall_low_range")[:]:
            logger.info(
                "Created Soft Wall Low Range at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.soft_wall_low_range.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.soft_wall_high_range = []
        for obj in self.game.tmx_data.get_layer_by_name("soft_wall_high_range")[:]:
            logger.info(
                "Created Soft Wall High Range at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.soft_wall_high_range.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.soft_wall_low_collider = []
        for obj in self.game.tmx_data.get_layer_by_name("soft_wall_low_collider")[:]:
            logger.info(
                "Created Soft Wall Low Collider at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.soft_wall_low_collider.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.soft_wall_high_collider = []
        for obj in self.game.tmx_data.get_layer_by_name("soft_wall_high_collider")[:]:
            logger.info(
                "Created Soft Wall High Collider at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.soft_wall_high_collider.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.gear_wall_collider = []
        for obj in self.game.tmx_data.get_layer_by_name("gear_wall_collider")[:]:
            logger.info(
                "Created Gear Wall Collider at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.gear_wall_collider.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.shallow_water_finish = []
        for obj in self.game.tmx_data.get_layer_by_name("shallow_water_finish")[:]:
            logger.info(
                "Created Shallow Water Finish at {}, {} with dimensions {}, {}",
                obj.x,
                obj.y,
                obj.width,
                obj.height
            )
            self.shallow_water_finish.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.blue_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("blue_gem_collider")[0]
        )
        self.red_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("red_gem_collider")[0]
        )
        self.purple_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("purple_gem_collider")[0]
        )
        self.green_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("green_gem_collider")[0]
        )
        self.orange_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("orange_gem_collider")[0]
        )
        self.pink_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("pink_gem_collider")[0]
        )
        self.lemon_gem_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lemon_gem_collider")[0]
        )
        self.gear_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("gear_collider")[0]
        )
        self.boots_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("boots_collider")[0]
        )
        self.red_key_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("red_key_collider")[0]
        )
        self.red_key_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("red_key_range")[0]
        )
        self.gem_door_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("gem_door_range")[0]
        )
        self.konami_sign = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("konami_sign")[0]
        )
        self.button_door_one_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("button_door_one_range")[0]
        )
        self.lever_water_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_water_range")[0]
        )
        self.house_door_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("house_door_collider")[0]
        )
        self.lever_spawn_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_spawn_range")[0]
        )
        self.lever_door_one_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("lever_door_one_collider")[0]
        )
        self.button_house_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("button_house_range")[0]
        )
        self.simon_door_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_door_collider")[0]
        )
        self.simon_sign_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("simon_sign_range")[0]
        )
        self.beach_sign_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("beach_sign_range")[0]
        )
        self.music_door_collider = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("music_door_collider")[0]
        )
        self.hamer_lever_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("hamer_lever_range")[0]
        )
        self.beach_button_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("beach_button_range")[0]
        )
        self.final_gem_button_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("final_gem_button_range")[0]
        )
        self.gear_wall_range = tile_object_to_rect(
            self.game.tmx_data.get_layer_by_name("gear_wall_range")[0]
        )

        self.game.doorManager.new_door(
            "red_key_door",
            "red_key_door_collider",
            "red_key_door"
        )
        self.game.doorManager.new_door(
            "button_door_one",
            "button_door_one_collider",
            "button_door_one"
        )

        self.game.doorManager.new_door(
            "gem_door_one",
            "gem_door_collider",
            "gem_door_one"
        )

        self.game.doorManager.new_door(
            "button_door_two",
            "simon_door_collider",
            "button_door_two"
        )
        self.game.doorManager.new_door(
            "puzzle_door_one",
            "levers_door_collider",
            "puzzle_door_one"
        )
        self.game.doorManager.new_door(
            "beach_door",
            "beach_door_collider",
            "puzzle_door_two"
        )
        self.game.doorManager.new_door(
            "math_door",
            "math_door_collider",
            "puzzle_door"
        )
        self.game.doorManager.new_door(
            "morse_door",
            "mors_door_collider",
            "puzzle_door_three"
        )
        self.game.doorManager.new_door(
            "final_gem_door",
            "final_gem_door_collider",
            "puzzle_door_four"
        )

        self.konami_text_show = False
        self.simon_text_show = False
        self.math_text_show = False

    def draw(self, screen) -> None:
        self.game.group.center(self.game.player.rect.center)
        self.game.group.draw(screen)
        sign_one = self.font.render("Do the konami code", False, (255, 255, 255))
        if self.konami_text_show:
            screen.blit(sign_one, (screen.get_width()/2, screen.get_height()/2 - sign_one.get_height()/2 - 50))
        sign_two = self.font.render("RRLLLR", False, (255, 255, 255))
        if self.simon_text_show:
            screen.blit(sign_two, (screen.get_width()/2, screen.get_height()/2 - sign_two.get_height()/2 - 50))
        sign_three = self.font.render("(((squareroot of 6512704) + 7)/3)*4", False, (255, 255, 255))
        if self.math_text_show:
            screen.blit(sign_three, (screen.get_width()/2, screen.get_height()/2 - sign_three.get_height()/2 - 50))

    def handle_input(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.f_key_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                self.f_key_pressed = False

    def update(self, dt_: float) -> None:
        self.game.group.update(dt_)

        def add_and_hide_skill(layername: str, skill: Skills) -> None:
            set_layer_visibility(self.game.tmx_data, self.game.map_layer, layername, False)
            add_skill(sprite, skill)

        def add_and_hide_gem(layername: str, gem: Gems) -> None:
            set_layer_visibility(self.game.tmx_data, self.game.map_layer, layername, False)
            add_gem(sprite, gem)

        def hide_layer(layername: str) -> None:
            set_layer_visibility(self.game.tmx_data, self.game.map_layer, layername, False)

        for sprite in self.game.group.sprites():
            self.game.doorManager.update(sprite, dt_)

            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt_)
            if sprite.feet.collidelist(self.shallowwater) > -1 and not Skills.SWIM in sprite.skills:
                sprite.move_back(dt_)

            if sprite.feet.colliderect(self.blue_gem_collider) and not check_gem(sprite, Gems.BLUE):
                add_and_hide_gem("blue_gem", Gems.BLUE)
            if sprite.feet.colliderect(self.red_gem_collider) and not check_gem(sprite, Gems.RED):
                add_and_hide_gem("red_gem", Gems.RED)
            if sprite.feet.colliderect(self.purple_gem_collider) and not check_gem(sprite, Gems.PURPLE):
                add_and_hide_gem("purple_gem", Gems.PURPLE)
            if sprite.feet.colliderect(self.green_gem_collider) and not check_gem(sprite, Gems.GREEN):
                add_and_hide_gem("green_gem", Gems.GREEN)
            if sprite.feet.colliderect(self.orange_gem_collider) and not check_gem(sprite, Gems.ORANGE):
                add_and_hide_gem("orange_gem", Gems.ORANGE)
            if sprite.feet.colliderect(self.pink_gem_collider) and not check_gem(sprite, Gems.PINK):
                add_and_hide_gem("pink_gem", Gems.PINK)
            if sprite.feet.colliderect(self.lemon_gem_collider) and not check_gem(sprite, Gems.LEMON):
                add_and_hide_gem("lemon_gem", Gems.LEMON)
            if sprite.feet.colliderect(self.gear_collider) and not check_gem(sprite, Gems.GEAR):
                add_and_hide_gem("gear", Gems.GEAR)
            if sprite.feet.colliderect(self.boots_collider) and not check_skill(sprite, Skills.RUN):
                add_and_hide_skill("boots", Skills.RUN)
            if sprite.feet.colliderect(self.red_key_collider) and not check_gem(sprite, Gems.KEY):
                add_and_hide_gem("red_key", Gems.KEY)

            if sprite.feet.colliderect(self.red_key_range) and check_gem(sprite, Gems.KEY):
                self.game.doorManager.open_door_by_id("red_key_door")

            if sprite.feet.collidelist(self.soft_wall_low_range) > -1 and check_skill(sprite, Skills.HAMMER):
                hide_layer("soft_wall_low")
            if sprite.feet.collidelist(self.soft_wall_low_collider) > -1 and not check_skill(sprite, Skills.HAMMER):
                sprite.move_back(dt_)
            if sprite.feet.collidelist(self.soft_wall_high_range) > -1 and check_skill(sprite, Skills.HAMMER):
                hide_layer("soft_wall_high")
            if sprite.feet.collidelist(self.soft_wall_high_collider) > -1 and not check_skill(sprite, Skills.HAMMER):
                sprite.move_back(dt_)

            if sprite.feet.colliderect(self.gear_wall_range) and check_gem(sprite, Gems.GEAR):
                self.gear_wall_opened = True
                hide_layer("gear_wall")
            if sprite.feet.collidelist(self.gear_wall_collider) > -1 and not self.gear_wall_opened:
                sprite.move_back(dt_)

            if sprite.feet.colliderect(self.gem_door_range) and check_gem(sprite, Gems.BLUE) and check_gem(sprite, Gems.RED) and check_gem(sprite, Gems.GREEN):
                self.game.doorManager.open_door_by_id("gem_door_one")

            if sprite.feet.colliderect(self.final_gem_button_range) and check_gem(sprite, Gems.ORANGE) and check_gem(sprite, Gems.LEMON) and check_gem(sprite, Gems.PURPLE) and check_gem(sprite, Gems.PINK) and self.f_key_pressed is True:
                self.f_key_pressed = False
                self.water_wall_opened = True
                hide_layer("water_empty")
            if sprite.feet.collidelist(self.shallow_water_finish) > -1 and not self.water_wall_opened:
                sprite.move_back(dt_)

            if sprite.feet.colliderect(self.music_door_collider) and not self.music_door_opened:
                sprite.move_back(dt_)

            if sprite.feet.colliderect(self.konami_sign):
                self.konami_text_show = True
            else: self.konami_text_show = False
            if sprite.feet.colliderect(self.simon_sign_range):
                self.simon_text_show = True
            else: self.simon_text_show = False
            if sprite.feet.colliderect(self.beach_sign_range):
                self.math_text_show = True
            else: self.math_text_show = False

            if sprite.feet.colliderect(self.button_door_one_range) and self.f_key_pressed is True:
                self.game.doorManager.open_door_for_millis_by_id("button_door_one", 2000)

            if sprite.feet.colliderect(self.button_house_range) and self.f_key_pressed is True:
                self.game.doorManager.open_door_for_millis_by_id("button_door_two", 4000)


            if sprite.feet.colliderect(self.house_door_collider) and not self.door_lever_water_enabled:
                sprite.move_back(dt_)
            if sprite.feet.colliderect(self.lever_water_range) and self.f_key_pressed is True:
                self.f_key_pressed = False
                self.door_lever_water_enabled = not self.door_lever_water_enabled
                set_layer_visibility(
                    self.game.tmx_data,
                    self.game.map_layer,
                    "lever_water",
                    not get_layer_visibility(self.game.tmx_data, "lever_water")
                )
                set_layer_visibility(
                    self.game.tmx_data,
                    self.game.map_layer,
                    "lever_door_two",
                    not get_layer_visibility(self.game.tmx_data, "lever_door_two")
                )


            if sprite.feet.colliderect(self.lever_door_one_collider) and not self.door_lever_one_enabled:
                sprite.move_back(dt_)
            if sprite.feet.colliderect(self.lever_spawn_range) and self.f_key_pressed is True:
                self.f_key_pressed = False
                self.door_lever_one_enabled = not self.door_lever_one_enabled
                set_layer_visibility(
                    self.game.tmx_data,
                    self.game.map_layer,
                    "lever_spawn",
                    not get_layer_visibility(self.game.tmx_data, "lever_spawn")
                )
                set_layer_visibility(
                    self.game.tmx_data,
                    self.game.map_layer,
                    "lever_door_one",
                    not get_layer_visibility(self.game.tmx_data, "lever_door_one")
                )

            if sprite.feet.colliderect(self.hamer_lever_range) and self.f_key_pressed is True:
                self.f_key_pressed = False
                self.music_door_opened = not self.music_door_opened
                set_layer_visibility(
                    self.game.tmx_data,
                    self.game.map_layer,"lever_hamer",
                    not get_layer_visibility(self.game.tmx_data, "lever_hamer")
                )
                set_layer_visibility(
                    self.game.tmx_data,
                    self.game.map_layer,"lever_door_three",
                    not get_layer_visibility(self.game.tmx_data, "lever_door_three")
                )

            if sprite.feet.colliderect(self.beach_button_range) and self.f_key_pressed is True:
                self.game.doorManager.open_door_for_millis_by_id("math_door", 12000)
