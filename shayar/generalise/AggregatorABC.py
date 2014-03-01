__author__ = 'Nitin'
from abc import ABCMeta, abstractmethod
import threading


class AggregatorABC(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        self.aggregate(self.data)
        return self.data

    @abstractmethod
    def aggregate(self, data):
        pass