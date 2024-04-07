import pygame, sys, time
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kidnapping Kids")
        self.level = Level()
        self.clock = pygame.time.Clock()
    
    def run(self):
        previous_time = time.time()
        while True:
            dt = time.time() - previous_time # delta time to make it frame independent
            previous_time = time.time()
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.level.run(dt)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()