import math
import pygame as pg
from main import WIN, WIDTH, HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
AIUT_BLUE = (0, 149, 218)


class AMR():
    def __init__(self, x=WIDTH // 2, y=HEIGHT // 2):
        self.width, self.height = 50, 75
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle_rad = 0  # angle > 0 => rotated left
        self.color = BLACK
        self.front_color = AIUT_BLUE
        self.lin_speed = 3 # pixels per frame
        self.rot_speed_deg = 1  # degree per frame
        self.leave_track = False
        self.coord_memory = []
        self.plan_trajectory = False
        self.target = None

    def print_dof(self):
        print(f"x = {round(self.x, 2)}, y = {round(self.y, 2)}, angle = {round(self.angle_rad * 180 / math.pi, 2)}")

    def handle_movement(self, keys, mouse):
        if mouse:
            self.plan_trajectory = True
        if self.plan_trajectory:
            self.trajectory_planning(mouse)
        else:
            if keys[pg.K_UP]:
                self.move_fwd_bwd(-1)
            if keys[pg.K_DOWN]:
                self.move_fwd_bwd(1)
            if keys[pg.K_LEFT]:
                self.rotate(1)
            if keys[pg.K_RIGHT]:
                self.rotate(-1)

    def move_fwd_bwd(self, direction):
        self.y += self.lin_speed * math.cos(self.angle_rad) * direction
        self.x += self.lin_speed * math.sin(self.angle_rad) * direction
        self.print_dof()
        self.coord_memory.append((self.x, self.y))

    def rotate(self, direction):
        self.angle_rad += self.rot_speed_deg * math.pi / 180 * direction
        self.angle_rad %= 2 * math.pi
        self.print_dof()

    def draw_waypoints(self):
        for idx, coords in enumerate(self.coord_memory):
            if idx % 5 == 0:
                pg.draw.circle(WIN, RED, coords, 2)

    def draw(self):
        if self.leave_track:
            self.draw_waypoints()

        # AMR body base
        points = []

        half_diag = math.sqrt((self.height / 2) ** 2 + (self.width / 2) ** 2)
        rect_ang = math.atan2(self.height / 2, self.width / 2)  # from x-axis perspective
        rect_angles = [rect_ang, -rect_ang + math.pi, rect_ang + math.pi, -rect_ang]  # angle to each corner

        for angle in rect_angles:
            y_offset = -1 * half_diag * math.sin(angle + self.angle_rad)
            x_offset = half_diag * math.cos(angle + self.angle_rad)
            points.append((self.x + x_offset, self.y + y_offset))

        pg.draw.polygon(WIN, self.color, points)

        # AMR front light feature
        points = []

        half_diag_outer = math.sqrt((self.height / 2) ** 2 + (self.width / 2) ** 2)
        half_diag_inner = math.sqrt((self.height / 2 - 5) ** 2 + (self.width / 2) ** 2)
        rect_ang_outer = math.atan2(self.height / 2, self.width / 2)  # from x-axis perspective
        rect_ang_inner = math.atan2(self.height / 2 - 5, self.width / 2)  # from x-axis perspective
        rect_angles = [rect_ang_outer, -rect_ang_outer + math.pi, -rect_ang_inner + math.pi, rect_ang_inner]  # angle to each corner

        for idx, angle in enumerate(rect_angles):
            if idx < 2:
                y_offset = -1 * half_diag_outer * math.sin(angle + self.angle_rad)
                x_offset = half_diag_outer * math.cos(angle + self.angle_rad)
            else:
                y_offset = -1 * half_diag_inner * math.sin(angle + self.angle_rad)
                x_offset = half_diag_inner * math.cos(angle + self.angle_rad)
            points.append((self.x + x_offset, self.y + y_offset))

        pg.draw.polygon(WIN, self.front_color, points)

    def trajectory_planning(self, mouse):
        if mouse:
            self.target = mouse
        target_angle_rad = math.atan2(self.x - self.target[0], self.y - self.target[1])
        if target_angle_rad < 0:
            target_angle_rad += 2 * math.pi
        angle_diff_rad = target_angle_rad - self.angle_rad # angular distance to cover
        print(f"target_angle = {round(target_angle_rad * 180 / math.pi, 2)}, angle_diff = {round(angle_diff_rad * 180 / math.pi, 2)}")
        if abs(angle_diff_rad * 180/math.pi) > 1:
            if angle_diff_rad > 0:
                self.rotate(1)
            else:
                self.rotate(-1)
        else:
            self.plan_trajectory = False