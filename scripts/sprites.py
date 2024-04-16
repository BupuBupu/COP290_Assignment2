import pygame
from settings import *
from timers import Timer

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Water(Generic):
    def __init__(self, pos, frames, groups, z=LAYERS['main']):
        # animation setup
        self.frames_index = 0
        self.frames = frames
        
        # sprite setup
        super().__init__(pos, self.frames[self.frames_index], groups, z)
    
    def animate(self, dt):
        self.frames_index += 5*dt
        self.frames_index %= len(self.frames)
        self.image = self.frames[int(self.frames_index)]
    
    def update(self, dt):
        self.animate(dt)

class Tree(Generic):
	def __init__(self, pos, surf, name, groups, z=LAYERS['main']):
		super().__init__(pos, surf, groups, z)
		self.name=name

class Garbage(pygame.sprite.Sprite):
    def __init__(self, points, pos, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = pygame.Surface((32, 64))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
        self.points = points
