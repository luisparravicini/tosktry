
class Board:
    def __init__(self, width, height):
        self.size = (width, height)
        self.cells = [[None] * width for _ in range(height)]

    def can_move(self, tetro, pos):
        bottom = pos[1] + tetro.height()
        if bottom >= self.size[1]:
            return False

        left = pos[0] + tetro.first_used_x()
        if left < 0:
            return False

        right = pos[0] + tetro.last_used_x()
        if right >= self.size[0]:
            return False

        return True

    def consume(self, tetro):
        pass
