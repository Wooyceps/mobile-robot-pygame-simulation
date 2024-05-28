import pygame as pg
from AMR import Amr
from interface import Interface
from map import Map
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

    amr = Amr()
    interface = Interface(amr)
    map = Map()

    run = True
    while run:
        clock.tick(FPS)
        mouse_down = None
        mouse_up = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = (event.pos[0], event.pos[1])
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_up = (event.pos[0], event.pos[1])

        keys = pg.key.get_pressed()
        amr.handle_movement(keys, mouse_down)
        amr.map.draw_obstacles(mouse_down, mouse_up)
        draw_simulation(amr, interface)


if __name__ == "__main__":
    main()
