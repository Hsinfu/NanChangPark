


import layers
from constant import default_map_width, default_map_height, blank_colors
from connection import Connection

def get_box(p):
    return {
        'top': p.y + p.img.height,
        'bottom': p.y,
        'left': p.x,
        'right': p.x + p.img.width,
    }

def is_intersect(p1, p2):
    r1, r2 = get_box(p1), get_box(p2)
    return not (
        r1['right'] < r2['left'] or
        r1['left'] > r2['right'] or
        r1['top'] < r2['bottom'] or
        r1['bottom'] > r2['top']
    )

def is_intersect_ppl(p, ppl):
    for _p in ppl:
        if is_intersect(p, _p):
            return True
    return False

def is_intersect_map(p, map_wall):
    b = get_box(p)
    for wi in range(floor(b['left']), ceil(b['right'])):
        for hi in range(floor(b['bottom']), ceil(b['top'])):
            if map_wall[wi][hi] == 1:
                return True
    return False

def get_v_rebound(p1, p2):
    if p1.pre_x > p2.pre_x:
        x_dist = p1.pre_x - p2.pre_x - p2.img.width
    else:
        x_dist = p2.pre_x - p1.pre_x - p1.img.width

    if p1.pre_y > p2.pre_y:
        y_dist = p1.pre_y - p2.pre_y - p2.img.height
    else:
        y_dist = p2.pre_y - p1.pre_y - p1.img.height

    if x_dist < 0 and y_dist < 0:
        print('get_v_rebound both dist < 0')
        print('p1 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p1.pre_x, p1.pre_y, p1.pre_vx, p1.pre_vy, p1.x, p1.y, p1.vx, p1.vy))
        print('p2 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p2.pre_x, p2.pre_y, p2.pre_vx, p2.pre_vy, p2.x, p2.y, p2.vx, p2.vy))

    if x_dist < 0:
        return False, True

    if y_dist < 0:
        return True, False

    x_step = abs(p1.pre_vx - p2.pre_vx)
    y_step = abs(p1.pre_vy - p2.pre_vy)

    if x_step == 0:
        return False, True
    if y_step == 0:
        return True, False

    x_time = x_dist / x_step
    y_time = y_dist / y_step

    print('get_v_rebound both dist >= 0')
    print('p1 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p1.pre_x, p1.pre_y, p1.pre_vx, p1.pre_vy, p1.x, p1.y, p1.vx, p1.vy))
    print('p2 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p2.pre_x, p2.pre_y, p2.pre_vx, p2.pre_vy, p2.x, p2.y, p2.vx, p2.vy))
    if x_time > y_time:
        return True, False
    return False, True

def get_v_rebound_bg(p, map_wall):
    print('p (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p.pre_x, p.pre_y, p.pre_vx, p.pre_vy, p.x, p.y, p.vx, p.vy))

    b = get_box(p)

    def get_w_overlap(t='left'):
        w_range = range(floor(b['left']), ceil(b['right']))

        if t == 'right':
            w_range = reverse(w_range)

        for wi in w_range:
            for hi in range(floor(b['bottom']), ceil(b['top'])):
                if map_wall[wi][hi] == 1:
                    return wi

    def get_h_overlap(t='bottom'):
        h_range = range(floor(b['bottom']), ceil(b['top']))
        if t == 'top':
            h_range = reverse(h_range)

        for hi in h_range:
            for wi in range(floor(b['left']), ceil(b['right'])):
                if map_wall[wi][hi] == 1:
                    return hi

    x_collision = get_w_overlap('left') if p.vx > 0 else get_w_overlap('right')
    y_collision = get_h_overlap('bottom') if p.vy > 0 else get_h_overlap('top')

    # print('collision', x_collision, y_collision)

    if p.pre_vx > 0:
        x_dist = x_collision - (p.pre_x + p.img.width)
    else:
        x_dist = p.pre_x - x_collision

    if p.pre_vy > 0:
        y_dist = y_collision - (p.pre_y + p.img.height)
    else:
        y_dist = p.pre_y - y_collision

    if x_dist < 0 and y_dist < 0:
        print('both dist < 0 -> pre: ({}, {}), collision: ({}, {}), dist: ({}, {}), pre_v: ({}, {})'.format(p.pre_x, p.pre_y, x_collision, y_collision, x_dist, y_dist, p.pre_vx, p.pre_vy))
        return True, True

    if x_dist < 0:
        return False, True

    if y_dist < 0:
        return True, False

    x_time = x_dist / abs(p.pre_vx)
    y_time = y_dist / abs(p.pre_vy)

    print('both dist >= 0 -> pre: ({}, {}), collision: ({}, {}), dist: ({}, {}), pre_v: ({}, {}), time: ({}, {})'.format(p.pre_x, p.pre_y, x_collision, y_collision, x_dist, y_dist, p.pre_vx, p.pre_vy, x_time, y_time))

    if x_time > y_time:
        return True, False
    return False, True


class HouseMap:
    def __init__(self, map_img, bottom_img=None, top_img=None,
                 map_width=None, map_height=None):
        self.people = []
        self.connection = Connection()
        self.init_map(map_img, map_width, map_height)
        self.init_bg_imgs(bottom_img, top_img)

    def init_map(self, img, map_width=None, map_height=None):
        # init width, height, x, y
        self.map_width = map_width or default_map_width
        self.map_height = map_height or default_map_height
        self.map_x = (width - self.map_width) / 2
        self.map_y = (height - self.map_height) / 2

        # init img
        img.resize(self.map_width, self.map_height)
        self.map_img = img
        self.map_wall = [[1 if img.get(wi, hi) not in blank_colors else 0
                            for hi in range(img.height)] for wi in range(img.width)]

        # init pgs
        layers.pg_people = createGraphics(self.map_width, self.map_height)
        layers.pg_connections = createGraphics(self.map_width, self.map_height)

    def init_bg_imgs(self, bottom_img=None, top_img=None):
        if bottom_img:
            layers.pg_bottom = createGraphics(self.map_width, self.map_height)
            bottom_img.resize(self.map_width, self.map_height)
            self.bottom_img = bottom_img
        if top_img:
            layers.pg_top = createGraphics(self.map_width, self.map_height)
            top_img.resize(self.map_width, self.map_height)
            self.top_img = top_img

    def is_overlap_current_people(self, p):
        return is_intersect_ppl(p, self.people)

    def is_overlap_bg(self, p):
        return is_intersect_map(p, self.map_wall)

    def check_init_location_ok(self, p):
        if self.is_overlap_current_people(p):
            return False
        if self.is_overlap_bg(p):
            return False
        return True

    def add_person(self, p, max_retry=1000):
        for retry_i in range(max_retry):
            if self.check_init_location_ok(p):
                self.people.append(p)
                return
            else:
                print('retry add_person {} times'.format(retry_i))
                p.init_location()
        print('add_person failed!!')
        raise Exception

    def draw_pg_bottom(self):
        if self.bottom_img:
            layers.pg_bottom.beginDraw()
            layers.pg_bottom.clear()
            layers.pg_bottom.background(204)
            layers.pg_bottom.image(self.bottom_img, 0, 0)
            layers.pg_bottom.endDraw()
            image(layers.pg_bottom, self.map_x, self.map_y)

    def draw_pg_top(self):
        if self.top_img:
            layers.pg_top.beginDraw()
            layers.pg_top.clear()
            layers.pg_top.image(self.top_img, 0, 0)
            layers.pg_top.endDraw()
            image(layers.pg_top, self.map_x, self.map_y)

    def draw_pg_people(self):
        layers.pg_people.beginDraw()
        layers.pg_people.clear()
        for p in self.people:
            layers.pg_people.image(p.img, p.x, p.y)
        layers.pg_people.endDraw()
        image(layers.pg_people, self.map_x, self.map_y)

    def draw_pg_connections(self):
        layers.pg_connections.beginDraw()
        layers.pg_connections.clear()
        for con in self.connection.connects:
            c, p1, p1_coord, p2, p2_coord = con
            layers.pg_connections.stroke(c)
            layers.pg_connections.line(
                p1.x + p1_coord[1],
                p1.y + p1_coord[0],
                p2.x + p2_coord[1],
                p2.y + p2_coord[0],
            )
        layers.pg_connections.endDraw()
        image(layers.pg_connections, self.map_x, self.map_y)

    def draw(self):
        self.draw_pg_bottom()
        self.draw_pg_people()
        self.draw_pg_connections()
        self.draw_pg_top()

    def connect(self, p1, p2):
        self.connection.connect(p1, p2)

    def move(self):
        for p in self.people:
            p.move()

    def hit_rebound(self):
        people = [p for p in self.people]
        while len(people) > 0:
            p = people.pop()
            for pi in people:
                if is_intersect(p, pi):
                    vx_re, vy_re = get_v_rebound(p, pi)
                    if vx_re:
                        pi.set_vx_rebound()
                        p.set_vx_rebound()
                    if vy_re:
                        pi.set_vy_rebound()
                        p.set_vy_rebound()
                    self.connect(p, pi)

    def hit_rebound_bg(self):
        for p in self.people:
            if self.is_overlap_bg(p):
                vx_re, vy_re = get_v_rebound_bg(p, self.map_wall)
                if vx_re:
                    p.set_vx_rebound()
                if vy_re:
                    p.set_vy_rebound()

    def apply_rebound(self):
        for p in self.people:
            p.apply_rebound()

    def next(self):
        self.move()
        self.hit_rebound()
        self.hit_rebound_bg()
        self.apply_rebound()

    def next_draw(self):
        self.draw()
        self.next()

    def save(self):
        layers.pg_people.save('../layers/imgs_layer.png')
        layers.pg_connections.save('../layers/connections_layer.png')
