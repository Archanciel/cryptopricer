from abstractcommand import AbstractCommand

class CommandQuit(AbstractCommand):
    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData=''):
        super().__init__(receiver, 'CommandQuit', rawParmData, parsedParmData)


    def _initialiseParsedParmData(self):
        pass


    def execute(self):
        inp = input('Quit ? y/n ')

        if inp.upper() == 'Y':
            self.receiver.exit(0)

        return ''
