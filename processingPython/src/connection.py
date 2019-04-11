
from constant import max_connections, max_connections_per_collision

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

    def connect(self, p1, p2, max_num=max_connections_per_collision):
        """
            p1 (Person)
            p2 (Person)
            max_num (int, optional, default max_connections_per_collision in constant.py)
        """
        s1 = set(p1.img.pixels)
        s2 = set(p2.img.pixels)
        ss = s1.intersection(s2)
        l = int(random(max_num))
        ss = sorted(ss, key=lambda x: random(1))

        for c in list(ss)[:l]:
            p1_coord = self.get_img_color_idx(p1.img, c)
            p2_coord = self.get_img_color_idx(p2.img, c)
            n = self.connect_num.get((p1, p2), 0)
            if n < max_connections:
                self.connects.append((c, p1, p1_coord, p2, p2_coord))
                self.connect_num[(p1, p2)] = n + 1
