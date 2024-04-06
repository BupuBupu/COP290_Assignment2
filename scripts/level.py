import pygame, sys
from settings import *
from player import Player
from overlay import Overlay_points

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()

        self.setup()
        self.points_display = Overlay_points(f"Naughty Kids Kidnapped: {self.player.points}", (SCREEN_WIDTH/2, SCREEN_HEIGHT*0.1/2), 'freesansbold.ttf', 60, text_rect_col=None)
    
    def setup(self):
        self.player = Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), self.all_sprites, 2)
    
    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
        self.points_display.display()
        self.all_sprites.update(dt)