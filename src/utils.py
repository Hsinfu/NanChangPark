import os
import logging
import random
import subprocess
import pygame as pg

import g_var
from constant import (
    game_settings,
    house_settings,
    VIRTUALENV,
    INSTAGRAM_UPLOADER_PY,
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


def get_player_ig_img_fpath(player_name):
    return get_player_img_fpath('{}_ig'.format(player_name))


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
    rm(player_name)
    if game_settings['is_scanner_connected']:
        scan(player_name)
    else:
        cp(player_name)


def upload_ig(player_name, caption):
    img_fpath = get_player_img_fpath(player_name)
    ig_img_fpath = get_player_ig_img_fpath(player_name)
    img_area = game_settings['instagram_img_center_area']
    cmd1 = 'convert {} -crop {}x{}+{}+{} {}'.format(
        img_fpath,
        img_area.width,
        img_area.height,
        img_area.x,
        img_area.y,
        ig_img_fpath,
    )
    cmd2 = '{} {} --img-fpath "{}" --caption "{}"'.format(
        VIRTUALENV, INSTAGRAM_UPLOADER_PY, ig_img_fpath, caption)
    command_line('({} && {}) &'.format(cmd1, cmd2))


def load_img(fname, img_dir, size):
    fpath = os.path.join(img_dir, fname)
    img = pg.image.load(fpath)
    if size:
        img = pg.transform.scale(img, size)
    img = img.convert_alpha()
    return img


imgs = {}
people_imgs = {}


def get_img(fpath, size):
    key = (fpath, size)
    if key not in people_imgs:
        people_imgs[key] = load_img(fpath, img_dir='', size=size)
    return people_imgs[key]


def get_player_img(player_name, size=tuple(house_settings['img_size'])):
    # NOTE: Do not cache, since there will be multiple sizes
    fpath = get_player_img_fpath(player_name)
    return load_img(fpath, img_dir='', size=size)


def get_map_img(fname):
    if fname not in imgs:
        size = tuple(house_settings['map_size'])
        imgs[fname] = load_img(fname, IMAGES_DIR, size)
    return imgs[fname]


def get_layout_img(fname):
    if fname not in imgs:
        size = tuple(game_settings['screen_size'])
        imgs[fname] = load_img(fname, IMAGES_DIR, size)
    return imgs[fname]


def get_layout_imgs(dname, count=48):
    def get_fname(i):
        return os.path.join(dname, '{:05d}.png'.format(i))
    return [get_layout_img(get_fname(i)) for i in range(count)]


def get_countdown_imgs(dname, count=96):
    return get_layout_imgs(dname, count)


def load_all_imgs():
    get_map_img('house/bottom.png')
    get_map_img('house/map.png')
    get_map_img('level1/player_map.png')

    # get_layout_imgs('bg')
    # get_layout_imgs('bar')

    get_layout_imgs('welcome/logo')
    get_layout_imgs('welcome/press_a')

    get_layout_img('scan/face.png')
    get_layout_imgs('scan/press_a')

    # get_layout_imgs('loading/ball')

    get_layout_imgs('confirm/press')
    get_layout_imgs('confirm/ball')

    get_layout_img('intro1/description.png')
    get_layout_img('intro2/description.png')
    get_layout_img('intro3/description.png')
    get_layout_imgs('intro1/press_a')
    get_layout_imgs('intro2/press_a')
    get_layout_imgs('intro3/press_a')

    get_layout_img('level1/box.png')
    get_layout_img('level2/box.png')
    get_layout_img('level3/box.png')
    get_countdown_imgs('level1/start')
    get_countdown_imgs('level2/start')
    get_countdown_imgs('level3/start')
    get_countdown_imgs('level1/end')
    get_countdown_imgs('level2/end')
    get_countdown_imgs('level3/end')

    get_layout_img('rank/ranking.png')
    get_layout_imgs('rank/press_a')

    for img_fpath in gen_available_imgs_fpath():
        get_img(img_fpath, tuple(house_settings['img_size']))

walls = {}


def load_wall(fname):
    try:
        img = get_map_img(fname)
    except Exception:
        return None
    blank_color = house_settings['blank_color']

    def is_wall(wi, hi):
        return 0 if img.get_at((wi, hi)) == blank_color else 1
    return [[is_wall(wi, hi) for hi in range(img.get_height())]
                                for wi in range(img.get_width())]


def get_wall(fname):
    if fname not in walls:
        walls[fname] = load_wall(fname)
    return walls[fname]


def load_all_walls():
    get_wall('house/map.png')
    get_wall('level1/player_map.png')


def gen_pixels(img):
    for h in range(img.get_height()):
        for w in range(img.get_width()):
            yield tuple(img.get_at((w, h)))


def gen_available_imgs_fpath(excluded_fpaths=[]):
    for i in range(1, 35):
        fpath = os.path.join(IMAGES_DIR, 'pool/{:05d}.jpg'.format(i))
        if fpath not in excluded_fpaths:
            yield fpath

    df = g_var.records.df
    for i in range(g_var.player_idx):
        player_name = 'Player-{:03d}'.format(i)
        fpath = get_player_img_fpath(player_name)
        if fpath in excluded_fpaths:
            continue
        if int(df.loc[df['name'] == player_name]['score']) > game_settings['starting_scores']:
            continue
        yield fpath


def get_available_imgs_fpath(num, excluded_fpaths=[]):
    return list(random.sample(list(gen_available_imgs_fpath(excluded_fpaths)), num))
