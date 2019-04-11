import os


THIS_FILE_DIR = os.path.dirname(__file__)
GAME_RECORDS_PATH = os.path.abspath(os.path.join(THIS_FILE_DIR, '../record.json'))
IMAGES_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../imgs/'))
PLAYERS_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../players/'))

# General
game_title = 'NanChangPark Never Lock'
screen_size = [1440, 900]
frame_rate = 24

# game
starting_scores = 100