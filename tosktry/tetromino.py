import pygame
from pygame.locals import *


class Tetromino:
    def __init__(self, x, y):
        self.pos = [x, y]
        #F7D309
        #31C8EF
        #AE4D9C
        #42B742
        #EF2029
        #5A65AE
        #EF7922
        self.color = Color('#EF7922')
        self.pieces = [
            'xxxx',
            '    ',
            '    ',
            '    ',
            '    ',
        ]

    def rotate(self):
        print('rotate')
        pass

    def draw(self, surface, cell_size):
        delta = 2
        y = self.pos[1]
        for row in self.pieces:
            x = self.pos[0]
            for cell in row:
                if cell == 'x':
                    pygame.draw.rect(surface, self.color,
                        (x * cell_size + delta,
                        y * cell_size + delta,
                        cell_size - delta * 2,
                        cell_size - delta * 2
                        ), width=0)
                x += 1
            y += 1
