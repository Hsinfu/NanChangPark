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
PLAYER_IMG_EXT = 'jpg'


### game
game_settings = {
    'game_title': 'NanChangPark Never Lock',
    'frame_rate': 24,
    'starting_scores': 100,
    'get_player_img_method': 'scan',  # or 'scan'
    'screen_size': SizeStyle(width=1440, height=810),
}

# layout
layout_settings = {
    'confirm': {
        'img': BoxStyle(x=524, y=100, width=390, height=540)
    },
    'level': {
        # 'name': TextSytle(fontsize=24, x=165, y=54),
        'score_font': TextSytle(x=1205, y=72, fontsize=42, color=pg.Color(255, 255, 255)),
        'time_font': TextSytle(x=660, y=80, fontsize=48, color=pg.Color(117, 249, 76)),
        'viewbox_location': LocationStyle(x=48, y=141),
        'hit_shake_range': 5,
    },
    'rank': {
        'player_box': BoxStyle(x=66, y=96, width=369, height=507),
        'rank1': BoxStyle(x=386, y=246, width=259, height=356),
        'rank2': BoxStyle(x=616, y=246, width=259, height=356),
        'rank3': BoxStyle(x=835, y=246, width=259, height=356),
    },
}

viewbox_settings = {
    'level1': {
        'is_static': True,
        'viewbox_area': BoxStyle(x=778, y=846, width=1345, height=628)
    },
}

connection_settings = {
    'max_num': 15,
    'max_num_per_collision': 5,
    'line_width': 3,
}

house_settings = {
    'map_size': SizeStyle(width=2575, height=2279),
    'img_size': SizeStyle(width=110, height=150),
    'step': 20,
    'blank_color': pg.Color(255, 255, 255, 255),
    'level1': {
        'game_time': 40,  # 40 seconds
        'hit_delay': 0.5,  # 0.5 second
        'player_name_font': TextSytle(x=-17, y=-10, fontsize=12, color=pg.Color(255, 255, 255)),
        'player_img_box': BoxStyle(x=1282, y=879, width=110, height=150),
        'people': [
            {
                'frame_idx': 0,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man01.png')),
            },
            {
                'frame_idx': game_settings['frame_rate'] * 1,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man02.png')),
            },
            {
                'frame_idx': game_settings['frame_rate'] * 2,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man03.png')),
            },
            {
                'frame_idx': game_settings['frame_rate'] * 3,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man04.png')),
            },
            {
                'frame_idx': game_settings['frame_rate'] * 4,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man05.png')),
            },
            {
                'frame_idx': game_settings['frame_rate'] * 5,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man06.png')),
            },
            {
                'frame_idx': game_settings['frame_rate'] * 6,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
                'img_path': os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1/man07.png')),
            },
        ]
    },
    'level2': {
        'game_time': 40,  # 40 seconds
        'hit_delay': 0.5,  # 0.5 second
        'player_name_font': TextSytle(x=-17, y=-10, fontsize=12, color=pg.Color(255, 255, 255)),
        'player_img_box': BoxStyle(x=719, y=382, width=110, height=150),
        'people': [

        ],
    },
    'level3': {
        'game_time': 40,  # 40 seconds
        'hit_delay': 0.5,  # 0.5 second
        'player_name_font': TextSytle(x=-17, y=-10, fontsize=12, color=pg.Color(255, 255, 255)),
        'player_img_box': BoxStyle(x=843, y=1650, width=110, height=150),
        'people': [

        ],
    },
}
