import pygame
from pygame.locals import *
import random
import copy


COLORS = [
    '#F7D309',
    '#31C8EF',
    '#AE4D9C',
    '#42B742',
    '#EF2029',
    '#5A65AE',
    '#EF7922',
]
PIECES = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0],
    ],
    [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0],
    ],
    [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1],
    ],
    [
        [0, 0, 0],
        [1, 1, 1],
        [1, 0, 0],
    ],
    [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
    ],
]


class Tetromino:
    def __init__(self, x, y):
        self.pos = [x, y]

        i = random.randrange(0, len(COLORS))
        self.color = Color(COLORS[i])
        self.pieces = copy.deepcopy(PIECES[i])

    def rotate(self):
        size = len(self.pieces)
        new_piece = [[0] * size for _ in range(size)]
        i = size - 1
        for row in self.pieces:
            for j in range(size):
                new_piece[j][i] = row[j]
            i -= 1

        self.pieces = new_piece

    def height(self):
        y = len(self.pieces) - 1
        while y > 0 and 1 not in self.pieces[y]:
            y -= 1
        return y

    def first_used_x(self):
        x = 0
        while x < len(self.pieces[0]):
            for row in self.pieces:
                if row[x] == 1:
                    return x
            x += 1
        return x

    def last_used_x(self):
        x = len(self.pieces[0]) - 1
        while x >= 0:
            for row in self.pieces:
                if row[x] == 1:
                    return x
            x -= 1
        return x

    def draw(self, surface, cell_size):
        delta = 2
        y = self.pos[1]
        for row in self.pieces:
            x = self.pos[0]
            for cell in row:
                if cell == 1:
                    pygame.draw.rect(
                        surface,
                        self.color,
                        (x * cell_size + delta,
                         y * cell_size + delta,
                         cell_size - delta * 2,
                         cell_size - delta * 2),
                        width=0)
                x += 1
            y += 1
