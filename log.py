import time

from singleton import Singleton


class Log(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._start_time = 0

    def info(self, message):
        print(message)

    def init_time(self):
        self._start_time = time.time()

    def elapsed_time(self):
        return time.time() - self._start_time

log = Log()
