import os
import sys

from commandcrypto import CommandCrypto
from commanderror import CommandError
from commandprice import CommandPrice
from commandquit import CommandQuit
from configurationmanager import ConfigurationManager
from crypcompexchanges import CrypCompExchanges
from pricerequester import PriceRequester
from processor import Processor
from requester import Requester


class Controller:
    '''
    Instanciate the app component and
    control the rep loop
    '''
    
    def __init__(self, printer):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(FILE_PATH)
        self.priceRequester = PriceRequester()
        self.crypCompTranslator = CrypCompExchanges()
        self.processor = Processor(self.configMgr, self.priceRequester, self.crypCompTranslator)
        self.requester = Requester()

        self.commandPrice = CommandPrice(self.processor, self.configMgr)
        self.commandCrypto = CommandCrypto(self.processor)
        self.requester.commandPrice = self.commandPrice
        self.requester.commandCrypto = self.commandCrypto

        self.commandQuit = CommandQuit(sys)
        self.requester.commandQuit = self.commandQuit

        self.commandError = CommandError(None)
        self.requester.commandError = self.commandError

        self.printer = printer
        

    def run(self):
        '''
        Used essentially by the command line version of CryptoPricer.

        :return: nothing
        '''
        while True:
            command = self.requester.request()
            result = command.execute()

            if result != '':
                self.printer.printDataToConsole(result)


if __name__ == '__main__':
    import os
    from io import StringIO

    from consoleprinter import ConsolePrinter

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

    c = Controller(ConsolePrinter())
    c.run()

    sys.stdin = stdin
    #sys.stdout = stdout
