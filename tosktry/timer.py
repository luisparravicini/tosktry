
class Timer:
    def __init__(self, max):
        self.max = max
        self.modifier = 1
        self.acum = 0

    def reset(self):
        self.acum = 0

    def update(self, dt):
        self.acum += dt
        reached_max = self.acum > self.max * self.modifier
        if reached_max:
            self.acum = 0
        return reached_max

    def enable_fast(self):
        self.modifier = 0.1

    def disable_fast(self):
        self.modifier = 1
