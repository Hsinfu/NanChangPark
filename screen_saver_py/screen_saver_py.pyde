screen_saver_py/screen_saver_py.pyde
max_connection = 2
speed = 5
# window_width, window_height = 1200, 800
map_x, map_y = 0, 0
map_width, map_height = 600, 600
obj_width, obj_height = 32, 44

# black_colors = [
#     -14477291,
# ]

blank_colors = [
    0,
    16777215,
]

def random_positive_negative():
    return 1 if random(1) > 0.5 else -1

def get_box(o):
    return {'top': o.y + o.img.height, 'bottom': o.y, 'left': o.x, 'right': o.x + o.img.width}

def intersect(o1, o2):
    r1 = get_box(o1)
    r2 = get_box(o2)
    return not (r1['right'] < r2['left'] or r1['left'] > r2['right'] or r1['top'] < r2['bottom'] or r1['bottom'] > r2['top'])

def getColorIdx(img, c):
    for h in range(img.height):
        for w in range(img.width):
            if img.pixels[h*img.width+w] == c:
                return h, w


def get_v_rebound(o1, o2):
    if o1.pre_x > o2.pre_x:
        x_dist = o1.pre_x - o2.pre_x - o2.img.width
    else:
        x_dist = o2.pre_x - o1.pre_x - o1.img.width

    if o1.pre_y > o2.pre_y:
        y_dist = o1.pre_y - o2.pre_y - o2.img.height
    else:
        y_dist = o2.pre_y - o1.pre_y - o1.img.height

    if x_dist < 0 and y_dist < 0:
        print('get_v_rebound both dist < 0')
        print('o1 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(o1.pre_x, o1.pre_y, o1.pre_vx, o1.pre_vy, o1.x, o1.y, o1.vx, o1.vy))
        print('o2 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(o2.pre_x, o2.pre_y, o2.pre_vx, o2.pre_vy, o2.x, o2.y, o2.vx, o2.vy))


    if x_dist < 0:
        return False, True

    if y_dist < 0:
        return True, False

    x_speed = abs(o1.pre_vx - o2.pre_vx)
    y_speed = abs(o1.pre_vy - o2.pre_vy)

    if x_speed == 0:
        return False, True
    if y_speed == 0:
        return True, False

    x_time = x_dist / x_speed
    y_time = y_dist / y_speed

    print('get_v_rebound both dist >= 0')
    print('o1 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(o1.pre_x, o1.pre_y, o1.pre_vx, o1.pre_vy, o1.x, o1.y, o1.vx, o1.vy))
    print('o2 (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(o2.pre_x, o2.pre_y, o2.pre_vx, o2.pre_vy, o2.x, o2.y, o2.vx, o2.vy))
    if x_time > y_time:
        return True, False
    return False, True


connect_num = {}
connects = []

def connect(o1, o2, max_num=5):
    s1 = set(o1.img.pixels)
    s2 = set(o2.img.pixels)
    ss = s1.intersection(s2)
    l = int(random(max_num))
    ss = sorted(ss, key=lambda x: random(1))
    # print('zzz', l, len(ss))
    for c in list(ss)[:l]:
        o1_coord = getColorIdx(o1.img, c)
        o2_coord = getColorIdx(o2.img, c)
        n = connect_num.get((o1, o2), 0)
        if n < max_connection:
            connects.append((c, o1, o1_coord, o2, o2_coord))
            connect_num[(o1, o2)] = n + 1

class MovingObject:
    def __init__(self, img):
        self.pre_x = 0
        self.pre_y = 0
        self.pre_vx = 0
        self.pre_vy = 0
        self.vx_rebound = False
        self.vy_rebound = False
        self.img = img
        self.x_l = pg1.width - self.img.width
        self.y_l = pg1.height - self.img.height
        self.init_location()
        self.init_speed()

    def init_location(self):
        self.x = floor(random(self.x_l))
        self.y = floor(random(self.y_l))
        # self.x = 186 # floor(random(self.x_l))
        # self.y = 276 # floor(random(self.y_l))
        self.pre_x = self.x
        self.pre_y = self.y

    def init_speed(self):
        w, h = self.img.width, self.img.height
        l = sqrt(w * w + h * h)
        # print(int(random(1)))
        # self.vx = speed * 1 * w / l
        # self.vy = speed * -1 * h / l
        self.vx = speed * random_positive_negative() * w / l
        self.vy = speed * random_positive_negative() * h / l
        # print('init vx:{}, vy:{}'.format(self.vx, self.vy))
        self.pre_vx = self.vx
        self.pre_vy = self.vy

    def next(self):
        self.pre_x = self.x
        self.pre_y = self.y
        self.pre_vx = self.vx
        self.pre_vy = self.vy
        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x *= -1
            self.vx *= -1

        if self.y < 0:
            self.y *= -1
            self.vy *= -1

        if self.x > self.x_l:
            self.x = 2 * self.x_l - self.x
            self.vx *= -1

        if self. y > self.y_l:
            self.y = 2 * self.y_l - self.y
            self.vy *= -1

        return self.x, self.y

    def set_vx_rebound(self):
        self.vx_rebound = True

    def set_vy_rebound(self):
        self.vy_rebound = True

    def apply_rebound(self):
        if self.vx_rebound:
            self.vx *= -1
            self.vx_rebound = False
        if self.vy_rebound:
            self.vy *= -1
            self.vy_rebound = False


class Map:

    def __init__(self):
        self.points = []

    def is_overlap_other_points(self, p):
        for _p in self.points:
            if intersect(p, _p):
                return True
        return False

    def get_v_rebound_bg(self, p):
        print('p (pre_x: {}, pre_y: {}, pre_vx: {}, pre_vy: {}, x: {}, y: {}, vx: {}, vy: {})'.format(p.pre_x, p.pre_y, p.pre_vx, p.pre_vy, p.x, p.y, p.vx, p.vy))

        b = get_box(p)

        def get_w_overlap(t='left'):
            w_range = range(floor(b['left']), ceil(b['right']))

            if t == 'right':
                w_range = reverse(w_range)

            for wi in w_range:
                for hi in range(floor(b['bottom']), ceil(b['top'])):
                    if self.bg_wall[wi][hi] == 1:
                        return wi

        def get_h_overlap(t='bottom'):
            h_range = range(floor(b['bottom']), ceil(b['top']))
            if t == 'top':
                h_range = reverse(h_range)

            for hi in h_range:
                for wi in range(floor(b['left']), ceil(b['right'])):
                    if self.bg_wall[wi][hi] == 1:
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
            return True, True
            print('both dist < 0 -> pre: ({}, {}), collision: ({}, {}), dist: ({}, {}), pre_v: ({}, {})'.format(p.pre_x, p.pre_y, x_collision, y_collision, x_dist, y_dist, p.pre_vx, p.pre_vy))

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

    def is_overlap_bg(self, p):
        b = get_box(p)
        # print('qweewq', p.x, p.y, p.img.width, p.img.height)
        for wi in range(floor(b['left']), ceil(b['right'])):
            for hi in range(floor(b['bottom']), ceil(b['top'])):
                if self.bg_wall[wi][hi] == 1:
                    return True
        return False

    def check_init_location_ok(self, p):
        if self.is_overlap_other_points(p):
            return False
        if self.is_overlap_bg(p):
            return False
        return True

    def add_point(self, p):
        while not self.check_init_location_ok(p):
            p.init_location()
        self.points.append(p)

    def add_bg(self, bg_img):
        self.bg_img = bg_img
        self.bg_wall = [[1 if bg_img.get(wi, hi) not in blank_colors else 0 for hi in range(bg_img.height)] for wi in range(bg_img.width)]

    def next(self):
        for p in self.points:
            p.next()
        self.hit_rebound()
        self.hit_rebound_bg()
        self.apply_rebound()

    def draw(self):
        pg0.beginDraw()
        pg0.clear()
        pg0.background(204)
        pg0.image(self.bg_img, 0, 0)
        pg0.endDraw()
        image(pg0, map_x, map_y)

        pg1.beginDraw()
        pg1.clear()
        for p in self.points:
            pg1.image(p.img, p.x, p.y)
        pg1.endDraw()
        image(pg1, map_x, map_y)
        pg2.beginDraw()
        pg2.clear()
        for con in connects:
            c, o1, o1_coord, o2, o2_coord = con
            pg2.stroke(c)
            pg2.line(
                o1.x + o1_coord[1],
                o1.y + o1_coord[0],
                o2.x + o2_coord[1],
                o2.y + o2_coord[0],
            )
        pg2.endDraw()
        image(pg2, map_x, map_y)

    def hit_rebound(self):
        points = [p for p in self.points]
        while len(points) > 0:
            p = points.pop()
            for pi in points:
                if intersect(p, pi):
                    vx_re, vy_re = get_v_rebound(p, pi)
                    if vx_re:
                        pi.set_vx_rebound()
                        p.set_vx_rebound()
                    if vy_re:
                        pi.set_vy_rebound()
                        p.set_vy_rebound()
                    connect(p, pi)

    def hit_rebound_bg(self):
        for p in self.points:
            if self.is_overlap_bg(p):
                vx_re, vy_re = self.get_v_rebound_bg(p)
                if vx_re:
                    p.set_vx_rebound()
                if vy_re:
                    p.set_vy_rebound()

    def apply_rebound(self):
        for p in self.points:
            p.apply_rebound()

    def next_draw(self):
        self.draw()
        self.next()


my_map = Map()


def setup():
    # size(window_width, window_height)
    fullScreen()

    global map_x, map_y
    map_x = (width - map_width) / 2
    map_y = (height - map_height) / 2

    global pg0, pg1, pg2
    pg0 = createGraphics(map_width, map_height)
    pg1 = createGraphics(map_width, map_height)
    pg2 = createGraphics(map_width, map_height)

    # add back ground image
    bg_img = loadImage("img/map_background.png")
    bg_img.resize(map_width, map_height)

    pxls = {}
    for p in bg_img.pixels:
        pxls[p] = 1 if p not in pxls else pxls[p] + 1

    p_most = max(pxls.iteritems(), key=lambda i: i[1])[0]
    print('bg_img pixel {} with the most num: {}'.format(p_most, pxls[p_most]))
    print('bg_img pixels', pxls)  # all pixels
    print('bg_img width {} height {}'.format(bg_img.width, bg_img.height))
    my_map.add_bg(bg_img)

    # add users
    w, h = obj_width, obj_height

    # add man01.png
    img = loadImage("img/man01.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    # add man02.png
    img = loadImage("img/man02.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    # add man03.png
    img = loadImage("img/man03.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    # add man04.png
    img = loadImage("img/man04.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    # add man05.png
    img = loadImage("img/man05.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    # add man06.png
    img = loadImage("img/man06.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    # add man07.png
    img = loadImage("img/man07.png")
    img.resize(w, h)
    my_map.add_point(MovingObject(img))

    noLoop()  # draw() will not loop

def draw():
    my_map.next_draw()

def mousePressed():
    print('mouseX: {}, mouseY: {}'.format(mouseX, mouseY))
    loop()  # Holding down the mouse activates looping

def mouseReleased():
    noLoop()  # Releasing the mouse stops looping draw()

def keyPressed():
    # print("pressed %s %d" % (key, keyCode))
    pg1.save('layers/img_layer.png')
    pg2.save('layers/line_layer.png')
