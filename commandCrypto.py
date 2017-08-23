from abstractcommand import AbstractCommand

class CommandCrypto(AbstractCommand):
    def __init__(self, receiver, parmData = ''):
        super().__init__(receiver,'CommandCrypto',parmData)

    def execute(self):
        self.receiver.processCrypto(self.parmData)
