import pygame as pg
import numpy as np
from time import time
from assets import WIDTH, HEIGHT, WIN, BLACK, INTERFACE_HEIGHT, INTERFACE_WIDTH, FONT, GREEN, RED, DARK_GREY, ALARM_YELLOW
from a_star import a_star_search

def draw_large_grid_path(large_grid_path):
    """
    Draw the path on the grid.

    Args:
        large_grid_path (list): List of points representing the path.
    """
    for point in large_grid_path:
        pg.draw.line(WIN, (0, 0, 255), (point[0] - 5, point[1] - 5), (point[0] + 5, point[1] + 5), 2)
        pg.draw.line(WIN, (0, 0, 255), (point[0] + 5, point[1] - 5), (point[0] - 5, point[1] + 5), 2)

def map_path_to_large_grid(path):
    """
    Map the path to the large grid.

    Args:
        path (list): List of points representing the path.

    Returns:
        list: List of points mapped to the large grid.
    """
    return [(coord[0] * 10 + 5, coord[1] * 10 + 5) for coord in path]

class Map:
    """
    Class representing the map.

    Attributes:
        amr (Amr): The AMR object.
        width (int): The width of the map.
        height (int): The height of the map.
        obstacles (list): List of obstacles on the map.
        target (tuple): The target position on the map.
        start (tuple): The start position of the obstacle.
        end (tuple): The end position of the obstacle.
        downsized_grid (np.array): The downsized grid.
        danger_map (np.array): The danger map.
        enable_map (bool): Flag to enable the map.
        enable_input (bool): Flag to enable input.
        enable_pathfinding (bool): Flag to enable pathfinding.
        enable_targeting (bool): Flag to enable targeting.
        button_radius (int): The radius of the button.
        buttons (list): List of buttons.
        font (pg.font): The font used for the buttons.
    """
    def __init__(self, amr):
        """
        Initialize the Map object.

        Args:
            amr (Amr): The AMR object.
        """
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

    def _init_obstacles(self):
        """
        Initialize the obstacles.

        Returns:
            list: List of obstacles.
        """
        return [((0, 0), (0, 5), (WIDTH, 5), (WIDTH, 0)),
                ((0, 0), (0, HEIGHT), (5, HEIGHT), (5, 0)),
                ((0, HEIGHT - 5), (0, HEIGHT), (WIDTH, HEIGHT), (WIDTH, HEIGHT - 5)),
                ((WIDTH - 5, 0), (WIDTH, 0), (WIDTH, HEIGHT), (WIDTH - 5, HEIGHT))]

    def _init_buttons(self):
        """
        Initialize the buttons.

        Returns:
            list: List of buttons.
        """
        button_1 = (WIDTH - INTERFACE_WIDTH - self.button_radius - 10, HEIGHT - INTERFACE_HEIGHT + self.button_radius + 5)
        button_2 = (button_1[0] - 2 * self.button_radius - 10, button_1[1])
        button_3 = (button_2[0] - 2 * self.button_radius - 10, button_2[1])
        button_4 = (button_3[0] - 2 * self.button_radius - 10, button_3[1])
        return [button_1, button_2, button_3, button_4]

    def input_obstacles(self, mouse_down, mouse_up):
        """
        Input the obstacles.

        Args:
            mouse_down (tuple): The position of the mouse when the button is pressed.
            mouse_up (tuple): The position of the mouse when the button is released.
        """
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
        """
        Check if the mouse is on a button.

        Args:
            mouse_pos (tuple): The position of the mouse.

        Returns:
            bool: True if the mouse is on a button, False otherwise.
        """
        return any(self._is_on_button(mouse_pos, button) for button in self.buttons)

    def _is_on_button(self, mouse_pos, button):
        """
        Check if the mouse is on a specific button.

        Args:
            mouse_pos (tuple): The position of the mouse.
            button (tuple): The position of the button.

        Returns:
            bool: True if the mouse is on the button, False otherwise.
        """
        return button[0] - self.button_radius <= mouse_pos[0] <= button[0] + self.button_radius and \
               button[1] - self.button_radius <= mouse_pos[1] <= button[1] + self.button_radius

    def put_obstacle_on_grid(self):
        """
        Put the obstacle on the grid.
        """
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
        """
        Check if a position is an obstacle.

        Args:
            pos (tuple): The position to check.

        Returns:
            bool: True if the position is an obstacle, False otherwise.
        """
        return any(self._is_in_range(pos, obstacle) for obstacle in self.obstacles)

    def _is_in_range(self, pos, obstacle):
        """
        Check if a position is in the range of an obstacle.

        Args:
            pos (tuple): The position to check.
            obstacle (tuple): The obstacle to check against.

        Returns:
            bool: True if the position is in the range of the obstacle, False otherwise.
        """
        x_range = sorted({point[0] for point in obstacle})
        y_range = sorted({point[1] for point in obstacle})
        return x_range[0] <= pos[0] <= x_range[1] and y_range[0] <= pos[1] <= y_range[1]

    def is_danger_zone(self, pos):
        """
        Check if a position is in the danger zone.

        Args:
            pos (tuple): The position to check.

        Returns:
            bool: True if the position is in the danger zone, False otherwise.
        """
        return any(self._is_in_danger_zone(pos, obstacle) for obstacle in self.obstacles)

    def _is_in_danger_zone(self, pos, obstacle):
        """
        Check if a position is in the danger zone of an obstacle.

        Args:
            pos (tuple): The position to check.
            obstacle (tuple): The obstacle to check against.

        Returns:
            bool: True if the position is in the danger zone of the obstacle, False otherwise.
        """
        x_range = sorted({point[0] for point in obstacle})
        y_range = sorted({point[1] for point in obstacle})
        padding = self.amr.half_diag
        return (x_range[0] - padding) <= pos[0] <= (x_range[1] + padding) and \
               (y_range[0] - padding) <= pos[1] <= (y_range[1] + padding)

    def button_handler(self, mouse_pos):
        """
        Handle the button events.

        Args:
            mouse_pos (tuple): The position of the mouse.
        """
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
                        self.amr.buffer = []

    def draw_buttons(self):
        """
        Draw the buttons on the map.
        """
        for button, text, enabled in zip(self.buttons, ["obstacles", "find path", "targeting", "   reset"], [self.enable_input, self.enable_pathfinding, self.enable_targeting, None]):
            pg.draw.circle(WIN, BLACK, (button[0], button[1]), self.button_radius + 2)
            pg.draw.circle(WIN, RED if enabled else GREEN, (button[0], button[1]), self.button_radius)
            WIN.blit(self.font.render(text, 1, BLACK), (button[0] - self.button_radius + 5, button[1] - 8))

    def draw_obstacles(self):
        """
        Draw the obstacles on the map.
        """
        for obstacle in self.obstacles:
            pg.draw.polygon(WIN, DARK_GREY, obstacle)

    def handle_obstacles(self, mouse_down, mouse_up=None):
        """
        Handle the obstacles.

        Args:
            mouse_down (tuple): The position of the mouse when the button is pressed.
            mouse_up (tuple): The position of the mouse when the button is released.
        """
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
                self.amr.buffer = map_path_to_large_grid(path)
                self.amr.target = self.amr.buffer.pop(0)
                print(f"pathfinding a*: {time() - start} s")
                print(self.amr.buffer)
                self.enable_pathfinding = False

    def draw_danger_zones(self):
        """
        Draw the danger zones on the map.
        """
        h_d = self.amr.half_diag
        for obstacle in self.obstacles:
            x = []
            y = []
            for point in obstacle:
                x.append(point[0])
                y.append(point[1])
            zone = ((min(x)-h_d, min(y)-h_d), (min(x)-h_d, max(y)+h_d), (max(x)+h_d, max(y)+h_d), (max(x)+h_d, min(y)-h_d))
            pg.draw.polygon(WIN, ALARM_YELLOW, zone)

    def draw(self):
        """
        Draw the map.
        """
        if self.enable_map:
            self.draw_danger_zones()
            self.draw_obstacles()
            self.draw_buttons()
            if self.enable_targeting or self.target:
                mouse_pos = pg.mouse.get_pos() if self.enable_targeting else self.target
                pg.draw.line(WIN, RED, (mouse_pos[0] - 10, mouse_pos[1] - 10), (mouse_pos[0] + 10, mouse_pos[1] + 10), 2)
                pg.draw.line(WIN, RED, (mouse_pos[0] + 10, mouse_pos[1] - 10), (mouse_pos[0] - 10, mouse_pos[1] + 10), 2)
            if self.amr.buffer:
                draw_large_grid_path(self.amr.buffer)