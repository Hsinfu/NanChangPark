import os
import pygame as pg
from collections import namedtuple


TextSytle = namedtuple('TextSytle', ['x', 'y', 'fontsize', 'color'])
AreaStyle = namedtuple('AreaStyle', ['x', 'y', 'width', 'height'])
LocationStyle = namedtuple('LocationStyle', ['x', 'y'])
SizeStyle = namedtuple('SizeStyle', ['width', 'height'])

### Static Path
VIRTUALENV = os.path.expanduser('~/.venv/NanChangPark/bin/python')
THIS_FILE_DIR = os.path.dirname(__file__)
INSTAGRAM_UPLOADER_PY = os.path.abspath(os.path.join(THIS_FILE_DIR, 'ig_upload.py'))
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
    'is_scanner_connected': False,  # or True
    'screen_size': SizeStyle(width=1440, height=810),
    'instagram_img_center_area': AreaStyle(x=0, y=239, width=1276, height=1276),
}

# layout
layout_settings = {
    'confirm': {
        'img_area': AreaStyle(x=524, y=100, width=390, height=540)
    },
    'intro1': {
        'press_a_delay_frames': game_settings['frame_rate'] * 3,  # 3 seconds
    },
    'intro2': {
        'press_a_delay_frames': game_settings['frame_rate'] * 3,  # 3 seconds
    },
    'intro3': {
        'press_a_delay_frames': game_settings['frame_rate'] * 3,  # 3 seconds
    },
    'level': {
        # 'name': TextSytle(fontsize=24, x=165, y=54),
        'score_font': TextSytle(x=1205, y=72, fontsize=42, color=pg.Color(255, 255, 255)),
        'time_font': TextSytle(x=660, y=80, fontsize=48, color=pg.Color(117, 249, 76)),
        'layout_location': LocationStyle(x=48, y=141),
        'hit_shake_range': 5,
    },
    'rank': {
        'player_name_fontstyle': TextSytle(x=-55, y=-20, fontsize=32, color=pg.Color(255, 255, 255)),
        'player_name_rectstyle': AreaStyle(x=-60, y=-22, width=165, height=40),
        'player_score_fontstyle': TextSytle(x=100, y=12, fontsize=32, color=pg.Color(255, 255, 255)),
        'rank_name_fontstyle': TextSytle(x=-35, y=-20, fontsize=28, color=pg.Color(255, 255, 255)),
        'rank_name_rectstyle': AreaStyle(x=-40, y=-22, width=160, height=35),
        'rank_score_fontstyle': TextSytle(x=58, y=12, fontsize=28, color=pg.Color(255, 255, 255)),

        'player_area': AreaStyle(x=91, y=96, width=365, height=506),
        'rank1_area': AreaStyle(x=517, y=247, width=257, height=355),
        'rank2_area': AreaStyle(x=823, y=247, width=257, height=355),
        'rank3_area': AreaStyle(x=1115, y=247, width=257, height=355),
    },
}

viewbox_settings = {
    'level1': {
        'is_static': True,
        'view_area': AreaStyle(x=778, y=846, width=1345, height=628)
    },
    'level2': {
        'is_static': False,
        'view_area': AreaStyle(x=101, y=143, width=1345, height=628)
    },
    'level3': {
        'is_static': False,
        'view_area': AreaStyle(x=225, y=1411, width=1345, height=628)
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
    'player_name_fontstyle': TextSytle(x=-28, y=-13, fontsize=18, color=pg.Color(255, 255, 255)),
    'player_name_rectstyle': AreaStyle(x=-32, y=-14, width=94, height=24),
    'level1': {
        'game_time': 30,  # 30 seconds
        'hit_delay': 0.5,  # 0.5 second
        'player_img_area': AreaStyle(x=1282, y=879, width=110, height=150),
        'add_person_max_retry': 1,
        'people': [
            {
                'frame_idx': 0,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
            {
                'frame_idx': game_settings['frame_rate'] * 1,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
            {
                'frame_idx': game_settings['frame_rate'] * 2,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
            {
                'frame_idx': game_settings['frame_rate'] * 3,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
            {
                'frame_idx': game_settings['frame_rate'] * 4,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
            {
                'frame_idx': game_settings['frame_rate'] * 5,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
            {
                'frame_idx': game_settings['frame_rate'] * 6,
                'added': False,
                'img_location': LocationStyle(x=1873, y=1067),
                'img_size': None,
            },
        ]
    },
    'level2': {
        'game_time': 30,  # 30 seconds
        'hit_delay': 0.5,  # 0.5 second
        'player_img_area': AreaStyle(x=719, y=382, width=110, height=150),
        'add_person_max_retry': 100,
        'people': [
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
        ],
    },
    'level3': {
        'game_time': 30,  # 30 seconds
        'hit_delay': 0.5,  # 0.5 second
        'player_img_area': AreaStyle(x=843, y=1650, width=110, height=150),
        'add_person_max_retry': 100,
        'people': [
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
            {
                'frame_idx': 0,
                'added': False,
                'img_location': None,
                'img_size': None,
            },
        ],
    },
}
