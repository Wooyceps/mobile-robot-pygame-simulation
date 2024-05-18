import pygame
import math


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AMR simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
AIUT_BLUE = (0, 149, 218)

FPS = 60


class AMR():
    def __init__(self, x=WIDTH // 2, y=HEIGHT // 2):
        self.width, self.height = 50, 75
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle_rad = 0  # angle > 0 => rotated left
        self.color = BLACK
        self.front_color = AIUT_BLUE
        self.lin_speed = 3 # pixels per frame
        self.rot_speed_deg = 1  # degree per frame

    def print_dof(self):
        print(f"x = {round(self.x, 2)}, y = {round(self.y, 2)}, angle = {round(self.angle_rad * 180 / math.pi, 2)}")

    def handle_movement(self, keys):
        if keys[pygame.K_UP]:
            self.move_fwd_bwd(-1)
        if keys[pygame.K_DOWN]:
            self.move_fwd_bwd(1)
        if keys[pygame.K_LEFT]:
            self.rotate(1)
        if keys[pygame.K_RIGHT]:
            self.rotate(-1)

    def move_fwd_bwd(self, direction):
        self.y += self.lin_speed * math.cos(self.angle_rad) * direction
        self.x += self.lin_speed * math.sin(self.angle_rad) * direction
        self.print_dof()

    def rotate(self, direction):
        self.angle_rad += self.rot_speed_deg * math.pi / 180 * direction
        self.print_dof()

    def draw(self):
        # AMR body base
        points = []

        half_diag = math.sqrt((self.height / 2) ** 2 + (self.width / 2) ** 2)
        rect_ang = math.atan2(self.height / 2, self.width / 2)  # from x-axis perspective
        rect_angles = [rect_ang, -rect_ang + math.pi, rect_ang + math.pi, -rect_ang]  # angle to each corner

        for angle in rect_angles:
            y_offset = -1 * half_diag * math.sin(angle + self.angle_rad)
            x_offset = half_diag * math.cos(angle + self.angle_rad)
            points.append((self.x + x_offset, self.y + y_offset))

        pygame.draw.polygon(WIN, self.color, points)

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

        pygame.draw.polygon(WIN, self.front_color, points)

        pygame.display.update()


def draw_simulation(*argv):
    WIN.fill(WHITE)

    for obj in argv:
        obj.draw()


def main():
    pygame.init()
    clock = pygame.time.Clock()

    amr = AMR()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        amr.handle_movement(keys)
        draw_simulation(amr)


if __name__ == "__main__":
    main()