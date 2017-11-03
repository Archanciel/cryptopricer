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
            FILE_PATH = '/sdcard/currencypairs.txt'
        else:
            FILE_PATH = 'c:\\temp\\currencypairs.txt'

        self.currencyPairTester = CurrencyPairTester(FILE_PATH)


    def testInit(self):
        pass


if __name__ == '__main__':
    unittest.main()