import pygame, sys
from settings import *
from player import Player
from enemy import Enemy
from sprites import Generic
from overlay import Overlay_points
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        self.setup()
        self.points_display = Overlay_points(f"Naughty Kids Kidnapped: {self.player.points}", (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1/2), 'freesansbold.ttf', 60, text_rect_col=None)
    
    def setup(self):
        tmx_data = load_pygame("assets/tilesets/Map/Map.tmx")
        for layer in tmx_data.layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x*TILE_SIZE, y*TILE_SIZE)
                    Generic(pos, surf, self.all_sprites, LAYERS["map"])
        
        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.all_sprites, 2)
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
        self.all_sprites.custom_draw(self.player)
        self.points_display.display()
        self.all_sprites.update(dt)
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self, ):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        # zoom
        self.zoom_scale = 4
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA) # this enables alpha on this surface
        self.internal_rect = self.internal_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.internal_surf_size_vector = pygame.math.Vector2(self.internal_surf_size) 
    
    def custom_draw(self, player):
        #self.internal_surf.fill(self.display_surface.get_colorkey())
        
        self.offset.x = player.rect.centerx - SCREEN_WIDTH/2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT/2
        for layer in LAYERS.values():
            # for same layer, create fake 3D effect
            for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)