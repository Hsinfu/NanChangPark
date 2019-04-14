import logging
import pygame as pg
import pandas as pd

import g_var
from keyboard import Keyboard
from frame import Frame
from utils import load_imgs
from constant import GAME_RECORDS_PATH, game_settings, house_settings
from stage import (
    WelcomeStage,
    ScanStage,
    LoadingStage,
    ConfirmStage,
    IntroStage,
    Level,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


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
        self.bg_frames = Frame(g_var.surface, load_imgs('bg'))
        self.bar_frames = Frame(g_var.surface, load_imgs('bar'))
        super().__init__(
            states=[
                # 'welcome',
                # 'scan',
                # 'loading',
                # 'confirm',
                # 'intro1',
                'level1',
                # 'intro2',
                # 'level2',
                # 'intro3',
                # 'level3',
            ],
            stages={
                # 'welcome': WelcomeStage(),
                # 'scan': ScanStage(),
                # 'loading': LoadingStage(player_name),
                # 'confirm': ConfirmStage(player_name),
                # 'intro1': IntroStage('intro1'),
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
            if 'level' in self.state:
                g_var.player_score -= len(self.stage.viewbox.house.connection.connects)
            if 'welcome' in self.state:
                g_var.player_score = game_settings['starting_scores']
            self.change_stage()

        g_var.screen.blit(g_var.surface, (0, 0))
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
            # get pygame events
            events = pg.event.get()
            logger.debug('events: {}'.format(events))

            # update keyboard
            self.keyboard.update(events)
            logger.debug('keyboard: {}'.format(self.keyboard.keys))

            # exit while player close the pygame display window
            if any([e.type == pg.QUIT for e in events]):
                break
            # exit while player click esc
            if self.keyboard.is_pressed(pg.K_ESCAPE):
                break

            # tick
            self.tick(self.keyboard)
            # refresh pygame display
            pg.display.flip()
            # delay 1/frame_rate time by pygame clock
            g_var.pg_clock.tick(game_settings['frame_rate'])


def main():
    # init pygame
    pg.init()
    pg.display.set_caption(game_settings['game_title'])

    # init pygame screen
    # display_flags = pg.DOUBLEBUF | pg.RESIZABLE
    display_flags = pg.FULLSCREEN | pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE
    g_var.screen = pg.display.set_mode(tuple(game_settings['screen_size']), display_flags)

    # init pygame surface
    surface_flags = pg.HWACCEL | pg.HWSURFACE
    g_var.surface = pg.Surface(g_var.screen.get_size(), flags=surface_flags).convert()

    # init pygame clock
    g_var.pg_clock = pg.time.Clock()

    # init player_score
    g_var.player_score = game_settings['starting_scores']

    # run rank game
    RankGame().start()

    # quit pygame
    pg.quit()


if __name__ == "__main__":
    main()
