import pygame as pg

class Keyboard:
    def __init__(self):
        self.reset_keys()

    def reset_keys(self):
        self.keys = {
            pg.K_ESCAPE: False,
            pg.K_LEFT: False,
            pg.K_RIGHT: False,
            pg.K_DOWN: False,
            pg.K_UP: False,
            pg.K_a: False,
            pg.K_b: False,
        }

    def press(self, key):
        try:
            self.keys[key] = True
        except KeyError:
            pass

    def release(self, key):
        try:
            self.keys[key] = False
        except KeyError:
            pass

    def update(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                self.press(e.key)
            elif e.type == pg.KEYUP:
                self.release(e.key)

    def is_pressed(self, key):
        try:
            return self.keys[key]
        except KeyError:
            return False
