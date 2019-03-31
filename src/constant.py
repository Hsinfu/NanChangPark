from utils import Color, TextSytle, ImgStyle

### main
frame_rate = 20
text_color = Color(r=255, g=255, b=255)

# scan
scan_name_style = TextSytle(fontsize=42, x=610, y=135)

# confirm
confirm_name_style = TextSytle(fontsize=26, x=417, y=604)
confirm_img_style = ImgStyle(width=450, height=600, x=800, y=120)

# level1
level1_name_style = TextSytle(fontsize=24, x=165, y=80)
level1_score_style = TextSytle(fontsize=24, x=1153, y=80)
level1_user_init_x = 800
level1_user_init_y = 700
level1_user_name_style = TextSytle(fontsize=12, x=-17, y=-10)

### game
# connection
max_connections = 15
max_connections_per_collision = 5

# map
# default_map_width, default_map_height = 1920, 1080
default_map_width, default_map_height = 1440, 900
blank_colors = [0, 16777215]

# person
default_step = 5
default_img_width, default_img_height = 32, 44
