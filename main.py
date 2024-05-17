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
        self.width, self.height = 50, 50
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.angle = 0  # angle > 0 => rotated left
        self.color = WHITE
        self.lin_speed = VEL
        self.rot_speed = VEL

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
        self.y += self.lin_speed * math.cos(self.angle) * direction
        self.x += self.lin_speed * math.sin(self.angle) * direction
        print(f"self.x = {self.x}, self.y = {self.y}")

    def rotate(self, direction):
        self.angle += self.rot_speed * 180 / math.pi * direction

    def draw(self):
        WIN.fill(BLACK)
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(WIN, self.color, rect)
        pygame.display.update()


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
