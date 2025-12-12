import pygame

class Input(object):
    def __init__(self):
        self.quit = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
