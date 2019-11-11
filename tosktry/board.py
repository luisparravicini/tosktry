from .tetromino import Tetromino, COLORS


class Board:
    def __init__(self, width, height):
        self.size = (width, height)
        self.clear()

    def can_move(self, tetro, pos):
        if not self.inside_board(tetro, pos):
            return False

        if self.collides_with_others(tetro, pos):
            return False

        return True

    def clear(self):
        self.cells = [[None] * self.size[0] for _ in range(self.size[1])]

    def collides_with_others(self, tetro, pos):
        for y in range(len(tetro.pieces)):
            row = tetro.pieces[y]
            for x in range(len(row)):
                if row[x] == 0:
                    continue

                bx = pos[0] + x
                by = pos[1] + y

                if self.cells[by][bx] is not None:
                    return True

        return False

    def inside_board(self, tetro, pos):
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

    def check_completed_lines(self):
        indices = list()
        for y in range(self.size[1]):
            if all(v is not None for v in self.cells[y]):
                indices.append(y)
        return indices

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
        for y in range(len(tetro.pieces)):
            row = tetro.pieces[y]
            for x in range(len(row)):
                bx = tetro.pos[0] + x
                by = tetro.pos[1] + y
                if row[x] != 0:
                    self.cells[by][bx] = tetro.id

    def remove_lines(self, indices):
        for index in indices:
            for y in range(index, 0, -1):
                self.cells[y] = self.cells[y - 1]
            self.cells[0] = [None] * len(self.cells[0])

    def draw(self, surface, cell_size, completed_lines):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                cell_id = self.cells[y][x]
                if cell_id is not None:
                    if completed_lines is not None and y in completed_lines:
                        color = (255, 255, 255)
                    else:
                        color = COLORS[cell_id]
                    Tetromino.draw_piece(surface, (x, y), cell_size, color)
