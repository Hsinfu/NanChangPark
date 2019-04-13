import os
import pygame as pg
from collections import namedtuple


TextSytle = namedtuple('TextSytle', ['fontsize', 'x', 'y'])
BoxStyle = namedtuple('BoxStyle', ['width', 'height', 'x', 'y'])
LocationStyle = namedtuple('LocationStyle', ['x', 'y'])
SizeStyle = namedtuple('SizeStyle', ['width', 'height'])

### Static Path
THIS_FILE_DIR = os.path.dirname(__file__)
INSTAGRAM_ACCOUNT_PATH = os.path.abspath(os.path.join(THIS_FILE_DIR, '../instagram_account.json'))
GAME_RECORDS_PATH = os.path.abspath(os.path.join(THIS_FILE_DIR, '../record.json'))
IMAGES_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/'))
SCANLINE_CMD = os.path.abspath(os.path.join(THIS_FILE_DIR, '../tools/scanline'))
CP_SOURCES_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1'))
PLAYERS_IMG_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../players'))
PLAYER_IMG_EXT = 'jpeg'

### General
game_title = 'NanChangPark Never Lock'
frame_rate = 24
get_player_img_method = 'cp'  # or 'scan'


### game
# score
starting_scores = 100

# color
empty_color = pg.Color(0, 0, 0, 0)
text_color = pg.Color(255, 255, 255)
time_color = pg.Color(117, 249, 76)

# layout
screen_size = [1440, 900]
layout_settings = {
    'confirm': {
        'img': BoxStyle(width=407, height=620, x=516, y=100)
    },
    'level': {
        'name': TextSytle(fontsize=24, x=165, y=54),
        'score': TextSytle(fontsize=24, x=1153, y=54),
        'time': TextSytle(fontsize=24, x=697, y=72),
        'viewbox': BoxStyle(width=1240, height=650, x=100, y=200)
    },
}

viewbox_settings = {
    'level1': {
        'is_static': True,
        'viewbox': [1500, 2700, 1200, 1900]
    },
}

connection_settings = {
    'max_num': 15,
    'max_num_per_collision': 5,
}

house_settings = {
    'map_size': SizeStyle(width=4485, height=3968),
    'img_size': SizeStyle(width=32, height=44),
    'step': 5,
    'level1': {
        'game_time': 20 * 1000,  # 20 seconds
        'hit_delay': 1 * 1000,  # 1 second
        'player_name_location': TextSytle(fontsize=12, x=-17, y=-10),
        'player_img_size': SizeStyle(width=32, height=44),
        'player_img_location': LocationStyle(x=200, y=300),
        'people': [
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man01.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man02.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man03.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man04.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man05.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man06.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'location': None,
                'img': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man07.png')),
            },
        ]
    },
}
