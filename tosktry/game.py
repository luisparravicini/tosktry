import random
import pygame
from pygame.locals import *
from .tetromino import Tetromino
from .board import Board
from .bot import Bot
from .fsm import GameFSM, State


class Game:

    def __init__(self):
        self.enable_bot(False)

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
        pygame.key.set_repeat(150)
        self.highlighted_lines = None
        self.fsm = GameFSM(self)

    def enable_bot(self, enabled):
        if enabled:
            bot = Bot()
        else:
            bot = None
        self.bot = bot

    def _update(self, dt):
        self.fsm.state.update(dt)

    def _draw(self):
        self.tetro.draw(self.screen, self.cell_size)
        self.board.draw(self.screen, self.cell_size, self.highlighted_lines)
        self.fsm.state.draw(self.screen)

    def _createTetro(self):
        self.tetro = Tetromino(self.board.size[0] // 2 - 2, 0)

    def _main(self):
        background_color = (40, 10, 40)

        self.done = False
        self._createTetro()
        while not self.done:
            dt = self.clock.tick(60)

            if self.fsm.state.accept_input():
                self._process_input()
            self._update(dt)

            self.screen.fill(background_color)
            self._draw()
            pygame.display.update()

    def _process_input(self):
        events = pygame.event.get()
        if self.bot is not None:
            event = self.bot.next_move()
            if event is not None:
                events.append(event)

        for e in events:
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                self.done = True
                break

            if e.type == KEYDOWN and e.key == K_RIGHT:
                self._move_right()
            if e.type == KEYDOWN and e.key == K_LEFT:
                self._move_left()
            if e.type == KEYDOWN and e.key == K_DOWN:
                self.fsm.state.timer.enable_fast()
            if e.type == KEYUP and e.key == K_DOWN:
                self.fsm.state.timer.disable_fast()
            if e.type == KEYDOWN and e.key == K_UP:
                self._rotate()

    def _move_left(self):
        self._move((-1, 0))

    def _move_right(self):
        self._move((1, 0))

    def _rotate(self):
        self.tetro.rotate()
        self.board.push_into(self.tetro)
        if not self.board.can_move(self.tetro, self.tetro.pos):
            # HACK if the rotated teromino falls outside the board
            # it gets rotated back to it's original position by
            # rotating it 3 times (270 degress + 90 of first rotation)
            for _ in range(3):
                self.tetro.rotate()

    def _move_down(self):
        if not self._move((0, 1)):
            self.board.consume(self.tetro)

            self._createTetro()
            if self.board.collides_with_others(self.tetro, self.tetro.pos):
                self.fsm.change(State.GAME_OVER)
                return

            highlighted_lines = self.board.check_completed_lines()
            if len(highlighted_lines) > 0:
                self.fsm.change(State.REMOVING_LINES)
                self.highlighted_lines = highlighted_lines

    def _move(self, deltas):
        new_pos = list(self.tetro.pos)
        new_pos[0] += deltas[0]
        new_pos[1] += deltas[1]

        can_move = self.board.can_move(self.tetro, new_pos)
        if can_move:
            self.tetro.pos = new_pos

        return can_move
