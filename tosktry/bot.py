import random
import pygame
from pygame.locals import *


class Bot:
    def __init__(self):
        pass

    def next_move(self):
        if random.random() < 0.5:
            return None

        key = random.choice((K_RIGHT, K_LEFT, K_DOWN, K_UP))
        return pygame.event.Event(KEYDOWN, {'key': key})
