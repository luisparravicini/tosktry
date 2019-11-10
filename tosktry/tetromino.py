import pygame
from pygame.locals import *
import random
import copy


COLORS = [
    Color('#F7D309'),
    Color('#31C8EF'),
    Color('#AE4D9C'),
    Color('#42B742'),
    Color('#EF2029'),
    Color('#5A65AE'),
    Color('#EF7922'),
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

        self.id = random.randrange(0, len(COLORS))
        self.color = COLORS[self.id]
        self.pieces = copy.deepcopy(PIECES[self.id])

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
        y = self.pos[1]
        for row in self.pieces:
            x = self.pos[0]
            for cell in row:
                if cell == 1:
                    Tetromino.draw_piece(surface, (x, y), cell_size, self.color)
                x += 1
            y += 1

    @staticmethod
    def draw_piece(surface, pos, cell_size, color):
        delta = 2
        pygame.draw.rect(
            surface,
            color,
            (pos[0] * cell_size + delta,
             pos[1] * cell_size + delta,
             cell_size - delta * 2,
             cell_size - delta * 2),
            width=0)
