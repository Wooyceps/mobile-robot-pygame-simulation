from assets import WIDTH, HEIGHT, WIN, BLACK
import pygame as pg


class Map:

    def __init__(self):
        self.enable_map = True
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.downsized_grid = []
        self.obstacles = []

    def input_obstacles(self, mouse):
        if mouse:
            x, y = mouse
            self.grid[x][y] = 1
            self.obstacles.append((x, y))

    def draw_obstacles(self):
        pg.draw.polygon(WIN, BLACK, self.obstacles, 1)


