
class Board:
    def __init__(self, width, height):
        self.size = (width, height)

    def can_move(self, tetro, pos):
        bottom = pos[1] + tetro.height()
        return bottom < self.size[1]

    def consume(self, tetro):
        pass
