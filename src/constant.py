import os
import pygame as pg
from collections import namedtuple


TextSytle = namedtuple('TextSytle', ['fontsize', 'x', 'y'])
BoxStyle = namedtuple('BoxStyle', ['width', 'height', 'x', 'y'])
LocationStyle = namedtuple('LocationStyle', ['x', 'y'])


### Static Path
THIS_FILE_DIR = os.path.dirname(__file__)
INSTAGRAM_ACCOUNT_PATH = os.path.abspath(os.path.join(THIS_FILE_DIR, '../instagram_account.json'))
GAME_RECORDS_PATH = os.path.abspath(os.path.join(THIS_FILE_DIR, '../record.json'))
IMAGES_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/'))
PLAYERS_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../players/'))
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

# connection
max_connections = 15
max_connections_per_collision = 5

# person
default_step = 5
default_img_width, default_img_height = 32, 44

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
        'map': BoxStyle(width=1240, height=650, x=100, y=200)
    },
}

viewbox_settings = {
    'level1': {
        'is_static': True,
        'viewbox': [1500, 2700, 1200, 1900]
    },
}

house_settings = {
    'level1': {
        'player_name_location': TextSytle(fontsize=12, x=-17, y=-10),
        'player_box': BoxStyle(width=default_img_width, height=default_img_height, x=200, y=300),
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
