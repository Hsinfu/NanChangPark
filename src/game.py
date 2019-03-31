import layers
from constant import (
    text_color,
    scan_name_style,
    confirm_name_style,
    confirm_img_style,
    level1_user_init_x,
    level1_user_init_y,
)
from person import Person
from house import HouseMap
from utils import command_line

STATE = {
    'welcome': 0,
    'scan': 0.1,
    'confirm': 0.2,
    'level1-description': 0.99,
    'level1': 1,
}


def get_state_img(n):
    for k, v in STATE.items():
        if n == v:
            img = loadImage('../img/{}.png'.format(k))
            img.resize(width, height)
            return img


class Game:
    def __init__(self, state=STATE['welcome']):
        layers.pg_start = createGraphics(width, height)
        self.imgs = {
            STATE['welcome']: get_state_img(STATE['welcome']),
            STATE['scan']: get_state_img(STATE['scan']),
            STATE['confirm']: get_state_img(STATE['confirm']),
            STATE['level1-description']: get_state_img(STATE['level1-description']),
        }
        self.state = state
        self.init_map_level1_called = 0
        self.user_idx = 1
        self.key_codes = {
            LEFT: False,
            RIGHT: False,
            DOWN: False,
            UP: False,
        }

    @property
    def user_name(self):
        return 'Player-{:03d}'.format(self.user_idx)

    def init_map_level1(self):
        if self.init_map_level1_called == 1:
            self._init_map_level1()
        self.init_map_level1_called += 1

    def _init_map_level1(self):
        self.map = HouseMap(
            map_img=loadImage("../img/level1/bg_map.png"),
            bottom_img=loadImage("../img/level1/bg_bottom.png"),
            top_img=loadImage("../img/level1/bg_top.png"),
        )

        self.map.set_user(Person(
            img=loadImage("../img/user/user.png"),
            init_x=level1_user_init_x,
            init_y=level1_user_init_y,
        ), self.user_name)

        # add static people
        self.map.add_person(Person(
            img=loadImage("../img/level1/man01.png")
        ))
        self.map.add_person(Person(
            img=loadImage("../img/level1/man02.png")
        ))
        self.map.add_person(Person(
            img=loadImage("../img/level1/man03.png")
        ))
        self.map.add_person(Person(
            img=loadImage("../img/level1/man04.png")
        ))
        self.map.add_person(Person(
            img=loadImage("../img/level1/man05.png")
        ))
        self.map.add_person(Person(
            img=loadImage("../img/level1/man06.png")
        ))
        self.map.add_person(Person(
            img=loadImage("../img/level1/man07.png")
        ))

    def draw_start(self, state):
        # print('draw_start', state)
        layers.pg_start.beginDraw()
        layers.pg_start.clear()
        layers.pg_start.image(self.imgs[state], 0, 0)

        if state == STATE['scan']:
            layers.pg_start.textSize(scan_name_style.fontsize)
            layers.pg_start.text(self.user_name, scan_name_style.x, scan_name_style.y)
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
        elif state == STATE['confirm']:
            layers.pg_start.textSize(confirm_name_style.fontsize)
            layers.pg_start.text(self.user_name, confirm_name_style.x, confirm_name_style.y)
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
            layers.pg_start.image(self.user_img, confirm_img_style.x, confirm_img_style.y)

        layers.pg_start.endDraw()
        image(layers.pg_start, 0, 0)

    def cp(self, level=1):
        if level == 1:
            i = int(random(7)) + 1
            f = '../img/level{}/man{:02d}.png'.format(level, i)
        command_line('cp {} ../img/user/user.png'.format(f))

    def load_user_img(self):
        img = loadImage('../img/user/user.png')
        img.resize(confirm_img_style.width, confirm_img_style.height)
        self.user_img = img

    def scan(self):
        self.cp()
        self.load_user_img()

    def next_draw(self):
        # print('next_draw', self.state)
        if self.state in [
            STATE['welcome'],
            STATE['scan'],
            STATE['confirm'],
        ]:
            self.draw_start(self.state)
        elif self.state == STATE['level1-description']:
            self.draw_start(self.state)
            self.init_map_level1()
        else:
            self.map.draw()
            self.map.move()
            self.map.hit_rebound_user()
            self.map.hit_rebound_people()
            self.map.hit_rebound_bg()
            self.set_user_dictection()
            self.map.apply_rebound()

    def set_user_dictection(self):
        def reverse_vx():
            if not self.map.user.vx_rebound:
                self.map.user.pre_vx = self.map.user.vx
                self.map.user.vx *= -1

        def reverse_vy():
            if not self.map.user.vy_rebound:
                self.map.user.pre_vy = self.map.user.vy
                self.map.user.vy *= -1

        # x direction
        if self.key_codes[LEFT] and self.key_codes[RIGHT]:
            pass
        elif self.key_codes[LEFT] and self.map.user.vx > 0:
            reverse_vx()
        elif self.key_codes[RIGHT] and self.map.user.vx < 0:
            reverse_vx()

        # y direction
        if self.key_codes[DOWN] and self.key_codes[UP]:
            pass
        elif self.key_codes[DOWN] and self.map.user.vy < 0:
            reverse_vy()
        elif self.key_codes[UP] and self.map.user.vy > 0:
            reverse_vy()

    def key_pressed(self, key, key_code):
        # print('key_pressed', key, key_code, self.state)
        if self.state == STATE['welcome']:
            self.state = STATE['scan']
        elif self.state == STATE['scan']:
            self.scan()
            self.state = STATE['confirm']
        elif self.state == STATE['confirm']:
            if key == 'x':
                self.scan()
            if key == 'a':
                self.state = STATE['level1-description']
        elif self.state == STATE['level1-description']:
            self.timeout = 20
            self.state = STATE['level1']
        elif self.state == STATE['level1']:
            if key == 's':
                self.map.save()
            if key_code in [LEFT, RIGHT, DOWN, UP]:
                self.key_codes[key_code] = True

    def key_released(self, key, key_code):
        if self.state == STATE['level1']:
            if key_code in [LEFT, RIGHT, DOWN, UP]:
                self.key_codes[key_code] = False
