import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager


class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            self.filePath = '/sdcard/cryptopricer.ini'
        else:
            self.filePath = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(self.filePath)


    def testConfigurationManagerInstanciation(self):
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')


    def testConfigurationManagerInstanciationNoConfigFile(self):
        os.remove(self.filePath)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')


    def testConfigurationManagerInstanciationEmptyConfigFile(self):
        open(self.filePath, 'w').close()
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')


if __name__ == '__main__':
    unittest.main()
