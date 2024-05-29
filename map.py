from assets import WIDTH, HEIGHT, WIN, BLACK, INTERFACE_HEIGHT, INTERFACE_WIDTH, FONT, GREEN, RED
import pygame as pg
import numpy as np
from time import time


class AStarNode:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Map:

    def __init__(self, amr):
        self.enable_map = True
        self.enable_input = False
        self.enable_pathfinding = False
        self.enable_targeting = False
        self.amr = amr
        self.width = WIDTH
        self.height = HEIGHT
        self.grid = np.zeros((self.height, self.width))
        self.start = None
        self.end = None
        self.downsized_grid = []
        self.obstacles = []
        self.button_radius = INTERFACE_HEIGHT // 2 - 10
        self.button_1 = (WIDTH - INTERFACE_WIDTH - self.button_radius - 10, HEIGHT - INTERFACE_HEIGHT + self.button_radius + 5)
        self.button_2 = (self.button_1[0] - 2 * self.button_radius - 10, self.button_1[1])
        self.button_3 = (self.button_2[0] - 2 * self.button_radius - 10, self.button_2[1])
        self.font = pg.font.SysFont(FONT, 10)
        self.target = None

    def input_obstacles(self, mouse_down, mouse_up):
        """
        Input obstacles on the map by making.
        :param mouse_down:
        :param mouse_up:
        :return:
        """
        if mouse_down and not self.start:
            if not self.is_on_button(mouse_down):
                self.start = mouse_down
        elif mouse_up:
            if not self.is_on_button(mouse_up):
                self.end = mouse_up
                self.obstacles.append(
                    (self.start, (self.start[0], self.end[1]), self.end, (self.end[0], self.start[1])))
                self.start = None
                self.end = None

    def is_on_button(self, mouse_pos):
        if mouse_pos:
            if self.button_1[0] - self.button_radius <= mouse_pos[0] <= self.button_1[0] + self.button_radius and \
                    self.button_1[1] - self.button_radius <= mouse_pos[1] <= self.button_1[1] + self.button_radius:
                return True
            elif self.button_2[0] - self.button_radius <= mouse_pos[0] <= self.button_2[0] + self.button_radius and \
                    self.button_2[1] - self.button_radius <= mouse_pos[1] <= self.button_2[1] + self.button_radius:
                return True
            elif self.button_3[0] - self.button_radius <= mouse_pos[0] <= self.button_3[0] + self.button_radius and \
                    self.button_3[1] - self.button_radius <= mouse_pos[1] <= self.button_3[1] + self.button_radius:
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
                if 1 in self.grid[row * 10: (row + 1) * 10, col * 10: (col + 1) * 10]:
                    self.downsized_grid[row][col] = 1
                else:
                    self.downsized_grid[row][col] = 0

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
        if mouse_pos:
            if self.button_1[0] - self.button_radius <= mouse_pos[0] <= self.button_1[0] + self.button_radius and \
                    self.button_1[1] - self.button_radius <= mouse_pos[1] <= self.button_1[1] + self.button_radius:
                self.enable_input = not self.enable_input
            elif self.button_2[0] - self.button_radius <= mouse_pos[0] <= self.button_2[0] + self.button_radius and \
                    self.button_2[1] - self.button_radius <= mouse_pos[1] <= self.button_2[1] + self.button_radius:
                self.enable_pathfinding = not self.enable_pathfinding
            elif self.button_3[0] - self.button_radius <= mouse_pos[0] <= self.button_3[0] + self.button_radius and \
                    self.button_3[1] - self.button_radius <= mouse_pos[1] <= self.button_3[1] + self.button_radius:
                self.enable_targeting = not self.enable_targeting

    def draw_buttons(self):
        if not self.enable_input:
            pg.draw.circle(WIN, GREEN, (self.button_1[0], self.button_1[1]), self.button_radius)
            WIN.blit(self.font.render(
                "input obstacles", 1, BLACK), (self.button_1[0] - self.button_radius + 5, self.button_1[1] - 5))
        else:
            pg.draw.circle(WIN, RED, (self.button_1[0], self.button_1[1]), self.button_radius)
            WIN.blit(self.font.render(
                "stop input", 1, BLACK), (self.button_1[0] - self.button_radius + 5, self.button_1[1] - 5))
        if not self.enable_pathfinding:
            pg.draw.circle(WIN, GREEN, (self.button_2[0], self.button_2[1]), self.button_radius)
            WIN.blit(self.font.render(
                "find path", 1, BLACK), (self.button_2[0] - self.button_radius + 5, self.button_2[1] - 5))
        else:
            pg.draw.circle(WIN, RED, (self.button_2[0], self.button_2[1]), self.button_radius)
            WIN.blit(self.font.render(
                "stop", 1, BLACK), (self.button_2[0] - self.button_radius + 5, self.button_2[1] - 5))
        if not self.enable_targeting:
            pg.draw.circle(WIN, GREEN, (self.button_3[0], self.button_3[1]), self.button_radius)
            WIN.blit(self.font.render(
                "enable targeting", 1, BLACK), (self.button_3[0] - self.button_radius + 5, self.button_3[1] - 5))
        else:
            pg.draw.circle(WIN, RED, (self.button_3[0], self.button_3[1]), self.button_radius)
            WIN.blit(self.font.render(
                "disable targeting", 1, BLACK), (self.button_3[0] - self.button_radius + 5, self.button_3[1] - 5))

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pg.draw.polygon(WIN, BLACK, obstacle)

    def handle_obstacles(self, mouse_down, mouse_up=None):
        self.button_handler(mouse_down)
        if self.enable_targeting:
            if mouse_down is not None:
                if not self.is_on_button(mouse_down) and not self.is_obstacle(mouse_down):
                    self.target = mouse_down
                    print("target set")
                    self.enable_targeting = False if self.target else True
                elif self.is_obstacle(mouse_down):
                    print("Target is on an obstacle.")
        elif self.enable_input:
            self.input_obstacles(mouse_down, mouse_up)
        elif self.enable_pathfinding:
            if self.target is not None:
                start = time()
                self.put_obstacle_on_grid()
                path = self.a_star((int(self.target[1] // 10), int(self.target[0] // 10)))
                print(f"Time taken: {time() - start} s")
                self.enable_pathfinding = False
            else:
                print("Target is not set yet.")

    def draw(self):
        if self.enable_map:
            self.draw_buttons()
            self.draw_obstacles()

    def a_star(self, end):
        start_node = AStarNode(None, (self.amr.y // 10, self.amr.x // 10))
        end_node = AStarNode(None, end)

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if node_position[0] > (len(self.downsized_grid) - 1) or node_position[0] < 0 or node_position[1] > (len(self.downsized_grid[len(self.downsized_grid)-1]) -1) or node_position[1] < 0:
                    continue

                if self.downsized_grid[int(node_position[0])][int(node_position[1])] != 0:
                    continue

                new_node = AStarNode(current_node, node_position)
                children.append(new_node)

            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)


