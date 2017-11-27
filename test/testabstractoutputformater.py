import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from abstractoutputformater import AbstractOutputFormater

class TestAbstractOutputFormater(unittest.TestCase):

    def testAbstractPrinterInstanciation(self):
        with self.assertRaises(TypeError):
            c = AbstractOutputFormater()

if __name__ == '__main__':
    unittest.main()