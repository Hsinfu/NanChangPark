import layers
from constant import (
    text_color,
    scan_name_style,
    confirm_name_style,
    confirm_img_style,
    level1_name_style,
    level1_score_style,
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
            layers.pg_start.text('Player-112', scan_name_style.x, scan_name_style.y)
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
        elif state == STATE['confirm']:
            layers.pg_start.textSize(confirm_name_style.fontsize)
            layers.pg_start.text('Player-112', confirm_name_style.x, confirm_name_style.y)
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
            self.map.next_draw()

    def key_pressed(self, key, keyCode):
        # print('key_pressed', key, keyCode, self.state)
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
            elif keyCode == LEFT:
                print('left')
            elif keyCode == RIGHT:
                print('right')
            elif keyCode == DOWN:
                print('down')
            elif keyCode == UP:
                print('up')

