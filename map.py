from assets import WIDTH, HEIGHT


class Map:

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.downsized_grid = []