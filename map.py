from assets import WIDTH, HEIGHT, WIN, BLACK, INTERFACE_HEIGHT, INTERFACE_WIDTH, FONT, GREEN, RED
import pygame as pg
import numpy as np


class Map:

    def __init__(self, amr):
        self.enable_map = True
        self.enable_input = False
        self.amr = amr
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = np.zeros((self.height, self.width))
        self.start = None
        self.end = None
        self.downsized_grid = []
        self.obstacles = []
        self.button_radius = INTERFACE_HEIGHT // 2 - 10
        self.button_x = WIDTH - INTERFACE_WIDTH - self.button_radius - 10
        self.button_y = HEIGHT - INTERFACE_HEIGHT + self.button_radius + 5
        self.font = pg.font.SysFont(FONT, 10)

    def input_obstacles(self, mouse_down, mouse_up):
        """
        Input obstacles on the map by making.
        :param mouse_down:
        :param mouse_up:
        :return:
        """
        if mouse_down and not self.start:
            self.start = mouse_down
        elif mouse_up:
            self.end = mouse_up
            self.obstacles.append((self.start, (self.start[0], self.end[1]), self.end, (self.end[0], self.start[1])))
            self.start = None
            self.end = None

    def put_obstacle_on_grid(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.is_obstacle((row, col)):
                    self.grid[row][col] = 1

    def is_obstacle(self, pos):
        for obstacle in self.obstacles:
            x_range = []
            y_range = []
            for i in range(4):
                if obstacle[i][0] not in x_range:
                    x_range.append(obstacle[i][0])
                if obstacle[i][1] not in y_range:
                    y_range.append(obstacle[i][1])
            x_range.sort()
            y_range.sort()
            if x_range[0] <= pos[0] <= x_range[1] and y_range[0] <= pos[1] <= y_range[1]:
                return True
        return False

    def button_handler(self, mouse_pos):
        self.draw_input_button()
        if self.button_x - self.button_radius <= mouse_pos[0] <= self.button_x + self.button_radius and \
                self.button_y - self.button_radius <= mouse_pos[1] <= self.button_y + self.button_radius:
            self.enable_input = not self.enable_input

    def draw_input_button(self):
        if not self.enable_input:
            pg.draw.circle(WIN, GREEN, (self.button_x, self.button_y), self.button_radius)
            WIN.blit(self.font.render(
                "stop input", 1, BLACK), (self.button_x - self.button_radius + 5, self.button_y + 5))
        if self.enable_input:
            pg.draw.circle(WIN, RED, (self.button_x, self.button_y), self.button_radius)
            WIN.blit(self.font.render(
                "stop input", 1, BLACK), (self.button_x - self.button_radius + 5, self.button_y + 5))

    def handle_obstacles(self, mouse_down, mouse_up=None):
        self.button_handler(mouse_down)
        if self.enable_input:
            self.input_obstacles(mouse_down, mouse_up)

