import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from abstractprinter import AbstractPrinter

class TestAbstractPrinter(unittest.TestCase):

    def testAbstractPrinterInstanciation(self):
        with self.assertRaises(TypeError):
            c = AbstractPrinter()

if __name__ == '__main__':
    unittest.main()