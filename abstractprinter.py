from abc import ABCMeta
from abc import abstractmethod

class AbstractPrinter(metaclass=ABCMeta):
    '''
    '''

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        pass


    @abstractmethod
    def printData(self):
         pass

