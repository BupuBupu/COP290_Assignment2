import pygame
from settings import *
from support import import_folder
from sprites import Particle
from overlay import OverlayNullPointers
from timers import Timer
from random import choice
import math

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
        self.hitbox = self.rect.copy().inflate((0.1*self.rect.width, 0.1*self.rect.height))
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
            choices = [ (-1, -1), (-1, 1),(-1,0)]
            dirxn = choice(choices)
        elif (self.direction.x>0 and self.direction.y<0):
            choices = [(-1,-1), (-1, 0), (0, 1)]
            dirxn = choice(choices)
        elif self.direction.x>0 and self.direction.y>0:
            choices = [(-1, -1), (-1, 0), (0, -1)]
            dirxn = choice(choices)
        elif self.direction.x==0 and self.direction.y>0:
            choices = [(0,-1),(-1,-1),(1,-1)]
            dirxn = choice(choices)
        elif self.direction.x==0 and self.direction.y<0:
            choices = [(-1,1),(1,1),(0,1)]
            dirxn = choice(choices)
        elif self.direction.x<0 and self.direction.y<0:
            choices = [(1,1),(0,1),(1,0)]
            dirxn = choice(choices)
        elif self.direction.x<0 and self.direction.y==0:
            choices = [(1,-1),(1,1),(1,0)]
            dirxn = choice(choices)
        elif self.direction.x<0 and self.direction.y>0:
            choices = [(1,0),(0,-1),(1,-1)]
            dirxn = choice(choices)
        relx = sprite.hitbox.centerx-self.hitbox.centerx
        rely = -(sprite.hitbox.centery-self.hitbox.centery)
        degree = 0
        if relx < 0 and rely < 0:
            # 3rd part
            try:
                degree = 180+math.degrees(math.atan(rely/relx))
            except ZeroDivisionError:
                degree = 270
            if(degree>=225):
                self.hitbox.bottom = sprite.hitbox.top
            else:
                self.hitbox.left = sprite.hitbox.right
        elif(relx>0 and rely > 0):
            # 1st part
            try:
                degree = math.degrees(math.atan(rely/relx))
            except ZeroDivisionError:
                degree = 90
            if(degree>=45):
                self.hitbox.top = sprite.hitbox.bottom
            else:
                self.hitbox.right = sprite.hitbox.left
        elif(relx > 0 and rely < 0):
            # 4th part
            try:
                degree = 360 + math.degrees(math.atan(rely/relx))
            except ZeroDivisionError:
                degree = 270
            if(degree>=315):
                self.hitbox.right = sprite.hitbox.left
            else:
                self.hitbox.bottom = sprite.hitbox.top
        else:
            # 2nd part part
            try:
                degree = 180 + math.degrees(math.atan(rely/relx))
            except:
                degree = 90
            if(degree>=135):
                self.hitbox.left = sprite.hitbox.right
            else:
                self.hitbox.top = sprite.hitbox.bottom
        self.direction.x = dirxn[0]
        self.direction.y = dirxn[1]
        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery
        self.pos.x = self.hitbox.centerx
        self.pos.y = self.hitbox.centery
            
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
               self.target.points += round(self.speed*0.1+(16-self.garbage_drop_interval)*3) # multiplier for points, more the interval lesser the points and more the speed more the points
               Particle(self.rect.topleft, self.image, self.groups()[0], self.z, 450)
               self.kill()
               self.target.kids_caught += 1
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
        if(self.pos.x<290 or self.pos.x>7330 or self.pos.y<290 or self.pos.y>4130):
            if(self.target.pos.x>=320 and self.target.pos.x<=3264):
                self.pos.x = (4416+7360)/2
                self.pos.y = (320+4160)/2
            else:
                self.pos.x = (320+3264)/2
                self.pos.y = (320+4160)/2
            self.hitbox.centerx = self.pos.x
            self.hitbox.centery = self.pos.y
            self.rect.centerx = self.pos.x
            self.rect.centery = self.pos.y
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