import time


class Clock:
    def __init__(self, seconds, enabled=False):
        self.timeout = seconds
        self.time_left = seconds
        self.start = None
        if enabled:
            self.resume()
        else:
            self.pause()

    @property
    def enabled(self):
        return self.start is not None

    @property
    def time_left_str(self):
        return '{:02.2f}'.format(self.time_left)

    def is_timeout(self, t=0):
        return self.time_left < t

    def pause(self):
        if self.enabled:
            self.start = None

    def resume(self):
        if not self.enabled:
            self.start = time.time()

    def tick(self):
        if self.enabled:
            current = time.time()
            pass_time = current - self.start
            self.start = current
            self.time_left -= pass_time
