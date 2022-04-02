import pygame
from typing import List
from utils import load_image

from enums import Skills

class Player(pygame.sprite.Sprite):
  """ Our Player, It goes brrrrr """

  def __init__(self, game) -> None:
    super().__init__()
    self.game = game
    self.image = load_image("player.png").convert_alpha()
    self.velocity = [0, 0]
    self._position = [0.0, 0.0]
    self._old_position = self._position
    self.rect = self.image.get_rect()
    self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 8)
    self.skills = []
    self.inventory = []

  @property
  def position(self) -> List[float]:
    return list(self._position)

  @position.setter
  def position(self, value: List[float]) -> None:
    self._position = list(value)
  
  def update(self, dt: float) -> None:
    self._old_position = self._position[:]
    self._position[0] += self.velocity[0] * dt
    self._position[1] += self.velocity[1] * dt
    self.rect.topleft = self._position
    self.feet.midbottom = self.rect.midbottom

  def move_back(self, dt: float) -> None:
    self._position = self._old_position
    self.rect.topleft = self._position
    self.feet.midbottom = self.rect.midbottom
