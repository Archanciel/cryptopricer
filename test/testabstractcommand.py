import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from abstractcommand import AbstractCommand

class TestAbstractCommand(unittest.TestCase):

    def testAbstractCommandInstanciation(self):
        with self.assertRaises(TypeError):
            c = AbstractCommand(None, '', '')

if __name__ == '__main__':
    unittest.main()