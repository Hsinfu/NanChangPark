import os
import pygame as pg
from utils import TextSytle, ImgStyle, LocationStyle

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
screen_size = [1440, 900]
frame_rate = 24
get_player_img_method = 'cp'  # or 'scan'

# scan player img
confirm_img_style = ImgStyle(width=407, height=620, x=516, y=100)


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

# general level
level_name_style = TextSytle(fontsize=24, x=165, y=54)
level_score_style = TextSytle(fontsize=24, x=1153, y=54)
level_time_style = TextSytle(fontsize=24, x=697, y=72)
level_player_name_style = TextSytle(fontsize=12, x=-17, y=-10)

# level1
level1_player_location = LocationStyle(x=800, y=700)
