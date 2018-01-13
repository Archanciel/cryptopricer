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


    def __str__(self):
        return 'Raw data: ' + str(self.rawParmData) + '\nParm data: ' + str(self.parsedParmData)
        
        
    @abstractmethod
    def initialiseParsedParmData(self):
        '''
        Prefill the parsedParmData dictionary with empty key/value pair.
        If this is not done, the parsedParmData dictionary will only contain
        key/value pairs added at the first use of the command. See CommandPrice
        for a more detailed explanation.
        :return:
        '''
        pass


    @abstractmethod
    def execute(self):
        pass


    @abstractmethod
    def isValid(self):
        '''
        Return True if the command contains valid data and can be executed
        '''
        pass
