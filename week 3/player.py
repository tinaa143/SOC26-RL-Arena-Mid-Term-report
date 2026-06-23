class Player:
    def __init__(self, row, col, color, number):
        self.pos = (row, col)
        self.color = color
        self.dir = (1, 0)
        self.trail = []
        self.alive = True
        self.number = number
        self.on_territory = True
        self.start_pos = (row, col)
        self.start_dir = (1, 0)

    def reset(self):
        self.pos = self.start_pos
        self.dir = self.start_dir
        self.trail = []
        self.alive = True
        self.on_territory = True
