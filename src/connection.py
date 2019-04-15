import random
import pygame as pg
import numpy as np

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
                self.connects.append((pg.Color(*c), p1, p1_coord, p2, p2_coord))
                self.connect_num[(p1, p2)] = n + 1

    def draw(self, layout_location, view_area):
        area = view_area
        for c, p1, p1_coord, p2, p2_coord in self.connects:

            positions = [
                [p1.x + p1_coord[0], p1.y + p1_coord[1]],
                [p2.x + p2_coord[0], p2.y + p2_coord[1]],
            ]
            x_min = min(positions[0][0], positions[1][0])
            x_max = max(positions[0][0], positions[1][0])
            y_min = min(positions[0][1], positions[1][1])
            y_max = max(positions[0][1], positions[1][1])

            if x_max < area.x or x_min > area.x + area.width:
                continue

            if y_max < area.y or y_min > area.y + area.height:
                continue

            A = np.array(positions)
            B = np.array([1, 1])
            a, b = np.linalg.solve(A, B)

            def gen():
                x = area.x
                y = (1 - a * x) / b
                if y > y_min and y < y_max:
                    yield (x, y)

                x = area.x + area.width
                y = (1 - a * x) / b
                if y > y_min and y < y_max:
                    yield (x, y)

                y = area.y
                x = (1 - b * y) / a
                if x > x_min and x < x_max:
                    yield (x, y)

                y = area.y + area.height
                x = (1 - b * y) / a
                if x > x_min and x < x_max:
                    yield (x, y)

            new_positions = list(gen())
            # print('new_positions', new_positions)

            def merge_gen():
                new_idx = 0
                for p in positions:
                    if p[0] > area.x and p[0] < area.x + area.width and p[1] > area.y and p[1] < area.y + area.height:
                        yield p
                    else:
                        yield new_positions[new_idx]
                        new_idx += 1

            def post_processing():
                for p in merge_gen():
                    yield (p[0] - area.x + layout_location.x, p[1] - area.y + layout_location.y)

            final_positions = list(post_processing())
            # print('final_positions', final_positions)
            line_widht = connection_settings['line_width']
            pg.draw.line(g_var.surface, c, final_positions[0], final_positions[1], line_widht)
