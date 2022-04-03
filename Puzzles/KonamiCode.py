import pygame
import logging

from enums import Skills
from utils import add_skill, check_skill

class KonamiCode():
  def __init__(self, game) -> None:
    self.active = True
    self.solved = False
    self.game = game

    self.sequence = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
    self.enteredSequence = []
    self.index = 0

  def draw(self, screen: pygame.Surface) -> None:
    return
  
  def update(self, df: float) -> None:
    return
  
  def reset(self) -> None:
    return

  def handle_input(self, event) -> None:
    if not self.solved:
      if event.key == self.sequence[self.index]:
        self.enteredSequence.append(event.key)
        self.index += 1
        logging.info(f"Konami code index: {self.index} / {len(self.sequence)} | {self.sequence[self.index-1]}")
        if self.sequence == self.enteredSequence:
          self.solved = True
          logging.info("Konami code entered correctly")
          self.game.toastManager.addToast("Konami code Solved", 17)
          if not check_skill(self.game.player, Skills.SWIM):
            logging.info("Komani code entered correctly, adding swim skill")
            add_skill(self.game.player, Skills.SWIM)