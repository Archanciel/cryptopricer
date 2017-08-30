import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from commanderror import CommandError

class TestCommandError(unittest.TestCase):

    def testCommandErrorInstanciation(self):
        commandError = CommandError(None)
        commandError.rawParmData = "invalid user input"
        commandError.parsedParmData = [commandError.CRYPTO_SYMBOL_MISSING_MSG]
        self.assertEquals("Error in input invalid user input: crypto symbol missing !", commandError.execute())

if __name__ == '__main__':
    unittest.main()