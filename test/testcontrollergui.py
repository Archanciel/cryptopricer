import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) #this instruction is necessary for successful importation of testcontroller module when TestControllerGui is executed standalone

import re
from controller import Controller
from datetimeutil import DateTimeUtil
from guioutputformater import GuiOutputFormater
from testcontroller import TestController


class TestControllerGui(TestController):
    '''
    This test class is launched from allguy.py, the class that runs
    all the tests in Pydroid on Android.

    Test the Controller using a GuiOuputFormater in place of a ConsoleOutputFormaater
    since GuiOuputFormater runs on Android in Pydroid, but fails in QPython !

    All the test cases are defineed in the TestController parent to avoid code duplication
    '''
    def setUp(self):
        #print('---- Instanciating Controller with GuiOuputFormater ----')
        self.controller = Controller(GuiOutputFormater())


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
        nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = self.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !


    def testGetPrintableResultForInputscenarioWithValueCommand(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        yesterday = now.shift(days=-2)
        yesterdayDay = yesterday.day
        yesterdayMonth = yesterday.month

        nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = self.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        yesterdayMinute = yesterday.minute

        if yesterdayMinute < 10:
            if yesterdayMinute > 0:
                yesterdayMinuteStr = '0' + str(yesterdayMinute)
            else:
                yesterdayMinuteStr = '00'
        else:
            yesterdayMinuteStr = str(yesterdayMinute)

        yesterdayHour = yesterday.hour

        if yesterdayHour < 10:
            if yesterdayHour > 0:
                yesterdayHourStr = '0' + str(yesterdayHour)
            else:
                yesterdayHourStr = '00'
        else:
            yesterdayHourStr = str(yesterdayHour)

        yesterdayDay = yesterday.day

        if yesterdayDay < 10:
            yesterdayDayStr = '0' + str(yesterdayDay)
        else:
            yesterdayDayStr = str(yesterdayDay)

        yesterdayMonth = yesterday.month

        if yesterdayMonth < 10:
            yesterdayMonthStr = '0' + str(yesterdayMonth)
        else:
            yesterdayMonthStr = str(yesterdayMonth)

        #first command: RT price command
        inputStr = 'eth usd 0 bitfinex'
        printResult, fullCommandStr, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr,
                                                               nowMinuteStr),
            self.removePriceFromResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #second command: value command
        inputStr = '-v10eth'
        printResult, fullCommandStr, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr,
                                                               nowMinuteStr),
            self.removePricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)

        #third command: value save command
        inputStr = '-vs100usd'
        printResult, fullCommandStr, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr,
                                                               nowMinuteStr),
            self.removePricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #fourth command: '' to replay lst command
        inputStr = ''
        printResult, fullCommandStr, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr,
                                                               nowMinuteStr),
            self.removePricesFromCommandValueResult(printResult))
        self.assertEqual('eth usd 0 bitfinex', fullCommandStr)
        self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #fifth command: change crypto
        inputStr = '-cneo'
        printResult, fullCommandStr, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr,
                                                               nowMinuteStr),
            self.removePricesFromCommandValueResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveModeOptions)

        #sixth command: remove value command
        inputStr = '-v0'
        printResult, fullCommandStr, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)
        self.assertEqual(
            'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr,
                                                               nowMinuteStr),
            self.removePriceFromResult(printResult))
        self.assertEqual('neo usd 0 bitfinex', fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)


    def removePricesFromCommandValueResult(self, resultStr):
        match = re.match(r"(?:[\d\.]*) (\w*/)(?:[\d\.]*) (.*) (?:[\d\.]*)", resultStr)

        if match != None:
            return match.group(1) + match.group(2)
        else:
            return ()


if __name__ == '__main__':
    unittest.main()
