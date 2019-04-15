import random
import pygame as pg

import g_var
from constant import AreaStyle, layout_settings, viewbox_settings
from frame import Frame
from house import House
from utils import (
    do_scan,
    load_img,
    load_imgs,
    get_player_img_fpath,
    random_positive_negative,
)


class Stage:
    def __init__(self):
        pass


class WelcomeStage(Stage):
    def __init__(self):
        self.logo_frames = Frame(g_var.surface, load_imgs('welcome/logo'))
        self.press_a_frames = Frame(g_var.surface, load_imgs('welcome/press_a'))

    def tick(self, keyboard):
        self.logo_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False


class ScanStage(Stage):
    def __init__(self, player_name):
        self.player_name = player_name
        self.face_frames = Frame(g_var.surface, [load_img('scan/face.png')])
        self.press_a_frames = Frame(g_var.surface, load_imgs('scan/press_a'))

    def tick(self, keyboard):
        self.face_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            do_scan(self.player_name)
            keyboard.reset_keys()
            return True
        return False


class LoadingStage(Stage):
    def __init__(self, player_name):
        img_area = layout_settings['confirm']['img_area']
        self.img_size = [img_area.width, img_area.height]
        self.img_fpath = get_player_img_fpath(player_name)
        self.ball_frames = Frame(g_var.surface, load_imgs('loading/ball'))

    @property
    def loaded(self):
        try:
            load_img(self.img_fpath, img_dir='', size=self.img_size)
            return True
        except Exception:
            return False

    def tick(self, keyboard):
        self.ball_frames.tick()
        if self.loaded and self.ball_frames.is_last_frame:
            keyboard.reset_keys()
            return True
        return False


class ConfirmStage(Stage):
    def __init__(self, player_name):
        self.player_name = player_name
        self._player_frames = None
        self.press_frames = Frame(g_var.surface, load_imgs('confirm/press'))
        self.ball_frames = Frame(g_var.surface, load_imgs('loading/ball'))

    @property
    def player_frames(self):
        if self._player_frames is None:
            img = self.get_player_img()
            if img:
                self._player_frames = Frame(g_var.surface, [img])
        return self._player_frames

    def get_player_img(self):
        img_area = layout_settings['confirm']['img_area']
        player_img_size = [img_area.width, img_area.height]
        player_img_fpath = get_player_img_fpath(self.player_name)
        try:
            return load_img(player_img_fpath, img_dir='', size=player_img_size)
        except Exception:
            return None

    def do_scan(self):
        self._player_frames = None
        do_scan(self.player_name)

    def tick(self, keyboard):
        if not self.player_frames:
            self.ball_frames.tick()
            keyboard.reset_keys()
            return False
        img_area = layout_settings['confirm']['img_area']
        self.player_frames.tick(img_area.x, img_area.y)
        self.press_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        if keyboard.is_pressed(pg.K_b):
            self.do_scan()
        return False


class IntroStage(Stage):
    def __init__(self, introX):
        self.frame_idx = 0
        self.house_setting = layout_settings[introX]
        self.delay_frames = self.house_setting['press_a_delay_frames']
        self.description_frames = Frame(g_var.surface, [load_img('{}/description.png'.format(introX))])
        self.press_a_frames = Frame(g_var.surface, load_imgs('{}/press_a'.format(introX)))

    def tick(self, keyboard):
        self.description_frames.tick()
        self.frame_idx += 1
        if self.frame_idx < self.delay_frames:
            return False
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False


class Viewbox(Stage):
    def __init__(self, levelX, player_name):
        viewbox_setting = viewbox_settings[levelX]
        self.is_static = viewbox_setting['is_static']
        self.layout_location = layout_settings['level']['layout_location']
        self.shake_range = layout_settings['level']['hit_shake_range']
        self._view_area = viewbox_setting['view_area']
        self.house = House(levelX, player_name)

    @property
    def view_area(self):
        if not self.house.is_delay:
            return self._view_area
        a = self._view_area
        shake_x = random_positive_negative() * random.randrange(self.shake_range)
        shake_y = random_positive_negative() * random.randrange(self.shake_range)
        return AreaStyle(x=a.x+shake_x, y=a.y+shake_y, width=a.width, height=a.height)

    def update(self):
        # TODO: update viewbox by self.house.player
        pass

    def next(self, keyboard):
        self.house.next(keyboard)
        if not self.is_static:
            self.update()

    def draw_time(self):
        font_style = layout_settings['level']['time_font']
        time_font = pg.font.SysFont('arial', font_style.fontsize)
        time_str = '{:02.2f}'.format(max(self.house.game_clock.time_left, 0))
        time_surface = time_font.render(time_str, True, font_style.color)
        g_var.surface.blit(time_surface, (font_style.x, font_style.y))

    def draw_score(self):
        font_style = layout_settings['level']['score_font']
        time_font = pg.font.SysFont('arial', font_style.fontsize)
        score = '{:03d}'.format(g_var.player_score - len(self.house.connection.connects))
        time_surface = time_font.render(score, True, font_style.color)
        g_var.surface.blit(time_surface, (font_style.x, font_style.y))

    def draw(self):
        self.draw_time()
        self.draw_score()
        self.house.draw(self.layout_location, self.view_area)

    def tick(self, keyboard):
        self.draw()
        self.next(keyboard)
        return self.house.game_clock.time_left


class Level(Stage):
    def __init__(self, levelX, player_name):
        self.viewbox = Viewbox(levelX, player_name)
        self.box_frames = Frame(g_var.surface, [load_img('{}/box.png'.format(levelX))])
        self.start_frames = Frame(g_var.surface, load_imgs('{}/start'.format(levelX), 96))
        self.end_frames = Frame(g_var.surface, load_imgs('{}/end'.format(levelX), 96))

    def tick(self, keyboard):
        if not self.start_frames.is_last_frame:
            self.viewbox.draw()
            self.box_frames.tick()
            self.start_frames.tick()
            keyboard.reset_keys()
            return False
        time_remain = self.viewbox.tick(keyboard)
        self.box_frames.tick()
        if time_remain < 3:
            end_frames_idx = int((3 - time_remain) * 24)
            if end_frames_idx >= 95:
                return True
            self.end_frames.idx = end_frames_idx
            self.end_frames.draw()
        return False
