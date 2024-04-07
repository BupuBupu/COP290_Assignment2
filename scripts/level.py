import pygame, sys
from settings import *
from player import Player
from enemy import Enemy
from overlay import Overlay_points

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        self.setup()
        self.points_display = Overlay_points(f"Naughty Kids Kidnapped: {self.player.points}", (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1/2), 'freesansbold.ttf', 60, text_rect_col=None)
    
    def setup(self):
        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.all_sprites, 1)
        self.enemy1 = Enemy(
            target=self.player,
            pos=(SCREEN_WIDTH/4, SCREEN_HEIGHT/2),
            group=self.all_sprites,
            speed=PLAYER_SPEED*0.8,
            anim_speed=PLAYER_ANIMATION_SPEED*0.8,
            enemy_num=1
        )
    
    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.custom_draw()
        self.points_display.display()
        self.all_sprites.update(dt)
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self, ):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
    
    def custom_draw(self):
        for layer in LAYERS.values():
            # for same layer, create fake 3D effect
            for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image, sprite.pos)