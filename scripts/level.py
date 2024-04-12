import pygame 
from settings import *
from player import Player
from enemy import Enemy
from overlay import Overlay_points
from sprites import Generic
from pytmx.util_pygame import load_pygame
from support import *

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup()
        self.points_display = Overlay_points(f"Naughty Kids Kidnapped: {self.player.points}", (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1/2), 'freesansbold.ttf', 60, text_rect_col=None)

    def setup(self):
        tmx_data = load_pygame("assets/Another_New_Map/Map.tmx")
        for layer in tmx_data.layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x*TILE_SIZE, y*TILE_SIZE)
                    Generic(pos, surf, self.all_sprites, LAYERS["map"])
        
        for obj in tmx_data.get_layer_by_name("Trees"):
            if obj.name=="tree_medium":
                surf = obj.image
                Generic(
                    pos=(obj.x, obj.y),
                    surf=surf,
                    groups=[self.all_sprites, self.collision_sprites]
                )
        
        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.all_sprites, collision_sprites=self.collision_sprites)
        self.enemy1 = Enemy(
            target=self.player,
            pos=(SCREEN_WIDTH/4, SCREEN_HEIGHT/2),
            group=self.all_sprites,
            speed=160,
            anim_speed=3.2,
            enemy_num=1
        )
    
    def run(self, dt):
        self.display_surface.fill("black")
        
        self.all_sprites.custom_draw(self.player)
        self.points_display.display()
        self.all_sprites.update(dt)
class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)

					# # anaytics
					if sprite == player:
						pygame.draw.rect(self.display_surface,'red',offset_rect,5)
						hitbox_rect = player.hitbox.copy()
						hitbox_rect.center = offset_rect.center
						pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
						# target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
						# pygame.draw.circle(self.display_surface,'blue',target_pos,5)