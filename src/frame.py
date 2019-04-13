class Frame:
    def __init__(self, surface, imgs):
        self.idx = 0
        self.imgs = imgs
        self.num = len(imgs)
        self.surface = surface

    @property
    def img(self):
        return self.imgs[self.idx]

    @property
    def is_last_frame(self):
        return self.idx == self.num - 1

    def move(self):
        self.idx += 1
        self.idx %= self.num

    def draw(self, x=0, y=0):
        self.surface.blit(self.img, (x, y))

    def tick(self, x=0, y=0):
        self.draw(x, y)
        self.move()