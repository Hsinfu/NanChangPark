import random
import pygame as pg

import g_var
from constant import connection_settings


class Connection:
    def __init__(self):
        self.connect_num = {}
        self.connects = []

    @staticmethod
    def get_img_color_idx(img, c):
        for hi in range(img.get_height()):
            for wi in range(img.get_width()):
                if img.get_at((wi, hi)) == c:
                    return wi, hi

    def connect(self, p1, p2, max_num=connection_settings['max_num_per_collision']):
        """
            p1 (Person)
            p2 (Person)
            max_num (int, optional, default connection_settings['max_num_per_collision']
        """
        colors = p1.img_colors.intersection(p2.img_colors)
        num = int(random.randrange(max_num))
        for c in random.sample(colors, num):
            p1_coord = self.get_img_color_idx(p1.img, c)
            p2_coord = self.get_img_color_idx(p2.img, c)
            n = self.connect_num.get((p1, p2), 0)
            if n < connection_settings['max_num']:
                self.connects.append((c, p1, p1_coord, p2, p2_coord))
                self.connect_num[(p1, p2)] = n + 1

    def draw(self):
        for c, p1, p1_coord, p2, p2_coord in self.connects:
            position1 = (p1.x + p1_coord[0], p1.y + p1_coord[1])
            position2 = (p2.x + p2_coord[0], p2.y + p2_coord[1])
            line_widht = connection_settings['line_width']
            pg.draw.line(g_var.map_surface, c, position1, position2, width=line_widht)
