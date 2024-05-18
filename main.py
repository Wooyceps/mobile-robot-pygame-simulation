import pygame
import math


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AMR simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5  # pixels or degrees


class AMR():
    def __init__(self, x=WIDTH // 2, y=HEIGHT // 2):
        self.width, self.height = 50, 75
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle_rad = 0  # angle > 0 => rotated left
        self.color = WHITE
        self.lin_speed = VEL
        self.rot_speed_deg = 0.5

    def handle_movement(self, keys):
        if keys[pygame.K_UP]:
            print("K_UP")
            self.move_fwd_bwd(1)
        if keys[pygame.K_DOWN]:
            self.move_fwd_bwd(-1)
        if keys[pygame.K_LEFT]:
            self.rotate(1)
        if keys[pygame.K_RIGHT]:
            self.rotate(-1)

    def move_fwd_bwd(self, direction):
        self.y += self.lin_speed * math.cos(self.angle_rad) * direction
        self.x += self.lin_speed * math.sin(self.angle_rad) * direction
        print(f"self.x = {self.x}, self.y = {self.y}")

    def rotate(self, direction):
        self.angle_rad += self.rot_speed_deg * math.pi / 180 * direction
        print(f"current angle: {self.angle_rad * 180 / math.pi} [deg], {self.angle_rad} [rad]")

    def draw(self):
        WIN.fill(BLACK)
        # rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(WIN, self.color, rect)
        self.draw_rectangle()
        pygame.display.update()

    def draw_rectangle(self):
        points = []
        half_diag = math.sqrt((self.height / 2) ** 2 + (self.width / 2) ** 2)

        rect_ang = math.atan2(self.height / 2, self.width / 2)  # from x-axis perspective

        rect_angles = [rect_ang, -rect_ang + math.pi, rect_ang + math.pi, -rect_ang]  # angle to each corner

        # Calculate the coordinates of each point.
        for angle in rect_angles:
            y_offset = -1 * half_diag * math.sin(angle + self.angle_rad)
            x_offset = half_diag * math.cos(angle + self.angle_rad)
            points.append((self.x + x_offset, self.y + y_offset))

        pygame.draw.polygon(WIN, self.color, points)


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
        amr.draw()


if __name__ == "__main__":
    main()

# rotated_amr = pygame.transform.rotate(amr, amr.angle)
# WIN.blit(rotated_amr, amr)
