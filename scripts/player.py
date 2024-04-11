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
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.2, -self.rect.height*0.2))
        
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
            
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"): # has attribute
                if sprite.hitbox.colliderect(self.hitbox):
                    print(sprite)
                    pygame.draw.rect(pygame.display.get_surface(), "orange", sprite.hitbox)
                    #pygame.draw.rect(pygame.display.get_surface(), "orange", sprite.hitbox)
                    # we need to know the direction of collision, so that we can snap it back
                    if direction == "horizontal":
                        if self.direction.x > 0: # moving to right, so collision happened on left
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # moving left
                            self.hitbox.left = sprite.hitbox.right
                        # above we are only updating hitbox, we are not updating our image rect which the player actually sees
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    elif direction == "vertical":
                        if self.direction.y > 0: #moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0: # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                
            
    def move(self, dt):
        # Normalizing the vector
        if(self.direction.magnitude()):
            self.direction = self.direction/self.direction.magnitude()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.x = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx # round for consistency since rect positions work in integer
        self.collision("horizontal")
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.y = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")
        
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        print(self.direction)
        #print(self.rect.center, self.rect.copy().center, self.pos)