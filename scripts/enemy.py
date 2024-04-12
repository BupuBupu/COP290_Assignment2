import pygame
from settings import *
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, target, pos, group, speed, anim_speed, garbage_drop_interval=4, enemy_num=1): # garbage drop interval is in seconds
        super().__init__(group)
        self.garbage_drop_interval = garbage_drop_interval
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
        # Will move randomly in a pattern when player is far away by some threshold, it will only decide its direction based on target when it is in some proximity
        pass # will decide on self.target

    def garbage_drop(self): # drop garbage at some intervals
        pass
    