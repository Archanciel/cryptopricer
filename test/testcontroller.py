import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from controller import Controller
from commandprice import CommandPrice
from commandcrypto import CommandCrypto
from commandquit import CommandQuit
from commanderror import CommandError

'''
GBYTE/USD on Bittrex:  ERROR - e param is not valid the market does not exist for this coin pair
Enter command (h for help, q to quit)
BTC/USD on BitTrex:  25/10/17 00:39 5499.9
Enter command (h for help, q to quit)
GBYTE/BTC on BitTrex:  25/10/17 00:39 0.03331
Enter command (h for help, q to quit)
ERROR - Unknown market does not exist for this coin pair (BTC-USD)
Enter command (h for help, q to quit)
ERROR - exchange name does not respect required format: must start with an upper case
Enter command (h for help, q to quit)
Quit ? y/n 
'''
class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()


    # def testRunGetHistoMinutePrice(self):
    #     stdin = sys.stdin
    #     sys.stdin = StringIO('btc usd 24/10/2017 22:33 Bittrex' + \
    #                          '\ngbyte btc 24/10/2017 22:33 Bittrex' + \
    #                          '\ngbyte usd 24/10/2017 22:33 Bittrex' + \
    #                          '\nbtc usd 0 Bittrex' + \
    #                          '\ngbyte btc 0 Bittrex' + \
    #                          '\nbtc usd 12/10/2017 12:00 Unknown' + \
    #                          '\nbtc usd 12/10/2017 12:00 bittrex\nq\ny')
    #
    #     self.controller.run()
    #
    #     #capture stdout for your assert !
    #
    #     sys.stdin = stdin


if __name__ == '__main__':
    unittest.main()