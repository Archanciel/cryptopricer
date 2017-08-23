from abstractcommand import AbstractCommand

class CommandQuit(AbstractCommand):
    def __init__(self, receiver, parmData = ''):
        super().__init__(receiver,'CommandQuit',parmData)

    def execute(self):
        inp = input('Quit ? y/n ')

        if inp.upper() == 'Y':
            self.receiver.exit(0)

        return ''
