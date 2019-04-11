import logging
import os
import time
import pygame as pg
import pandas as pd

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

imgs = {
    'bg': load_imgs('bg', 48),
    'bar': load_imgs('bar', 48),
    # 'welcome': load_img('welcome.png'),
    # 'scan': load_img('scan.png'),
    # 'confirm': load_img('confirm.png'),
    # 'level1-description': load_img('level1-description.png'),
    # 'level1-map': load_img('level1-description.png'),
}


class Level:
    def __init__(self):
        pass


class Stage:
    def __init__(self):
        pass


class WelcomeStage(Stage):
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


class Game:
    def __init__(self, player_name):
        self.bg_frames = Frame(imgs['bg'])
        self.bar_frames = Frame(imgs['bar'])
        self._scores = starting_scores

    def tick(self, events):
        logger.info('Game tick')
        surface_flags = pg.HWACCEL | pg.HWSURFACE
        sf = pg.Surface(screen.get_size(), flags=surface_flags).convert()
        self.bg_frames.draw(sf)
        self.bar_frames.draw(sf)
        screen.blit(sf, (0, 0))
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

    def add(self, record):
        self.records.append(pd.DataFrame([record]), ignore_index=True)
        self.records.to_json(self.records_path, orient='records')
        self._game = None

    def tick(self, events):
        # logger.info('RankGame tick')
        record = self.game.tick(events)
        if record is not None:
            self.add(record)

    def start(self):
        while True:
            events = pg.event.get()
            # print(events)
            if any([e.type == pg.QUIT for e in events]):
                break
            if any([e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE for e in events]):
                break
            self.tick(events)
            pg.display.flip()
            clock.tick(frame_rate)


# run
RankGame().start()

# quit pygame
pg.quit()
