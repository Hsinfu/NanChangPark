import logging
import os
import time
import pygame as pg
import pandas as pd

from keyboard import Keyboard

from constant import (
    GAME_RECORDS_PATH,
    PLAYERS_DIR,
    IMAGES_DIR,
    game_title,
    screen_size,
    frame_rate,
    starting_scores,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


pg.init()
pg.display.set_caption(game_title)

# display_flags = pg.DOUBLEBUF | pg.RESIZABLE
display_flags = pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE

screen = pg.display.set_mode(screen_size, display_flags)
clock = pg.time.Clock()

EMPTY_COLOR = pg.Color(0, 0, 0, 0)

def load_img(fname, size=None):
    fpath = os.path.join(IMAGES_DIR, fname)
    img = pg.image.load(fpath)
    img = pg.transform.scale(img, size or screen_size)
    return img

def load_imgs(dir_name, count, size=None):
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


class Level:
    def __init__(self):
        pass


class Frame:
    def __init__(self, imgs):
        self.idx = 0
        self.imgs = imgs
        self.num = len(imgs)

    @property
    def img(self):
        return self.imgs[self.idx]

    def move(self):
        self.idx += 1
        self.idx %= self.num

    def draw(self, surface):
        surface.blit(self.img, (0, 0))
        self.move()



class Stage:
    def __init__(self):
        pass


class WelcomeStage(Stage):
    def __init__(self):
        self.welcome_frames = Frame([load_img('welcome.png')])



class Game:
    def __init__(self, player_name):
        self.bg_frames = Frame(load_imgs('bg', 48))
        self.bar_frames = Frame(load_imgs('bar', 48))
        self._scores = starting_scores
        self.state = 'welcome'
        self.stages = {
            'welcome': WelcomeStage(),
        }

    @property
    def stage(self):
        return self.stages[self.state]

    @property
    def is_playing_stage(self):
        return 'level' in self.state

    def draw(self):
        surface_flags = pg.HWACCEL | pg.HWSURFACE
        sf = pg.Surface(screen.get_size(), flags=surface_flags).convert()
        self.bg_frames.draw(sf)
        if not self.is_playing_stage:
            self.bar_frames.draw(sf)
        screen.blit(sf, (0, 0))

    def tick(self, keyboard):
        logger.info('Game tick')
        self.draw()
        # self.stage
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
