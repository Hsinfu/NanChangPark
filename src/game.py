import layers
# from constant import default_map_width, default_map_height
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
        self.init(state)

    def init(self, state):
        print('init', state)
        self.state = state
        if state == STATE['level1']:
            self.timeout = 20
            self.init_map_level1()

    def init_map_level1(self):
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

    def try_load_user(self):
        try:
            user_img = loadImage('../img/user/user.png')
            self.init(STATE['confirm'])
        except Exception:
            pass

    def draw_start(self, state):
        # print('draw_start', state)
        layers.pg_start.beginDraw()
        layers.pg_start.clear()
        layers.pg_start.image(self.imgs[state], 0, 0)

        if state == STATE['scan']:
            layers.pg_start.textSize(42)
            layers.pg_start.text('Player-112', 610, 135)
            layers.pg_start.fill(0, 102, 153)
        elif state == STATE['confirm']:
            layers.pg_start.textSize(26)
            layers.pg_start.text('Player-112', 417, 604)
            layers.pg_start.fill(0, 102, 153)
            layers.pg_start.image(self.user_img, 800, 120)
        elif state == STATE['level1-description']:
            layers.pg_start.textSize(24)
            layers.pg_start.text('Player-112', 165, 80)
            layers.pg_start.fill(0, 102, 153)
            layers.pg_start.text('00000000', 1153, 80)
            layers.pg_start.fill(0, 102, 153)

        layers.pg_start.endDraw()
        image(layers.pg_start, 0, 0)

    def cp(self, level=1):
        if level == 1:
            i = int(random(7)) + 1
            f = '../img/level{}/man{:02d}.png'.format(level, i)
        command_line('cp {} ../img/user/user.png'.format(f))

    def load_user_img(self):
        img = loadImage('../img/user/user.png')
        img.resize(450, 600)
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
            STATE['level1-description'],
        ]:
            self.draw_start(self.state)
        else:
            self.map.next_draw()

    def key_pressed(self, key, keyCode):
        # print('key_pressed', key, keyCode, self.state)
        if self.state == STATE['welcome']:
            self.init(STATE['scan'])
        elif self.state == STATE['scan']:
            self.scan()
            self.init(STATE['confirm'])
        elif self.state == STATE['confirm']:
            if key == 'x':
                self.scan()
            if key == 'a':
                self.init(STATE['level1-description'])
        elif self.state == STATE['level1-description']:
            self.init(STATE['level1'])
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

