
window_width, window_height = 1200, 800
map_x, map_y, map_width, map_height = 500, 100, 600, 600
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


def get_vxm_vym(o1, o2):
    if o1.pre_x > o2.pre_x:
        x_dist = o1.pre_x - o2.pre_x - o2.img.width
    else:
        x_dist = o2.pre_x - o1.pre_x - o1.img.width

    if o1.pre_y > o2.pre_y:
        y_dist = o1.pre_y - o2.pre_y - o2.img.height
    else:
        y_dist = o2.pre_y - o1.pre_y - o1.img.height


    if x_dist < 0:
        return 1, -1

    if y_dist < 0:
        return -1, 1

    x_speed = abs(o1.pre_vx - o2.pre_vx)
    y_speed = abs(o1.pre_vy - o2.pre_vy)

    if x_speed == 0:
        return 1, -1
    if y_speed == 0:
        return -1, 1

    x_time = x_dist / x_speed
    y_time = y_dist / y_speed

    if x_time > y_time:
        return -1, 1
    return 1, -1


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
        connects.append((c, o1, o1_coord, o2, o2_coord))


class MovingObject:
    speed = 5

    def __init__(self, img):
        self.pre_x = 0
        self.pre_y = 0
        self.pre_vx = 0
        self.pre_vy = 0
        self.img = img
        self.x_l = pg1.width - self.img.width
        self.y_l = pg1.height - self.img.height
        self.init_location()
        self.init_speed()

    def init_location(self):
        self.x = random(self.x_l)
        self.y = random(self.y_l)
        self.pre_x = self.x
        self.pre_y = self.y

    def init_speed(self):
        w, h = self.img.width, self.img.height
        l = sqrt(w * w + h * h)
        # print(int(random(1)))
        self.vx = self.speed * random_positive_negative() * w / l
        self.vy = self.speed * random_positive_negative() * h / l
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


class Map:

    def __init__(self):
        self.points = []

    def is_overlap_other_points(self, p):
        for _p in self.points:
            if intersect(p, _p):
                return True
        return False

    def is_overlap_bg(self, p):
        b = get_box(p)
        for wi in range(floor(b['left']), ceil(b['right'])):
            for hi in range(floor(b['bottom']), ceil(b['top'])):
                if self.blank_map[wi][hi] == 0:
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
        self.blank_map = [[1 if bg_img.get(wi, hi) in blank_colors else 0 for hi in range(bg_img.height)] for wi in range(bg_img.width)]

    def next(self):
        for p in self.points:
            p.next()
        self.hit_rebound()

    def draw(self):
        rect(map_x-1, map_y-1, map_width+1, map_height+1)

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
                    vxm, vym = get_vxm_vym(p, pi)
                    pi.vx *= vxm
                    pi.vy *= vym
                    p.vx *= vxm
                    p.vy *= vym
                    connect(p, pi)

    def next_draw(self):
        self.next()
        self.draw()


my_map = Map()


def setup():
    size(window_width, window_height)

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
    loop()  # Holding down the mouse activates looping

def mouseReleased():
    noLoop()  # Releasing the mouse stops looping draw()

def keyPressed():
    # print("pressed %s %d" % (key, keyCode))
    pg1.save('layers/img_layer.png')
    pg2.save('layers/line_layer.png')
