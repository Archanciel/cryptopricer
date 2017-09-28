import sys
from requester import Requester
from processor import Processor
from printer import Printer
from commandprice import CommandPrice
from commandcrypto import CommandCrypto
from commandquit import CommandQuit
from commanderror import CommandError
from pricerequester import PriceRequester
from configurationmanager import ConfigurationManager

class Controller:
    '''
    Instanciate the app component and
    control the rep loop
    '''

    def run(self):
        configMgr = ConfigurationManager()
        pr = PriceRequester(configMgr)
        req = Requester()
        proc = Processor(pr)
        pri = Printer()

        commandPrice = CommandPrice(proc)
        commandCrypto = CommandCrypto(proc)
        req.commandPrice = commandPrice
        req.commandCrypto = commandCrypto

        commandQuit = CommandQuit(sys)
        req.commandQuit = commandQuit

        commandError = CommandError(None)
        req.commandError = commandError

        while True:
            command = req.request()
            result = command.execute()

            if result != '':
                pri.print(result)

            # if CommandDataEnum.QUIT in command:
            #     input('Quit ?')
            #     sys.exit(0)
            # elif command == commandCrypto:
            #     result = proc.execute(command)
            #     pri.print(result)
            # elif CommandDataEnum.ERROR in command:
            #     print("Error in input")
            # else:
            #     raise ValueError('Invalid command encountered: ' + command)
            
if __name__ == '__main__':
    c = Controller()
    c.run()