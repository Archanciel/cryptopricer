from abstractcommand import AbstractCommand

class CommandCrypto(AbstractCommand):
    CRYPTO_LIST = "CRYPTO"
    UNIT_LIST = "UNIT"
    FLAG = "FLAG"

    def __init__(self, receiver = None):
        super().__init__(receiver, 'CommandCrypto')


    def initialiseParsedParmData(self):
        self.parsedParmData[self.CRYPTO_LIST] = None
        self.parsedParmData[self.UNIT_LIST] = None
        self.parsedParmData[self.FLAG] = None


    def execute(self):
        self.receiver.processCrypto(self.parsedParmData)


    def isValid(self):
        '''
        Return True if the command contains valid data and can be executed
        '''
        return True
