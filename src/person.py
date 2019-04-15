import logging
import math
import random
import pygame as pg

import g_var
from constant import house_settings, AreaStyle, LocationStyle
from utils import random_positive_negative, sign, gen_pixels


logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


class Person:
    def __init__(self, img, name=None, is_show_name=False, w=None, h=None, step=None,
                 init_x=None, init_y=None, init_vx=None, init_vy=None):
        self.step = step or house_settings['step']
        self.name = name
        self.is_show_name = is_show_name
        self.name_fontstyle = house_settings['player_name_fontstyle']
        self.name_rectstyle = house_settings['player_name_rectstyle']
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
        logger.debug('person apply_rebound init - vx: {} vy: {} vxd: {} vyd: {}'.format(self.vx, self.vy, self.vxd, self.vyd))
        v = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        vd = math.sqrt(self.vxd * self.vxd + self.vyd * self.vyd)
        logger.debug('person apply_rebound calculated - v: {} vd: {}'.format(v, vd))
        self.vx = v * self.vxd / vd
        self.vy = v * self.vyd / vd
        self.vxd = sign(self.vx)
        self.vyd = sign(self.vy)

    def calculate_view(self, layout_location, view_area, target_area):
        view_box = (
            view_area.x,
            view_area.y,
            view_area.x + view_area.width,
            view_area.y + view_area.height,
        )
        target_box = (
            target_area.x,
            target_area.y,
            target_area.x + target_area.width,
            target_area.y + target_area.height,
        )
        overlay_box = (
            max(view_box[0], target_box[0]),
            max(view_box[1], target_box[1]),
            min(view_box[2], target_box[2]),
            min(view_box[3], target_box[3]),
        )

        if overlay_box[0] >= overlay_box[2] or overlay_box[1] >= overlay_box[3]:
            return None, None

        surface_loc = LocationStyle(
            x=overlay_box[0] - view_area.x + layout_location.x,
            y=overlay_box[1] - view_area.y + layout_location.y,
        )
        overlay_area = AreaStyle(
            x=overlay_box[0] - target_area.x,
            y=overlay_box[1] - target_area.y,
            width=overlay_box[2] - overlay_box[0],
            height=overlay_box[3] - overlay_box[1],
        )
        return surface_loc, overlay_area

    def draw_img(self, layout_location, view_area):
        img_area = AreaStyle(
            x=self.x,
            y=self.y,
            width=self.img.get_width(),
            height=self.img.get_height(),
        )

        surface_loc, overlay_area = self.calculate_view(
            layout_location, view_area, img_area)

        if surface_loc and overlay_area:
            g_var.surface.blit(self.img, tuple(surface_loc), tuple(overlay_area))

    def draw_name(self, layout_location, view_area):
        if not self.is_show_name:
            return

        fontstyle = self.name_fontstyle
        # name
        name_font = pg.font.SysFont('arial', fontstyle.fontsize)
        name_surface = name_font.render(self.name, True, fontstyle.color)
        name_area = AreaStyle(
            x=self.x + fontstyle.x,
            y=self.y + fontstyle.y,
            width=name_surface.get_width(),
            height=name_surface.get_height(),
        )
        surface_loc, overlay_area = self.calculate_view(
            layout_location, view_area, name_area
        )
        if surface_loc and overlay_area:
            g_var.surface.blit(name_surface, tuple(surface_loc), tuple(overlay_area))

        # rect
        rectstyle = self.name_rectstyle
        rect_area = AreaStyle(
            x=self.x + rectstyle.x,
            y=self.y + rectstyle.y,
            width=rectstyle.width,
            height=rectstyle.height,
        )
        surface_loc, overlay_area = self.calculate_view(
            layout_location, view_area, rect_area
        )
        if surface_loc and overlay_area:
            rect = pg.Rect(
                surface_loc.x,
                surface_loc.y,
                overlay_area.width,
                overlay_area.height,
            )
            pg.draw.rect(g_var.surface, fontstyle.color, rect, 1)

    def draw(self, layout_location, view_area):
        self.draw_img(layout_location, view_area)
        self.draw_name(layout_location, view_area)
