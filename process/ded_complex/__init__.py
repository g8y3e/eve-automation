import abc


class DEDComplex:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        pass