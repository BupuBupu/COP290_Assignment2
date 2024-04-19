import pygame
from pygame.math import Vector2
# screen
pygame.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
# SCREEN_WIDTH = 1080
# SCREEN_HEIGHT = 720
TILE_SIZE = 64
# only this much offset will actually be blit on the screen, i.e. what the player currently see on the screen
OFFSET_X = 1000
OFFSET_Y = 600

# player attributes
PLAYER_SPAWN_POS = (3832, 2219)
PLAYER_SPEED = 200
PLAYER_ANIMATION_SPEED = 4

# lower the layer num, more below it is in z-axis
LAYERS = {
    "map":0,
    "main": 1,
}

# apple positions
APPLE_POS = {
	'tree_small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'tree_medium': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

# Attributes of level
MAX_KIDS = 10
MAX_GARBAGE = 20

#Garbage points
GARBAGE_POINTS = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 1,
    17: 1,
    18: 1,
    19: 1,
    20: 1
}

# Enemy range detection
TARGET_RADIUS = 700
#Enemy spawn positions
POSITION_AREAS = [((384, 7200), (384, 1660)), ((384, 3100), (1664, 2786)), ((4500, 7200), (1664, 2786)), ((384, 7200), (2790, 4100))]

# Powerups duration(in seconds) and Range
MAGNET_SPAWN_TIME = 20
MAGNET_DESPAWN_TIME = 15
MAGNET_DURATION = 10 
MAGNET_RANGE = 400

FASTBOOTS_SPAWN_TIME = 25
FASTBOOTS_DESPAWN_TIME = 15
FASTBOOTS_DURATION = 10

TIME_ADDER_SPAWN_TIME = 25 
TIME_ADDER_DESPAWN_TIME = 15
TIME_INCREMENT = 10