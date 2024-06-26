import pygame
from random import randint, choice
from settings import *
from support import import_folder
from timers import Timer

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class DummyObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = pygame.Surface((32, 64))
        self.image.fill("orange")
        self.rect = self.image.get_rect(center=pos)
        self.z = z

class Water(Generic):
    def __init__(self, pos, frames, groups, z=LAYERS['main']):
        # animation setup
        self.frames_index = 0
        self.frames = frames
        
        # sprite setup
        super().__init__(pos, self.frames[self.frames_index], groups, z)
    
    def animate(self, dt):
        self.frames_index += 5*dt
        self.frames_index %= len(self.frames)
        self.image = self.frames[int(self.frames_index)]
    
    def update(self, dt):
        self.animate(dt)

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration=200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        
        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, name, groups, z=LAYERS["main"]):
        super().__init__(pos, surf, groups, z)
        
    #     # apples
    #     self.apple_surf = pygame.image.load("graphics/fruit/apple.png")
    #     self.apple_pos = APPLE_POS[name]
    
    # def create_fruit(self):
    #     for pos in self.apple_pos:
    #         if randint(0,10) < 2:
    #             x = pos[0] + self.rect.left
    #             y = pos[1] + self.rect.top
    #             print("puppies")
    #             print(self.groups())
    #             Generic(
	# 				pos = (x,y), 
	# 				surf = self.apple_surf, 
	# 				groups = self.groups()[0],
	# 				z = 2)

class Garbage(pygame.sprite.Sprite):
    def __init__(self, points, pos, groups, player, garbage_num, garbages, garbage_index, dec_garbageLeftfunc, z=LAYERS['main']):
        super().__init__(groups)
    
        self.image = pygame.image.load(f"assets/objects/Park_Garbage/j{garbage_num}.png").convert_alpha()
        if (garbage_num < 5):
            self.image = pygame.transform.scale(self.image, (2.25*self.image.get_width(), 2.25*self.image.get_height()))
        else:
            self.image = pygame.transform.scale(self.image, (0.5*self.image.get_width(), 0.5*self.image.get_height()))
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.player = player
        self.pos = pygame.math.Vector2(self.rect.center)
        self.garbages = garbages
        self.garbage_index = garbage_index
        self.dec_garbageLeftfunc = dec_garbageLeftfunc
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.2)
        self.points = points
    
    def garbage_collected(self):
        # check if player collided or withing reach of magnet radius
        diff = self.player.pos - self.pos
        if(self.player.timers["magnet"].active and diff.magnitude()<=MAGNET_RANGE):
            self.player.points += self.points
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS["main"], 300)
            self.kill()
            self.dec_garbageLeftfunc()
            self.garbages[self.garbage_index]=DummyGarbage()
        elif(self.hitbox.colliderect(self.player.hitbox)):
            # check if self.player presses the key space
            # self.player.garbage_signal = False
            # in this between if the player presses space the garbage, self.player.garbage_signal will turn on
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.timers["garbage_collect"].activate()
                # garbage collected
                self.player.points += self.points
                Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS["main"], 300)
                self.kill()
                self.dec_garbageLeftfunc()
                self.garbages[self.garbage_index]=DummyGarbage()
                
    
    def update(self, dt):
        self.garbage_collected()

class DummyGarbage:
    def __init__(self) -> None:
        pass
            
class Magnet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = pygame.image.load("assets/powerups/magnet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (0.1*self.image.get_width(), 0.1*self.image.get_height()))
        self.image.set_colorkey((232, 28, 232))
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.1, -self.rect.height * 0.1)

        self.pos = pos
        self.player = player
        
        self.timers={
            "despawn": Timer(MAGNET_DESPAWN_TIME*1000, self.kill)
        }
        self.timers["despawn"].activate()
    
    def magnet_collected(self):
        if(self.hitbox.colliderect(self.player.hitbox)):
            self.player.timers["magnet"].activate()
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS["main"], 300)
            self.kill()
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
            
    def update(self, dt):
        self.update_timers()
        self.magnet_collected()

class FastBoot(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = pygame.image.load("assets/powerups/fastboots.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (0.09*self.image.get_width(), 0.09*self.image.get_height()))
        self.image.set_colorkey((232, 28, 232))
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.1, -self.rect.height * 0.1)

        self.pos = pos
        self.player = player
        
        self.timers={
            "despawn": Timer(FASTBOOTS_DESPAWN_TIME*1000, self.kill)
        }
        self.timers["despawn"].activate()
        
    def fastboot_collected(self):
        if(self.hitbox.colliderect(self.player.hitbox)):
            self.player.timers["fast_boot"].activate()
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS["main"], 300)
            self.kill()
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
            
    def update(self, dt):
        self.update_timers()
        self.fastboot_collected()

class TimeAdder(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = pygame.image.load("assets/powerups/timeadder.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1/3*self.image.get_width(), 1/3*self.image.get_height()))
        self.image.set_colorkey((232, 28, 232))
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.1, -self.rect.height * 0.1)

        self.pos = pos
        self.player = player
        
        self.timers={
            "despawn": Timer(TIME_ADDER_DESPAWN_TIME*1000, self.kill)
        }
        self.timers["despawn"].activate()
        
    def timeadder_collected(self):
        if(self.hitbox.colliderect(self.player.hitbox)):
            self.player.timers["time_adder"].activate()
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS["main"], 300)
            self.kill()
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
            
    def update(self, dt):
        self.update_timers()
        self.timeadder_collected()

# class Drop(Generic):
#     def __init__(self, surf, pos, moving, groups, z):
#         super().__init__(pos, surf, groups, z)
#         self.lifetime = randint(400, 500)
#         self.start_time = pygame.time.get_ticks()
        
#         self.moving = moving
#         if self.moving:
#             self.pos = pygame.math.Vector2(self.rect.topleft)
#             self.direction = pygame.math.Vector2(-2, 4)
#             self.speed = randint(200, 250)
    
#     def update(self, dt):
#         if self.moving:
#             self.pos += self.direction * self.speed * dt
#             self.rect.topleft = (round(self.pos.x), round(self.pos.y))
#         if pygame.time.get_ticks()-self.start_time>=self.lifetime:
#             self.kill()

# class Rain:
#     def __init__(self, all_sprites):
#         self.all_sprites = all_sprites
#         self.rain_drops = import_folder("graphics/rain/drops/", 1)
#         self.rain_floor = import_folder("graphics/rain/floor/", 1)
#         print(self.rain_drops, self.rain_floor)
#         self.map_width = 7360
#         self.map_height = 4800
    
#     def create_floor(self):
#         Drop(
#             surf = choice(self.rain_drops),
#             pos = (randint(0, self.map_width), randint(0, self.map_height)),
#             moving = False,
#             groups = self.all_sprites,
#             z = LAYERS["rain floor"]
#         )
    
#     def create_drops(self):
#         Drop(
#             surf = choice(self.rain_drops), 
# 			pos = (randint(0,self.map_width),randint(0,self.map_height)), 
# 			moving = True, 
# 			groups = self.all_sprites, 
# 			z = LAYERS["rain drops"]
#         )
    
#     def update(self):
#         self.create_floor()
#         self.create_drops()
#         #print(self.all_sprites)