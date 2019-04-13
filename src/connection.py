import random
from constant import connection_settings


class Connection:
    def __init__(self):
        self.connect_num = {}
        self.connects = []

    @staticmethod
    def get_img_color_idx(img, c):
        for h in range(img.height):
            for w in range(img.width):
                if img.pixels[h*img.width+w] == c:
                    return h, w

    def connect(self, p1, p2, max_num=connection_settings['max_num_per_collision']):
        """
            p1 (Person)
            p2 (Person)
            max_num (int, optional, default connection_settings['max_num_per_collision']
        """
        s1 = set(p1.img.pixels)
        s2 = set(p2.img.pixels)
        ss = s1.intersection(s2)

        num = int(random.randrange(max_num))
        ss = sorted(ss, key=lambda x: random.random(1))

        for c in list(ss)[:num]:
            p1_coord = self.get_img_color_idx(p1.img, c)
            p2_coord = self.get_img_color_idx(p2.img, c)
            n = self.connect_num.get((p1, p2), 0)
            if n < connection_settings['max_num']:
                self.connects.append((c, p1, p1_coord, p2, p2_coord))
                self.connect_num[(p1, p2)] = n + 1
