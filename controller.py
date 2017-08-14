import sys
from command import Command
from requester import Requester
from processor import Processor
from printer import Printer

class Controller:
    '''
    Instanciate the app component and
    control the rep loop
    '''

    def run(self):
        req = Requester()
        ex = Processor()
        pri = Printer()
        
        while True:
            commands = req.request()
            if Command.QUIT in commands:
                input('Quit ?')
                sys.exit(0)
            elif Command.CRYPTO in commands:
                result = ex.execute(commands)
                pri.print(result)
            else:
                raise ValueError('Invalid command encountered: ' + commands)
            
if __name__ == '__main__':
    c = Controller()
    c.run()