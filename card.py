import pygame

class Card():

	def __init__(self, x, y, val, img):
		self.x = x
		self.y = y
		self.image = pygame.image.load(img).convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.width = self.rect.width
		self.height = self.rect.height
		self.vel = 3
		self.selected = False
		self.value = val;

	def draw(self, win):
		if self.selected:
			pygame.draw.rect(win, (0,0,0), (self.x-2,self.y-2,self.width+4,self.height+4),0)
		win.blit(self.image, self.rect)

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True

		return False