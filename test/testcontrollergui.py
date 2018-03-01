import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
                              # the test is executed standalone

import re
from controller import Controller
from datetimeutil import DateTimeUtil
from guioutputformater import GuiOutputFormater
from configurationmanager import ConfigurationManager
from utilityfortest import UtilityForTest


class TestControllerGui(unittest.TestCase):
    '''
    This test class is launched from allguy.py, the class that runs
    all the tests in Pydroid on Android.

    Test the Controller using a GuiOuputFormater in place of a ConsoleOutputFormaater
    since GuiOuputFormater runs on Android in Pydroid, but fails in QPython !

    All the test cases are defineed in the TestController parent to avoid code duplication
    '''
    def setUp(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        self.controller = Controller(GuiOutputFormater(configMgr), configMgr)


    @unittest.skip
    def testControllerAskRTWithValueSave(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all -vc0.01btc\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run() #will eat up what has been filled in stdin using StringIO above
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !


    def testGetPrintableResultForInputscenarioWithValueCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: value command
        inputStr = '-v10eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #third command: value save command
        inputStr = '-vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #fourth command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #fifth command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #sixth command: remove value command
        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithValueCommandV0InFullCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        yesterday = now.shift(days=-2)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price full command with save value command
        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #second command: RT price full command with remove value command. This is not usefull since
        #each time you enter a full command, you wioe out any previously entered command, as tested
        #by testGetPrintableResultForInputscenarioWithValueSaveCommandWipedOutByFullCommand() !
        inputStr = 'eth usd 0 bitfinex -v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithValueSaveCommandWipedOutByFullCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        yesterday = now.shift(days=-2)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price full command with save value command
        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #second command: RT price full command with remove value command. This is not usefull since
        #each time you enter a full command, you wioe out any previously entered command !
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithValueCommandAndError(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 bitfinex -vs10btc'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStr)
        self.assertEqual('btc usd 0 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)

        inputStr = '-feth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'PROVIDER ERROR - Bitfinex market does not exist for this coin pair (BTC-ETH)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-cxmr'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'PROVIDER ERROR - Bitfinex market does not exist for this coin pair (XMR-ETH)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-cbtc'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'PROVIDER ERROR - Bitfinex market does not exist for this coin pair (BTC-ETH)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-fusd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStr)
        self.assertEqual('btc usd 0 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyDateBegOfYear(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        requestYearStr = nowYearStr
        requestDayStr = '1'
        requestMonthStr = '1'
        requestArrowDate = DateTimeUtil.dateTimeComponentsToArrowLocalDate(int(requestDayStr), int(requestMonthStr), now.year, 0, 0, 0, timezoneStr)
        inputStr = 'mcap btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(requestArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = nowHourStr
            minuteStr = nowMinuteStr
            priceType = 'M'

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '0{}/0{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('mcap btc 0{}/0{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyValueCommandAfterAskHistoDay(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        requestYearStr = eightDaysBeforeYearStr
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

        inputStr = '-v12mcap'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('mcap btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifySaveValueCommandAfterAskHistoDay(self):
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

        inputStr = '-vs12mcap'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('mcap btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('mcap btc {}/{}/{} {}:{} all -vs12mcap'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyValueCommandAfterAskHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v12eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifySaveValueCommandAfterAskHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-vs12eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('eth btc {}/{}/{} {}:{} binance -vs12eth'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyValueCommandAfterAskHistoMinuteYearSupplied(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v12eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifySaveValueCommandAfterAskHistoMinuteYearSupplied(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-vs12eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('eth btc {}/{}/{} {}:{} binance -vs12eth'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTime(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayHistoDay(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        requestYearStr = eightDaysBeforeYearStr
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

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('mcap btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenValueCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value command
        inputStr = '-v10eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value save command
        inputStr = '-vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: remove value command
        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayHistoMinuteThenValueCommand(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = requestHourStr
            minuteStr = requestMinuteStr
            priceType = 'M'

        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value command
        inputStr = '-v10eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value save command
        inputStr = '-vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: remove value command
        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayHistoDayThenValueCommand(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        requestYearStr = eightDaysBeforeYearStr
        requestHourStr = eightDaysBeforeHourStr
        requestMinuteStr = eightDaysBeforeMinuteStr
        inputStr = 'eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr)

        if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = requestHourStr
            minuteStr = requestMinuteStr
            priceType = 'M'

        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value command
        inputStr = '-v10eth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value save command
        inputStr = '-vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: remove value command
        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForRealThenChangeTimeThenChangeCrypto(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        tenMinutesBeforeArrowDate = now.shift(minutes=-10)

        tenMinutesBeforeYearStr, tenMinutesBeforeMonthStr, tenMinutesBeforeDayStr, tenMinutesBeforeHourStr, tenMinutesBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenMinutesBeforeArrowDate)

        requestHourStr = tenMinutesBeforeHourStr
        requestMinuteStr = tenMinutesBeforeMinuteStr

        if DateTimeUtil.isDateOlderThan(tenMinutesBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = requestHourStr
            minuteStr = requestMinuteStr
            priceType = 'M'

        #next command: '-t' 10 minutes before
        inputStr = '-t{}:{}'.format(hourStr, minuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-ceth'
        inputStr = '-ceth'.format(hourStr, minuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidDayFormatAfterHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -d with invalid date format
        inputStr = '-d10:01'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 10:01 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidMonthFormatAfterHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -d with invalid date format
        inputStr = '-d10/O1'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: O1 violates format for month (DD/MM)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidYearFormatAfterHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -d with invalid date format
        inputStr = '-d1/1/20O1'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 20O1 violates format for year (DD/MM/YY)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidMinuteFormatAfterHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -t with invalid time format
        inputStr = '-t10:O1'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: O1 violates format for minute (HH:mm)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidMinuteValueAfterHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -t with invalid time format
        inputStr = '-t10:61'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - minute must be in 0..59', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidHourFormatAfterHistoMinute(self):
        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = fiveDaysBeforeHourStr
            minuteStr = fiveDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -t with invalid time format
        inputStr = '-t1O:01'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 1O violates format for hour (HH:mm)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenOneDigitDateSpec(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowBegOfMonth = now.replace(day = 1, hours = 0)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
        nowBegOfMonthYearStr, nowBegOfMonthMonthStr, nowBegOfMonthDayStr, nowBegOfMonthHourStr, nowBegOfMonthMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonth)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-d1'
        inputStr = '-d1'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(nowBegOfMonth, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = nowBegOfMonthHourStr
            minuteStr = nowBegOfMonthMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenTwoPartDateSpec(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowBegOfMonth = now.replace(day = 1, month = 1)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
        nowBegOfMonthYearStr, nowBegOfMonthMonthStr, nowBegOfMonthDayStr, nowBegOfMonthHourStr, nowBegOfMonthMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonth)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-d1'
        inputStr = '-d1/1'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(nowBegOfMonth, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = nowBegOfMonthHourStr
            minuteStr = nowBegOfMonthMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenThreePartDateSpec(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowBegOfMonthLastYear = now.replace(day = 1, month = 1, year = now.year - 1)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
        nowBegOfMonthLastYearYearStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearHourStr, nowBegOfMonthLastYearMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonthLastYear)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-d1'
        inputStr = '-d1/1/{}'.format(nowBegOfMonthLastYearYearStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(nowBegOfMonthLastYear, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = nowBegOfMonthLastYearHourStr
            minuteStr = nowBegOfMonthLastYearMinuteStr
            priceType = 'M'

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithInvalidValueCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 -vs10btc bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - full request btc usd 0 -vs10btc bitfinex violates format <crypto> <fiat> <date|time> <exchange> <opt commands>', printResult)
        self.assertEqual('', fullCommandStr) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithInvalidCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 all -ebitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported command -ebitfinex in request btc usd 0 all -ebitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removePriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStr) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        # then replay same request with no error
        inputStr = 'btc usd 0 all'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removePriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStr) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithValueCommandAndInvalidCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 all -vs100.2usd -ebitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported command -ebitfinex in request btc usd 0 all -vs100.2usd -ebitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removeAllPricesFromCommandValueResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStr)
        self.assertEqual('btc usd 0 all -vs100.2usd', fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithSaveValueCommandAndWarning(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        inputStr = '-cxmr'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'XMR/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('xmr usd 0 bitfinex', fullCommandStr)
        self.assertEqual('xmr usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        inputStr = '-fbtc'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'XMR/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R\nWARNING - price value symbol USD differs from both crypto (XMR) and fiat (BTC) of last request. -vs parameter ignored'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('xmr btc 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-ceth'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R\nWARNING - price value symbol USD differs from both crypto (ETH) and fiat (BTC) of last request. -vs parameter ignored'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithInvalidCommandInFullAndPartialRequests(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 all -zooo'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported command -zooo in request btc usd 0 all -zooo'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removePriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStr) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        # then replay same request with no error
        inputStr = '-feth -zooo'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/ETH on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported command -zooo in request -feth -zooo'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removePriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc eth 0 all', fullCommandStr) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultWithInvalidDateCommandAfterInvalidTimeCommandFollowingRealTimeRequest(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-t12.56'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid partial request -t12.56: in -t12.56, 12.56 must respect HH:mm format', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-d23:11'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 23:11 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultWithInvalidTimeCommandAfterInvalidDateCommandFollowingRealTimeRequest(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-d23:11'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 23:11 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-t12.56'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid partial request -t12.56: in -t12.56, 12.56 must respect HH:mm format', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: valid -e command
        inputStr = '-eall'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 23:11 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultWithInvalidDateAndTimePartialRequestCommandsFollowingRealTimeRequest(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-d{}:{} -t00.01'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid partial request -d{}:{} -t00.01: in -t00.01, 00.01 must respect HH:mm format'.format(requestDayStr, requestMonthStr), printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-t00:01'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: {}:{} violates format for day (DD/MM)'.format(requestDayStr, requestMonthStr), printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-d{}/{}'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} 00:01M'.format(requestDayStr, requestMonthStr, requestYearStr,
                                                               requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} 00:01 bitfinex'.format(requestDayStr, requestMonthStr, requestYearStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputscenarioWithValueCommandVAfterValueCommandVS(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        inputStr = '-v100usd'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -v100usd', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -v100usd', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForRealThenAddVSCommandAndChangeExchangeTimeCryptoDate(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        requestHourStr = threeDaysBeforeHourStr
        requestMinuteStr = threeDaysBeforeMinuteStr
        requestDayStr = threeDaysBeforeDayStr
        requestMonthStr = threeDaysBeforeMonthStr
        requestYearStr = threeDaysBeforeYearStr

        if DateTimeUtil.isDateOlderThan(threeDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = requestHourStr
            minuteStr = requestMinuteStr
            priceType = 'M'

        inputStr = '-vs100usd -eall -t{}:{} -ceth -d{}/{}'.format(requestHourStr, requestMinuteStr, requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStr)
        self.assertEqual('eth usd {}/{}/{} {}:{} all -vs100usd'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForRealThenChangeFiatExchangeTimeAddVSCommandAndChangeCryptoDate(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price command
        inputStr = 'btc usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        requestHourStr = threeDaysBeforeHourStr
        requestMinuteStr = threeDaysBeforeMinuteStr
        requestDayStr = threeDaysBeforeDayStr
        requestMonthStr = threeDaysBeforeMonthStr
        requestYearStr = threeDaysBeforeYearStr

        if DateTimeUtil.isDateOlderThan(threeDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = requestHourStr
            minuteStr = requestMinuteStr
            priceType = 'M'

        inputStr = '-fbtc -eall -t{}:{} -vs100eth -ceth -d{}/{}'.format(requestHourStr, requestMinuteStr, requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStr)
        self.assertEqual('eth btc {}/{}/{} {}:{} all -vs100eth'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForRealTimeWithMarketNotExistForCoinPairAndInvalidCommandCausingErrorAndWarning(self):
        #first command: RT price command
        inputStr = 'btc eth 0 binance -eall'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-ETH)\nWarning - unsupported command -eall in request btc eth 0 binance -eall', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForHistoMinuteWithMarketNotExistForCoinPairAndInvalidCommandCausingErrorAndWarning(self):
        #first command: RT price command
        inputStr = 'btc eth 0 binance -eall'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-ETH)\nWarning - unsupported command -eall in request btc eth 0 binance -eall', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        now = DateTimeUtil.localNow('Europe/Zurich')
        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        requestDayStr = threeDaysBeforeDayStr
        requestMonthStr = threeDaysBeforeMonthStr

        #second command: histo price command
        inputStr = 'btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-ETH)\nWarning - unsupported command -eall in request btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr), printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForHistoDayWithMarketNotExistForCoinPairAndInvalidCommandCausingErrorAndWarning(self):
        #first command: RT price command
        inputStr = 'btc eth 0 binance -eall'
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-ETH)\nWarning - unsupported command -eall in request btc eth 0 binance -eall', printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        now = DateTimeUtil.localNow('Europe/Zurich')
        tenDaysBeforeArrowDate = now.shift(days=-10)

        tenDaysBeforeYearStr, tenDaysBeforeMonthStr, tenDaysBeforeDayStr, tenDaysBeforeHourStr, tenDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenDaysBeforeArrowDate)

        requestDayStr = tenDaysBeforeDayStr
        requestMonthStr = tenDaysBeforeMonthStr

        #second command: histo price command
        inputStr = 'btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-ETH)\nWarning - unsupported command -eall in request btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr), printResult)
        self.assertEqual('', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeOnlyWithoutDateFullRequest(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #here, even if we request a price at now hour and now minute, the price returned is
        #not a RT price, but a histo minute price. We may request a price at 12:55 and we are
        #at 12:55:01 !
        inputStr = 'btc usd {}:{} bitfinex'.format(nowHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeAndDayOnlyFullRequest_3daysBefore(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == threeDaysBeforeMonthStr:
            # this test can only be performed after the 3rd day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 3 days before today - so, in the future
            # if we are between the 1st and the 3rd since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removePriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStr)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeAndDayOnlyFullRequest_8daysBefore(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        heightDaysBeforeArrowDate = now.shift(days=-8)

        heightDaysBeforeYearStr, heightDaysBeforeMonthStr, heightDaysBeforeDayStr, heightDaysBeforeHourStr, heightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(heightDaysBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(heightDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == heightDaysBeforeMonthStr:
            # this test can only be performed after the 8th day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 8 days before today - so, in the future
            # if we are between the 1st and the 8th since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'.format(heightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removePriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(heightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStr)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeAndDayOnlyFullRequest_1daysAfter(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        oneDaysAfterArrowDate = now.shift(days=1)

        oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

        oneYearBeforeArrowDate = now.shift(years=-1)

        oneYearBeforeYearStr, oneYearBeforeMonthStr, oneYearBeforeDayStr, oneYearBeforeHourStr, oneYearBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(oneDaysAfterDayStr, oneDaysAfterHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == oneDaysAfterMonthStr:
            # this test can only be performed on a day which is not the last day of the mnnth.
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to tomorrow - in the future can not be
            # run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr, oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterYearStr, nowHourStr, nowMinuteStr),
                UtilityForTest.removePriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysAfterDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStr)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)



#-------------------




    def testGetPrintableResultForTimeAndDayOnlyPartialRequest_3daysBefore(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        #here, even if we request a price at now hour and now minute, the price returned is
        #not a RT price, but a histo minute price. We may request a price at 12:55 and we are
        #at 12:55:01 !
        inputStr = 'btc usd {} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == threeDaysBeforeMonthStr:
            # this test can only be performed after the 3rd day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 3 days before today - so, in the future
            # if we are between the 1st and the 3rd since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removePriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStr)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeAndDayOnlyPartialRequest_8daysBefore(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        heightDaysBeforeArrowDate = now.shift(days=-8)

        heightDaysBeforeYearStr, heightDaysBeforeMonthStr, heightDaysBeforeDayStr, heightDaysBeforeHourStr, heightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(heightDaysBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(heightDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == heightDaysBeforeMonthStr:
            # this test can only be performed after the 8th day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 8 days before today - so, in the future
            # if we are between the 1st and the 8th since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'.format(heightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removePriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(heightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStr)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeAndDayOnlyPartialRequest_1daysAfter(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        oneDaysAfterArrowDate = now.shift(days=1)

        oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

        oneYearBeforeArrowDate = now.shift(years=-1)

        oneYearBeforeYearStr, oneYearBeforeMonthStr, oneYearBeforeDayStr, oneYearBeforeHourStr, oneYearBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(oneDaysAfterDayStr, oneDaysAfterHourStr, nowMinuteStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == oneDaysAfterMonthStr:
            # this test can only be performed on a day which is not the last day of the mnnth.
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to tomorrow - in the future can not be
            # run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr, oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterYearStr, nowHourStr, nowMinuteStr),
                UtilityForTest.removePriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysAfterDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStr)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


if __name__ == '__main__':
    unittest.main()
