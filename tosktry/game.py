import random
import pygame
from pygame.locals import *
from .tetromino import Tetromino
from .fall_timer import FallTimer
from .board import Board


class Game:

    def run(self):
        self._setup()
        self._main()

    def _setup(self):
        self.board = Board(10, 20)
        self.cell_size = 16
        self.screen_size = (
            self.cell_size * self.board.size[0],
            self.cell_size * self.board.size[1])
        random.seed()

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Tosktry')
        self.clock = pygame.time.Clock()

        self.falling_timer = FallTimer(800)

    def _update(self, dt):
        reached_max = self.falling_timer.update(dt)
        if reached_max:
            self.move_down()

    def _draw(self):
        self.tetro.draw(self.screen, self.cell_size)

    def _createTetro(self):
        self.tetro = Tetromino(self.board.size[0] // 2 - 2, 0)

    def _main(self):
        background_color = (40, 10, 40)

        self.done = False
        self._createTetro()
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
                self.falling_timer.enable_fast()
            if e.type == KEYUP and e.key == K_DOWN:
                self.falling_timer.disable_fast()
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
        new_pos = list(self.tetro.pos)
        new_pos[1] += 1
        if self.board.can_move(self.tetro, new_pos):
            self.tetro.pos = new_pos
        else:
            self.board.consume(self.tetro)
            self._createTetro()
