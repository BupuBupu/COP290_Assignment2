import pygame
from pygame.math import Vector2
# screen
pygame.init()
# SCREEN_WIDTH = pygame.display.Info().current_w
# SCREEN_HEIGHT = pygame.display.Info().current_h
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
TILE_SIZE = 64
# only this much offset will actually be blit on the screen, i.e. what the player currently see on the screen
OFFSET_X = 1000
OFFSET_Y = 600

# player attributes
PLAYER_SPEED = 200
PLAYER_ANIMATION_SPEED = 4

# lower the layer num, more below it is in z-axis
LAYERS = {
    "map":0,
    "main": 1,
}

# Attributes of level
MAX_KIDS = 10
MAX_GARBAGE = 20

# Enemy range detection
TARGET_RADIUS = 700
#Enemy spawn positions
POSITION_AREAS = [((320, 3264), (320, 2786)), ((320, 4416), (2786, 4160)), ((4416, 7360), (1664, 4160)), ((3264, 7630), (320, 1664))]