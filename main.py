import pygame as pg
import math
import AMR

WIDTH, HEIGHT = 900, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AMR simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
AIUT_BLUE = (0, 149, 218)

FPS = 60


def draw_simulation(*argv):
    WIN.fill(WHITE)

    for obj in argv:
        obj.draw()

    pg.display.update()


def main():
    pg.init()
    clock = pg.time.Clock()

    amr = AMR.AMR()

    run = True
    while run:
        clock.tick(FPS)
        mouse = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = (event.pos[0], event.pos[1])

        keys = pg.key.get_pressed()
        amr.handle_movement(keys, mouse)
        draw_simulation(amr)


if __name__ == "__main__":
    main()
