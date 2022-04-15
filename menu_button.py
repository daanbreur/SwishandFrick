"""menu_button module: implements the MenuButton class for creating buttons on screen."""
# pylint: disable=R0902,R0913

from __future__ import annotations
from typing import List, Tuple
import pygame

from utils import get_font_at_size


class MenuButton:
    """MenuButton class, creates a button at position and text with callback handler.
    Needs manual drawing.
    """
    def __init__(self,
                 position: Tuple[int, int],
                 size: Tuple[int, int],
                 color: List[int] = None,
                 hover_color: List[int] = None,
                 cb_=None,
                 text: str = '',
                 font_size: int = 16,
                 font_color=None):
        if color is None:
            color = [100, 100, 100]

        if hover_color is None:
            hover_color = [184, 184, 184]

        if font_color is None:
            font_color = [0, 0, 0]

        self.color = color
        self.current_color = self.color
        self.hover_color = hover_color
        self.font_color = font_color

        self._size = size
        self._callback_function = cb_
        self._surface = pygame.Surface(size)
        self.rect = self._surface.get_rect(center=position)

        if len(color) == 4:
            self._surface.set_alpha(color[3])

        self.font = get_font_at_size(font_size=font_size)
        self.txt = text
        self.txt_surf = self.font.render(self.txt, 1, self.font_color)
        self.txt_rect = self.txt_surf.get_rect(center=[wh // 2 for wh in self._size])

    def draw(self, screen: pygame.Surface) -> None:
        """Handles drawing for the menubutton to specified screen

        Args:
            screen (pygame.Surface): screen to draw to
        """
        self.mouseover()

        self._surface.fill(self.current_color)
        self._surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self._surface, self.rect)

    def mouseover(self) -> None:
        """Check if mouse is over the button and changes color based on it
        """
        self.current_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color

    def callback(self, *args) -> None:
        """If button clicked, run callback function.
        """
        if self._callback_function:
            self._callback_function(*args)
