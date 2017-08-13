import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requester import Requester

class TestRequester(unittest.TestCase):
    def setUp(self):
        self.requester = Requester()


if __name__ == '__main__':
    unittest.main()