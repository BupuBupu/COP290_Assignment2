import pygame

class Timer:
    def __init__(self, duration, func=None): # if we want to execute some code, if once timer runs out
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
    
    def activate(self):
        # activate the times
        self.active = True
        self.start_time = pygame.time.get_ticks() # starting time doesn't need to necessarily be 0, it could be anything in our some point in game, it returns ms

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        # actual timer happens here, this update func will be called continuously
        
        # We will actually activate it outside, so no need to activate it here
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time!=0: # therefore it solves the previous bug
                self.func()
            self.deactivate()
        
        