import pygame
from . import setup,tool
class main_manu:
    def __init__(self):
        self.setup_backgroung()
        self.setup_player()
        self.setup_cursor()

    def setup_background(self):
        pass
    def setup_player(self):
        pass
    def setup_cursor(self):
        pass
    def update(self,surface):
        import random
        self.screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

        