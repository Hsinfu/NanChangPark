import os
import pygame as pg
from collections import namedtuple


TextSytle = namedtuple('TextSytle', ['x', 'y', 'fontsize', 'color'])
BoxStyle = namedtuple('BoxStyle', ['x', 'y', 'width', 'height'])
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


### game
game_settings = {
    'game_title': 'NanChangPark Never Lock',
    'frame_rate': 24,
    'starting_scores': 100,
    'get_player_img_method': 'cp',  # or 'scan'
    'screen_size': SizeStyle(width=1440, height=900),
}

# layout
layout_settings = {
    'confirm': {
        'img': BoxStyle(x=516, y=100, width=407, height=620)
    },
    'level': {
        # 'name': TextSytle(fontsize=24, x=165, y=54),
        'score_font': TextSytle(x=1205, y=72, fontsize=42, color=pg.Color(255, 255, 255)),
        'time_font': TextSytle(x=660, y=80, fontsize=48, color=pg.Color(117, 249, 76)),
        'viewbox_location': LocationStyle(x=50, y=155),
        'hit_shake_range': 10,
    },
}

viewbox_settings = {
    'level1': {
        'is_static': True,
        # 'viewbox_area': BoxStyle(x=1300, y=2200, width=1345, height=700)
        'viewbox_area': BoxStyle(x=650, y=1100, width=1345, height=700)
    },
}

connection_settings = {
    'max_num': 15,
    'max_num_per_collision': 5,
    'line_width': 1,
}

house_settings = {
    # 'map_size': SizeStyle(width=4485, height=3968),
    'map_size': SizeStyle(width=2242, height=1984),
    'img_size': SizeStyle(width=32, height=44),
    'step': 5,
    'blank_color': pg.Color(0, 0, 0, 0),
    'level1': {
        'game_time': 20,  # 20 seconds
        'hit_delay': 1,  # 1 second
        'player_name_font': TextSytle(x=-17, y=-10, fontsize=12, color=pg.Color(255, 255, 255)),
        'player_img_box': BoxStyle(x=800, y=1400, width=32, height=44),
        # 'player_img_box': BoxStyle(x=2000, y=2000, width=32, height=44),
        'people': [
            {
                'frame_idx': 0,
                'added': False,
                'img_location': LocationStyle(x=850, y=1450),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man01.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man02.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man03.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man04.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man05.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man06.png')),
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man07.png')),
            },
        ]
    },
}
