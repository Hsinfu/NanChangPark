

class Clock:
    def __init__(self, milli_seconds, enabled=False):
        self.timeout = milli_seconds
        self.time_left = milli_seconds
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
        return '{:02.2f}'.format(self.time_left / 1000.0)

    @property
    def is_timeout(self):
        return self.time_left < 0

    def pause(self):
        if self.enabled:
            self.start = None

    def resume(self):
        if not self.enabled:
            self.start = millis()

    def tick(self):
        if self.enabled:
            current = millis()
            pass_time = current - self.start
            self.start = current
            self.time_left -= pass_time
