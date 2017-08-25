from abstractcommand import AbstractCommand

class CommandError(AbstractCommand):
    CRYPTO_SYMBOL_MISSING_MSG = 'crypto symbol missing'

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData=''):
        super().__init__(receiver, 'CommandError', rawParmData, parsedParmData)

    def execute(self):
        return "Error in input "  + self.rawParmData + ": " + self.parsedParmData[0] + " !"
