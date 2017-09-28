import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager


class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        self.configMgr = ConfigurationManager()

    def testConfigurationManagerInstanciation(self):
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')


if __name__ == '__main__':
    unittest.main()
