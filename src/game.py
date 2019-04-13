import logging
import os
import time
import random
import pygame as pg
import pandas as pd

from keyboard import Keyboard
from utils import command_line
from constant import (
    GAME_RECORDS_PATH,
    PLAYERS_DIR,
    IMAGES_DIR,
    game_title,
    SCANLINE_CMD,
    screen_size,
    frame_rate,
    starting_scores,
    get_player_img_method,
    CP_SOURCES_DIR,
    PLAYERS_IMG_DIR,
    PLAYER_IMG_EXT,
    confirm_img_style,
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


def load_img(fname, img_dir=IMAGES_DIR, size=None):
    fpath = os.path.join(img_dir, fname)
    img = pg.image.load(fpath)
    img = pg.transform.scale(img, size or screen_size)
    img = img.convert_alpha()
    return img

def load_imgs(dir_name, count=48, size=None):
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
            return ['next_stage']
        return []


class ScanStage(Stage):
    def __init__(self):
        self.face_frames = Frame(surface, [load_img('scan/face.png')])
        self.press_a_frames = Frame(surface, load_imgs('scan/press_a'))

    def tick(self, keyboard):
        self.face_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return ['scan', 'next_stage']
        return []


class LoadingStage(Stage):
    def __init__(self, is_end=False):
        self.is_end = is_end
        self.ball_frames = Frame(surface, load_imgs('loading/ball'))

    def set_end(self):
        self.is_end = True

    def tick(self, keyboard):
        self.ball_frames.tick()
        if self.is_end and self.ball_frames.is_last_frame:
            keyboard.reset_keys()
            return ['next_stage']
        return []

class ConfirmStage(Stage):
    def __init__(self):
        self.press_frames = Frame(surface, load_imgs('confirm/press'))
        self.player_frames = None

    def set_player_img(self, img):
        self.player_frames = Frame(surface, [img])

    def tick(self, keyboard):
        if self.player_frames:
            self.player_frames.tick(confirm_img_style.x, confirm_img_style.y)
        self.press_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return ['next_stage']
        if keyboard.is_pressed(pg.K_b):
            return ['scan']
        return []


class IntroStage(Stage):
    def __init__(self, introX):
        self.description_frames = Frame(surface, [load_img('{}/description.png'.format(introX))])
        self.press_a_frames = Frame(surface, load_imgs('{}/press_a'.format(introX)))

    def tick(self, keyboard):
        self.description_frames.tick()
        self.press_a_frames.tick()
        if keyboard.is_pressed(pg.K_a):
            keyboard.reset_keys()
            return ['next_stage']
        return []


class Level(Stage):
    def __init__(self, levelX):
        self.start_frames = Frame(surface, load_imgs('{}/start'.format(levelX), 96))
        self.end_frames = Frame(surface, load_imgs('{}/end'.format(levelX), 96))

    def tick(self, keyboard):
        if not self.start_frames.is_last_frame:
            self.map.draw()
            self.start_frames.tick()
            keyboard.reset_keys()
            return []
        self.map.set_start()
        time_remain = self.map.tick()
        if time_remain < 3:
            end_frames_idx = int((3 - time_remain) * 24)
            if end_frames_idx >= 95:
                return 'next_stage'
            self.end_frames.idx = end_frames_idx
            self.end_frames.draw()
        return []


class Level1(Level):
    def __init__(self):
        super().__init__('level1')

    # def tick(self, keyboard):
    #     return []


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
        self._player_img = None
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
                # 'level2',
                # 'level3',
            ],
            stages={
                'welcome': WelcomeStage(),
                'scan': ScanStage(),
                'loading': LoadingStage(),
                'confirm': ConfirmStage(),
                'intro1': IntroStage('intro1'),
                'level1': Level1(),
            },
        )

    @property
    def is_playing_stage(self):
        return 'level' in self.state

    @property
    def player_img_fpath(self):
        fname = '{}.{}'.format(self.player_name, PLAYER_IMG_EXT)
        return os.path.join(PLAYERS_IMG_DIR, fname)

    def cp(self):
        i = random.randrange(1, 8)
        f = '{}/man{:02d}.png'.format(CP_SOURCES_DIR, i)
        command_line('cp {} {}'.format(f, self.player_img_fpath))

    def scan(self):
        command_line('{} -verbose -flatbed -a4 -jpeg -dir {} -name {}'.format(
            SCANLINE_CMD, PLAYERS_IMG_DIR, self.player_name))

    @property
    def player_img(self):
        if self._player_img is None:
            self._player_img = self.load_player_img()
        return self._player_img

    def load_player_img(self):
        size = [confirm_img_style.width, confirm_img_style.height]
        try:
            return load_img(self.player_img_fpath, img_dir='', size=size)
        except Exception:
            return None

    def do_scan(self):
        self._player_img = None
        if get_player_img_method == 'cp':
            self.cp()
        elif get_player_img_method == 'scan':
            self.scan()
        else:
            logger.error('get_player_img_method error')
            raise Exception

    def tick(self, keyboard):
        logger.info('Game tick')
        self.bg_frames.tick()
        if not self.is_playing_stage:
            self.bar_frames.tick()

        if self.state == 'loading':
            if self.player_img:
                self.stage.set_end()
        elif self.state == 'confirm':
            self.stage.set_player_img(self.player_img)

        status = self.stage.tick(keyboard)
        if 'scan' in status:
            # TODO: thread
            self.do_scan()
        if 'next_stage' in status:
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
