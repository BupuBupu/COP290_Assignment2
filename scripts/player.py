import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, player_num=1):
        super().__init__(group)
        self.player_num = player_num
        self.import_assets()
        self.status = "down_idle"
        self.frame_index = 0
        
        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.animate_speed = PLAYER_ANIMATION_SPEED
        self.z = LAYERS["main"]
        
        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED
        
        # collision
        self.collision_sprites = collision_sprites
        self.old_rect = self.rect.copy()
        
        # attributes
        self.points = 0
    
    def import_assets(self):
        self.animations = {
            "up": [], "down": [], "left": [], "right": [],
            "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": []
        }
        for animation in self.animations.keys():
            full_path = f"assets/characters/player/player{self.player_num}/" + animation
            self.animations[animation] = import_folder(full_path, 4)
    
    def animate(self, dt):
        self.frame_index += self.animate_speed * dt
        self.frame_index %= len(self.animations[self.status])
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0
    
        # faster movement
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.speed = PLAYER_SPEED * 2
            self.animate_speed = PLAYER_ANIMATION_SPEED * 2
        else:
            self.speed = PLAYER_SPEED
            self.animate_speed = PLAYER_ANIMATION_SPEED
    
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
        self.old_rect.copy() # previous frame
        self.input()
        self.get_status()
        self.move(dt) # current frame
        self.animate(dt)
        print(self.rect.center, self.rect.copy().center, self.pos)