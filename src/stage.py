import pygame as pg

import g_var
from constant import layout_settings, viewbox_settings
from frame import Frame
from house import House
from utils import do_scan, load_img, load_imgs, get_player_img_fpath


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
    def __init__(self):
        self.face_frames = Frame(g_var.surface, [load_img('scan/face.png')])
        self.press_a_frames = Frame(g_var.surface, load_imgs('scan/press_a'))

    def tick(self, keyboard):
        self.face_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False


class LoadingStage(Stage):
    def __init__(self, player_name):
        s = layout_settings['confirm']['img']
        self.img_size = [s.width, s.height]
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
            self._player_frames = Frame(g_var.surface, [self.get_player_img()])
        return self._player_frames

    def get_player_img(self):
        s = layout_settings['confirm']['img']
        player_img_size = [s.width, s.height]
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
        s = layout_settings['confirm']['img']
        self.player_frames.tick(s.x, s.y)
        self.press_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        if keyboard.is_pressed(pg.K_b):
            self.do_scan()
        return False


class IntroStage(Stage):
    def __init__(self, introX):
        self.description_frames = Frame(g_var.surface, [load_img('{}/description.png'.format(introX))])
        self.press_a_frames = Frame(g_var.surface, load_imgs('{}/press_a'.format(introX)))

    def tick(self, keyboard):
        self.description_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False


class Viewbox(Stage):
    def __init__(self, levelX, player_name):
        viewbox_setting = viewbox_settings[levelX]
        self.is_static = viewbox_setting['is_static']
        self.viewbox_location = layout_settings['level']['viewbox_location']
        self.viewbox_area = viewbox_setting['viewbox_area']
        self.house = House(levelX, player_name)

    def update(self):
        # TODO: update viewbox by self.house.player
        pass

    def next(self, keyboard):
        self.house.next(keyboard)
        if not self.is_static:
            self.update()
        if self.house.is_delay:
            # TODO: random change the viewbox to simulate collision
            pass

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
        self.house.draw(self.viewbox_location, self.viewbox_area)

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
