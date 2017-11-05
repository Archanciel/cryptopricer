import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from currencypairtester import CurrencyPairTester


class TestCurrencyPairTester(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            self.filepath = '/sdcard/currencypairs.txt'
        else:
            self.filepath = 'c:\\temp\\currencypairs.txt'

        #deleting currency pair file
        with open(self.filepath, 'w') as file:
            pass
            

    def testLoadFromEmptyFile(self):
        currencyPairTester = CurrencyPairTester(self.filepath)
        self.assertEqual(len(currencyPairTester.currencyPairDic.keys()), 0)


    def testAddEntryToEmptyFile(self):
        currencyPairTester = CurrencyPairTester(self.filepath)

        crypto = 'mcap'
        fiat = 'usd'
        exchange = 'ccex'
        
        self.assertFalse(currencyPairTester.isListed(crypto, fiat, exchange))
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)
        self.assertTrue(currencyPairTester.isListed(crypto, fiat, exchange))


    def testAddEntryToNonEmptyFile(self):
        currencyPairTester = CurrencyPairTester(self.filepath)

        crypto = 'mcap'
        fiat = 'usd'
        exchange = 'ccex'
        
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)
        currencyPairTester = None

        # recreating a CurrencyPairTester
        currencyPairTester = CurrencyPairTester(self.filepath)
        self.assertTrue(currencyPairTester.isListed(crypto, fiat, exchange))

        crypto = 'kmd'
        fiat = 'usd'
        exchange = 'bittrex'
        
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)
        self.assertTrue(currencyPairTester.isListed(crypto, fiat, exchange))

        with open(self.filepath, 'r') as ff:
            lines = ff.readlines()
            self.assertEqual(len(lines), 2)


    def testAddEntryTwiceToNonEmptyFile(self):
        currencyPairTester = CurrencyPairTester(self.filepath)

        crypto = 'mcap'
        fiat = 'usd'
        exchange = 'ccex'
        
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)
        currencyPairTester = None

        # recreating a CurrencyPairTester
        currencyPairTester = CurrencyPairTester(self.filepath)
        
        #adding same pair a second time
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)
   
        with open(self.filepath, 'r') as ff:
            lines = ff.readlines()
            self.assertEqual(len(lines), 1)


    def testAddEntryTwiceToEmptyFile(self):
        currencyPairTester = CurrencyPairTester(self.filepath)

        crypto = 'mcap'
        fiat = 'usd'
        exchange = 'ccex'
        
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)

        #adding same pair a second time
        currencyPairTester.addCurrencyPair(crypto, fiat, exchange)
   
        with open(self.filepath, 'r') as ff:
            lines = ff.readlines()
            self.assertEqual(len(lines), 1)


if __name__ == '__main__':
    unittest.main()
