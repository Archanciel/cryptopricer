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


    def testConfigurationManagerInstanciation(self):
        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')
        
        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')


    def testConfigurationManagerInstanciationNoConfigFile(self):
        os.remove(self.filePath)
        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')
        
        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')


    def testConfigurationManagerInstanciationEmptyConfigFile(self):
        open(self.filePath, 'w').close()
        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')
        
        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')


    def testConfigurationManagerInstanciationOneMissingKey(self):
        #removing first line in config file
        with open(self.filePath, 'r') as configFile:
            lines = configFile.readlines()
            lines = lines[1:]

        with open(self.filePath, 'w') as configFile:
            configFile.write(''.join(lines))

        self.configMgr = ConfigurationManager(self.filePath)
        self.assertEqual(self.configMgr.localTimeZone, 'Europe/Zurich')
        self.assertEqual(self.configMgr.dateTimeFormat, 'DD/MM/YY HH:mm')
        self.assertEqual(self.configMgr.dateOnlyFormat, 'DD/MM/YY')
        
        if os.name == 'posix':
            self.assertEqual(self.configMgr.dataPath, '/sdcard')
        else:
            self.assertEqual(self.configMgr.dataPath, 'c:\\temp')


if __name__ == '__main__':
    unittest.main()
