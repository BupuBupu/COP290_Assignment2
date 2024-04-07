import pygame
from pygame.math import Vector2
# screen
pygame.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
TILE_SIZE = 64

# player attributes
PLAYER_SPEED = 200
PLAYER_ANIMATION_SPEED = 4

# lower the layer num, more below it is in z-axis
LAYERS = {
    "enemy": 0,
    "player": 0
}