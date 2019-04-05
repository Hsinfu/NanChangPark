import layers
from constant import (
    get_player_img_method,
    scanline_cmd,
    player_name_template,
    player_img_dir,
    player_img_ext,
    text_color,
    time_color,
    scan_name_style,
    confirm_name_style,
    confirm_img_style,
    level1_player_init_x,
    level1_player_init_y,
    level1_name_style,
    level1_score_style,
    level1_time_style,
    level1_timeout_millis,
)
from person import Person
from house import HouseMap
from utils import command_line
from clock import Clock

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
            STATE['level1']: get_state_img(STATE['level1'])
        }
        self.player_idx = 0
        self.init_game(state)

    def init_game(self, state):
        self.player_idx += 1
        self.init_map_level1_called = 0
        self.key_codes = {
            LEFT: False,
            RIGHT: False,
            DOWN: False,
            UP: False,
        }
        self.init_state(state)

    def init_state(self, state):
        self.state = state
        if state == STATE['level1']:
            self.game_clock = Clock(level1_timeout_millis)
        else:
            self.game_clock = Clock(0)

    @property
    def player_name(self):
        return player_name_template.format(self.player_idx)

    @property
    def player_img_fname(self):
        return '{}.{}'.format(self.player_name, player_img_ext)

    @property
    def player_img_fpath(self):
        return '{}{}'.format(player_img_dir, self.player_img_fname)

    def init_map_level1(self):
        if self.init_map_level1_called == 1:
            self._init_map_level1()
        self.init_map_level1_called += 1

    def _init_map_level1(self):
        self.map = HouseMap(
            map_img=loadImage("../img/level1/bg_map.png"),
            top_img=loadImage("../img/level1/bg_top.png"),
            start_move=False,
        )

        self.map.set_player(Person(
            img=loadImage(self.player_img_fpath),
            init_x=level1_player_init_x,
            init_y=level1_player_init_y,
        ), self.player_name)

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
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
            layers.pg_start.text(self.player_name, scan_name_style.x, scan_name_style.y)
        elif state == STATE['confirm']:
            layers.pg_start.textSize(confirm_name_style.fontsize)
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
            layers.pg_start.text(self.player_name, confirm_name_style.x, confirm_name_style.y)
            layers.pg_start.image(self.player_img, confirm_img_style.x, confirm_img_style.y)
        elif state == STATE['level1']:
            # name
            layers.pg_start.textSize(level1_name_style.fontsize)
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
            layers.pg_start.text(self.player_name, level1_name_style.x, level1_name_style.y)
            # score
            layers.pg_start.textSize(level1_score_style.fontsize)
            layers.pg_start.fill(text_color.r, text_color.g, text_color.b)
            layers.pg_start.text(self.map.score, level1_score_style.x, level1_score_style.y)
            # time
            layers.pg_start.textSize(level1_time_style.fontsize)
            layers.pg_start.fill(time_color.r, time_color.g, time_color.b)
            layers.pg_start.text(self.game_clock.time_left_str, level1_time_style.x, level1_time_style.y)

        layers.pg_start.endDraw()
        image(layers.pg_start, 0, 0)

    def cp(self, level=1):
        if level == 1:
            i = int(random(7)) + 1
            f = '../img/level{}/man{:02d}.png'.format(level, i)
        command_line('cp {} {}'.format(f, self.player_img_fpath))

    def load_player_img(self):
        img = loadImage(self.player_img_fpath)
        img.resize(confirm_img_style.width, confirm_img_style.height)
        self.player_img = img

    def scan(self):
        command_line('{} -verbose -flatbed -a4 -jpeg -dir {} -name {}'.format(
            scanline_cmd, player_img_dir, self.player_name))

    def do_scan(self):
        if get_player_img_method == 'cp':
            self.cp()
        elif get_player_img_method == 'scan':
            self.scan
        else:
            print('get_player_img_method error')
            raise Exception
        self.load_player_img()

    def next_draw(self):
        self.game_clock.tick()
        # game clock timeout
        if self.game_clock.is_timeout:
            if self.state == STATE['level1']:
                self.init_game(STATE['welcome'])

        # normal
        self.draw_start(self.state)
        if self.state == STATE['level1-description']:
            self.init_map_level1()
        elif self.state == STATE['level1']:
            self.map.draw()
            self.map.move()
            self.map.hit_rebound_player()
            self.map.hit_rebound_people()
            self.map.hit_rebound_bg()
            self.set_player_dictection()
            self.map.apply_rebound()

    def set_player_dictection(self):
        def reverse_vx():
            if not self.map.player.vx_rebound:
                self.map.player.pre_vx = self.map.player.vx
                self.map.player.vx *= -1

        def reverse_vy():
            if not self.map.player.vy_rebound:
                self.map.player.pre_vy = self.map.player.vy
                self.map.player.vy *= -1

        # x direction
        if self.key_codes[LEFT] and self.key_codes[RIGHT]:
            pass
        elif self.key_codes[LEFT] and self.map.player.vx > 0:
            reverse_vx()
        elif self.key_codes[RIGHT] and self.map.player.vx < 0:
            reverse_vx()

        # y direction
        if self.key_codes[DOWN] and self.key_codes[UP]:
            pass
        elif self.key_codes[DOWN] and self.map.player.vy < 0:
            reverse_vy()
        elif self.key_codes[UP] and self.map.player.vy > 0:
            reverse_vy()

    def key_pressed(self, key, key_code):
        # print('key_pressed', key, key_code, self.state)
        if self.state == STATE['welcome']:
            self.init_state(STATE['scan'])
        elif self.state == STATE['scan']:
            self.do_scan()
            self.init_state(STATE['confirm'])
        elif self.state == STATE['confirm']:
            if key == 'x':
                self.do_scan()
            if key == 'a':
                self.init_state(STATE['level1-description'])
        elif self.state == STATE['level1-description']:
            self.init_state(STATE['level1'])
        elif self.state == STATE['level1']:
            if key == 's':
                self.map.save()
            elif key == 'a':
                self.game_clock.resume()
                self.map.start_move = True
            elif key == 'b':
                self.game_clock.pause()
                self.map.start_move = False
            elif key_code in [LEFT, RIGHT, DOWN, UP]:
                self.key_codes[key_code] = True

    def key_released(self, key, key_code):
        if self.state == STATE['level1']:
            if key_code in [LEFT, RIGHT, DOWN, UP]:
                self.key_codes[key_code] = False
