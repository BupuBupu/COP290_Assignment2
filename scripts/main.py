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
		self.start_btn = button.Button(self.screen.get_width()/4 - self.start_image.get_width()/2, 300, self.start_image, 1)
		self.exit_btn = button.Button(3*self.screen.get_width()/4 - self.exit_image.get_width()/2, 300, self.exit_image, 1)
		self.continue_btn = button.Button(self.screen.get_width()/2 - self.continue_image.get_width()/2, 500, self.continue_image, 1)
		self.font = pygame.font.SysFont("garamond",100)
		self.text_col = (255,255,255)
		self.init_start = False
		self.click_sfx = pygame.mixer.Sound("./assets/SoundEffects/click_sound.wav")
		pygame.mixer.music.load("./assets/SoundEffects/BGM.mp3")
		self.game_over_img = pygame.image.load("./assets/UIs/background.jpg").convert_alpha()
		self.game_over_img = pygame.transform.scale(self.game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.gover_btn = button.Button(0,0,self.game_over_img,1)
		self.level = Level(180)

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
			dt = time.time() - previous_time
			previous_time = time.time()
			if self.game_paused:
				pygame.mouse.set_visible(True)
				self.screen.fill((52,78,91))
				if self.game_menu == "main_menu":
					self.draw_text("Naughty Kids", self.font, self.text_col, self.screen.get_width()/2 - 2*self.continue_image.get_width()/2-15, 100)
					
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
						self.level = Level(180)
						
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
			keys = pygame.key.get_pressed()
			if keys[pygame.K_ESCAPE]:
				self.game_paused = True
				self.game_menu = "main_menu"
				self.pause_music()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			if not self.game_paused:
				if self.level.game_over():
					# print("Game Over")
					self.screen.fill((0,0,0))
					pygame.mouse.set_visible(True)
					
					if self.gover_btn.draw(self.screen):
						# print("hell")
						self.game_menu = "main_menu"
						self.game_paused = True 
					self.draw_text(f"Your Score: {self.level.player.points}", self.font, (0,0,0), self.screen.get_width()/2 - 2*self.continue_image.get_width()/2-15, 100)
				else:
					pygame.mouse.set_visible(False)
					self.level.run(dt, self.game_paused)
				pygame.display.update()
			else:
				pygame.display.update()
			
			# pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
