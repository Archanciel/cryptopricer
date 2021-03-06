import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from commanderror import CommandError
from resultdata import ResultData

class TestCommandError(unittest.TestCase):


    def testCommandErrorInstanciation(self):
        commandError = CommandError(None)
        commandError.requestInputString = "-c"
        commandError.parsedParmData[commandError.COMMAND_ERROR_TYPE_KEY] = commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
        commandError.parsedParmData[commandError.COMMAND_ERROR_MSG_KEY] = commandError.CRYPTO_SYMBOL_MISSING_MSG


        resultData = commandError.execute()
        self.assertEqual("ERROR - invalid partial request -c: crypto symbol missing.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


if __name__ == '__main__':
    unittest.main()