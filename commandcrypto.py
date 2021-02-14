from abstractcommand import AbstractCommand

class CommandCrypto(AbstractCommand):
    """
    Currently not used by CryptoPricer. Will be develop to handle
    user commands of type
    oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave !
    """
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
