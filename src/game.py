from person import Person
from house import HouseMap


class Game:
    def __init__(self, state=0):
        self.init(state)

    def init(self, state):
        self.state = state
        if state == 0:
            self.timeout = 20
            pass
        elif state == 1:
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
            self.init(state=1)
        except Exception:
            pass

    def next_draw(self):
        if self.state == 0:
            self.try_load_user()
        else:
            self.map.next_draw()

    def key_pressed(self, key):
        if key == 's':
            self.map.save()
