import math
import pygame as pg
from assets import WIDTH, HEIGHT, BLACK, AIUT_BLUE, GREY, INTERFACE_WIDTH, INTERFACE_HEIGHT, WIN


class Interface():

    def __init__(self, amr: object):
        """
        Initialize the interface with the provided AMR object.
        :param amr: object
        """
        self.amr = amr
        self.width, self.height = INTERFACE_WIDTH, INTERFACE_HEIGHT
        self.x, self.y = WIDTH - INTERFACE_WIDTH, HEIGHT - INTERFACE_HEIGHT
        self.font = pg.font.SysFont('arial', 20)
        self.fill_color = GREY

    def draw(self):
        """
        Draw the interface on the screen.
        """
        pg.draw.rect(WIN, self.fill_color, (self.x, self.y, self.width, self.height))

        x_text = self.font.render(
            "X: " + str(round(self.amr.x, 2)), 1, BLACK)
        y_text = self.font.render(
            "Y: " + str(round(self.amr.y, 2)), 1, BLACK)
        angle_text = self.font.render(
            "Angle: " + str(round(math.degrees(self.amr.angle_rad), 2)), 1, BLACK)
        WIN.blit(x_text, (self.x + 10, self.y + 10))
        WIN.blit(y_text, (self.x + 90, self.y + 10))
        WIN.blit(angle_text, (self.x + 10, self.y + x_text.get_height() + 20))
