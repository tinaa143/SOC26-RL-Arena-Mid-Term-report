class Player:
    def __init__(self, row, col, color, number):
        self.color = color
        self.number = number
        self.start_pos = (row, col)
        self.start_dir = (1, 0)
        self.reset()

    def reset(self):
        self.pos = self.start_pos
        self.dir = self.start_dir
        self.trail = []
        self.alive = True
        self.on_territory = True
