import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from commandquit import CommandQuit

class TestCommandQuit(unittest.TestCase):

    def testAbstractCommandInstanciation(self):
        commandQuit = CommandQuit(sys)
        stdin = sys.stdin
        sys.stdin = StringIO("y")

        with self.assertRaises(SystemExit):
            commandQuit.execute()

        sys.stdin = stdin

if __name__ == '__main__':
    unittest.main()