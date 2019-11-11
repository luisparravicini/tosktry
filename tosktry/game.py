import random
import pygame
from pygame.locals import *
from .tetromino import Tetromino
from .timer import Timer
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

        self.falling_timer = Timer(800)

        pygame.key.set_repeat(150)

    def _update(self, dt):
        if not self.removing_lines:
            reached_max = self.falling_timer.update(dt)
            if reached_max:
                self._move_down()
        else:
            self._update_remove_lines(dt)

    def _update_remove_lines(self, dt):
        reached_max = self.lineRemovalTimer.update(dt)
        if reached_max:
            self.board.remove_lines(self.completed_lines)
            self.lineRemovalTimer = None
            self.removing_lines = False
            self.completed_lines = None

    def _draw(self):
        self.tetro.draw(self.screen, self.cell_size)
        self.board.draw(self.screen, self.cell_size, self.completed_lines)

    def _createTetro(self):
        self.tetro = Tetromino(self.board.size[0] // 2 - 2, 0)

    def _main(self):
        background_color = (40, 10, 40)

        self.removing_lines = False
        self.completed_lines = None
        self.done = False
        self._createTetro()
        while not self.done:
            dt = self.clock.tick(60)

            if not self.removing_lines:
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
                self._move_right()
            if e.type == KEYDOWN and e.key == K_LEFT:
                self._move_left()
            if e.type == KEYDOWN and e.key == K_DOWN:
                self.falling_timer.enable_fast()
            if e.type == KEYUP and e.key == K_DOWN:
                self.falling_timer.disable_fast()
            if e.type == KEYDOWN and e.key == K_UP:
                self._rotate()

    def _move_left(self):
        self._move((-1, 0))

    def _move_right(self):
        self._move((1, 0))

    def _rotate(self):
        self.tetro.rotate()
        self.board.push_into(self.tetro)

    def _move_down(self):
        if not self._move((0, 1)):
            self.board.consume(self.tetro)
            completed_lines = self.board.check_completed_lines()
            if len(completed_lines) > 0:
                self._start_line_removal(completed_lines)
            self._createTetro()

    def _start_line_removal(self, indices):
        self.completed_lines = indices
        self.removing_lines = True
        self.lineRemovalTimer = Timer(250)

    def _move(self, deltas):
        new_pos = list(self.tetro.pos)
        new_pos[0] += deltas[0]
        new_pos[1] += deltas[1]

        can_move = self.board.can_move(self.tetro, new_pos)
        if can_move:
            self.tetro.pos = new_pos

        return can_move
