import pygame as pg
import AMR
from interface import Interface
from assets import WHITE, WIN


pg.display.set_caption("AMR simulation")

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
    interface = Interface(amr)

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
        draw_simulation(amr, interface)


if __name__ == "__main__":
    main()
