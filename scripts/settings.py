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
    "water":0,
    "map": 1,
    "spec":2,
    "decoration":3,
    "bridge":4,
    "fences":5,
    "main": 6
}

# Attributes of level
MAX_KIDS = 10
MAX_GARBAGE = 20