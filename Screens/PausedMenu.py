import pygame
from enums import GameState, UserEvents
from utils import getFontAtSize
from constants import PAUSE_BLINK_TIME_MS

from MenuButton import MenuButton

class PausedMenu:
  def __init__(self, game) -> None:
    self.game = game
    self.font = getFontAtSize(fontSize=20)
    self.blinkTimer = pygame.time.set_timer(UserEvents.PAUSE_BLINK.value, PAUSE_BLINK_TIME_MS)
    self.drawPaused = False

    def resumeGame() -> None: self.game.gameState = GameState.IN_GAME
    def settings() -> None: self.game.gameState = GameState.SETTINGS
    def mainMenu() -> None: self.game.gameState = GameState.MAIN_MENU
    
    w, h = pygame.display.get_surface().get_size()
    self.buttons = [MenuButton((w/2, h/2), (200, 50), color=(220, 220, 220), cb=resumeGame, text='Resume Game'), MenuButton((w/2, h/2+50+10), (200, 50), color=(220, 220, 220), cb=settings, text='Settings'), MenuButton((w/2, h/2+100+20), (200, 50), color=(220, 220, 220), cb=mainMenu, text='Main Menu')]

  def draw(self, screen) -> None:
    self.game.menus['ingame'].draw(screen)

    if self.drawPaused:
      textSurface=self.font.render('Paused', False, (255, 255, 255))
      screen.blit(textSurface, (screen.get_width()/2 - textSurface.get_width()/2, screen.get_height()/2 - textSurface.get_height()/2 - 50))
    
    for btn in self.buttons:
      btn.draw(screen)

  def blink(self) -> None:
    self.drawPaused = not self.drawPaused

  def handle_click(self, pos) -> None:
    for btn in self.buttons:
      if btn.rect.collidepoint(pos):
        btn.callback()