from .timer import Timer
from enum import Enum
import pygame
from pygame.locals import *
import os


class StartPlayState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.game = fsm.game

    def on_enter(self):
        self.game.board.clear()

    def update(self, dt):
        self.fsm.change(State.PLAYING)

    def draw(self, surface):
        pass

    def accept_input(self):
        return False


class PlayingState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.game = fsm.game
        self.timer = Timer(800)

    def on_enter(self):
        self.timer.reset()

    def update(self, dt):
        reached_max = self.timer.update(dt)
        if reached_max:
            self.game._move_down()

    def draw(self, surface):
        pass

    def accept_input(self):
        return True


class RemovingLinesState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.game = fsm.game
        self.timer = Timer(250)

    def on_enter(self):
        self.timer.reset()
        self.game.highlighted_lines = None

    def update(self, dt):
        reached_max = self.timer.update(dt)
        if reached_max:
            self.game.board.remove_lines(self.game.highlighted_lines)
            self.game.highlighted_lines = None
            self.fsm.change(State.PLAYING)

    def draw(self, surface):
        pass

    def accept_input(self):
        return False


class GameOverState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.game = fsm.game
        self.timer = Timer(20)

    def on_enter(self):
        self.timer.reset()
        self.game.highlighted_lines = [self.game.board.size[1] - 1]

    def update(self, dt):
        reached_max = self.timer.update(dt)
        if reached_max:
            last_y = self.game.highlighted_lines[-1]
            if last_y == 0:
                self.game.highlighted_lines = None
                self.fsm.change(State.GAME_OVER_MENU)
            else:
                self.game.highlighted_lines.append(last_y - 1)

    def draw(self, surface):
        pass

    def accept_input(self):
        return False


class GameOverMenuState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.game = fsm.game
        font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts/VT323/VT323-Regular.ttf')
        self.font = pygame.font.Font(font_path, 30)

    def on_enter(self):
        color = Color('white')
        self.textsurfaces = (
            (
                (25, 40),
                self.font.render("Game Over", False, color),
            ),
            (
                (16, 65),
                self.font.render("Play again?", False, color),
            ),
            (
                (45, 95),
                self.font.render("(Y/N)", False, color),
            )
        )

    def update(self, dt):
        events = pygame.event.get()
        if self.game.bot is not None:
            event = self.game.bot.game_over()
            if event is not None:
                events.append(event)

        for e in events:
            if e.type == KEYDOWN and e.key == K_y:
                self.fsm.change(State.START_PLAY)
            if e.type == KEYDOWN and e.key == K_n:
                self.game.done = True

    def draw(self, surface):
        pygame.draw.rect(self.game.screen, (10, 10, 10),
                         (10, 30, 140, 100))
        for pos, txt_surface in self.textsurfaces:
            self.game.screen.blit(txt_surface, pos)

    def accept_input(self):
        return False


class State(Enum):
    START_PLAY = 0
    PLAYING = 1
    REMOVING_LINES = 2
    GAME_OVER = 3
    GAME_OVER_MENU = 4


class GameFSM:
    def __init__(self, game):
        self.game = game
        self.states = {
            State.START_PLAY: StartPlayState(self),
            State.PLAYING: PlayingState(self),
            State.REMOVING_LINES: RemovingLinesState(self),
            State.GAME_OVER: GameOverState(self),
            State.GAME_OVER_MENU: GameOverMenuState(self),
        }
        self.change(State.START_PLAY)

    def change(self, state_id):
        # print('changing state to', state_id)
        self.state = self.states[state_id]
        self.state.on_enter()
