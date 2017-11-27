from abc import ABCMeta
from abc import abstractmethod

class AbstractPrinter(metaclass=ABCMeta):
    '''
    '''

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        pass


    @abstractmethod
    def printDataToConsole(self):
        '''
        Output formated data in the console
        :return: nothing
        '''
        pass


    @abstractmethod
    def getPrintableData(self):
        '''
        Return formated data ready to be output
        :return: nothing
        '''
        pass
