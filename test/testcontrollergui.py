import unittest
import os,sys,inspect
from io import StringIO

LOCAL_TIME_ZONE = 'Europe/Zurich'

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
from pricerequesterteststub import PriceRequesterTestStub
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
        self.controller = Controller(GuiOutputFormater(configMgr), configMgr, PriceRequesterTestStub())


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

        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !


    def testControllerBugSpecifyDateBegOfYear(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        requestYearStr = nowYearStr
        requestDayStr = '1'
        requestMonthStr = '1'
        requestArrowDate = DateTimeUtil.dateTimeComponentsToArrowLocalDate(int(requestDayStr), int(requestMonthStr), now.year, 0, 0, 0, timezoneStr)
        inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            'MCO/BTC on CCCAGG: ' + '0{}/0{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('mco btc 0{}/0{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)




    def testGetPrintableResultForReplayRealTime(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayHistoDay(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        requestYearStr = eightDaysBeforeYearStr
        inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            'MCO/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCO/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForRealThenChangeTimeThenChangeCrypto(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
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
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-ceth'
        inputStr = '-ceth'.format(hourStr, minuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
                                                               minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidDayFormatAfterHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -d with invalid date format
        inputStr = '-d10:01'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 10:01 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidMonthFormatAfterHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -d with invalid date format
        inputStr = '-d10/O1'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: O1 violates format for month (DD/MM)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidYearFormatAfterHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -d with invalid date format
        inputStr = '-d1/1/20O1'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 20O1 violates format for year (DD/MM/YY)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidMinuteFormatAfterHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -t with invalid time format
        inputStr = '-t10:O1'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: O1 violates format for minute (HH:mm)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidMinuteValueAfterHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -t with invalid time format
        inputStr = '-t10:61'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - minute must be in 0..59', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInvalidHourFormatAfterHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: -t with invalid time format
        inputStr = '-t1O:01'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 1O violates format for hour (HH:mm)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenOneDigitDateSpec(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowBegOfMonth = now.replace(day = 1, hours = 0)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
        nowBegOfMonthYearStr, nowBegOfMonthMonthStr, nowBegOfMonthDayStr, nowBegOfMonthHourStr, nowBegOfMonthMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonth)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-d1'
        inputStr = '-d1'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenTwoPartDateSpec(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowBegOfMonth = now.replace(day = 1, month = 1)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
        nowBegOfMonthYearStr, nowBegOfMonthMonthStr, nowBegOfMonthDayStr, nowBegOfMonthHourStr, nowBegOfMonthMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonth)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-d1'
        inputStr = '-d1/1'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForReplayRealTimeThenThreePartDateSpec(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowBegOfMonthLastYear = now.replace(day = 1, month = 1, year = now.year - 1)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
        nowBegOfMonthLastYearYearStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearHourStr, nowBegOfMonthLastYearMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonthLastYear)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '-d1'
        inputStr = '-d1/1/{}'.format(nowBegOfMonthLastYearYearStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputScenarioWithInvalidOption(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 all -ebitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported option -ebitfinex in request btc usd 0 all -ebitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        # then replay same request with no error
        inputStr = 'btc usd 0 all'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForInputScenarioWithInvalidOptionInFullAndPartialRequests(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 all -zooo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported option -zooo in request btc usd 0 all -zooo'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        # then replay same request with no error
        inputStr = '-ueth -zooo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/ETH on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported option -zooo in request -ueth -zooo'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc eth 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultWithInvalidDateCommandAfterInvalidTimeCommandFollowingRealTimeRequest(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-t12.56'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid partial request -t12.56: in -t12.56, 12.56 must respect HH:mm format', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-d23:11'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 23:11 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultWithInvalidTimeCommandAfterInvalidDateCommandFollowingRealTimeRequest(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-d23:11'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 23:11 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: invalid time command '-t12.56'
        inputStr = '-t12.56'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid partial request -t12.56: in -t12.56, 12.56 must respect HH:mm format', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next: valid -e command
        inputStr = '-eall'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: 23:11 violates format for day (DD/MM)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultWithInvalidDateAndTimePartialRequestCommandsFollowingRealTimeRequest(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-d{}:{} -t00.01'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid partial request -d{}:{} -t00.01: in -t00.01, 00.01 must respect HH:mm format'.format(requestDayStr, requestMonthStr), printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-t00:01'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - invalid value: {}:{} violates format for day (DD/MM)'.format(requestDayStr, requestMonthStr), printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-d{}/{}'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} 00:01M'.format(requestDayStr, requestMonthStr, requestYearStr,
                                                               requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} 00:01 bitfinex'.format(requestDayStr, requestMonthStr, requestYearStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForRealThenAddVSCommandAndChangeExchangeTimeCryptoDate(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
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
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth usd {}/{}/{} {}:{} all -vs100usd'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForRealThenChangeUnitExchangeTimeAddVSCommandAndChangeCryptoDate(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
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

        inputStr = '-ubtc -eall -t{}:{} -vs100eth -ceth -d{}/{}'.format(requestHourStr, requestMinuteStr, requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth btc {}/{}/{} {}:{} all -vs100eth'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr), fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForHistoMinuteWithMarketNotExistForCoinPairAndInvalidOptionCausingErrorAndWarning(self):
        #first command: RT price request
        inputStr = 'btc eth 0 binance -eall'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        self.assertEqual(
            'BTC/ETH on Binance: {}/{}/{} {}:{}R\nWarning - unsupported option -eall in request btc eth 0 binance -eall'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        requestDayStr = threeDaysBeforeDayStr
        requestMonthStr = threeDaysBeforeMonthStr

        #second command: histo minute price request
        inputStr = 'btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/ETH on Binance: {}/{}/{} 00:00M\nWarning - unsupported option -eall in request btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr, threeDaysBeforeYearStr, requestDayStr, requestMonthStr), UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc eth {}/{}/{} 00:00 binance'.format(requestDayStr, requestMonthStr, threeDaysBeforeYearStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForHistoDayWithMarketNotExistForCoinPairAndInvalidOptionCausingErrorAndWarning(self):
        #first command: RT price request
        inputStr = 'btc eth 0 binance -eall'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        self.assertEqual(
            'BTC/ETH on Binance: {}/{}/{} {}:{}R\nWarning - unsupported option -eall in request btc eth 0 binance -eall'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        tenDaysBeforeArrowDate = now.shift(days=-10)

        tenDaysBeforeYearStr, tenDaysBeforeMonthStr, tenDaysBeforeDayStr, tenDaysBeforeHourStr, tenDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenDaysBeforeArrowDate)

        requestDayStr = tenDaysBeforeDayStr
        requestMonthStr = tenDaysBeforeMonthStr

        #second command: histo day price request
        inputStr = 'btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/ETH on Binance: {}/{}/{} 00:00C\nWarning - unsupported option -eall in request btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr, tenDaysBeforeYearStr, requestDayStr, requestMonthStr), UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc eth {}/{}/{} 00:00 binance'.format(requestDayStr, requestMonthStr, tenDaysBeforeYearStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForTimeOnlyWithoutDateFullRequest(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #here, even if we request a price at now hour and now minute, the price returned is
        #not a RT price, but a histo minute price. We may request a price at 12:55 and we are
        #at 12:55:01 !
        inputStr = 'btc usd {}:{} bitfinex'.format(nowHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForDayOnlyAndTimeFullRequest_3daysBefore(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == threeDaysBeforeMonthStr:
            # this test can only be performed after the 3rd day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 3 days before today - so, in the future
            # if we are between the 1st and the 3rd since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForDayOnlyAndTimeFullRequestOn31st(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        oneMonthBeforeArrowDate = now.shift(months=-1)
        day = 31
        inputStr = 'btc usd {} {}:{} bitfinex'.format(day, nowHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        try:
            _ = DateTimeUtil.dateTimeComponentsToArrowLocalDate(day, now.month, now.year, now.hour, now.minute, 0,
                                                                                   LOCAL_TIME_ZONE)
        except ValueError:
            # only if the request is for a month which does not have a 31st is the test performed !
            self.assertEqual(
                'ERROR - day is out of range for month: day 31, month {}'.format(now.month), printResult)
            self.assertEqual('', fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForDayOnlyAndTimeFullRequest_8daysBefore(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == eightDaysBeforeMonthStr:
            # this test can only be performed after the 8th day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 8 days before today - so, in the future
            # if we are between the 1st and the 8th since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForDayOnlyAndTimeFullRequest_1daysAfter(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        oneDaysAfterArrowDate = now.shift(days=1)

        oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

        oneYearBeforeArrowDate = now.shift(years=-1)

        oneYearBeforeYearStr, oneYearBeforeMonthStr, oneYearBeforeDayStr, oneYearBeforeHourStr, oneYearBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(oneDaysAfterDayStr, oneDaysAfterHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == oneDaysAfterMonthStr:
            # this test can only be performed on a day which is not the last day of the mnnth.
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to tomorrow - in the future can not be
            # run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr, oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterYearStr, nowHourStr, nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysAfterDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForDayOnlyAndTimePartialRequest_3daysBefore(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        threeDaysBeforeArrowDate = now.shift(days=-3)

        threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

        #here, even if we request a price at now hour and now minute, the price returned is
        #not a RT price, but a histo minute price. We may request a price at 12:55 and we are
        #at 12:55:01 !
        inputStr = 'btc usd {} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == threeDaysBeforeMonthStr:
            # this test can only be performed after the 3rd day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 3 days before today - so, in the future
            # if we are between the 1st and the 3rd since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForDayOnlyAndTimePartialRequest_8daysBefore(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == eightDaysBeforeMonthStr:
            # this test can only be performed after the 8th day of the mnnth,
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to 8 days before today - so, in the future
            # if we are between the 1st and the 8th since the month is not specified, can not be run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForDayOnlyAndTimePartialRequest_1daysAfter(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        oneDaysAfterArrowDate = now.shift(days=1)

        oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

        oneYearBeforeArrowDate = now.shift(years=-1)

        oneYearBeforeYearStr, oneYearBeforeMonthStr, oneYearBeforeDayStr, oneYearBeforeHourStr, oneYearBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        inputStr = 'btc usd {} {}:{} bitfinex'.format(oneDaysAfterDayStr, oneDaysAfterHourStr, nowMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        if nowMonthStr == oneDaysAfterMonthStr:
            # this test can only be performed on a day which is not the last day of the mnnth.
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to tomorrow - in the future can not be
            # run.
            self.assertEqual(
                'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr, oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterYearStr, nowHourStr, nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(printResult))
            self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysAfterDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                   nowMinuteStr), fullCommandStrNoOptions)
            self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testBtcEthBinanceInvertedCryptoUnitBug(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        inputStr = 'eth btc 0 binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc 0 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        invertedInputStr = 'btc eth 0 binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            invertedInputStr)

        self.assertEqual(
            'BTC/ETH on Binance: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    # testing option value scenario

    def testGetPrintableResultForInputScenarioWithInvalidOptionValueSaveAndWarning(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        inputStr = 'eth usd 0 bitfinex -vs100'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        #        self.assertTrue('WARNING - currency value option symbol missing. -vs option ignored' in printResult)
        self.assertEqual(
            'ERROR - full request eth usd 0 bitfinex -vs100: -vs100 option violates the -vs option format. See help for more information.',
            printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testControllerBugSpecifyOptionValueAfterAskHistoDay(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        requestYearStr = eightDaysBeforeYearStr
        inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            'MCO/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v12mco'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCO/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyOptionValueSaveAfterAskHistoDay(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestYearStr = eightDaysBeforeYearStr
        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
            'MCO/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-vs12mco'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCO/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('mco btc {}/{}/{} {}:{} all -vs12mco'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyOptionValueAfterAskHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v12eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyOptionValueSaveAfterAskHistoMinute(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-vs12eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth btc {}/{}/{} {}:{} binance -vs12eth'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyOptionValueAfterAskHistoMinuteYearSupplied(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v12eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testControllerBugSpecifyOptionValueSaveAfterAskHistoMinuteYearSupplied(self):
        timezoneStr = LOCAL_TIME_ZONE
        now = DateTimeUtil.localNow(timezoneStr)
        fiveDaysBeforeArrowDate = now.shift(days=-5)

        fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

        requestDayStr = fiveDaysBeforeDayStr
        requestMonthStr = fiveDaysBeforeMonthStr
        requestYearStr = fiveDaysBeforeYearStr
        requestHourStr = fiveDaysBeforeHourStr
        requestMinuteStr = fiveDaysBeforeMinuteStr
        inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
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
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-vs12eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth btc {}/{}/{} {}:{} binance -vs12eth'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputScenarioWithInvalidOptionValue(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        # first command: RT price request
        inputStr = 'btc usd 0 -vs10btc bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ERROR - full request btc usd 0 -vs10btc bitfinex violates format <crypto> <unit> <date|time> <exchange> <options>',
            printResult)
        self.assertEqual('', fullCommandStrNoOptions)  # empty string since request caused an error !
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForInputScenarioWithOptionValue(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: value option
        inputStr = '-v10eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #third command: value save option
        inputStr = '-vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #fourth command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #fifth command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #sixth command: remove value option
        inputStr = '-v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecified(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs0.1btc'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.1 BTC/414.94 USD on Bitfinex: 12/09/17 00:00C 4149.4',printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs0.1btc', fullCommandStrWithSaveModeOptions)

    # here
    def testGetPrintableResultForInputScenarioWithOptionValueV0InFullRequest(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        yesterday = now.shift(days=-2)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price full command with save value option
        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #second command: RT price full command with remove value option. This is not usefull since
        #each time you enter a full command, you wioe out any previously entered command, as tested
        #by testGetPrintableResultForInputScenarioWithValueSaveCommandWipedOutByFullCommand() !
        inputStr = 'eth usd 0 bitfinex -v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputScenarioWithOptionValueSaveWipedOutByFullRequest(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        yesterday = now.shift(days=-2)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price full command with save value option
        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #second command: RT price full command with remove value option. This is not usefull since
        #each time you enter a full command, you wioe out any previously entered command !
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForInputScenarioWithOptionValueAndError(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 bitfinex -vs10btc'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 0 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)

        inputStr = '-ueth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/ETH on Bitfinex: '+ '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr), UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('btc eth 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc eth 0 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)

        inputStr = '-cxmr'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'PROVIDER ERROR - Bitfinex market does not exist for this coin pair (XMR-ETH)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-cbtc'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/ETH on Bitfinex: '+ '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr), UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('btc eth 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc eth 0 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)

        inputStr = '-uusd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 0 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForInputScenarioWithOptionValueVAfterOptionValueVS(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        inputStr = '-v100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -v100usd', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -v100usd', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForReplayHistoMinuteThenOptionValue(self):
        timezoneStr = LOCAL_TIME_ZONE
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

        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value option
        inputStr = '-v10eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value save option
        inputStr = '-vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveModeOptions)

        #next command: remove value option
        inputStr = '-v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr, priceType),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForReplayHistoDayThenOptionValue(self):
        timezoneStr = LOCAL_TIME_ZONE
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

        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value option
        inputStr = '-v10eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value save option
        inputStr = '-vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveModeOptions)

        #next command: remove value option
        inputStr = '-v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                               minuteStr, priceType),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForReplayRealTimeThenOptionValue(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value option
        inputStr = '-v10eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: value save option
        inputStr = '-vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #next command: remove value option
        inputStr = '-v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #next command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
                                                               requestMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForInputScenarioWithOptionValueAndInvalidOption(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'btc usd 0 all -vs100.2usd -ebitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R\nWarning - unsupported option -ebitfinex in request btc usd 0 all -vs100.2usd -ebitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                nowMinuteStr), UtilityForTest.removeAllPricesFromCommandValueResult(printResult))  #removing \n from contentList entry !
        self.assertEqual('btc usd 0 all', fullCommandStrNoOptions)
        self.assertEqual('btc usd 0 all -vs100.2usd', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForInputScenarioWithOptionValueSaveAndWarning(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        inputStr = 'eth usd 0 bitfinex -vs100usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        inputStr = '-cxmr'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'XMR/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
        self.assertEqual('xmr usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('xmr usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        inputStr = '-ubtc'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'XMR/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R\nWARNING - currency value option symbol USD currently in effect differs from both crypto (XMR) and unit (BTC) of last request. -vs option ignored'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('xmr btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-ceth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R\nWARNING - currency value option symbol USD currently in effect differs from both crypto (ETH) and unit (BTC) of last request. -vs option ignored'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        inputStr = '-v0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveUnitAmountSpecified(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs70usd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.01686991 BTC/70 USD on Bitfinex: 12/09/17 00:00C 4149.4',printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs70usd', fullCommandStrWithSaveModeOptions)

# testing option fiat scenario

    def testGetPrintableResultForFullRequestWithOptionFiatNoExchange(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth btc 0 bitfinex -fusd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC/USD.CCCAGG on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth btc 0 bitfinex -fusd', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForPartialRequestWithOptionFiatNoExchange(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth btc 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: fiat option
        inputStr = '-fusd'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC/USD.CCCAGG on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth btc 0 bitfinex -fusd', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForPartialRequestWithOptionFiatExchangeSpecified(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth btc 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: fiat option
        inputStr = '-fusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC/USD.Kraken on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth btc 0 bitfinex -fusd.kraken', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForFullRequestWithOptionFiatExchangeSpecified(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth btc 0 bitfinex -fusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/BTC/USD.Kraken on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth btc 0 bitfinex -fusd.kraken', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForInputScenarioWithOptionFiat(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        #first command: RT price request
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: fiat option
        inputStr = '-fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD/CHF.CCCAGG on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -fchf', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #third command: value save option
        inputStr = '-fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD/CHF.CCCAGG on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

        #fourth command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD/CHF.CCCAGG on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('eth usd 0 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

        #fifth command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD/CHF.CCCAGG on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeTwoEndPricesFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('neo usd 0 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

        #sixth command: remove fiat save option
        inputStr = '-f0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                               nowMinuteStr),
            UtilityForTest.removeOneEndPriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs0.1btc -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.1 BTC/414.94 USD/415.35494 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs0.1btc', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs0.1btc -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.1 BTC/414.94 USD/415.35494 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs0.1btc -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueCryptoAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v0.1btc -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.1 BTC/414.94 USD/415.35494 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueCryptoAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v0.1btc -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.1 BTC/414.94 USD/415.35494 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveUnitAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs1000usd -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.2409987 BTC/1000 USD/1001 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000usd', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveUnitAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs1000usd -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.2409987 BTC/1000 USD/1001 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000usd -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueUnitAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v1000usd -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.2409987 BTC/1000 USD/1001 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueUnitAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v1000usd -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.2409987 BTC/1000 USD/1001 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveFiatAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs1000chf -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.24075794 BTC/999.000999 USD/1000 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveFiatAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs1000chf -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.24075794 BTC/999.000999 USD/1000 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionFiatSaveOptionValueSaveFiatAmountSpecified(self):
        # inverting value and fiat options compared to previous tst
        inputStr = 'btc usd 12/09/17 bitfinex -fschf -vs1000chf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.24075794 BTC/999.000999 USD/1000 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueFiatAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v1000chf -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.24075794 BTC/999.000999 USD/1000 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueFiatAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v1000chf -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.24075794 BTC/999.000999 USD/1000 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveFiatOptionSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs1000chf -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '0.24075794 BTC/999.000999 USD/1000 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSavedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs10btc -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '10 BTC/41494 USD/41535.494 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fchf', fullCommandStrWithOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs10btc', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v10btc -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            '10 BTC/41494 USD/41535.494 CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -v10btc', fullCommandStrWithOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueSaveInvalidCurrencyAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -vs1000eth -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/USD/CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494\nWARNING - currency value option symbol ETH currently in effect differs from crypto (BTC), unit (USD) and fiat (CHF) of last request. -vs option ignored', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueInvalidCurrencyAmountSpecifiedOptionFiatSave(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v1000eth -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/USD/CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494\nWARNING - currency value option symbol ETH currently in effect differs from crypto (BTC), unit (USD) and fiat (CHF) of last request. -v option ignored', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetPrintableResultForHistoricalRequestWithOptionValueInvalidCurrencyAmountSpecifiedOptionFiat(self):
        inputStr = 'btc usd 12/09/17 bitfinex -v1000eth -fchf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/USD/CHF.CCCAGG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494\nWARNING - currency value option symbol ETH currently in effect differs from crypto (BTC), unit (USD) and fiat (CHF) of last request. -v option ignored', printResult)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
        self.assertEqual('btc usd 12/09/17 00:00 bitfinex -v1000eth -fchf', fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testControllerBugSpecifyOptionValueSaveThenFiatSaveAfterAskHistoDay(self):
        inputStr = 'btc eth 12/9/17 binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('BTC/ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
        self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        # adding value save option
        inputStr = '-vs10eth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('0.706 BTC/10 ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
        self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('btc eth 12/09/17 00:00 binance -vs10eth', fullCommandStrWithSaveModeOptions)

        # adding fiat save option
        inputStr = '-fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('0.706 BTC/10 ETH/2947.7 CHF.CCCAGG on Binance: 12/09/17 00:00C 14.16430595 4175.21246459', printResult)
        self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('btc eth 12/09/17 00:00 binance -vs10eth -fschf', fullCommandStrWithSaveModeOptions)

    def testOptionFiatValueComputationIsCorrectFullRequestHistoDayPrice(self):
        '''
        This test verifies that the fiat computed amount is correct
        :return:
        '''
        #first command: btc usd histo day on kraken price request
        inputStr = 'btc usd 1/1/19 kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
        self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

        #second command: eth btc histo day price request with usd fiat option
        inputStr = 'eth btc 1/1/19 binance -fsusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
        self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken', fullCommandStrWithSaveModeOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken\n(0.03663 * 3820.1 = 139.930263)', fullCommandStrForStatusBar)

        ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
        fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

        #ensure fiat value of eth is correct
        self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

    def testOptionFiatValueComputationIsCorrectFullRequestCurrentPrice(self):
        '''
        This test verifies that the fiat computed amount is correct
        :return:
        '''
        #first command: eth usd histo day on kraken price request
        inputStr = 'btc usd 0 kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('btc usd 0 kraken', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0])

        #second command: eth btc histo day price request with usd fiat option
        inputStr = 'eth btc 0 binance -fsusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('eth btc 0 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth btc 0 binance -fsusd.kraken', fullCommandStrWithSaveModeOptions)

        ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0])
        ethUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1])

        #ensure fiat value of eth is correct
        self.assertEqual(round(ethBtcRate * btcUsdRate, GuiOutputFormater.PRICE_FLOAT_ROUNDING), ethUsdRate)

    def testOptionFiatValueComputationIsCorrectPartialRequestHistoDayPrice(self):
        '''
        This test verifies that the fiat computed amount is correct
        :return:
        '''
        #first command: btc usd histo day on kraken price request
        inputStr = 'btc usd 1/1/19 kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
        self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

        #second command: eth btc histo day price request
        inputStr = 'eth btc 1/1/19 binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC on Binance: 01/01/19 00:00C 0.03663', printResult)
        self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: usd fiat save option
        inputStr = '-fsusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
        self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken', fullCommandStrWithSaveModeOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken\n(0.03663 * 3820.1 = 139.930263)', fullCommandStrForStatusBar)

        ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
        fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

        #ensure fiat value of eth is correct
        self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

    def testOptionFiatValueComputationIsCorrectPartialRequestCurrentPrice(self):
        '''
        This test verifies that the fiat computed amount is correct
        :return:
        '''
        #first command: eth usd histo day on kraken price request
        inputStr = 'btc usd 0 kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0])

        #second command: eth btc histo day price request
        inputStr = 'eth btc 0 binance'
        _, _, _, _, _ = self.controller.getPrintableResultForInput(inputStr)

        #third command: usd fiat save option
        inputStr = '-fsusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual('eth btc 0 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth btc 0 binance -fsusd.kraken', fullCommandStrWithSaveModeOptions)

        ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0])
        ethUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1])

        #ensure fiat value of eth is correct
        self.assertEqual(round(ethBtcRate * btcUsdRate, GuiOutputFormater.PRICE_FLOAT_ROUNDING), ethUsdRate)

    def testOptionFiatValueComputationIsCorrectFullRequestHistoDayPriceNoSave(self):
        '''
        This test verifies that the fiat computed amount is correct
        :return:
        '''
        #first command: btc usd histo day on kraken price request
        inputStr = 'btc usd 1/1/19 kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
        self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

        #second command: eth btc histo day price request with usd fiat option
        inputStr = 'eth btc 1/1/19 binance -fusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
        self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fusd.kraken\n(0.03663 * 3820.1 = 139.930263)', fullCommandStrForStatusBar)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
        fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

        #ensure fiat value of eth is correct
        self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

    def testOptionFiatValueComputationIsCorrectPartialRequestHistoDayPriceNoSave(self):
        '''
        This test verifies that the fiat computed amount is correct
        :return:
        '''
        #first command: btc usd histo day on kraken price request
        inputStr = 'btc usd 1/1/19 kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
        self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

        #second command: eth btc histo day price request
        inputStr = 'eth btc 1/1/19 binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC on Binance: 01/01/19 00:00C 0.03663', printResult)
        self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: usd fiat save option
        inputStr = '-fusd.kraken'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
        self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fusd.kraken', fullCommandStrWithOptions)
        self.assertEqual('eth btc 01/01/19 00:00 binance -fusd.kraken\n(0.03663 * 3820.1 = 139.930263)', fullCommandStrForStatusBar)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
        fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

        #ensure fiat value of eth is correct
        self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

    def testOptionFiatFullRequestHistoDayPriceFullCommandStrForStatusBarFormat(self):
        inputStr = 'eth btc 12/9/17 binance -fschf'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC/CHF.CCCAGG on Binance: 12/09/17 00:00C 0.0706 293.854144', printResult)
        self.assertEqual('eth btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth btc 12/09/17 00:00 binance -fschf', fullCommandStrWithSaveModeOptions)
        self.assertEqual('eth btc 12/09/17 00:00 binance -fschf\n(0.0706 * 4162.24 = 293.854144)', fullCommandStrForStatusBar)

    def testGetCryptoPriceHistoricalOptionFiatHandlingInvertedUnitFiat(self):
        '''
        Tests correct working of a fiat option where the unit/fiat pair is not supported
        by the fiat exchange and so causes an inverted fiat/unit pair request.

        btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
        and its result is inverted ((1/returned price)
        :return:
        '''
        # mco btc 12/09/17 00:00 binance -fseth.binance
        #first command: mco btc 12/09/17 00:00 binance -fseth.binance
        inputStr = 'mco btc 12/09/17 00:00 binance -fseth.binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCO/BTC/ETH.Binance on Binance: 12/09/17 00:00C 0.002049 0.02902266', printResult)
        self.assertEqual('mco btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveModeOptions)
        self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance\n(0.002049 * 14.16430595 = 0.02902266)', fullCommandStrForStatusBar)

    def testGetCryptoPriceHistoricalOptionFiatScenarioSettingUnitEqualToFiat(self):
        '''
        Tests correct working of a fiat option where the unit/fiat pair is not supported
        by the fiat exchange and so causes an inverted fiat/unit pair request.

        btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
        and its result is inverted ((1/returned price)
        :return:
        '''
        # mco btc 12/09/17 00:00 binance -fseth.binance
        #first command: mco btc 12/09/17 00:00 binance -fseth.binance
        inputStr = 'mco btc 12/09/17 00:00 binance -fseth.binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCO/BTC/ETH.Binance on Binance: 12/09/17 00:00C 0.002049 0.02902266', printResult)
        self.assertEqual('mco btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveModeOptions)
        self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance\n(0.002049 * 14.16430595 = 0.02902266)', fullCommandStrForStatusBar)

        #second command: -cbtc -ueth Here, unit is equal to fiat which causes warning
        inputStr = '-cbtc -ueth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'PROVIDER ERROR - Trade pair ETH/ETH is invalid! (ETH-ETH)', printResult)
        self.assertEqual('', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #third command: -cbtc -ueth with cancelling fiat option
        inputStr = '-cbtc -ueth -f0'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'BTC/ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
        self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

    def testGetCryptoPriceHistoricalOptionFiatScenarioSettingCryptoEqualToFiat(self):
        '''
        Tests correct working of a fiat option where the unit/fiat pair is not supported
        by the fiat exchange and so causes an inverted fiat/unit pair request.

        btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
        and its result is inverted ((1/returned price)
        :return:
        '''
        # mco btc 12/09/17 00:00 binance -fseth.binance
        #first command: mco btc 12/09/17 00:00 binance -fseth.binance
        inputStr = 'mco btc 12/09/17 00:00 binance -fseth.binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'MCO/BTC/ETH.Binance on Binance: 12/09/17 00:00C 0.002049 0.02902266', printResult)
        self.assertEqual('mco btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveModeOptions)
        self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance\n(0.002049 * 14.16430595 = 0.02902266)', fullCommandStrForStatusBar)

        #second command: -cbtc -ueth Here, unit is equal to fiat which causes warning
        inputStr = '-ceth'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/BTC/ETH.Binance on Binance: 12/09/17 00:00C 0.0706 1', printResult)
        self.assertEqual('eth btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual('eth btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveModeOptions)
        self.assertEqual('eth btc 12/09/17 00:00 binance -fseth.binance\n(0.0706 * 14.16430595 = 1)', fullCommandStrForStatusBar)

    def testGetCryptoPriceHistoDayValidExchangeHandlingInvertedCryptoUnit(self):
        '''
        Tests correct working of a request where the crypto/unit pair is not supported
        by the fiat exchange and so causes an inverted unit/crypto pair request.

        btc (crypto) eth (unit) on binance is not supported. So eth/btc is requested
        and its result is inverted ((1/returned price)
        :return:
        '''
        # btc eth 12/09/17 00:00 binance
        #first command: mco btc 12/09/17 00:00 binance -fseth.binance
        inputStr = 'btc eth 12/09/17 00:00 binance'
        printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'BTC/ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
        self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
        self.assertEqual(None, fullCommandStrWithOptions)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

if __name__ == '__main__':
    unittest.main()
