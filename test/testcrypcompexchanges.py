import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from crypcompexchanges import CrypCompExchanges

class TestCrypCompExchanges(unittest.TestCase):
    def setUp(self):
        self.crypCompExchanges = CrypCompExchanges()


    def testGetExchange(self):
        exch = self.crypCompExchanges.getExchange('bittrex')
        self.assertEqual('BitTrex', exch)


    def testGetExchangeAll(self):
        exch = self.crypCompExchanges.getExchange('all')
        self.assertEqual('CCCAGG', exch)


    def testGetExchangeCCCAGG(self):
        exch = self.crypCompExchanges.getExchange('cccagg')
        self.assertEqual('CCCAGG', exch)


if __name__ == '__main__':
    unittest.main()