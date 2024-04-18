import pygame, math
from settings import *

class Overlay_text:
    def __init__(self, pos, font=None, font_size=60, text_col=(0, 255, 0), text_rect_col = (0, 0, 108)):
        
        self.display_surface = pygame.display.get_surface()
        self.pos = pos
        self.font = pygame.font.Font(font, font_size)
        self.text_col = text_col
        self.text_rect_col = text_rect_col
    
    def render(self, text, extra=""):
        self.text = self.font.render(text+str(extra), True, self.text_col, self.text_rect_col)
        self.textRect = self.text.get_rect(center=self.pos)
    def display(self):
        self.display_surface.blit(self.text, self.textRect)

class Overlay_pointers:
    def __init__(self, enemy, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.enemy = enemy
        self.player = player 
        
        # imports
        pointer_path = "assets/UIs/pointers/"
        self.pointer_surf = pygame.image.load(f"{pointer_path}/0.jpg").convert_alpha()
        self.pointer_surf.set_alpha(125)
        self.pointer_surf = pygame.transform.scale(self.pointer_surf, (self.pointer_surf.get_width()*0.1, self.pointer_surf.get_height()*0.1))
        self.pointer_surf.set_colorkey((255, 255, 255))
    
    def display(self):
        enemy_pos = self.enemy.pos  # Vector2
        player_pos = self.player.pos # Vector2
        diff = enemy_pos - player_pos
        diff.y = -diff.y
        diff_mag = diff.magnitude()
        put_radius = 10
        degree = 0
        pos = pygame.math.Vector2((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        pos_offset = 50
        if(diff.x < 0 and diff.y < 0):
            # enemy on 3rd part of x-y plane
            try:
                degree = 180+math.degrees(math.atan(diff.y/diff.x))
            except ZeroDivisionError:
                degree = 270
            pos.x += pos_offset * math.cos(math.radians(degree))
            pos.y -= pos_offset * math.sin(math.radians(degree))
        elif(diff.x>0 and diff.y > 0):
            # enemy on 1st part of x-y plane
            try:
                degree = math.degrees(math.atan(diff.y/diff.x))
            except ZeroDivisionError:
                degree = 90
            pos.x += pos_offset * math.cos(math.radians(degree))
            pos.y -= pos_offset * math.sin(math.radians(degree))
        elif(diff.x > 0 and diff.y < 0):
            # enemy on 4th part of x-y plane
            try:
                degree = 360 + math.degrees(math.atan(diff.y/diff.x))
            except ZeroDivisionError:
                degree = 270
            pos.x += pos_offset * math.cos(math.radians(degree))
            pos.y -= pos_offset * math.sin(math.radians(degree))
        else:
            # enemy on 2nd part of x-y plane
            try:
                degree = 180 + math.degrees(math.atan(diff.y/diff.x))
            except:
                degree = 90
            pos.x += pos_offset * math.cos(math.radians(degree))
            pos.y -= pos_offset * math.sin(math.radians(degree))
        
        # print("enemy:", enemy_pos, "player:", player_pos, "diff: ", diff, "degrees:", degree, math.cos(math.radians(degree)), math.sin(math.radians(degree)))
        
        if(abs(diff.x)>SCREEN_WIDTH/2 or abs(diff.y)>SCREEN_HEIGHT/2):
            # we have to blit it on screen with the required rotation and pos on screen
            pointer = pygame.transform.rotate(self.pointer_surf, degree)
            pointer_rect = pointer.get_rect(center=pos)
            self.display_surface.blit(pointer, pointer_rect)
    
class OverlayNullPointers:
    def __init__(self):
        pass
    def display(self):
        pass