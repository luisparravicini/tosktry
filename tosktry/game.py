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

    def _update(self, dt):
        self.acum_fall += dt
        if self.acum_fall > self.fall_time * self.falling_mod:
            self.acum_fall = 0
            self.move_down()
        pass

    def _draw(self):
        self.tetro.draw(self.screen, self.cell_size)

    def _main(self):
        background_color = (40, 10, 40)

        self.done = False
        self.fall_time = 800
        self.acum_fall = 0
        self.falling_mod = 1
        self.tetro = Tetromino(2, 2)
        while not self.done:
            dt = self.clock.tick(60)

            self._process_input()
            self._update(dt)

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
            if e.type == KEYDOWN and e.key == K_DOWN:
                self.falling_mod = 0.1
            if e.type == KEYUP and e.key == K_DOWN:
                self.falling_mod = 1
            if e.type == KEYDOWN and e.key == K_UP:
                self.rotate()

    def move_left(self):
        x = self.tetro.pos[0] - 1
        self.tetro.pos[0] = x

    def move_right(self):
        x = self.tetro.pos[0] + 1
        self.tetro.pos[0] = x

    def rotate(self):
        self.tetro.rotate()

    def move_down(self):
        x = self.tetro.pos[1] + 1
        self.tetro.pos[1] = x
