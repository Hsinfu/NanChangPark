from person import Person
from house import HouseMap


def setup():
    fullScreen()

    # init nan_chang_park
    global nan_chang_park
    nan_chang_park = HouseMap(
        map_img=loadImage("../img/bg_map.png"),
        bottom_img=loadImage("../img/bg_bottom.png"),
        top_img=loadImage("../img/bg_top.png"),
    )

    # add static people
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man01.png")
    ))
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man02.png")
    ))
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man03.png")
    ))
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man04.png")
    ))
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man05.png")
    ))
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man06.png")
    ))
    nan_chang_park.add_person(Person(
        img=loadImage("../img/man07.png")
    ))

    # draw() will not loop
    noLoop()


def draw():
    nan_chang_park.next_draw()


def mousePressed():
    # print('mouseX: {}, mouseY: {}'.format(mouseX, mouseY))
    # Holding down the mouse activates looping
    loop()


def mouseReleased():
    # Releasing the mouse stops looping draw()
    noLoop()


def keyPressed():
    # print("pressed %s %d" % (key, keyCode))
    nan_chang_park.save()
