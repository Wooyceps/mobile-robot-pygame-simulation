import pygame as pg
import numpy as np
from time import time
from assets import WIDTH, HEIGHT, WIN, BLACK, INTERFACE_HEIGHT, INTERFACE_WIDTH, FONT, GREEN, RED
from a_star import a_star_search


class Map:
    def __init__(self, amr):
        self.amr = amr
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = np.zeros((self.height, self.width))
        self.obstacles = []
        self.target = None
        self.start = self.end = None
        self.downsized_grid = np.zeros((self.height // 10, self.width // 10))
        self.enable_map = True
        self.enable_input = self.enable_pathfinding = self.enable_targeting = False
        self.button_radius = INTERFACE_HEIGHT // 2 - 10
        self.button_1 = (WIDTH - INTERFACE_WIDTH - self.button_radius - 10, HEIGHT - INTERFACE_HEIGHT + self.button_radius + 5)
        self.button_2 = (self.button_1[0] - 2 * self.button_radius - 10, self.button_1[1])
        self.button_3 = (self.button_2[0] - 2 * self.button_radius - 10, self.button_2[1])
        self.font = pg.font.SysFont(FONT, 10)

        self.optimal_path = []

    def input_obstacles(self, mouse_down, mouse_up):
        if mouse_down and not self.start and not self.is_on_button(mouse_down):
            self.start = mouse_down
        elif mouse_up and not self.is_on_button(mouse_up):
            self.end = mouse_up
            self.obstacles.append((self.start, (self.start[0], self.end[1]), self.end, (self.end[0], self.start[1])))
            self.start = self.end = None
            if self.target and self.is_obstacle(self.target):
                self.target = None
                print("Target reset because it was on an obstacle.")

    def is_on_button(self, mouse_pos):
        if mouse_pos:
            for button in [self.button_1, self.button_2, self.button_3]:
                if button[0] - self.button_radius <= mouse_pos[0] <= button[0] + self.button_radius and \
                        button[1] - self.button_radius <= mouse_pos[1] <= button[1] + self.button_radius:
                    return True
        return False

    def put_obstacle_on_grid(self):
        self.obstacles.append(((0, 0), (0, 5), (WIDTH, 5), (WIDTH, 0)))
        self.obstacles.append(((0, 0), (0, HEIGHT), (5, HEIGHT), (5, 0)))
        self.obstacles.append(((0, HEIGHT - 5), (0, HEIGHT), (WIDTH, HEIGHT), (WIDTH, HEIGHT - 5)))
        self.obstacles.append(((WIDTH - 5, 0), (WIDTH, 0), (WIDTH, HEIGHT), (WIDTH - 5, HEIGHT)))
        for row in range(self.height):
            for col in range(self.width):
                if self.is_obstacle((row, col)):
                    self.grid[row][col] = 1
                print(f"[{row}][{col}] = {self.grid[row][col]}")

        for row in range(self.height // 10):
            for col in range(self.width // 10):
                print(row, col)
                self.downsized_grid[row][col] = 1 if 1 in self.grid[row * 10: (row + 1) * 10, col * 10: (col + 1) * 10] else 0


    def is_obstacle(self, pos):
        for obstacle in self.obstacles:
            x_range = sorted({point[0] for point in obstacle})
            y_range = sorted({point[1] for point in obstacle})
            if x_range[0] <= pos[0] <= x_range[1] and y_range[0] <= pos[1] <= y_range[1]:
                return True
        return False

    def button_handler(self, mouse_pos):
        if mouse_pos:
            if self.button_1[0] - self.button_radius <= mouse_pos[0] <= self.button_1[0] + self.button_radius and \
                    self.button_1[1] - self.button_radius <= mouse_pos[1] <= self.button_1[1] + self.button_radius:
                self.enable_input = not self.enable_input
            elif self.button_2[0] - self.button_radius <= mouse_pos[0] <= self.button_2[0] + self.button_radius and \
                    self.button_2[1] - self.button_radius <= mouse_pos[1] <= self.button_2[1] + self.button_radius:
                self.enable_pathfinding = not self.enable_pathfinding
            elif self.button_3[0] - self.button_radius <= mouse_pos[0] <= self.button_3[0] + self.button_radius and \
                    self.button_3[1] - self.button_radius <= mouse_pos[1] <= self.button_3[1] + self.button_radius and \
                    not self.enable_input:
                self.enable_targeting = not self.enable_targeting

    def draw_buttons(self):
        for button, text, enabled in [(self.button_1, "input obstacles", self.enable_input),
                                      (self.button_2, "find path", self.enable_pathfinding),
                                      (self.button_3, "enable targeting", self.enable_targeting)]:
            pg.draw.circle(WIN, RED if enabled else GREEN, (button[0], button[1]), self.button_radius)
            WIN.blit(self.font.render(text, 1, BLACK), (button[0] - self.button_radius + 5, button[1] - 5))

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pg.draw.polygon(WIN, BLACK, obstacle)

    def handle_obstacles(self, mouse_down, mouse_up=None):
        if self.enable_map:
            self.button_handler(mouse_down)
            if self.enable_targeting and mouse_down and not self.is_on_button(mouse_down) and not self.is_obstacle(mouse_down):
                self.target = mouse_down
                print(f"target set: {mouse_down}")
                self.enable_targeting = False if self.target else True
            elif self.enable_input:
                self.input_obstacles(mouse_down, mouse_up)
            elif self.enable_pathfinding and self.target:
                start = time()
                print("putting obstacles on grid")
                self.put_obstacle_on_grid()
                start_node = (int(self.amr.x // 10), int(self.amr.y // 10))  # Swap x and y
                print("looking for path")
                path = a_star_search(self.downsized_grid, start_node, (int(self.target[0] // 10), int(self.target[1] // 10)))  # Swap x and y
                self.optimal_path = self.map_path_to_large_grid(path)
                print(f"Time taken: {time() - start} s")
                self.enable_pathfinding = False

    def map_path_to_large_grid(self, path):
        large_grid_path = [(coord[0] * 10 + 5, coord[1] * 10 + 5) for coord in path]
        return large_grid_path

    def draw_large_grid_path(self, large_grid_path):
        for point in large_grid_path:
            pg.draw.line(WIN, (0, 0, 255), (point[0] - 5, point[1] - 5), (point[0] + 5, point[1] + 5), 2)
            pg.draw.line(WIN, (0, 0, 255), (point[0] + 5, point[1] - 5), (point[0] - 5, point[1] + 5), 2)

    def draw(self):
        if self.enable_map:
            self.draw_buttons()
            self.draw_obstacles()
            if self.enable_targeting or self.target:
                mouse_pos = pg.mouse.get_pos() if self.enable_targeting else self.target
                pg.draw.line(WIN, RED, (mouse_pos[0] - 10, mouse_pos[1] - 10), (mouse_pos[0] + 10, mouse_pos[1] + 10), 2)
                pg.draw.line(WIN, RED, (mouse_pos[0] + 10, mouse_pos[1] - 10), (mouse_pos[0] - 10, mouse_pos[1] + 10), 2)
            if self.optimal_path:
                self.draw_large_grid_path(self.optimal_path)
