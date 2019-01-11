def random_positive_negative():
    return 1 if random(1) > 0.5 else -1

def intersect(o1, o2):
    r1 = {'top': o1.y + o1.img.height, 'bottom': o1.y, 'left': o1.x, 'right': o1.x + o1.img.width}
    r2 = {'top': o2.y + o2.img.height, 'bottom': o2.y, 'left': o2.x, 'right': o2.x + o2.img.width}
    return not (r1['right'] < r2['left'] or r1['left'] > r2['right'] or r1['top'] < r2['bottom'] or r1['bottom'] > r2['top'])

def reverse(o):
    o.vx *= -1
    o.vy *= -1


def getColorIdx(img, c):
    for h in range(img.height):
        for w in range(img.width):
            if img.pixels[h*img.width+w] == c:
                return h, w

connects = []

def connect(o1, o2, max_num=5):
    s1 = set(o1.img.pixels)
    s2 = set(o2.img.pixels)
    ss = s1.intersection(s2)
    l = int(random(max_num))
    for c in list(ss)[:1]:
        o1_coord = getColorIdx(o1.img, c)
        o2_coord = getColorIdx(o2.img, c)
        connects.append((o1, o1_coord, o2, o2_coord))


class MovingObject:
    speed = 5

    def __init__(self, img):
        self.img = img
        self.x_l = width - self.img.width
        self.y_l = height - self.img.height
        self.init_location()
        self.init_speed()

    def init_location(self):
        self.x = random(self.x_l)
        self.y = random(self.y_l)

    def init_speed(self):
        w, h = self.img.width, self.img.height
        l = sqrt(w * w + h * h)
        # print(int(random(1)))
        self.vx = self.speed * random_positive_negative() * w / l
        self.vy = self.speed * random_positive_negative() * h / l
        # print('init vx:{}, vy:{}'.format(self.vx, self.vy))

    def next(self):
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

    def add_point(self, p):
        self.points.append(p)

    def next(self):
        for p in self.points:
            p.next()
        self.hit_rebound()

    def draw(self):
        pg1.beginDraw()
        pg1.background(204)
        for p in self.points:
            pg1.image(p.img, p.x, p.y)
        pg1.endDraw()
        image(pg1, 0, 0)
        pg2.beginDraw()
        # pg2.clear()
        for con in connects:
            o1, o1_coord, o2, o2_coord = con

            # pg2.stroke(255)
            pg2.line(
                o1.x + o1_coord[1],
                o1.y + o1_coord[0],
                o2.x + o2_coord[1],
                o2.y + o2_coord[0],
            )
        pg2.endDraw()
        image(pg2, 0, 0)

    def hit_rebound(self):
        points = [p for p in self.points]
        while len(points) > 0:
            p = points.pop()
            inter = False
            for pi in points:
                if intersect(p, pi):
                    reverse(pi)
                    connect(p, pi)
                    inter = True
            if inter:
                reverse(p)


    def next_draw(self):
        self.next()
        self.draw()


my_map = Map()
window_width, window_height = 800, 800


def setup():
    size(window_width, window_height)

    global pg1, pg2
    pg1 = createGraphics(window_width, window_height)
    pg2 = createGraphics(window_width, window_height)

    w, h = 96, 132

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

    noLoop()  # draw() will not loop

def draw():
    my_map.next_draw()

def mousePressed():
    loop()  # Holding down the mouse activates looping

def mouseReleased():
    noLoop()  # Releasing the mouse stops looping draw()
