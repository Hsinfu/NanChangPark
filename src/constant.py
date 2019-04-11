import os
from utils import Color, TextSytle, ImgStyle


THIS_FILE_DIR = os.path.dirname(__file__)
GAME_RECORDS_PATH = os.path.abspath(os.path.join(THIS_FILE_DIR, '../record.json'))
IMAGES_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/'))
PLAYERS_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../players/'))

# General
game_title = 'NanChangPark Never Lock'
scanline_cmd = os.path.abspath(os.path.join(THIS_FILE_DIR, '../tools/scanline'))
screen_size = [1440, 900]
frame_rate = 24

# game
starting_scores = 100
get_player_img_method = 'cp'  # or 'scan'
cp_sources_dir = os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/level1'))
player_img_dir = os.path.abspath(os.path.join(THIS_FILE_DIR, '../players'))
player_img_ext = 'jpeg'


# scan player img
confirm_img_style = ImgStyle(width=407, height=620, x=516, y=100)
