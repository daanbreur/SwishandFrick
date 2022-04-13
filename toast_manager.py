"""toast_manager module: contains the ToastManager and ToastPopup class."""

from __future__ import annotations
from typing import List, Tuple

import logging
import pygame

from constants import TOAST_SHOW_TIME_MS
from utils import get_font_at_size

logger = logging.getLogger(__name__)

class ToastPopup():
    """ This class implements all toast logic. Used inside the ToastManager class
    """
    def __init__(self, screen_dimensions: Tuple[int,int], text: str='', font_size: int=18) -> None:
        self.start_show_time: int = 0
        self._text: str = text
        self._font_color: Tuple[int,int,int] = (255,255,255)
        self._color: Tuple[int,int,int] = (69, 69, 69)
        self._screen_dimensions: Tuple[int,int] = screen_dimensions

        self._font: pygame.font.Font = get_font_at_size(font_size=font_size)
        self._text_surface = self._font.render(self._text, 1, self._font_color)
        self._text_width, self._text_height = self._text_surface.get_size()

        self.surf = pygame.Surface(
            (self._text_width + 10, self._text_height + 10)
        )
        self.surf.set_alpha(230)
        self.rect = self.surf.get_rect(
            center=(
                self._screen_dimensions[0]-self._text_width//2-self._text_height,
                self._text_height
            )
        )
        self._text_rectangle = self._text_surface.get_rect(
            center=[wh//2 for wh in self.surf.get_size()]
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Draws toast to the specified screen.

        Args:
            screen (pygame.Surface): screen to draw the toast to.
        """
        if self.start_show_time == 0:
            self.start_show_time = pygame.time.get_ticks()
        self.surf.fill(self._color)
        self.surf.blit(self._text_surface, self._text_rectangle)
        screen.blit(self.surf, self.rect)

class ToastManager():
    """ This class handles toasts and the update cycle for each of them.
    Shows the toasts on the screen and removes them after a certain time.
    """
    def __init__(self, screen: pygame.Surface) -> None:
        self._toast_queue: List[ToastPopup] = []
        self._screen: pygame.Surface = screen

    def add_toast(self, text: str, font_size: int=18) -> None:
        """Add a new toast to the queue with given text and font size.

        Args:
            text (str): text to show on the toast.
            font_size (int, optional): fontsize to be used for the toast. Defaults to 18.
        """
        width: int = self._screen.get_width()
        height: int = self._screen.get_height()
        logger.info(
            "Creating toast with text: {} and fontSize: {} and screen dimensions: {}, {}",
            text,
            font_size,
            width,
            height
        )
        self._toast_queue.append(ToastPopup((width,height), text, font_size))

    def draw(self, screen: pygame.Surface) -> None:
        """Draws toast to the specified screen. Removes the toast from the queue if it's time is up.

        Args:
            screen (pygame.Surface): screen to draw the toast to.
        """
        if len(self._toast_queue) > 0:
            if self._toast_queue[0].start_show_time == 0 or \
                pygame.time.get_ticks() - self._toast_queue[0].start_show_time < TOAST_SHOW_TIME_MS:
                self._toast_queue[0].draw(screen)
            else:
                logger.info("Removing toast {}", self._toast_queue[0])
                self._toast_queue.pop(0)
