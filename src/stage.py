import copy
import math
import random
import pygame as pg
import pandas as pd

import g_var
from constant import AreaStyle, layout_settings, viewbox_settings
from frame import Frame
from house import House
from utils import (
    do_scan,
    get_layout_img,
    get_layout_imgs,
    get_countdown_imgs,
    get_player_img,
    random_positive_negative,
)


class Stage:
    def __init__(self):
        pass


class WelcomeStage(Stage):
    def __init__(self):
        self.logo_frames = Frame(g_var.surface, get_layout_imgs('welcome/logo'))
        self.press_a_frames = Frame(g_var.surface, get_layout_imgs('welcome/press_a'))

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
        self.face_frames = Frame(g_var.surface, [get_layout_img('scan/face.png')])
        self.press_a_frames = Frame(g_var.surface, get_layout_imgs('scan/press_a'))

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
        self.player_name = player_name
        self.ball_frames = Frame(g_var.surface, get_layout_imgs('loading/ball'))

    @property
    def loaded(self):
        try:
            img_area = layout_settings['confirm']['img_area']
            img_size = [img_area.width, img_area.height]
            get_player_img(self.player_name, size=img_size)
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
        self.player_img_area = layout_settings['confirm']['img_area']
        self._player_frames = None
        self.press_frames = Frame(g_var.surface, get_layout_imgs('confirm/press'))
        self.ball_frames = Frame(g_var.surface, get_layout_imgs('confirm/ball'))

    @property
    def player_frames(self):
        if self._player_frames is None:
            try:
                img_size = [self.player_img_area.width, self.player_img_area.height]
                img = get_player_img(self.player_name, size=img_size)
                if img:
                    self._player_frames = Frame(g_var.surface, [img])
            except Exception:
                pass
        return self._player_frames

    def do_scan(self):
        self._player_frames = None
        do_scan(self.player_name)

    def tick(self, keyboard):
        if not self.player_frames:
            self.ball_frames.tick()
            keyboard.reset_keys()
            return False
        self.player_frames.tick(self.player_img_area.x, self.player_img_area.y)
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
        self.description_frames = Frame(g_var.surface, [get_layout_img('{}/description.png'.format(introX))])
        self.press_a_frames = Frame(g_var.surface, get_layout_imgs('{}/press_a'.format(introX)))

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
        a = self._view_area
        p = self.house.player
        self._view_area = AreaStyle(
            x=math.floor(p.x + p.img.get_width()/2 - a.width/2),
            y=math.floor(p.y + p.img.get_height()/2 - a.height/2),
            width=a.width,
            height=a.height,
        )

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
        self.box_frames = Frame(g_var.surface, [get_layout_img('{}/box.png'.format(levelX))])
        self.start_frames = Frame(g_var.surface, get_countdown_imgs('{}/start'.format(levelX)))
        self.end_frames = Frame(g_var.surface, get_countdown_imgs('{}/end'.format(levelX)))

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


class Rank(Stage):
    def __init__(self, player_name):
        self.frame_idx = 0
        self.player_name = player_name
        self.player_imgs = {}
        self._rank_records = None
        self.rank_frames = Frame(g_var.surface, [get_layout_img('rank/ranking.png')])
        self.press_a_frames = Frame(g_var.surface, get_layout_imgs('rank/press_a'))

    @property
    def rank_records(self):
        if self._rank_records is None:
            self._rank_records = self.get_rank_record()
        return self._rank_records

    def get_player_record(self):
        return {
            'name': self.player_name,
            'score': g_var.player_score,
        }

    def get_player_img(self, player_name, size):
        key = (player_name, size)
        if key not in self.player_imgs:
            self.player_imgs[key] = get_player_img(player_name, size)
        return self.player_imgs[key]

    def get_rank_record(self, max_num=3):
        record_num = len(g_var.records.df)
        num = min(max_num, record_num + 1)
        player_df = pd.DataFrame([self.get_player_record()])
        merged_df = g_var.records.df.append(player_df, ignore_index=True)
        sorted_df = merged_df.sort_values(by=['score']).iloc[:num]
        return sorted_df.to_dict('records')

    def draw_player(self):
        a = layout_settings['rank']['player_area']
        img = self.get_player_img(self.player_name, (a.width, a.height))
        g_var.surface.blit(img, [a.x, a.y])

        name_rectstyle = layout_settings['rank']['player_name_rectstyle']
        name_fontstyle = layout_settings['rank']['player_name_fontstyle']
        score_fontstyle = layout_settings['rank']['player_score_fontstyle']

        name_rect = pg.Rect(
            name_rectstyle.x + a.x,
            name_rectstyle.y + a.y,
            name_rectstyle.width,
            name_rectstyle.height,
        )
        pg.draw.rect(g_var.surface, name_fontstyle.color, name_rect, 1)

        name_font = pg.font.SysFont('arial', name_fontstyle.fontsize)
        name_surface = name_font.render(self.player_name, True, name_fontstyle.color)
        g_var.surface.blit(name_surface, [name_fontstyle.x + a.x, name_fontstyle.y + a.y])

        score_font = pg.font.SysFont('arial', score_fontstyle.fontsize)
        score_str = 'Score: {:03d}'.format(g_var.player_score)
        score_surface = score_font.render(score_str, True, score_fontstyle.color)
        g_var.surface.blit(score_surface, [score_fontstyle.x + a.x, score_fontstyle.y + a.y + a.height])

    def draw_ranks(self):
        name_fontstyle = layout_settings['rank']['rank_name_fontstyle']
        name_rectstyle = layout_settings['rank']['rank_name_rectstyle']
        score_fontstyle = layout_settings['rank']['rank_score_fontstyle']

        for idx, record in enumerate(self.rank_records):
            rankX = 'rank{}_area'.format(idx + 1)
            a = layout_settings['rank'][rankX]
            img = self.get_player_img(record['name'], (a.width, a.height))
            g_var.surface.blit(img, [a.x, a.y])

            name_rect = pg.Rect(
                name_rectstyle.x + a.x,
                name_rectstyle.y + a.y,
                name_rectstyle.width,
                name_rectstyle.height,
            )
            pg.draw.rect(g_var.surface, name_fontstyle.color, name_rect, 1)

            name_font = pg.font.SysFont('arial', name_fontstyle.fontsize)
            name_surface = name_font.render(record['name'], True, name_fontstyle.color)
            g_var.surface.blit(name_surface, [name_fontstyle.x + a.x, name_fontstyle.y + a.y])

            score_font = pg.font.SysFont('arial', score_fontstyle.fontsize)
            score_str = 'Score: {:03d}'.format(record['score'])
            score_surface = score_font.render(score_str, True, score_fontstyle.color)
            g_var.surface.blit(score_surface, [score_fontstyle.x + a.x, score_fontstyle.y + a.y + a.height])

    def tick(self, keyboard):
        self.rank_frames.tick()
        self.draw_player()
        self.draw_ranks()
        self.frame_idx += 1
        if self.frame_idx <= 48:
            return False

        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False
