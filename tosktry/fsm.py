from .timer import Timer

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

    def accept_input(self):
        return True


class RemovingLinesState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.game = fsm.game
        self.timer = Timer(250)

    def on_enter(self):
        self.timer.reset()

    def update(self, dt):
        reached_max = self.timer.update(dt)
        if reached_max:
            self.game.board.remove_lines(self.game.completed_lines)
            self.game.completed_lines = None
            self.fsm.change(State.PLAYING)

    def accept_input(self):
        return False


from enum import Enum

class State(Enum):
    PLAYING = 0
    REMOVING_LINES = 1
    GAME_OVER_FX = 2
    GAME_OVER_MENU = 3


class GameFSM:
    def __init__(self, game):
        self.game = game
        self.states = {
            State.PLAYING: PlayingState(self),
            State.REMOVING_LINES: RemovingLinesState(self),
        }
        self.change(State.PLAYING)

    def change(self, state_id):
        self.state = self.states[state_id]
        self.state.on_enter()
