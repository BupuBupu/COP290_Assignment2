import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.import_assets()
        self.status = "down_idle"
        self.frame_index = 0
        
        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.animate_speed = 4
        
        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        
        # attributes
        self.points = 0
    
    def import_assets(self):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
        }
        print("heheeh")
        for animation in self.animations.keys():
            full_path = "../assets/characters/player/player1/" + animation
            self.animations[animation] = import_folder(full_path, 3)
        
        print(self.animations)
    
    def animate(self, dt):
        self.frame_index += self.animate_speed * dt
        self.frame_index %= len(self.animations[self.status])
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0
        
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0
    
        # faster movement
        if keys[pygame.K_LSHIFT]:
            self.speed = 400
            self.animate_speed = 8
        else:
            self.speed = 200
            self.animate_speed = 4
    
    def get_status(self):
        if self.direction.magnitude()==0:
            self.status = self.status.split('_')[0] + "_idle"
            
    def move(self, dt):
        # Normalizing the vector
        if(self.direction.magnitude()):
            self.direction = self.direction/self.direction.magnitude()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x) # round for consistency since rect positions work in integer
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)
        
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)