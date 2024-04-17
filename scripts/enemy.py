import pygame
from settings import *
from support import import_folder
from sprites import Particle
from overlay import OverlayNullPointers
from timers import Timer
from random import choice
from math import sqrt

class Enemy(pygame.sprite.Sprite):
    def __init__(self, target, pos, group, speed, anim_speed, collision_sprites, garbage_func, garbage_drop_interval=7.5, enemy_num=1, enemy_index=None, enemies=None, pointers=None): # garbage drop interval is in seconds
        super().__init__(group)
        self.garbage_drop_interval = garbage_drop_interval
        self.enemy_num = enemy_num
        self.enemy_index = enemy_index
        self.enemies = enemies
        self.pointers = pointers
        self.group = group
        
        # general setup
        self.import_assets()
        self.status = "down_idle"
        self.frame_index = 0
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.animate_speed = anim_speed
        self.z = LAYERS["main"]
        
        # movement
        self.direction = pygame.math.Vector2((1, 0))
        self.pos = pygame.math.Vector2(self.rect.center)
        
        # attributes
        self.speed = speed
        self.target = target
        
        # collision
        self.hitbox = self.rect.copy().inflate((0*self.rect.width, 0*self.rect.height))
        self.collision_sprites = collision_sprites
        self.collide = False
        
        # timers
        self.timers = {
            "change_direction": Timer(1000*5, self.change_direction_random),
            "garbage_drop": Timer(garbage_drop_interval*1000, garbage_func, enemy_index=enemy_index)
        }
    
    def import_assets(self):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
        }
        for animation in self.animations.keys():
            full_path = f"assets/characters/enemies/kids/en{self.enemy_num}/" + animation
            self.animations[animation] = import_folder(full_path, 2, None)
    
    def animate(self, dt):
        self.frame_index += self.animate_speed * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def get_status(self):
        if(self.direction.y < 0):
            self.status = "up"
            
        elif(self.direction.y > 0):
            self.status = "down"
        
        if(self.direction.x > 0):
            self.status = "right"
        elif(self.direction.x < 0):
            self.status = "left"
            
    def change_direction_random(self):
        possible_directions = [pygame.math.Vector2((1, 0)), pygame.math.Vector2(0, 1), pygame.math.Vector2(-1, 0), pygame.math.Vector2(0, -1), pygame.math.Vector2((1, 1)), pygame.math.Vector2((-1, 1)), pygame.math.Vector2((1, -1)), pygame.math.Vector2((-1, -1))]
        
        self.direction = choice(possible_directions)
    
    def change_direction_collide(self, sprite):
        #self.direction = -self.direction
        dirxn = (0, 0)
        if (self.direction.x>0 and self.direction.y==0):
            choices = [(0, -1),(0, 1), (-1, -1), (-1, 1),(-1,0)]
            dirxn = choice(choices)
        elif (self.direction.x>0 and self.direction.y<0):
            choices = [(-1,-1),(1, 1), (-1, 0), (0, 1), (-1, 1)]
            dirxn = choice(choices)
        elif self.direction.x>0 and self.direction.y>0:
            choices = [(-1, -1), (1,-1), (-1, 0), (0, -1), (-1, 1)]
            dirxn = choice(choices)
        elif self.direction.x==0 and self.direction.y>0:
            choices = [(0,-1),(-1,-1),(1,-1),(-1,0),(1,0)]
            dirxn = choice(choices)
        elif self.direction.x==0 and self.direction.y<0:
            choices = [(1,0),(-1,0),(-1,1),(1,1),(0,1)]
            dirxn = choice(choices)
        elif self.direction.x<0 and self.direction.y<0:
            choices = [(1,1),(0,1),(1,0),(-1,1),(1,-1)]
            dirxn = choice(choices)
        elif self.direction.x<0 and self.direction.y==0:
            choices = [(0,-1),(0,1),(1,-1),(1,1),(1,0)]
            dirxn = choice(choices)
        elif self.direction.x<0 and self.direction.y>0:
            choices = [(-1,-1),(1,1),(1,0),(0,-1),(1,-1)]
            dirxn = choice(choices)
        self.direction.x = dirxn[0]
        self.direction.y = dirxn[1]
            
    def change_direction_collide_proximity(self, sprite):
        # use dynamic collision to check the direction of collision
        if self.direction.x != 0 and self.direction.y != 0:
            pass
        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery
        self.pos.x = self.hitbox.centerx
        self.pos.y = self.hitbox.centery
        
    
    def decide_direction(self):
        # will randomly change directions from it's initial position after a set timer, otherwise also if collides with an object, it changes direction
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if self.hitbox.colliderect(sprite.hitbox):
                    self.collide = True
                    self.change_direction_collide(sprite)
                    break
                else:
                    self.collide = False
        if not self.collide and not self.timers["change_direction"].active:
            self.timers["change_direction"].activate()
    
    def update_timers(self):
        for key, timer in self.timers.items():
            timer.update(not self.collide)
    def enemy_catch(self):
       pass
       if self.hitbox.colliderect(self.target.hitbox):
           keys = pygame.key.get_pressed()
           if keys[pygame.K_SPACE]:
               self.target.timers["catch_kid"].activate()
               # kid catched
               self.target.points += (self.speed*0.1+(16-self.garbage_drop_interval)*3) # multiplier for points, more the interval lesser the points and more the speed more the points
               Particle(self.rect.topleft, self.image, self.groups()[0], self.z, 450)
               self.kill()
               self.enemies[self.enemy_index]=DummyEnemy()
               self.pointers[self.enemy_index]=OverlayNullPointers() # replace the pointer with None
               
    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        
        self.decide_direction()
    
    def update(self, dt):
        self.get_status()
        self.animate(dt)
        self.update_timers()
        self.enemy_catch()
        self.move(dt)

class DummyEnemy:
    def __init__(self) -> None:
        pass
    
    def update(self, dt):
        pass