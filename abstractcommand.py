from abc import ABCMeta
from abc import abstractmethod

class AbstractCommand(metaclass=ABCMeta):
    '''
    Classes derived from AbstractCommand implement the GOF AbstractCommand pattern
    '''

    def __init__(self, receiver = None, name = '', parmData = ''):
        self.receiver = receiver
        self.parmData = parmData
        self.name = name # used as key in a AbstractCommand dictionary

    @property
    def parmData(self):
        return self.__parmData

    @parmData.setter
    def parmData(self, parmData):
        self.__parmData = parmData

    @abstractmethod
    def execute(self):
        pass
