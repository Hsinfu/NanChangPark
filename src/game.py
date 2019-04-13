import logging
import os
import time
import random
import pygame as pg
import pandas as pd

from keyboard import Keyboard
from utils import do_scan, get_player_img_fpath
from constant import (
    GAME_RECORDS_PATH,
    PLAYERS_DIR,
    IMAGES_DIR,
    game_title,
    screen_size,
    frame_rate,
    starting_scores,
    PLAYERS_IMG_DIR,
    PLAYER_IMG_EXT,
    layout_settings,
    viewbox_settings,
    house_settings,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

pg.init()
pg.display.set_caption(game_title)

# display_flags = pg.DOUBLEBUF | pg.RESIZABLE
display_flags = pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
screen = pg.display.set_mode(screen_size, display_flags)

surface_flags = pg.HWACCEL | pg.HWSURFACE
surface = pg.Surface(screen.get_size(), flags=surface_flags).convert()
clock = pg.time.Clock()


def load_img(fname, img_dir=IMAGES_DIR, size=screen_size):
    fpath = os.path.join(img_dir, fname)
    img = pg.image.load(fpath)
    if size:
        img = pg.transform.scale(img, size)
    img = img.convert_alpha()
    return img

def load_imgs(dir_name, count=48, size=screen_size):
    def get_fname(i):
        return os.path.join(dir_name, '{:05d}.png'.format(i))
    return [load_img(get_fname(i)) for i in range(count)]

# imgs = {
#     'bg': load_imgs('bg', 48),
#     'bar': load_imgs('bar', 48),
#     # 'welcome': load_img('welcome.png'),
#     # 'scan': load_img('scan.png'),
#     # 'confirm': load_img('confirm.png'),
#     # 'level1-description': load_img('level1-description.png'),
#     # 'level1-map': load_img('level1-description.png'),
# }

class Frame:
    def __init__(self, surface, imgs):
        self.idx = 0
        self.imgs = imgs
        self.num = len(imgs)
        self.surface = surface

    @property
    def img(self):
        return self.imgs[self.idx]

    @property
    def is_last_frame(self):
        return self.idx == self.num - 1

    def move(self):
        self.idx += 1
        self.idx %= self.num

    def draw(self, x=0, y=0):
        self.surface.blit(self.img, (x, y))

    def tick(self, x=0, y=0):
        self.draw(x, y)
        self.move()


class Stage:
    def __init__(self):
        pass


class WelcomeStage(Stage):
    def __init__(self):
        self.logo_frames = Frame(surface, load_imgs('welcome/logo'))
        self.press_a_frames = Frame(surface, load_imgs('welcome/press_a'))

    def tick(self, keyboard):
        self.logo_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False


class ScanStage(Stage):
    def __init__(self):
        self.face_frames = Frame(surface, [load_img('scan/face.png')])
        self.press_a_frames = Frame(surface, load_imgs('scan/press_a'))

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
        self.ball_frames = Frame(surface, load_imgs('loading/ball'))

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
        self.press_frames = Frame(surface, load_imgs('confirm/press'))
        self.ball_frames = Frame(surface, load_imgs('loading/ball'))

    @property
    def player_frames(self):
        if self._player_frames is None:
            self._player_frames = Frame(surface, [self.get_player_img()])
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
        self.description_frames = Frame(surface, [load_img('{}/description.png'.format(introX))])
        self.press_a_frames = Frame(surface, load_imgs('{}/press_a'.format(introX)))

    def tick(self, keyboard):
        self.description_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return True
        return False

class Viewbox:
    def __init__(self, levelX, player_name):
        viewbox_setting = viewbox_settings[levelX]
        self.is_static = viewbox_setting['is_static']
        self.viewbox = viewbox_setting['viewbox']
        # self.house = House(levelX, player_name)

    def update(self):
        # TODO: update viewbox by self.house.player
        pass

    def move(self, keyboard):
        # self.house.move(keyboard)
        if not self.is_static:
            self.update()
        # if self.house.is_delay:
        #     # TODO: random change the viewbox to simulate collision
        #     pass

    def draw(self):
        # self.house.draw(self.viewbox)
        pass

    def tick(self, keyboard):
        self.draw()
        self.move(keyboard)
        # return self.house.clock.time_left
        return 10


class Level(Stage):
    def __init__(self, levelX, player_name):
        self.viewbox = Viewbox(levelX, player_name)
        self.start_frames = Frame(surface, load_imgs('{}/start'.format(levelX), 96))
        self.end_frames = Frame(surface, load_imgs('{}/end'.format(levelX), 96))

    def tick(self, keyboard):
        if not self.start_frames.is_last_frame:
            self.viewbox.draw(keyboard)
            self.start_frames.tick()
            keyboard.reset_keys()
            return False
        time_remain = self.viewbox.tick(keyboard)
        if time_remain < 3:
            end_frames_idx = int((3 - time_remain) * 24)
            if end_frames_idx >= 95:
                return True
            self.end_frames.idx = end_frames_idx
            self.end_frames.draw()
        return False


class Stages:
    def __init__(self, states, stages):
        self._states = states
        self._stages = stages
        self.state_idx = 0
        pass

    @property
    def num_states(self):
        return len(self._states)

    @property
    def state(self):
        return self._states[self.state_idx]

    @property
    def stage(self):
        return self._stages[self.state]

    def change_stage(self):
        if self.num_states == 0:
            return
        self.state_idx += 1
        self.state_idx %= self.num_states



class Game(Stages):
    def __init__(self, player_name):
        self.player_name = player_name
        self.bg_frames = Frame(surface, load_imgs('bg'))
        self.bar_frames = Frame(surface, load_imgs('bar'))
        self._scores = starting_scores
        super().__init__(
            states=[
                'welcome',
                'scan',
                'loading',
                'confirm',
                'intro1',
                'level1',
                # 'intro2',
                # 'level2',
                # 'intro3',
                # 'level3',
            ],
            stages={
                'welcome': WelcomeStage(),
                'scan': ScanStage(),
                'loading': LoadingStage(player_name),
                'confirm': ConfirmStage(player_name),
                'intro1': IntroStage('intro1'),
                'level1': Level('level1', player_name),
                # 'intro2': IntroStage('intro2'),
                # 'level2': Level('level2', player_name),
                # 'intro3': IntroStage('intro3'),
                # 'level3': Level('level3', player_name),
            },
        )

    @property
    def is_playing_stage(self):
        return 'level' in self.state or 'intro' in self.state

    def tick(self, keyboard):
        logger.info('Game tick')
        self.bg_frames.tick()
        if not self.is_playing_stage:
            self.bar_frames.tick()

        status = self.stage.tick(keyboard)
        if status:
            self.change_stage()

        screen.blit(surface, (0, 0))
        return None


class RankGame:
    def __init__(self, records_path=GAME_RECORDS_PATH):
        """
            records: [
                {
                    "name": "xxx",
                    "score": 26,
                    "avatar": "../avatars/xxx.png"
                }
            ]
        """
        self._game = None
        self._keyboard = None
        self.records_path = records_path
        try:
            self.records = pd.read_json(records_path)
        except Exception:
            self.records = []

    @property
    def player_idx(self):
        return len(self.records)

    @property
    def player_name(self):
        return 'Player-{:03d}'.format(self.player_idx)

    @property
    def game(self):
        if self._game is None:
            self._game = Game(self.player_name)
        return self._game

    @property
    def keyboard(self):
        if self._keyboard is None:
            self._keyboard = Keyboard()
        return self._keyboard

    def add(self, record):
        self.records.append(pd.DataFrame([record]), ignore_index=True)
        self.records.to_json(self.records_path, orient='records')
        self._game = None

    def tick(self, keyboard):
        # logger.info('RankGame tick')
        record = self.game.tick(keyboard)
        if record is not None:
            self.add(record)

    def start(self):
        while True:
            events = pg.event.get()
            logger.debug('events: {}'.format(events))
            self.keyboard.update(events)
            logger.debug('keyboard: {}'.format(self.keyboard.keys))

            if any([e.type == pg.QUIT for e in events]):
                break
            if self.keyboard.is_pressed(pg.K_ESCAPE):
                break
            self.tick(self.keyboard)
            pg.display.flip()
            clock.tick(frame_rate)


# run
RankGame().start()

# quit pygame
pg.quit()
