import pygame
from settings import *
from support import import_folder
from timers import Timer
from random import choice
from math import sqrt

class Enemy(pygame.sprite.Sprite):
    def __init__(self, target, pos, group, speed, anim_speed, collision_sprites, garbage_drop_interval=4, enemy_num=1): # garbage drop interval is in seconds
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
            "change_direction": Timer(2000, self.change_direction_random)
        }
    
    # def import_assets(self):
    #     self.animations = {
    #         "up": [], "down": [], "left": [], "right": [],
    #         "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
    #     }
    #     for animation in self.animations.keys():
    #         full_path = f"assets/characters/enemies/kid{self.enemy_num}/" + animation
    #         self.animations[animation] = import_folder(full_path, 4)
    
    # def animate(self, dt):
    #     self.frame_index += self.animate_speed * dt
    #     if self.frame_index >= len(self.animations[self.status]):
    #         self.frame_index = 0
        
    #     self.image = self.animations[self.status][int(self.frame_index)]
    def change_direction_random(self):
        possible_directions = [pygame.math.Vector2((1, 0)), pygame.math.Vector2(0, 1), pygame.math.Vector2(-1, 0), pygame.math.Vector2(0, -1), pygame.math.Vector2((1, 1)), pygame.math.Vector2((-1, 1)), pygame.math.Vector2((1, -1)), pygame.math.Vector2((-1, -1))]
        
        self.direction = choice(possible_directions)
    
    def change_direction_collide(self, sprite):
        #self.direction = -self.direction
        if (self.direction.x == 0 and self.direction.y > 0) or (self.direction.x < 0 and self.direction.y > 0):
            # moving down, collision on bottom
            self.hitbox.bottom = sprite.hitbox.top
            self.direction.x = 1
            self.direction.y = 0
        elif (self.direction.x == 0 and self.direction.y < 0) or (self.direction.x > 0 and self.direction.y < 0):
            # moving up, collision on top
            self.hitbox.top = sprite.hitbox.bottom
            self.direction.x = -1
            self.direction.y = 0
        elif (self.direction.x > 0 and self.direction.y == 0) or (self.direction.x > 0 and self.direction.y > 0):
            # moving right, collision on right
            self.hitbox.right = sprite.hitbox.left
            self.direction.y = -1
            self.direction.x = 0
        elif (self.direction.x < 0 and self.direction.y == 0) or (self.direction.x < 0 and self.direction.y < 0):
            # moving left, collision on left
            self.hitbox.left = sprite.hitbox.right
            self.direction.y = 1
            self.direction.x = 0
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
        
        # if not close to player, decide direction based on collision and random otherwise decide based on player's direction and collision too
        self.mutual_dist = self.target.pos - self.pos
        if(self.mutual_dist.magnitude()):
            self.collide = False
            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, "hitbox"):
                    if(sprite.hitbox.colliderect(self.hitbox)):
                        self.collide = True
                        self.change_direction_collide(sprite)
            
            if(not self.timers["change_direction"].active):
                # can lead to random transport via collision when randomly direction decided
                self.timers["change_direction"].activate()
        else:
            # first decide direction based on relative position of player and enemy
            self.collide = False
            self.direction = pygame.math.Vector2((1 if self.mutual_dist.x < 0 else -1, 1 if self.mutual_dist.y < 0 else -1))
            for sprite in self.collision_sprites.sprites():
                if hasattr(sprite, "hitbox"):
                    if(sprite.hitbox.colliderect(self.hitbox)):
                        self.collide = True
                        # if collide decide direction randomly, but we have to do 
                        self.change_direction_random()
                
    def garbage_drop(self): # drop garbage at some intervals
        pass
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
   
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
        print(self.direction, self.collide)
        self.update_timers()
        self.move(dt)
    