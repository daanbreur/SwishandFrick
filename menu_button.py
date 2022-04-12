import pygame

from utils import get_font_at_size

class MenuButton:
    def __init__(self, position, size, color=None, hover_color=None, cb_=None, text='', font_size=16, font_color=None):
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
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self._size])

    def draw(self, screen: pygame.Surface) -> None:
        self.mouseover()

        self._surface.fill(self.current_color)
        self._surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self._surface, self.rect)

    def mouseover(self) -> None:
        self.current_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color

    def callback(self, *args) -> None:
        if self._callback_function:
            return self._callback_function(*args)
