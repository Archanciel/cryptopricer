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


    def testSetGetWarning(self):
        commValWarningMsg = "test warning command value"
        futureDateWarningMsg = "test warning future date"

        self.resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE, commValWarningMsg)
        self.resultData.setWarning(ResultData.WARNING_TYPE_FUTURE_DATE, futureDateWarningMsg)

        self.assertEqual(commValWarningMsg, self.resultData.getWarningMessage(ResultData.WARNING_TYPE_COMMAND_VALUE))
        self.assertEqual(futureDateWarningMsg, self.resultData.getWarningMessage(ResultData.WARNING_TYPE_FUTURE_DATE))


    def testGetAllWarningMessages(self):
        commValWarningMsg = "test warning command value"
        futureDateWarningMsg = "test warning future date"

        self.resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE, commValWarningMsg)
        self.resultData.setWarning(ResultData.WARNING_TYPE_FUTURE_DATE, futureDateWarningMsg)

        self.assertEqual([commValWarningMsg, futureDateWarningMsg], self.resultData.getAllWarningMessages())


    def testContainsWarning(self):
        commValWarningMsg = "test warning command value"
        futureDateWarningMsg = "test warning future date"

        self.assertFalse(self.resultData.containsWarnings())

        self.resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE, commValWarningMsg)
        self.assertTrue(self.resultData.containsWarning(ResultData.WARNING_TYPE_COMMAND_VALUE))
        self.assertFalse(self.resultData.containsWarning(ResultData.WARNING_TYPE_FUTURE_DATE))

        self.resultData.setWarning(ResultData.WARNING_TYPE_FUTURE_DATE, futureDateWarningMsg)
        self.assertTrue(self.resultData.containsWarning(ResultData.WARNING_TYPE_FUTURE_DATE))


    def testOverwriteWarning(self):
        commValWarningMsgOne = "test warning command value one"
        futureDateWarningMsgOne = "test warning future date one"

        self.resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE, commValWarningMsgOne)
        self.resultData.setWarning(ResultData.WARNING_TYPE_FUTURE_DATE, futureDateWarningMsgOne)

        commValWarningMsgTwo = "test warning command value two"
        futureDateWarningMsgTwo = "test warning future date two"

        self.resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE, commValWarningMsgTwo)
        self.resultData.setWarning(ResultData.WARNING_TYPE_FUTURE_DATE, futureDateWarningMsgTwo)

        self.assertEqual(commValWarningMsgTwo, self.resultData.getWarningMessage(ResultData.WARNING_TYPE_COMMAND_VALUE))
        self.assertEqual(futureDateWarningMsgTwo, self.resultData.getWarningMessage(ResultData.WARNING_TYPE_FUTURE_DATE))


if __name__ == '__main__':
    unittest.main()