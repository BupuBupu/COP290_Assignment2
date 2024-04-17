import pygame
from settings import *
from support import *
from timers import Timer

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites, player_num=1):
		super().__init__(group)
		self.player_num = player_num
	
		self.import_assets()
		self.status = 'down_idle'
		self.frame_index = 0

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.z = LAYERS['main']

		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 200

		# collision
		self.hitbox = self.rect.copy().inflate((-0.2*self.rect.width,-0.2*self.rect.height))
		self.collision_sprites = collision_sprites
  
		# timers
		self.timers = {
			"garbage_collect": Timer(350),
			"catch_kid": Timer(350)
		}

		self.points = 0
		self.kids_caught = 0

	def import_assets(self):
		self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
        }
		for animation in self.animations.keys():
			full_path = f"assets/characters/player/player{self.player_num}/" + animation
			self.animations[animation] = import_folder(full_path, 4)

	def animate(self,dt):
		self.frame_index += 4 * dt
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]

	def input(self):
		keys = pygame.key.get_pressed()

		# directions 
		if (not self.timers["garbage_collect"].active and not self.timers["catch_kid"].active):
			if keys[pygame.K_w] or keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0
			# faster movement
			if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
				self.speed = PLAYER_SPEED * 2
				self.animate_speed = PLAYER_ANIMATION_SPEED * 2
			else:
				self.speed = PLAYER_SPEED
				self.animate_speed = PLAYER_ANIMATION_SPEED

			if keys[pygame.K_SPACE]:
				if(not self.timers["garbage_collect"].active):
					self.timers["garbage_collect"].activate()
				if (not self.timers["catch_kid"].active):
					self.timers["catch_kid"].activate()
		else:
			self.direction.x=0
			self.direction.y=0

	def get_status(self):
		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'
   
	def update_timers(self):
		for timer in self.timers.values():
			timer.update()
   
	def collision(self, direction):
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
					if direction == 'horizontal':
						if self.direction.x > 0: # moving right
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: # moving left
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

					if direction == 'vertical':
						if self.direction.y > 0: # moving down
							self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: # moving up
							self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery
  
	def move(self,dt):
		# normalizing a vector 
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		# horizontal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def update(self, dt):
		self.input()
		self.get_status()

		self.update_timers()
		self.move(dt)
		self.animate(dt)
