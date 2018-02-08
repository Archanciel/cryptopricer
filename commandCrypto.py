from abstractcommand import AbstractCommand

class CommandCrypto(AbstractCommand):
    CRYPTO_LIST = "CRYPTO"
    FIAT_LIST = "FIAT"
    FLAG = "FLAG"

    def __init__(self, receiver = None, rawParmData = '', parsedParmData = {}):
        super().__init__(receiver, 'CommandCrypto', rawParmData, parsedParmData)


    def initialiseParsedParmData(self):
        self.parsedParmData[self.CRYPTO_LIST] = None
        self.parsedParmData[self.FIAT_LIST] = None
        self.parsedParmData[self.FLAG] = None


    def execute(self):
        self.receiver.processCrypto(self.parsedParmData)


    def isValid(self):
        '''
        Return True if the command contains valid data and can be executed
        '''
        return True
