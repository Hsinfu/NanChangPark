import os
import logging
import random
import subprocess
from constant import (
    get_player_img_method,
    SCANLINE_CMD,
    CP_SOURCES_DIR,
    PLAYERS_IMG_DIR,
    PLAYER_IMG_EXT,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


# Ex. instruction -> 'ls -al'
def command_line(instruction):
    subprocess.check_output(instruction, shell=True)


def get_player_img_fpath(player_name):
    fname = '{}.{}'.format(player_name, PLAYER_IMG_EXT)
    return os.path.join(PLAYERS_IMG_DIR, fname)


def cp(player_name):
    i = random.randrange(1, 8)
    f = '{}/man{:02d}.png'.format(CP_SOURCES_DIR, i)
    command_line('cp {} {}'.format(f, get_player_img_fpath(player_name)))


def scan(player_name):
    # TODO: background
    command_line('{} -verbose -flatbed -a4 -jpeg -dir {} -name {} &'.format(
        SCANLINE_CMD, PLAYERS_IMG_DIR, player_name))


def do_scan(player_name):
    if get_player_img_method == 'cp':
        cp(player_name)
    elif get_player_img_method == 'scan':
        scan(player_name)
    else:
        logger.error('get_player_img_method error')
        raise Exception
