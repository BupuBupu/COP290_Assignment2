import pygame, random
from settings import *
from player import Player
from enemy import Enemy, DummyEnemy
from overlay import Overlay_text, Overlay_pointers
from sprites import Generic, Tree, Water, Garbage, DummyObject
from pytmx.util_pygame import load_pygame
from support import *
from timers import Timer

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.garbage_sprites = pygame.sprite.Group()
        
        self.setup()
        
        # Points of the level
        self.children_left = MAX_KIDS
        self.garbage_left = 0
        self.points_display = Overlay_text(f"Score: {self.player.points}", (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1/2), 'freesansbold.ttf', 60, text_rect_col=None)
        self.children_left_display = Overlay_text(f"Children Left:{self.children_left}/{MAX_KIDS}", (SCREEN_WIDTH-140, SCREEN_HEIGHT-125), "freesansbold.ttf", 24, text_col = (255, 255, 255), text_rect_col=None)
        self.garbage_left_display = Overlay_text(f" Garbage remaining:{self.garbage_left}/{MAX_GARBAGE}", (SCREEN_WIDTH-155, SCREEN_HEIGHT-100), "freesansbold.ttf", 24, text_col = (255, 255, 255), text_rect_col=None)

    def setup(self):
        # basic ground
        tmx_data = load_pygame("assets/Another_New_Map/Map.tmx")
        for x, y, surf in tmx_data.get_layer_by_name("Ground").tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS["map"])
                
        # water
        water_frames = import_folder("graphics/water", 1)
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
            Water((x*TILE_SIZE, y*TILE_SIZE), water_frames, self.all_sprites, LAYERS["map"])
        
        # spec decor
        for x, y, surf in tmx_data.get_layer_by_name("spec").tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS["map"])
        
        # decor
        for x, y, surf in tmx_data.get_layer_by_name("Decoration").tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS["map"])

        # bridge
        for x, y, surf in tmx_data.get_layer_by_name("Bridge").tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS["map"])
            
        # fences
        for x, y, surf in tmx_data.get_layer_by_name("Fences").tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS["main"])
            
        # collision layer
        for x, y, surf in tmx_data.get_layer_by_name("collision layer").tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS["map"])

        
        # objects
        for obj in tmx_data.get_layer_by_name("Trees"):
            surf = obj.image
            Tree(
                pos=(obj.x, obj.y),
                surf=surf,
                name=obj.name,
                groups=[self.all_sprites, self.collision_sprites]
            )
        
        # player and enemy spawn positions
        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.all_sprites, collision_sprites=self.collision_sprites)
        # DummyObject((0, 0), self.all_sprites)
        
        self.garbages = []
        self.enemies = []
        # self.enemy1 = Enemy(
        #     target=self.player,
        #     pos=(SCREEN_WIDTH/2-1, SCREEN_HEIGHT/2),
        #     group=self.all_sprites,
        #     speed=PLAYER_SPEED*0.8,
        #     collision_sprites=self.collision_sprites,
        #     anim_speed=PLAYER_ANIMATION_SPEED*0.8,
        #     enemy_num=1
        # )
        self.random_speeds = []
        self.random_positions = []
        for i in range(MAX_KIDS):
            self.random_speeds.append(random.random())
        for i in range(MAX_KIDS):
            random_choice = random.choice(POSITION_AREAS)
            rand_posx = random.randint(random_choice[0][0], random_choice[0][1])
            rand_posy = random.randint(random_choice[1][0], random_choice[1][1])
            self.random_positions.append((rand_posx, rand_posy))
        self.pointers = []
        for i in range(MAX_KIDS):
            self.enemies.append(Enemy(target=self.player,
                                      pos=self.random_positions[i],
                                      group=[self.all_sprites, self.enemy_sprites],
                                      speed=PLAYER_SPEED*(0.5+self.random_speeds[i]),
                                      anim_speed=PLAYER_ANIMATION_SPEED*(0.5+self.random_speeds[i]),
                                      collision_sprites=self.collision_sprites,
                                      garbage_func = self.enemy_drop_garbage,
                                      garbage_drop_interval=random.randint(5, 15),
                                      enemy_num=random.randint(1, 5),
                                      enemy_index=i,
                                      enemies=self.enemies,
                                      pointers=self.pointers))
        # pointers for every enemy
        for i in range(MAX_KIDS):
            self.pointers.append(Overlay_pointers(self.enemies[i], self.player))
    
    # def show_enemy_pointers(self, enemies):
    #     # will show arrow pointers as overlay on screen depending on enemie's position if they are outside of screen
    #     pass
            
    def enemy_drop_garbage(self, index):
        garbage_index = random.randint(1, 20)
        self.garbages.append(Garbage(
            points=GARBAGE_POINTS[garbage_index],
            pos=self.enemies[index].pos,
            groups=[self.all_sprites, self.garbage_sprites],
            player=self.player,
            garbage_num = garbage_index,
            garbages = self.garbages,
            garbage_index=len(self.garbages)-1,
            dec_garbageLeftfunc=self.dec_garbage_left,
            z=LAYERS['main']
        ))
        self.garbage_left+=1
        
    def dec_garbage_left(self):
        self.garbage_left-=1
        
    def run(self, dt):
        self.display_surface.fill("#9bd4c3")
        
        # garbage drops
        for i in range(len(self.enemies)):
            if(hasattr(self.enemies[i], "timers") and not self.enemies[i].timers["garbage_drop"].active):
                self.enemies[i].timers["garbage_drop"].activate()
        
        # all_sprites display
        self.all_sprites.custom_draw(self.player)
        
        # overlay display
        for i in range(len(self.pointers)):
            self.pointers[i].display()
        self.points_display.render("Score: ", self.player.points)
        self.points_display.display()
        self.children_left_display.render("Children Alive: ", MAX_KIDS-self.player.kids_caught)
        self.children_left_display.display()
        self.garbage_left_display.render("Garbage left: ", self.garbage_left)
        self.garbage_left_display.display()
        
        # updating all sprites
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
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    if(abs(sprite.rect.centerx-player.rect.centerx)<= OFFSET_X and abs(sprite.rect.centery-player.rect.centery)<=OFFSET_Y):
                        self.display_surface.blit(sprite.image, offset_rect)
                    
                    # analytics
                    if sprite == player:
                        pygame.draw.rect(self.display_surface, "red", offset_rect, 5)
                        hitbox_rect = player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        pygame.draw.rect(self.display_surface, "green", hitbox_rect, 5)