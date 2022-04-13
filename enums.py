import enum
import pygame


@enum.unique
class GameState(enum.Enum):
    MAIN_MENU = enum.auto()
    IN_GAME = enum.auto()
    PAUSE_MENU = enum.auto()
    SETTINGS = enum.auto()


@enum.unique
class Gems(enum.Enum):
    BLUE = enum.auto()
    RED = enum.auto()
    PURPLE = enum.auto()
    GREEN = enum.auto()
    ORANGE = enum.auto()
    PINK = enum.auto()
    LEMON = enum.auto()
    GEAR = enum.auto()
    KEY = enum.auto()


@enum.unique
class Skills(enum.Enum):
    SWIM = enum.auto()
    RUN = enum.auto()
    HAMMER = enum.auto()


@enum.unique
class UserEvents(enum.IntEnum):
    PAUSE_BLINK = pygame.USEREVENT
    SIMON_SAYS_BLINK = enum.auto()
