import pygame as pg
import numpy as np
from time import time
from assets import WIDTH, HEIGHT, WIN, BLACK, INTERFACE_HEIGHT, INTERFACE_WIDTH, FONT, GREEN, RED, DARK_GREY
from a_star import a_star_search


def draw_large_grid_path(large_grid_path):
    for point in large_grid_path:
        pg.draw.line(WIN, (0, 0, 255), (point[0] - 5, point[1] - 5), (point[0] + 5, point[1] + 5), 2)
        pg.draw.line(WIN, (0, 0, 255), (point[0] + 5, point[1] - 5), (point[0] - 5, point[1] + 5), 2)


def map_path_to_large_grid(path):
    return [(coord[0] * 10 + 5, coord[1] * 10 + 5) for coord in path]


class Map:
    def __init__(self, amr):
        self.amr = amr
        self.width = WIDTH
        self.height = HEIGHT
        self.obstacles = self._init_obstacles()
        self.target = None
        self.start = self.end = None
        self.downsized_grid = np.zeros((self.width // 10, self.height // 10))
        self.danger_map = np.zeros((self.width, self.height))
        self.enable_map = True
        self.enable_input = self.enable_pathfinding = self.enable_targeting = False
        self.button_radius = INTERFACE_HEIGHT // 2 - 10
        self.buttons = self._init_buttons()
        self.font = pg.font.SysFont(FONT, 14)
        self.optimal_path = []

    def _init_obstacles(self):
        return [((0, 0), (0, 5), (WIDTH, 5), (WIDTH, 0)),
                ((0, 0), (0, HEIGHT), (5, HEIGHT), (5, 0)),
                ((0, HEIGHT - 5), (0, HEIGHT), (WIDTH, HEIGHT), (WIDTH, HEIGHT - 5)),
                ((WIDTH - 5, 0), (WIDTH, 0), (WIDTH, HEIGHT), (WIDTH - 5, HEIGHT))]

    def _init_buttons(self):
        button_1 = (WIDTH - INTERFACE_WIDTH - self.button_radius - 10, HEIGHT - INTERFACE_HEIGHT + self.button_radius + 5)
        button_2 = (button_1[0] - 2 * self.button_radius - 10, button_1[1])
        button_3 = (button_2[0] - 2 * self.button_radius - 10, button_2[1])
        button_4 = (button_3[0] - 2 * self.button_radius - 10, button_3[1])
        return [button_1, button_2, button_3, button_4]

    def input_obstacles(self, mouse_down, mouse_up):
        if mouse_down and not self.start and not self.is_on_button(mouse_down):
            self.start = mouse_down
        elif mouse_up and not self.is_on_button(mouse_up):
            self.end = mouse_up
            self.obstacles.append((self.start, (self.start[0], self.end[1]), self.end, (self.end[0], self.start[1])))
            self.start = self.end = None
            if self.target and self.is_danger_zone(self.target):
                self.target = None
                print("Target reset because it was in danger zone.")

    def is_on_button(self, mouse_pos):
        return any(self._is_on_button(mouse_pos, button) for button in self.buttons)

    def _is_on_button(self, mouse_pos, button):
        return button[0] - self.button_radius <= mouse_pos[0] <= button[0] + self.button_radius and \
               button[1] - self.button_radius <= mouse_pos[1] <= button[1] + self.button_radius

    def put_obstacle_on_grid(self):
        last = None
        for col in range(self.width):
            for row in range(self.height):
                if self.is_danger_zone((col, row)):
                    self.danger_map[col][row] = 1
                prog = int((col * self.height + row)/(self.width*self.height)*100)
                print(prog, "%") if last != prog else None
                last = prog
        print("100 %")
        for col in range(self.width // 10):
            for row in range(self.height // 10):
                self.downsized_grid[col][row] = 1 if 1 in self.danger_map[col * 10: (col + 1) * 10, row * 10: (row + 1) * 10] else 0

    def is_obstacle(self, pos):
        return any(self._is_in_range(pos, obstacle) for obstacle in self.obstacles)

    def _is_in_range(self, pos, obstacle):
        x_range = sorted({point[0] for point in obstacle})
        y_range = sorted({point[1] for point in obstacle})
        return x_range[0] <= pos[0] <= x_range[1] and y_range[0] <= pos[1] <= y_range[1]

    def is_danger_zone(self, pos):
        return any(self._is_in_danger_zone(pos, obstacle) for obstacle in self.obstacles)

    def _is_in_danger_zone(self, pos, obstacle):
        x_range = sorted({point[0] for point in obstacle})
        y_range = sorted({point[1] for point in obstacle})
        padding = self.amr.half_diag - 15
        return (x_range[0] - padding) <= pos[0] <= (x_range[1] + padding) and \
               (y_range[0] - padding) <= pos[1] <= (y_range[1] + padding)

    def button_handler(self, mouse_pos):
        if mouse_pos:
            for i, button in enumerate(self.buttons):
                if self._is_on_button(mouse_pos, button):
                    if i == 0:
                        self.enable_input = not self.enable_input
                    elif i == 1 and not self.enable_input:
                        self.enable_pathfinding = not self.enable_pathfinding
                    elif i == 2 and not self.enable_input:
                        self.enable_targeting = not self.enable_targeting
                    elif i == 3 and not self.enable_input:
                        self.obstacles = self._init_obstacles()
                        self.target = None
                        self.optimal_path = []

    def draw_buttons(self):
        for button, text, enabled in zip(self.buttons, ["obstacles", "find path", "targeting", "   reset"], [self.enable_input, self.enable_pathfinding, self.enable_targeting, None]):
            pg.draw.circle(WIN, RED if enabled else GREEN, (button[0], button[1]), self.button_radius)
            WIN.blit(self.font.render(text, 1, BLACK), (button[0] - self.button_radius + 5, button[1] - 8))

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pg.draw.polygon(WIN, DARK_GREY, obstacle)

    def handle_obstacles(self, mouse_down, mouse_up=None):
        if self.enable_map:
            self.button_handler(mouse_down)
            if self.enable_targeting and mouse_down and not self.is_on_button(mouse_down) and not self.is_danger_zone(mouse_down):
                self.target = mouse_down
                print(f"target set: {mouse_down}")
                self.enable_targeting = False if self.target else True
            elif self.enable_input:
                self.input_obstacles(mouse_down, mouse_up)
            elif self.enable_pathfinding and self.target:
                start = time()
                self.put_obstacle_on_grid()
                print(f"mapping: {time() - start} s")
                start_node = (int(self.amr.x // 10), int(self.amr.y // 10))
                start = time()
                path = a_star_search(self.downsized_grid, start_node, (int(self.target[0] // 10), int(self.target[1] // 10)))  # Swap x and y
                self.optimal_path = map_path_to_large_grid(path)
                print(f"pathfinding a*: {time() - start} s")
                print(path)
                self.enable_pathfinding = False

    def draw(self):
        if self.enable_map:
            self.draw_obstacles()
            self.draw_buttons()
            if self.enable_targeting or self.target:
                mouse_pos = pg.mouse.get_pos() if self.enable_targeting else self.target
                pg.draw.line(WIN, RED, (mouse_pos[0] - 10, mouse_pos[1] - 10), (mouse_pos[0] + 10, mouse_pos[1] + 10), 2)
                pg.draw.line(WIN, RED, (mouse_pos[0] + 10, mouse_pos[1] - 10), (mouse_pos[0] - 10, mouse_pos[1] + 10), 2)
            if self.optimal_path:
                draw_large_grid_path(self.optimal_path)