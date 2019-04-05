from utils import Color, TextSytle, ImgStyle

### main
frame_rate = 20
get_player_img_method = 'cp'  # or 'scan'
scanline_cmd = '../tools/scanline'
player_name_template = 'Player-{:03d}'
player_img_dir = '../img/players/'
player_img_ext = 'jpeg'
text_color = Color(r=255, g=255, b=255)
time_color = Color(r=117, g=249, b=76)

# scan
scan_name_style = TextSytle(fontsize=42, x=610, y=135)

# confirm
confirm_name_style = TextSytle(fontsize=26, x=417, y=604)
confirm_img_style = ImgStyle(width=450, height=600, x=800, y=120)

# level1
level1_name_style = TextSytle(fontsize=24, x=165, y=54)
level1_score_style = TextSytle(fontsize=24, x=1153, y=54)
level1_time_style = TextSytle(fontsize=24, x=697, y=72)
level1_player_init_x = 800
level1_player_init_y = 700
level1_player_name_style = TextSytle(fontsize=12, x=-17, y=-10)
level1_timeout_millis = 20 * 1000  # 20 seconds
level1_hit_delay_millis = 1 * 1000  # 3 seconds

### game
# connection
max_connections = 15
max_connections_per_collision = 5

# map
blank_colors = [0, 16777215]

# person
default_step = 5
default_img_width, default_img_height = 32, 44
