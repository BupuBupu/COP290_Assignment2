import pygame
from settings import *

class Overlay_points:
    def __init__(self, player, pos, font=None, font_size=24, col=(0, 255, 0)):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = self.font.render(f"Points: {self.player.points}", True, (0, 255, 0))
        self.textRect = self.text.get_rect(center=pos)
    
    def display(self):
        self.display_surface.blit(self.text, self.textRect)