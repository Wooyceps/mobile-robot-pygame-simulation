import math
import pygame as pg
from assets import WIDTH, HEIGHT, BLACK, AIUT_BLUE, RED, WIN
from map import Map


class Amr():
    """
    Class representing an Autonomous Mobile Robot (AMR).
    """

    def __init__(self, x=WIDTH // 2, y=HEIGHT // 2):
        """
        Initialize the AMR with default or provided position, and other attributes.
        """
        self.leave_track = True
        self.plan_trajectory = False
        self.width, self.height = 50, 75
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle_rad = 0
        self.color = BLACK
        self.front_color = AIUT_BLUE
        self.lin_speed = 3
        self.rot_speed_deg = 1
        self.coord_memory = []
        self.target = None

    def handle_movement(self, keys, destination):
        """
        Handle the movement of the AMR based on keyboard inputs or destination position.
        """
        self.target = destination if (destination != self.target and destination) else self.target
        if self.plan_trajectory and self.target:
            self.trajectory_planning()
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
        """
        Move the AMR forward or backward based on the direction provided.
        """
        self.y += self.lin_speed * math.cos(self.angle_rad) * direction
        self.x += self.lin_speed * math.sin(self.angle_rad) * direction
        self.coord_memory.append((self.x, self.y))

    def rotate(self, direction):
        """
        Rotate the AMR based on the direction provided.
        """
        self.angle_rad += self.rot_speed_deg * math.pi / 180 * direction
        self.angle_rad %= 2 * math.pi

    def draw_waypoints(self):
        """
        Draw waypoints on the screen for the AMR's path.
        """
        for idx, coords in enumerate(self.coord_memory):
            if idx % 5 == 0:
                pg.draw.circle(WIN, RED, coords, 2)

    def draw(self):
        """
        Draw the AMR on the screen.
        """
        if self.leave_track:
            self.draw_waypoints()

        # AMR body base
        points = []

        half_diag = math.sqrt((self.height / 2) ** 2 + (self.width / 2) ** 2)
        rect_ang = math.atan2(self.height / 2, self.width / 2)
        rect_angles = [rect_ang, -rect_ang + math.pi, rect_ang + math.pi, -rect_ang]

        for angle in rect_angles:
            y_offset = -1 * half_diag * math.sin(angle + self.angle_rad)
            x_offset = half_diag * math.cos(angle + self.angle_rad)
            points.append((self.x + x_offset, self.y + y_offset))

        pg.draw.polygon(WIN, self.color, points)

        # AMR front light feature
        points = []

        half_diag_outer = math.sqrt((self.height / 2) ** 2 + (self.width / 2) ** 2)
        half_diag_inner = math.sqrt((self.height / 2 - 5) ** 2 + (self.width / 2) ** 2)
        rect_ang_outer = math.atan2(self.height / 2, self.width / 2)
        rect_ang_inner = math.atan2(self.height / 2 - 5, self.width / 2)
        rect_angles = [rect_ang_outer, -rect_ang_outer + math.pi, -rect_ang_inner + math.pi, rect_ang_inner]

        for idx, angle in enumerate(rect_angles):
            if idx < 2:
                y_offset = -1 * half_diag_outer * math.sin(angle + self.angle_rad)
                x_offset = half_diag_outer * math.cos(angle + self.angle_rad)
            else:
                y_offset = -1 * half_diag_inner * math.sin(angle + self.angle_rad)
                x_offset = half_diag_inner * math.cos(angle + self.angle_rad)
            points.append((self.x + x_offset, self.y + y_offset))

        pg.draw.polygon(WIN, self.front_color, points)

    def trajectory_planning(self):
        """
        Plan the trajectory of the AMR based on the destination position.
        """
        target_angle_rad = math.atan2(self.x - self.target[0], self.y - self.target[1])
        if target_angle_rad < 0:
            target_angle_rad += 2 * math.pi
        angle_diff_rad = target_angle_rad - self.angle_rad
        if abs(angle_diff_rad) * 180/math.pi > 1:
            if angle_diff_rad < - math.pi or (0 < angle_diff_rad < math.pi):
                self.rotate(1)
            else:
                self.rotate(-1)
        else:
            if math.sqrt((self.x - self.target[0]) ** 2 + (self.y - self.target[1]) ** 2) > 5:
                self.move_fwd_bwd(-1)
            else:
                self.target = None