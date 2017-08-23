from abstractcommand import AbstractCommand

class CommandError(AbstractCommand):
    def __init__(self, receiver, parmData = ''):
        super().__init__(receiver,'CommandError',parmData)
        self.errorMsgNoCryptoSymbol = 'crypto symbol missing'

    def execute(self):
        return "Error in input " + self.parmData[1] + ": " + self.parmData[0] + " !"
