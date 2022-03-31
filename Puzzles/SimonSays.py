import pygame

class SimonSays():
  def __init__(self, game) -> None:
    self.active = False
    self.solved = False
    self.game = game

    self.sequence = []

    return

  def draw(self, screen: pygame.Surface) -> None:
    screen.fill((255, 0, 0))
    return
  
  def update(df: float) -> None:
    return

  def reset() -> None:
    return