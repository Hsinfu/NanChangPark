import layers
from constant import default_speed, default_img_width, default_img_height
from utils import random_positive_negative

class Person:
    def __init__(self, img, w=None, h=None, speed=None,
                 init_x=None, init_y=None, init_vx=None, init_vy=None):
        self.speed = speed or default_speed
        self.init_img(img, w, h)
        self.init_location(init_x, init_y)
        self.init_speed(init_vx, init_vy)

    def random_location(self):
        random_x = random(layers.pg_people.width - self.img.width)
        random_y = random(layers.pg_people.height - self.img.height)
        return random_x, random_y

    def random_speed(self, direction='corners'):
        if direction == 'corners':
            w, h = self.img.width, self.img.height
            l = sqrt(w * w + h * h)
            vx_ratio = w / l
            vy_ratio = h / l
        else:  # random direction
            vx_ratio = random(1)
            vy_ratio = sqrt(1 - vx_ratio * vx_ratio)

        random_vx = self.speed * random_positive_negative() * vx_ratio
        random_vy = self.speed * random_positive_negative() * vy_ratio
        return random_vx, random_vy

    def init_img(self, img, w=None, h=None):
        img_w = w or default_img_width
        img_h = h or default_img_height
        img.resize(img_w, img_h)
        self.img = img

    def init_location(self, init_x=None, init_y=None):
        random_x, random_y = self.random_location()
        self.x = init_x or random_x
        self.y = init_y or random_y
        self.pre_x = self.x
        self.pre_y = self.y

    def init_speed(self, init_vx=None, init_vy=None):
        random_vx, random_vy = self.random_speed()
        self.vx = init_vx or random_vx
        self.vy = init_vy or random_vy
        self.pre_vx = self.vx
        self.pre_vy = self.vy
        self.vx_rebound = False
        self.vy_rebound = False

    def move(self):
        self.pre_x = self.x
        self.pre_y = self.y
        self.pre_vx = self.vx
        self.pre_vy = self.vy
        self.x += self.vx
        self.y += self.vy
        return self.x, self.y

    def set_vx_rebound(self):
        self.vx_rebound = True

    def set_vy_rebound(self):
        self.vy_rebound = True

    def apply_rebound(self):
        if self.vx_rebound:
            self.vx *= -1
            self.vx_rebound = False
        if self.vy_rebound:
            self.vy *= -1
            self.vy_rebound = False
