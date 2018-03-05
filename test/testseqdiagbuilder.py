import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
                              # the test is executed standalone

from seqdiagbuilder import SeqDiagBuilder
from controller import Controller
from pricerequester import PriceRequester

class TestSeqDiagBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def testInstanciateClassInitTwoArgs(self):
        className = 'Controller'
        moduleName = 'controller'

        instance = SeqDiagBuilder.instanciateClass(className, moduleName)

        self.assertIsInstance(instance, Controller)

    def testInstanciateClassInitNoArgs(self):
        className = 'PriceRequester'
        moduleName = 'pricerequester'

        instance = SeqDiagBuilder.instanciateClass(className, moduleName)

        self.assertIsInstance(instance, PriceRequester)


    def testBuildSeqDiagOnFullRequestHistoDayPrice(self):
        from datetimeutil import DateTimeUtil
        from utilityfortest import UtilityForTest
        from configurationmanager import ConfigurationManager
        from guioutputformater import GuiOutputFormater
        from controller import Controller

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        self.controller = Controller(GuiOutputFormater(configMgr), configMgr)

        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestYearStr = eightDaysBeforeYearStr
        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        inputStr = 'mcap btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = eightDaysBeforeHourStr
            minuteStr = eightDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('mcap btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        SeqDiagBuilder.printSeqDiagCommands()


if __name__ == '__main__':
    unittest.main()
