from abc import ABCMeta
from abc import abstractmethod

class AbstractCommand(metaclass=ABCMeta):
    '''
    Classes derived from AbstractCommand implement the GOF AbstractCommand pattern.

    rawParmData stores the command data as the user entered it. Useful in case a
                meaningful error message has to be displayed.

    parsedParmData stores a dictionary of elements parsed from the rawParmData.
    Ex: {CRYPTO:[]}
    '''

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        self.receiver = receiver
        self.rawParmData = rawParmData
        self.parsedParmData = parsedParmData
        self.name = name # used as key in a AbstractCommand dictionary


    def resetData(self):
        '''
        Ensure that internal parsedParmData is purged of previous value since command is reused
        :return:
        '''
        self.rawParmData = ''
        if len(self.parsedParmData) != 0:
            self.parsedParmData = self.parsedParmData.fromkeys(self.parsedParmData.keys())


    @abstractmethod
    def execute(self):
        pass
