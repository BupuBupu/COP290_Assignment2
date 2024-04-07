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
        self.clock = pygame.time.Clock()
        self.setup()
        self.points_display = Overlay_points(f"Naughty Kids Kidnapped: {self.player.points}", (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1/2), 'freesansbold.ttf', 60, text_rect_col=None)
    
    def setup(self):
        tmx_data = load_pygame("assets/New_Map/Map.tmx")
        for layer in tmx_data.layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x*TILE_SIZE, y*TILE_SIZE)
                    surf = pygame.transform.scale(surf, (surf.get_width()*self.all_sprites.zoom_scale, surf.get_height()*self.all_sprites.zoom_scale))
                    Generic(pos, surf, self.all_sprites, LAYERS["map"])
        
        for obj in tmx_data.get_layer_by_name("Tree 2"):
            # print(obj.image)
            # if obj.name == "tree_medium":
            #     print(obj.image)
            print(obj)
            Generic(pos = (obj.x, obj.y), 
                 surf = obj.image, 
                 groups = self.all_sprites)
        
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
        #print(pygame.time.Clock().get_fps())
        

class CameraGroup(pygame.sprite.Group):
    def __init__(self, ):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        # zoom
        self.zoom_scale = 1
    
    def custom_draw(self, player):
        # due to offset, rect and image are not in pos
        self.offset.x = player.rect.centerx - SCREEN_WIDTH/2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT/2
        for layer in LAYERS.values():
            # for same layer, create fake 3D effect
            for sprite in sorted(self.sprites(), key=lambda sprite:sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    if hasattr(sprite, "import_assets"):
                        # player's hitbox
                        sprite.rect.center -= self.offset
                        pygame.draw.rect(self.display_surface, "red", sprite.rect)
                        pygame.draw.rect(self.display_surface, "blue", sprite.old_rect)
                    self.display_surface.blit(sprite.image, offset_rect)