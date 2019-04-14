import os
import logging
import random
import subprocess
import pygame as pg
from constant import (
    game_settings,
    SCANLINE_CMD,
    CP_SOURCES_DIR,
    PLAYERS_IMG_DIR,
    PLAYER_IMG_EXT,
    IMAGES_DIR,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


def random_positive_negative():
    return 1 if random.random() > 0.5 else -1


def sign(v):
    if v == 0:
        return 0
    elif v > 0:
        return 1
    else:
        return -1


# Ex. instruction -> 'ls -al'
def command_line(instruction):
    subprocess.Popen([instruction], shell=True,
        stdin=None, stdout=None, stderr=None, close_fds=True)


def get_player_img_fpath(player_name):
    fname = '{}.{}'.format(player_name, PLAYER_IMG_EXT)
    return os.path.join(PLAYERS_IMG_DIR, fname)


def cp(player_name):
    i = random.randrange(1, 8)
    f = '{}/man{:02d}.png'.format(CP_SOURCES_DIR, i)
    command_line('cp -f {} {}'.format(f, get_player_img_fpath(player_name)))


def rm(player_name):
    img_fpath = get_player_img_fpath(player_name)
    command_line('rm -f {}'.format(img_fpath))


def scan(player_name):
    # TODO: background
    command_line('{} -verbose -flatbed -a4 -jpeg -dir {} -name {} &'.format(
        SCANLINE_CMD, PLAYERS_IMG_DIR, player_name))


def do_scan(player_name):
    m = game_settings['get_player_img_method']
    rm(player_name)
    if m == 'cp':
        cp(player_name)
    elif m == 'scan':
        scan(player_name)
    else:
        logger.error('game_settings["get_player_img_method"] error')
        raise Exception


def load_img(fname, img_dir=IMAGES_DIR, size=tuple(game_settings['screen_size'])):
    fpath = os.path.join(img_dir, fname)
    img = pg.image.load(fpath)
    if size:
        img = pg.transform.scale(img, size)
    img = img.convert_alpha()
    return img


def load_imgs(dir_name, count=48, size=tuple(game_settings['screen_size'])):
    def get_fname(i):
        return os.path.join(dir_name, '{:05d}.png'.format(i))
    return [load_img(get_fname(i)) for i in range(count)]


def gen_pixels(img):
    for h in range(img.get_height()):
        for w in range(img.get_width()):
            yield tuple(img.get_at((w,h)))
