import pygame
from settings import *

class Overlay_points:
    def __init__(self, text, pos, font=None, font_size=60, text_col=(0, 255, 0), text_rect_col = (0, 0, 108)):
        
        self.display_surface = pygame.display.get_surface()
        
        self.font = pygame.font.Font(font, font_size)
        self.text = self.font.render(text, True, text_col, text_rect_col)
        self.textRect = self.text.get_rect(center=pos)
    
    def display(self):
        self.display_surface.blit(self.text, self.textRect)