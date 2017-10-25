import os
import sys

from commandcrypto import CommandCrypto
from commanderror import CommandError
from commandprice import CommandPrice
from commandquit import CommandQuit
from configurationmanager import ConfigurationManager
from crypcompexchanges import CrypCompExchanges
from pricerequester import PriceRequester
from printer import Printer
from processor import Processor
from requester import Requester


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

        commandPrice = CommandPrice(proc, cm)
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
    sys.stdin = StringIO('btc usd 24/10/17 22:33 Bittrex' +
                         '\nbtc usd 24/10/017 22:33 Bittrex' +
                         '\nbtc usd 24/10/1 22:33 Bittrex' +
                         '\nbtc usd 23/10 2.56 bittrex' +
                         '\ngbyte btc 24/10/2017 22:33 Bittrex' +
                         '\ngbyte usd 24/10/2017 22:33 Bittrex' +
                         '\nbtc usd 0 Bittrex' +
                         '\ngbyte btc 0 Bittrex' +
                         '\nbtc usd 12/10/2017 12:00 Unknown' +
                         '\nbtc usd 12/10/2017 12:00 bittrex\nq\ny') #noticenq\ny to nicely quit the program

    # stdout = sys.stdout
    # if os.name == 'posix':
    #     FILE_PATH = '/sdcard/cryptoout.txt'
    # else:
    #     FILE_PATH = 'c:\\temp\\cryptoout.txt'
    # sys.stdout = open(FILE_PATH, 'w')

    c = Controller()
    c.run()

    sys.stdin = stdin
    #sys.stdout = stdout
