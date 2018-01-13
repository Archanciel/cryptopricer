import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from resultdata import ResultData

class TestResultData(unittest.TestCase):
    def setUp(self):
        self.resultData = ResultData()


    def testInit(self):
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_FIAT), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE_TIME_STAMP), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE_VALUE_FIAT), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE_VALUE_CRYPTO), None)
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_PRICE_VALUE_SAVE), None)


    def testIsEmpty(self):
        self.assertTrue(self.resultData.isEmpty(self.resultData.RESULT_KEY_CRYPTO))


    def testSetValue(self):
        self.resultData.setValue(self.resultData.RESULT_KEY_CRYPTO, 'USD')
        self.assertEqual(self.resultData.getValue(self.resultData.RESULT_KEY_CRYPTO), 'USD')


if __name__ == '__main__':
    unittest.main()