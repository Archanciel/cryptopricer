import sys, os
from requester import Requester
from processor import Processor
from printer import Printer
from commandprice import CommandPrice
from commandcrypto import CommandCrypto
from commandquit import CommandQuit
from commanderror import CommandError
from pricerequester import PriceRequester
from configurationmanager import ConfigurationManager
from crypcompexchanges import CrypCompExchanges

class Controller:
    '''
    Instanciate the app component and
    control the rep loop
    '''

    def run(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        cm = ConfigurationManager(FILE_PATH)
        pr = PriceRequester()
        cryp = CrypCompExchanges()
        proc = Processor(cm, pr, cryp)
        req = Requester()
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
    import os
    from io import StringIO

    stdin = sys.stdin
    sys.stdin = StringIO('btc usd 12/10/2017 12:00 CCCAGG' + \
                         '\nbtc usd 12/10/2017 12:00 Unknown' + \
                         '\nbtc usd 12/10/2017 12:00 unknown')

    c = Controller()
    c.run()

    sys.stdin = stdin
