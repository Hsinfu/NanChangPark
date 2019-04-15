import copy
import math
import logging
import pygame as pg

import g_var
from clock import Clock
from connection import Connection
from constant import house_settings
from person import Person
from utils import (
    sign,
    get_img,
    get_map_img,
    get_player_img,
    get_wall,
    get_available_imgs_fpath,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


def get_box(p):
    return {
        'top': p.y + p.img.get_height(),
        'bottom': p.y,
        'left': p.x,
        'right': p.x + p.img.get_width(),
    }


def is_intersect(p1, p2):
    r1, r2 = get_box(p1), get_box(p2)
    return not (
        r1['right'] < r2['left'] or
        r1['left'] > r2['right'] or
        r1['top'] < r2['bottom'] or
        r1['bottom'] > r2['top']
    )


def is_intersect_map(p, wall):
    b = get_box(p)
    for wi in range(math.floor(b['left']), math.ceil(b['right'])):
        for hi in range(math.floor(b['bottom']), math.ceil(b['top'])):
            try:
                if wall[wi][hi] == 1:
                    return True
            except Exception:
                print('is_intersect_map', wi, hi)
            # if wall[wi][hi] == 1:
            #     return True
    return False


def get_v_rebound(p1, p2):
    # return p1_vxd, p2_vxd, p1_vyd, p2_vyd
    if p1.pre_x > p2.pre_x:
        x_dist = p1.pre_x - p2.pre_x - p2.img.get_width()
    else:
        x_dist = p2.pre_x - p1.pre_x - p1.img.get_width()

    if p1.pre_y > p2.pre_y:
        y_dist = p1.pre_y - p2.pre_y - p2.img.get_height()
    else:
        y_dist = p2.pre_y - p1.pre_y - p1.img.get_height()

    if x_dist < 0 and y_dist < 0:
        print('Error: get_v_rebound both dist < 0')
        # print('p1 (pre_x: {}, pre_y: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p1.pre_x, p1.pre_y, p1.x, p1.y, p1.vx, p1.vy))
        # print('p2 (pre_x: {}, pre_y: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p2.pre_x, p2.pre_y, p2.x, p2.y, p2.vx, p2.vy))

    if x_dist < 0:
        return sign(p1.vx), sign(p2.vx), -1 * sign(p1.vy), -1 * sign(p2.vy)

    if y_dist < 0:
        return -1 * sign(p1.vx), -1 * sign(p2.vx), sign(p1.vy), sign(p2.vy)

    x_step = abs(p1.vx - p2.vx)
    y_step = abs(p1.vy - p2.vy)

    if x_step == 0:
        return sign(p1.vx), sign(p2.vx), -1 * sign(p1.vy), -1 * sign(p2.vy)
    if y_step == 0:
        return -1 * sign(p1.vx), -1 * sign(p2.vx), sign(p1.vy), sign(p2.vy)

    x_time = x_dist / x_step
    y_time = y_dist / y_step

    # print('get_v_rebound both dist >= 0')
    # print('p1 (pre_x: {}, pre_y: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p1.pre_x, p1.pre_y, p1.x, p1.y, p1.vx, p1.vy))
    # print('p2 (pre_x: {}, pre_y: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p2.pre_x, p2.pre_y, p2.x, p2.y, p2.vx, p2.vy))
    if x_time > y_time:
        return -1 * sign(p1.vx), -1 * sign(p2.vx), sign(p1.vy), sign(p2.vy)
    return sign(p1.vx), sign(p2.vx), -1 * sign(p1.vy), -1 * sign(p2.vy)


def get_v_rebound_map(p, wall):
    # print('p (pre_x: {}, pre_y: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p.pre_x, p.pre_y, p.x, p.y, p.vx, p.vy))

    b = get_box(p)

    def get_w_overlap(t='left'):
        w_range = range(math.floor(b['left']), math.ceil(b['right']))

        if t == 'right':
            w_range = reversed(w_range)

        for wi in w_range:
            for hi in range(math.floor(b['bottom']), math.ceil(b['top'])):
                if wall[wi][hi] == 1:
                    return wi

    def get_h_overlap(t='bottom'):
        h_range = range(math.floor(b['bottom']), math.ceil(b['top']))
        if t == 'top':
            h_range = reversed(h_range)

        for hi in h_range:
            for wi in range(math.floor(b['left']), math.ceil(b['right'])):
                if wall[wi][hi] == 1:
                    return hi

    x_collision = get_w_overlap('left') if p.vx > 0 else get_w_overlap('right')
    y_collision = get_h_overlap('bottom') if p.vy > 0 else get_h_overlap('top')

    # print('collision', x_collision, y_collision)

    if p.vx > 0:
        x_dist = x_collision - (p.pre_x + p.img.get_width())
    else:
        x_dist = p.pre_x - x_collision

    if p.vy > 0:
        y_dist = y_collision - (p.pre_y + p.img.get_height())
    else:
        y_dist = p.pre_y - y_collision

    if x_dist < 0 and y_dist < 0:
        print('both dist < 0 -> pre: ({}, {}), collision: ({}, {}), dist: ({}, {}))'.format(p.pre_x, p.pre_y, x_collision, y_collision, x_dist, y_dist))
        return -1 * sign(p.vx), -1 * sign(p.vy)

    if x_dist < 0:
        return sign(p.vx), -1 * sign(p.vy)

    if y_dist < 0:
        return -1 * sign(p.vx), sign(p.vy)

    x_time = x_dist / abs(p.vx)
    y_time = y_dist / abs(p.vy)

    print('both dist >= 0 -> pre: ({}, {}), collision: ({}, {}), dist: ({}, {}), time: ({}, {})'.format(p.pre_x, p.pre_y, x_collision, y_collision, x_dist, y_dist, x_time, y_time))

    if x_time > y_time:
        return -1 * sign(p.vx), sign(p.vy)
    return sign(p.vx), -1 * sign(p.vy)


class House:
    def __init__(self, levelX, player_name):
        self.frame_idx = 0
        self.player_name = player_name
        self._player = None
        self.people = []
        self.ppl_imgs_fpath = []
        self.connection = Connection()
        self._bottom_img = None
        self._map_wall = None
        self._player_wall = None
        self.house_setting = copy.deepcopy(house_settings[levelX])
        self.levelX = levelX
        self.delay_clock = None
        self.game_clock = Clock(self.house_setting['game_time'])
        self.add_person_max_retry = self.house_setting['add_person_max_retry']
        self.load_people()
        self.shake = False

    @property
    def bottom_img(self):
        if self._bottom_img is None:
            self._bottom_img = get_map_img('house/bottom.png')
        return self._bottom_img

    @property
    def is_delay(self):
        return False if self.delay_clock is None else True

    @property
    def player_wall(self):
        if self._player_wall is None:
            self._player_wall = get_wall('{}/player_map.png'.format(self.levelX))
        return self._player_wall

    @property
    def map_wall(self):
        if self._map_wall is None:
            self._map_wall = get_wall('house/map.png')
        return self._map_wall

    @property
    def player(self):
        if self._player is None:
            self._player = self.get_player()
        return self._player

    def get_player(self):
        img_area = self.house_setting['player_img_area']
        try:
            img_size = [img_area.width, img_area.height]
            player_img = get_player_img(self.player_name, img_size)
            return Person(
                img=player_img,
                name=self.player_name,
                is_show_name=True,
                w=img_area.width,
                h=img_area.height,
                init_x=img_area.x,
                init_y=img_area.y)
        except Exception:
            return None

    def load_people(self):
        def is_available(p):
            return p['added'] is False and p['frame_idx'] <= self.frame_idx

        ppl = list(filter(is_available, self.house_setting['people']))
        imgs_fpath = get_available_imgs_fpath(len(ppl), self.ppl_imgs_fpath)

        for p, img_fpath in zip(ppl, imgs_fpath):
            img = get_img(img_fpath)
            if p['img_size'] is None:
                w, h = None, None
            else:
                w, h = tuple(p['img_size'])
            if p['img_location'] is None:
                init_x, init_y = None, None
            else:
                init_x, init_y = tuple(p['img_location'])
            person = Person(img=img, w=w, h=h, init_x=init_x, init_y=init_y)
            p['added'] = self.add_person(person, img_fpath, max_retry=self.add_person_max_retry)

    def is_overley_player(self, p):
        if self.player is None:
            return False
        return is_intersect(self.player, p)

    def is_overlap_current_people(self, p):
        for pi in self.people:
            if is_intersect(p, pi):
                return True
        return False

    def is_overlap_wall(self, p, wall=None):
        return is_intersect_map(p, wall or self.map_wall)

    def check_init_location_ok(self, p):
        if self.is_overley_player(p):
            return False
        if self.is_overlap_current_people(p):
            return False
        if self.is_overlap_wall(p):
            return False
        return True

    def add_person(self, p, img_fpath, max_retry=1000):
        for retry_i in range(max_retry):
            if self.check_init_location_ok(p):
                self.people.append(p)
                self.ppl_imgs_fpath.append(img_fpath)
                return True
            else:
                logger.info('retry add_person {} times'.format(retry_i))
                p.init_location()
        logger.error('add_person failed!!')
        return False

    def move(self):
        if self.player:
            self.player.move()
        for p in self.people:
            p.move()

    def _hit_rebound_people(self, p, people, should_connect=False):
        for pi in people:
            if is_intersect(p, pi):
                self.shake = should_connect
                p.vxd, pi.vxd, p.vyd, pi.vyd = get_v_rebound(p, pi)
                if should_connect:
                    self.connection.connect(p, pi)

    def hit_rebound_player(self):
        if self.player is None:
            return
        self._hit_rebound_people(self.player, self.people, should_connect=True)

    def hit_rebound_people(self):
        people = [p for p in self.people]
        while len(people) > 0:
            p = people.pop()
            self._hit_rebound_people(p, people)

    def _hit_rebound_wall(self, p, wall):
        if self.is_overlap_wall(p, wall):
            p.vxd, p.vyd = get_v_rebound_map(p, wall)

    def hit_rebound_wall(self):
        if self.player:
            self._hit_rebound_wall(self.player, self.player_wall or self.map_wall)
        for p in self.people:
            self._hit_rebound_wall(p, self.map_wall)

    def apply_rebound(self):
        if self.player:
            self.player.apply_rebound()
        for p in self.people:
            p.apply_rebound()

    def set_delay_clock(self):
        if self.delay_clock:
            self.shake = False
            logger.info('delay_clock: {}'.format(self.delay_clock.time_left))
            if self.delay_clock.is_timeout():
                self.delay_clock = None
            else:
                self.delay_clock.tick()
        else:
            if self.shake:
                self.delay_clock = Clock(self.house_setting['hit_delay'], enabled=True)

    def set_player_dictection(self, keyboard):
        if self.player is None:
            return

        # skip while it need rebound or delay_clock exists
        if self.delay_clock or self.player.is_rebounded:
            return

        # if no key pressed return
        if keyboard.is_pressed(pg.K_LEFT) == keyboard.is_pressed(pg.K_RIGHT) and keyboard.is_pressed(pg.K_DOWN) == keyboard.is_pressed(pg.K_UP):
            return

        # x direction
        elif keyboard.is_pressed(pg.K_LEFT) and not keyboard.is_pressed(pg.K_RIGHT):
            self.player.vxd = -1
        elif not keyboard.is_pressed(pg.K_LEFT) and keyboard.is_pressed(pg.K_RIGHT):
            self.player.vxd = 1
        else:
            self.player.vxd = 0

        # y direction
        if keyboard.is_pressed(pg.K_DOWN) and not keyboard.is_pressed(pg.K_UP):
            self.player.vyd = 1
        elif not keyboard.is_pressed(pg.K_DOWN) and keyboard.is_pressed(pg.K_UP):
            self.player.vyd = -1
        else:
            self.player.vyd = 0

    def next(self, keyboard):
        self.frame_idx += 1
        self.game_clock.resume()
        self.game_clock.tick()
        if self.game_clock.time_left < 0:
            return
        self.move()
        self.load_people()
        self.hit_rebound_player()
        self.hit_rebound_people()
        self.hit_rebound_wall()
        self.set_delay_clock()
        self.set_player_dictection(keyboard)
        self.apply_rebound()

    def draw_bottom(self, layout_location, view_area):
        g_var.surface.blit(self.bottom_img, tuple(layout_location), tuple(view_area))

    def draw(self, layout_location, view_area):
        self.draw_bottom(layout_location, view_area)
        if self.player:
            self.player.draw(layout_location, view_area)
        for p in self.people:
            p.draw(layout_location, view_area)
        self.connection.draw(layout_location, view_area)

