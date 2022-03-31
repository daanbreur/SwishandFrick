import pygame

from utils import getFontAtSize

class MenuButton:
	def __init__(self, position, size, color=[100, 100, 100], hoverColor=[184, 184, 184], cb=None, text='', fontSize=16, fontColor=[0, 0, 0]):
		self.color    = color
		self.size   = size
		self.func   = cb
		self.surf   = pygame.Surface(size)
		self.rect   = self.surf.get_rect(center=position)

		if hoverColor: self.hoverColor = hoverColor
		else: self.hoverColor = color

		if len(color) == 4:
			self.surf.set_alpha(color[3])


		self.font = getFontAtSize(fontSize=fontSize)
		self.txt = text
		self.font_clr = fontColor
		self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
		self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

	def draw(self, screen):
		self.mouseover()

		self.surf.fill(self.currentColor)
		self.surf.blit(self.txt_surf, self.txt_rect)
		screen.blit(self.surf, self.rect)

	def mouseover(self):
		self.currentColor = self.color
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			self.currentColor = self.hoverColor

	def callback(self, *args):
		if self.func: 
			return self.func(*args)