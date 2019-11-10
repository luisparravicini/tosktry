
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

    def push_into(self, tetro):
        first_used = tetro.first_used_x()
        left = tetro.pos[0] + first_used
        if left < 0:
            tetro.pos[0] = first_used
            return

        last_used = tetro.last_used_x()
        right = tetro.pos[0] + last_used
        if right >= self.size[0]:
            tetro.pos[0] = self.size[0] - last_used - 1

    def consume(self, tetro):
        pass
