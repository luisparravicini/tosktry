import random
import pygame
from pygame.locals import *
from .tetromino import Tetromino


class Game:

    def run(self):
        self._setup()
        self._main()

    def _setup(self):
        self.cell_size = 16
        self.screen_size = (
            self.cell_size * 10,
            self.cell_size * 20)
        random.seed()

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Tosktry')
        self.clock = pygame.time.Clock()

    def _update(self):
        pass

    def _draw(self):
        delta = 2
        pygame.draw.rect(self.screen, self.tetro.color,
            (self.tetro_pos[0] * self.cell_size + delta,
            self.tetro_pos[1] * self.cell_size + delta,
            self.cell_size - delta * 2,
            self.cell_size - delta * 2
            ), width=0)
        self.screen

    def _main(self):
        background_color = (40, 10, 40)

        self.done = False
        self.tetro_pos = [2, 2]
        self.tetro = Tetromino()
        while not self.done:
            self._process_input()
            self._update()

            self.clock.tick(60)
            self.screen.fill(background_color)
            self._draw()
            pygame.display.update()

    def _process_input(self):
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                self.done = True
                break

            if e.type == KEYDOWN and e.key == K_RIGHT:
                self.move_right()
            if e.type == KEYDOWN and e.key == K_LEFT:
                self.move_left()
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.start_fall()
            if e.type == KEYDOWN and e.key == K_UP:
                self.rotate()

    def move_left(self):
        pass

    def move_right(self):
        pass

    def rotate(self):
        pass

    def start_fall(self):
        pass
