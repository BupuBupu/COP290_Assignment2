import pygame
from settings import *
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, target, pos, group, speed, anim_speed, enemy_num=1):
        super().__init__(group)
        self.enemy_num = enemy_num
        
        # general setup
        self.image = pygame.Surface((32, 64))
        self.image.fill("green")
        self.rect = self.image.get_rect(center=pos)
        self.animate_speed = anim_speed
        self.z = LAYERS["main"]
        
        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        
        # attributes
        self.speed = speed
        self.target = target
    
    def decide_direction(self):
        pass # will decide on self.target
    