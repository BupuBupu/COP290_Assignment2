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
		self.icon = pygame.image.load("./assets/UIs/game_icon.png")
		pygame.display.set_icon(self.icon)
		self.clock = pygame.time.Clock()
		self.game_paused = True
		self.game_menu = "main_menu"
		self.start_image = pygame.image.load("./assets/UIs/Main_Menu/start_btn.png").convert_alpha()
		self.exit_image = pygame.image.load("./assets/UIs/Main_Menu/exit_btn.png").convert_alpha()
		self.continue_image = pygame.image.load("./assets/UIs/Main_Menu/conti_btn.png").convert_alpha()
		self.start_btn = button.Button(400, 300, self.start_image, 1)
		self.exit_btn = button.Button(850, 300, self.exit_image, 1)
		self.continue_btn = button.Button(640, 500, self.continue_image, 1)
		self.font = pygame.font.SysFont("garamond",100)
		self.text_col = (255,255,255)
		self.init_start = False
		self.click_sfx = pygame.mixer.Sound("./assets/SoundEffects/click_sound.wav")
		pygame.mixer.music.load("./assets/SoundEffects/BGM.mp3")

		self.level = Level()

	def play_music(self):
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(0.5)
	
	def pause_music(self):
		pygame.mixer.music.pause()
	def unpause_music(self):
		pygame.mixer.music.unpause()
	
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
						self.click_sfx.play()
						time.sleep(0.5)
						self.game_menu = "playing"
						self.game_paused = False
						if not self.init_start:
							self.play_music()
						if self.init_start:
							self.play_music()
						self.init_start = True
						self.first_start = True
						self.level = Level()
						
					if self.init_start and self.continue_btn.draw(self.screen):
						self.click_sfx.play()
						time.sleep(0.5)
						self.game_menu = "playing"
						self.game_paused = False
						if not self.init_start:
							self.play_music()
						if self.init_start:
							self.unpause_music()
					if self.exit_btn.draw(self.screen):
						self.click_sfx.play()
						time.sleep(0.5)
						pygame.quit()
						sys.exit()
				# pygame.display.update()
			# dt = time.time() - previous_time
			# previous_time = time.time()
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				self.game_paused = True
				self.game_menu = "main_menu"
				self.pause_music()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = time.time() - previous_time
			previous_time = time.time()
			if not self.game_paused:
				pygame.mouse.set_visible(False)
				self.screen.fill((202, 228, 241))
				self.level.run(dt)
			pygame.display.update()
			if(self.level is not None):
				print(self.level.enemies[0].pos)

if __name__ == '__main__':
	game = Game()
	game.run()
