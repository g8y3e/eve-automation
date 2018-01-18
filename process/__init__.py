import abc


class Process:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        pass