import math
import random
import pygame as pg

from constant import house_settings
from utils import random_positive_negative, sign, gen_pixels


class Person:
    def __init__(self, img, w=None, h=None, step=None,
                 init_x=None, init_y=None, init_vx=None, init_vy=None):
        self.step = step or house_settings['step']
        self.init_img(img, w, h)
        self.init_location(init_x, init_y)
        self.init_step(init_vx, init_vy)

    def random_location(self):
        map_size = house_settings['map_size']
        random_x = random.random() * (map_size.width - self.img.get_width())
        random_y = random.random() * (map_size.height - self.img.get_height())
        return random_x, random_y

    def random_step(self, direction='corners'):
        if direction == 'corners':
            vx_ratio = 1 / math.sqrt(2)
            vy_ratio = 1 / math.sqrt(2)
        else:  # random direction
            vx_ratio = random.random()
            vy_ratio = math.sqrt(1 - vx_ratio * vx_ratio)

        random_vx = self.step * random_positive_negative() * vx_ratio
        random_vy = self.step * random_positive_negative() * vy_ratio
        return random_vx, random_vy

    def init_img(self, img, w=None, h=None):
        img_size = house_settings['img_size']
        img_w = w or img_size.width
        img_h = h or img_size.height
        self.img = pg.transform.scale(img, (img_w, img_h))
        self.img_colors = set(gen_pixels(self.img))

    def init_location(self, init_x=None, init_y=None):
        random_x, random_y = self.random_location()
        self.x = init_x or random_x
        self.y = init_y or random_y
        self.pre_x = self.x
        self.pre_y = self.y

    def init_step(self, init_vx=None, init_vy=None):
        random_vx, random_vy = self.random_step()
        self.vx = init_vx or random_vx
        self.vy = init_vy or random_vy
        self.vxd = sign(self.vx)
        self.vyd = sign(self.vy)

    @property
    def is_rebounded(self):
        return self.vxd != sign(self.vx) or self.vyd != sign(self.vy)

    def move(self):
        self.pre_x = self.x
        self.pre_y = self.y
        self.x += self.vx
        self.y += self.vy
        return self.x, self.y

    def apply_rebound(self):
        print('p: ', self.vx, self.vy, self.vxd, self.vyd)
        v = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        vd = math.sqrt(self.vxd * self.vxd + self.vyd * self.vyd)
        print('v vd:', v, vd)
        self.vx = v * self.vxd / vd
        self.vy = v * self.vyd / vd
        self.vxd = sign(self.vx)
        self.vyd = sign(self.vy)
