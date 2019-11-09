import random
import pygame
from pygame.locals import *


class Game:

    def run(self):
        self._setup()
        self._main()

    def _setup(self):
        self.cell_size = 48
        self.screen_size = (
            self.cell_size * 10,
            self.cell_size * 20)
        random.seed()

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bkg_surface = pygame.Surface(self.screen_size)
        pygame.display.set_caption('Tosktry')
        self.clock = pygame.time.Clock()

    def _update(self):
        pass

    def _main(self):
        background_color = (40, 10, 40)

        done = 0
        while not done:
            self.clock.tick(60)

            self.screen.fill(background_color)

            self._update()
            self.screen.blit(self.bkg_surface, (0, 0))

            pygame.display.update()

            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    done = 1
                    break

                if e.type == KEYDOWN and e.key == K_RIGHT:
                    self.move_right()
                if e.type == KEYDOWN and e.key == K_LEFT:
                    self.move_left()
                if e.type == KEYDOWN and e.key == K_SPACE:
                    self.start_fall()
                if e.type == KEYDOWN and e.key == K_UP:
                    self.rotate()

    def move_left(self):
        pass

    def move_right(self):
        pass

    def rotate(self):
        pass

    def start_fall(self):
        pass
