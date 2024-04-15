import pygame, sys, time
from settings import *
from level import Level
import button
import sys

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Sprout land')
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.game_paused = True
		self.game_menu = "main_menu"
		self.start_image = pygame.image.load("./assets/UIs/Main_Menu/start_btn.png").convert_alpha()
		self.exit_image = pygame.image.load("./assets/UIs/Main_Menu/exit_btn.png").convert_alpha()
		self.start_btn = button.Button(400, 300, self.start_image, 1)
		self.exit_btn = button.Button(850, 300, self.exit_image, 1)
		self.font = pygame.font.SysFont("garamond",100)
		self.text_col = (255,255,255)
	def draw_text(self,text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		self.screen.blit(img, (x, y))
	def run(self):
		pygame.mouse.set_visible(False)
		self.clock.tick(60)
		previous_time = time.time()
		while True:
			if self.game_paused:
				pygame.mouse.set_visible(True)
				self.screen.fill((52,78,91))
				if self.game_menu == "main_menu":
					self.draw_text("KID_LOVERS", self.font, self.text_col, self.screen.get_width()/2 - 300, 100)
					if self.start_btn.draw(self.screen):
						self.game_menu = "playing"
						self.game_paused = False
						self.level = Level()
					if self.exit_btn.draw(self.screen):
						pygame.quit()
						sys.exit()
				pygame.display.update()
			
			dt = time.time() - previous_time
			previous_time = time.time()
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				self.game_paused = True
				self.game_menu = "main_menu"
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			if not self.game_paused:
				pygame.mouse.set_visible(False)
				self.screen.fill((202, 228, 241))
				self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
