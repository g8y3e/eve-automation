import abc


class Mission:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        pass