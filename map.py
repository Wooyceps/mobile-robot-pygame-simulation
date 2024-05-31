import pygame as pg
import numpy as np
from time import time
from assets import WIDTH, HEIGHT, WIN, BLACK, INTERFACE_HEIGHT, INTERFACE_WIDTH, FONT, GREEN, RED


class AStarNode:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = self.h = self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Map:
    def __init__(self, amr):
        self.amr = amr
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = np.zeros((self.height, self.width))
        self.obstacles = []
        self.target = None
        self.start = self.end = None
        self.downsized_grid = []
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
        for row in range(self.height):
            for col in range(self.width):
                if self.is_obstacle((row, col)):
                    self.grid[row][col] = 1
        self.downsized_grid = np.zeros((self.height // 10, self.width // 10))
        for row in range(self.height // 10):
            for col in range(self.width // 10):
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
                self.put_obstacle_on_grid()
                start_node = (int(self.amr.x // 10), int(self.amr.y // 10))  # Swap x and y
                print("looking for path")
                path = self.a_star(start_node, (int(self.target[0] // 10), int(self.target[1] // 10)))  # Swap x and y
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

    def reset_a_star_nodes(self, open_list, closed_list):
        for node in open_list + closed_list:
            node.g = node.h = node.f = 0
            node.parent = None

    def a_star(self, start, end):
        start_node = AStarNode(None, start)  # Swap x and y
        end_node = AStarNode(None, end)  # Swap x and y
        open_list = [start_node]
        closed_list = []

        while open_list:
            current_node = min(open_list, key=lambda node: node.f)
            open_list.remove(current_node)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current:
                    path.append(current.position)
                    current = current.parent

                self.reset_a_star_nodes(open_list, closed_list)  # Reset the nodes

                return path[::-1]

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if not (0 <= node_position[0] < len(self.downsized_grid) and 0 <= node_position[1] < len(
                        self.downsized_grid[0]) and self.downsized_grid[int(node_position[0])][
                            int(node_position[1])] == 0):
                    continue

                new_node = AStarNode(current_node, node_position)
                children.append(new_node)

            for child in children:
                if child in closed_list:
                    continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                if any(child == open_node and child.g > open_node.g for open_node in open_list):
                    continue

                open_list.append(child)