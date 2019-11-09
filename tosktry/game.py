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
        self.tetro.draw(self.screen, self.cell_size)

    def _main(self):
        background_color = (40, 10, 40)

        self.done = False
        self.tetro = Tetromino(2, 2)
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
            if e.type == KEYDOWN and e.key == K_UP:
                self.start_fall()
            if e.type == KEYDOWN and e.key == K_DOWN:
                self.rotate()

    def move_left(self):
        self.tetro.pos[0] -= 1
        pass

    def move_right(self):
        self.tetro.pos[0] += 1
        pass

    def rotate(self):
        self.tetro.rotate()
        pass

    def start_fall(self):
        pass
