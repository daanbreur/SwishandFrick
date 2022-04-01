from re import L
from turtle import position
import pygame
import logging

from constants import TOAST_SHOW_TIME_MS
from utils import getFontAtSize

class ToastPopup():
    def __init__(self, screenDimensions, text='', fontSize=15):
        self.startShowTime = 0
        self.color = [69, 69, 69]
        self.screenDimensions = screenDimensions

        self.txt = text
        self.font = getFontAtSize(fontSize=fontSize)
        self.txt_surf = self.font.render(self.txt, True, [255, 255, 255])

        self.size = self.txt_surf.get_size()
        self.txt_rect = self.txt_surf.get_rect(center=[ screenDimensions[0] - self.size[0] / 2, screenDimensions[1] - self.size[1] / 2 ])

        # self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

        self.surf = pygame.Surface(self.size)
        self.surf.set_alpha(120)
        self.rect = self.surf.get_rect(center=self.txt_rect.center)

    def draw(self, screen):
        if self.startShowTime == 0:
            self.startShowTime = pygame.time.get_ticks()
        self.surf.fill(self.color)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

class ToastManager():
    def __init__(self, screen) -> None:
        self.toastsQueue = []
        self.screen = screen
    
    def addToast(self, text, fontSize=15):
        w,h = self.screen.get_width(), self.screen.get_height()
        logging.info(f"Creating toast with text: {text} and fontSize: {fontSize} and screen dimensions: {w}, {h}")
        self.toastsQueue.append(ToastPopup((w,h), text, fontSize))

    def draw(self, screen):
        if len(self.toastsQueue) > 0:
            logging.info(f"Found {len(self.toastsQueue)} toasts in queue")
            logging.info(f"Time since first show: {pygame.time.get_ticks() - self.toastsQueue[0].startShowTime}")
            if self.toastsQueue[0].startShowTime == 0 or pygame.time.get_ticks() - self.toastsQueue[0].startShowTime < TOAST_SHOW_TIME_MS:
                logging.info(f"Drawing toast {self.toastsQueue[0]}")
                self.toastsQueue[0].draw(screen)
            else:
                logging.info(f"Removing toast {self.toastsQueue[0]}")
                self.toastsQueue.pop(0)