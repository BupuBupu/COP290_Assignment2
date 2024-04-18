import pygame
from random import randint
from settings import *
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
    def __init__(self, pos, groups, player, z=LAYERS["main"]) -> None:
        super().__init__(groups)
        self.image = pygame.image.load("assets/powerups/magnet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (0.125*self.image.get_width(), 0.125*self.image.get_height()))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.1, -self.rect.height * 0.1)

        self.pos = pos
        self.player = player
    
    def magnet_collected(self):
        if(self.hitbox.colliderect(self.player.hitbox)):
            self.player.timers["magnet"].activate()
            Particle(self.rect.topleft, self.image, self.groups()[0], LAYERS["main"], 300)
            self.kill()
    
    def update(self, dt):
        self.magnet_collected()
        