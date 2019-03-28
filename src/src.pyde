from constant import frame_rate
from game import Game


def setup():
    fullScreen()
    frameRate(frame_rate)

    # init game
    global game
    game = Game()

    # draw() will not loop
    # noLoop()


def draw():
    game.next_draw()


# def mousePressed():
#     # print('mouseX: {}, mouseY: {}'.format(mouseX, mouseY))
#     # Holding down the mouse activates looping
#     loop()


# def mouseReleased():
#     # Releasing the mouse stops looping draw()
#     noLoop()


def keyPressed():
    # print("pressed %s %d" % (key, keyCode))
    game.key_pressed(key, keyCode)
