from __future__ import annotations

import logging
import os
import sys
from datetime import datetime

import pygame
import pytmx
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup
from pytmx.util_pygame import load_pygame

from Puzzles.konami_code import KonamiCode
from Puzzles.lever_combination import LeverCombination
from Puzzles.math import Math
from Puzzles.morse_code import MorseCode
from Puzzles.music import Music
from Puzzles.simon_says import SimonSays
from Screens.in_game import Ingame
from Screens.main_menu import MainMenu
from Screens.paused_menu import PausedMenu
from Screens.settings_menu import SettingsMenu

from colargulog import BraceFormatStyleFormatter, ColorizedArgsFormatter
from player import Player
from door_manager import DoorManager
from toast_manager import ToastManager

from enums import GameState, UserEvents, Skills
from constants import RESOURCES_DIR, PLAYER_MOVE_SPEED, PLAYER_RUN_SPEED
from utils import resource_path, initialize_screen

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


def init_logging():
    """Initialize color and file logger.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_level = "DEBUG"
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(console_level)
    console_format = "%(asctime)s - %(levelname)-8s - %(name)-25s - %(message)s"
    colored_formatter = ColorizedArgsFormatter(console_format)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(
        "{:%Y-%m-%d_%H-%M-%S}.log".format(datetime.now())
    )
    file_level = "DEBUG"
    file_handler.setLevel(file_level)
    file_format = "%(asctime)s - %(name)s (%(lineno)s) - %(levelname)-12s - %(message)s"
    file_handler.setFormatter(BraceFormatStyleFormatter(file_format))
    root_logger.addHandler(file_handler)


init_logging()
logger = logging.getLogger(__name__)


class Game:
    map_path = resource_path(RESOURCES_DIR / "map.tmx")

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.running = False
        self.game_state = GameState.MAIN_MENU

        self.tmx_data = load_pygame(self.map_path)

        self.player = Player(self)
        spawn_obj = self.tmx_data.get_layer_by_name("spawn")[0]
        self.player.position = (spawn_obj.x - spawn_obj.width / 2, spawn_obj.y)

        # Create new renderer
        self.map_layer = pyscroll.BufferedRenderer(
            data=pyscroll.data.TiledMapData(self.tmx_data),
            size=screen.get_size(),
            clamp_camera=False,
            zoom=2,
        )

        # Make Pyscroll group
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=50)
        self.group.add(self.player)

        self.toast_manager: ToastManager = ToastManager(self.screen)
        self.door_manager: DoorManager = DoorManager(self)

        self.puzzles = {
            "simonsays": SimonSays(self),
            "morsecode": MorseCode(self),
            "math": Math(self),
            "music": Music(self),
            "levercombination": LeverCombination(self),
            "konami": KonamiCode(self),
        }

        self.menus = {
            "mainmenu": MainMenu(self),
            "ingame": Ingame(self),
            "settings": SettingsMenu(self),
            "pausemenu": PausedMenu(self),
        }

    def draw(self) -> None:
        if self.game_state == GameState.MAIN_MENU:
            self.menus["mainmenu"].draw(self.screen)
        if self.game_state == GameState.SETTINGS:
            self.menus["settings"].draw(self.screen)
        if self.game_state == GameState.PAUSE_MENU:
            self.menus["pausemenu"].draw(self.screen)
        if self.game_state == GameState.IN_GAME:
            self.menus["ingame"].draw(self.screen)
            for puzzle in self.puzzles.values():
                if puzzle.active:
                    puzzle.draw(self.screen)
            self.toast_manager.draw(self.screen)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

            elif event.type == UserEvents.PAUSE_BLINK.value:
                self.menus["pausemenu"].blink()
            elif event.type == UserEvents.SIMON_SAYS_BLINK.value:
                self.puzzles["simonsays"].next_color()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.game_state == GameState.MAIN_MENU:
                    self.menus["mainmenu"].handle_click(event.pos)
                if event.button == 1 and self.game_state == GameState.PAUSE_MENU:
                    self.menus["pausemenu"].handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_ESCAPE
                    and self.game_state == GameState.MAIN_MENU
                ):
                    self.running = False
                    break
                elif (
                    event.key == pygame.K_ESCAPE and self.game_state == GameState.IN_GAME
                ):
                    self.game_state = GameState.PAUSE_MENU
                elif (
                    event.key == pygame.K_ESCAPE
                    and self.game_state == GameState.PAUSE_MENU
                ):
                    self.game_state = GameState.MAIN_MENU
                else:
                    if self.game_state == GameState.IN_GAME:
                        self.menus["ingame"].handle_input(event)
                    for puzzle in self.puzzles.values():
                        puzzle.handle_input(event)

            elif event.type == pygame.VIDEORESIZE:
                logger.info("Resizing screen to {}x{}", event.w, event.h)
                self.screen = initialize_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

            else:
                if self.game_state == GameState.IN_GAME:
                    self.menus["ingame"].handle_input(event)

        if self.game_state == GameState.IN_GAME:
            pressed = pygame.key.get_pressed()
            mods = pygame.key.get_mods()

            if pressed[pygame.K_w]:
                self.player.velocity[1] = (
                    -PLAYER_RUN_SPEED
                    if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills
                    else -PLAYER_MOVE_SPEED
                )
            elif pressed[pygame.K_s]:
                self.player.velocity[1] = (
                    PLAYER_RUN_SPEED
                    if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills
                    else PLAYER_MOVE_SPEED
                )
            else:
                self.player.velocity[1] = 0

            if pressed[pygame.K_a]:
                self.player.velocity[0] = (
                    -PLAYER_RUN_SPEED
                    if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills
                    else -PLAYER_MOVE_SPEED
                )
            elif pressed[pygame.K_d]:
                self.player.velocity[0] = (
                    PLAYER_RUN_SPEED
                    if mods & pygame.KMOD_SHIFT and Skills.RUN in self.player.skills
                    else PLAYER_MOVE_SPEED
                )
            else:
                self.player.velocity[0] = 0

    def update(self, dt_: float) -> None:
        self.menus["ingame"].update(dt_)
        for puzzle in self.puzzles.values():
            if puzzle.active:
                puzzle.update(dt_)

    def run(self) -> None:
        """Run 👏 The 👏 Game 👏 Loop 👏"""
        clock = pygame.time.Clock()
        self.running = True

        try:
            while self.running:
                dt_ = clock.tick() / 1000.0
                self.handle_input()
                self.update(dt_)
                self.draw()
                pygame.display.flip()
        except KeyboardInterrupt:
            self.running = False


def main() -> None:
    logger.debug("Python version: {}", str(sys.version))
    logger.debug("Pygame version: {}", str(pygame.version.ver))
    logger.debug("Pytmx version: {}", str(pytmx.__version__))
    logger.debug("Pyscroll version: {}", str(pyscroll.__version__))
    logger.debug("Current Process ID: {}", str(os.getpid()))
    logger.debug("Current Parent Process ID: {}", str(os.getppid()))

    pygame.init()
    logger.info("Pygame initialized")

    pygame.font.init()
    logger.info("Pygame font module initialized")

    pygame.mixer.init()
    logger.info("Pygame mixer module initialized")

    screen = initialize_screen(1280, 720)
    logger.info("Initialized screen")

    pygame.display.set_caption("Swish and Frick")
    logger.debug("Set window title to: {}", str(pygame.display.get_caption()[0]))

    try:
        game = Game(screen)
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
