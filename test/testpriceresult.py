import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from priceresult import PriceResult

class TestPriceResult(unittest.TestCase):
    def setUp(self):
        self.priceResult = PriceResult()


    def testInit(self):
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_CRYPTO), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_FIAT), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_PRICE_TIME_STAMP), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_PRICE), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_ERROR_MSG), None)

    def testIsEmpty(self):
        self.assertTrue(self.priceResult.isEmpty(self.priceResult.RESULT_KEY_CRYPTO))


    def testSetValue(self):
        self.priceResult.setValue(self.priceResult.RESULT_KEY_CRYPTO, 'USD')
        self.assertEqual(self.priceResult.getValue(self.priceResult.RESULT_KEY_CRYPTO), 'USD')


if __name__ == '__main__':
    unittest.main()