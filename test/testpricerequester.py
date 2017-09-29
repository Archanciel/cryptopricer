import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester


class TestPriceRequester(unittest.TestCase):
    def setUp(self):
        configMgr = ConfigurationManager()
        self.priceRequester = PriceRequester(configMgr)

    def testPriceRequesterInstanciation(self):
        self.assertIsInstance(self.priceRequester, PriceRequester)


if __name__ == '__main__':
    unittest.main()
