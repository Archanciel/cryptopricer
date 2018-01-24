import inspect
import os
import sys
import unittest
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
                              # the test is executed standalone


from controller import Controller
from datetimeutil import DateTimeUtil
from consoleoutputformater import ConsoleOutputFormater
from utilityfortest import UtilityForTest


class TestController(unittest.TestCase):
    '''
    This test class is launched from allcl.py (all command line), the class that runs
    all the tests in QPython on Android.

    Test the Controller using a ConsoleOutputFormaater in place of a GuiOuputFormater
    since ConsoleOutputFormaater runs on Android in QPython, but fails in Pydroid !
    '''
    def setUp(self):
        #print('---- Instanciating Controller with ConsoleOutputFormater ----')
        self.controller = Controller(ConsoleOutputFormater())


    def testControllerHistoDayPrice(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 23/9/2017 2:56 bittrex\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[1])


    def testControllerHistoDayPriceThenPartialDateDayOnly(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 23/9/2017 2:56 bittrex\n-d25\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on BitTrex: 25/09/17 00:00C 3931.12\n', contentList[3])


    def testControllerHistoDayPriceThenPartialDateDayOnly_2(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 30/9/2017 all\nbtc usd 30/9/2017 2:00 all\n-d25\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: 30/09/17 00:00C 4360.62\n', contentList[1])
            self.assertEqual('BTC/USD on CCCAGG: 30/09/17 00:00C 4360.62\n', contentList[3])
            self.assertEqual('BTC/USD on CCCAGG: 25/09/17 00:00C 3932.83\n', contentList[5])


    def testControllerHistoDayPriceThenEmptyPartialParms(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 30/9/2017 all\n-t\n-d\n-e\n-c\n-f\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: 30/09/17 00:00C 4360.62\n', contentList[1])
            self.assertEqual('ERROR - invalid command -t\n', contentList[3])
            self.assertEqual('ERROR - invalid command -d\n', contentList[5])
            self.assertEqual('ERROR - invalid command -e\n', contentList[7])
            self.assertEqual('ERROR - invalid command -c\n', contentList[9])
            self.assertEqual('ERROR - invalid command -f\n', contentList[11])


    def testControllerHistoDayPriceInvalidTimeFormat(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 23/9/2017 2.56 bittrex\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('ERROR - exchange could not be parsed due to an error in your command\n', contentList[1])


    def testControllerOnlyDayProvided(self):
        # error msg not optimal in this case !!
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 1 2:57 bittrex\nq\ny')

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

        now = DateTimeUtil.localNow('Europe/Zurich')

        nowMonth = now.month

        if nowMonth < 10:
            nowMonthStr = '0' + str(nowMonth)
        else:
            nowMonthStr = str(nowMonth)

        nowYear = now.year

        nowYearStr = str(nowYear)

        sys.stdin = stdin
        sys.stdout = stdout

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - date not valid".format(nowMonthStr, nowYearStr), contentList[1][:-1]) #removing \n from contentList entry !


    def testControllerDateContainZeroYear(self):
        # error msg not optimal in this case !!
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 1/10/0 2:58 bittrex\nq\ny')

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

        now = DateTimeUtil.localNow('Europe/Zurich')

        nowMonth = now.month

        if nowMonth < 10:
            nowMonthStr = '0' + str(nowMonth)
        else:
            nowMonthStr = str(nowMonth)

        nowYear = now.year

        nowYearStr = str(nowYear)

        sys.stdin = stdin
        sys.stdout = stdout

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - date not valid", contentList[1][:-1]) #removing \n from contentList entry !


    def testControllerRegressionOnDDMMDate(self):
        # error msg not optimal in this case !!
        requestDay = '11'
        requestMonth = '10'
        stdin = sys.stdin
        sys.stdin = StringIO('neo btc {}/{} bitfinex\nq\ny'.format(requestDay, requestMonth))

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

        now = DateTimeUtil.localNow('Europe/Zurich')

        nowMonth = now.month

        if nowMonth < 10:
            nowMonthStr = '0' + str(nowMonth)
        else:
            nowMonthStr = str(nowMonth)

        nowYear = now.year

        nowYearStr = str(nowYear)

        sys.stdin = stdin
        sys.stdout = stdout

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('NEO/BTC on Bitfinex: ' + '{}/{}/{} 00:00C'.format(requestDay, requestMonth, now.year - 2001), UtilityForTest.removePriceFromResult(contentList[1][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} 00:00 can not be in the future and was shifted back to last year !'.format(requestDay, requestMonth, now.year - 2000), contentList[2][:-1])
         #   self.assertEqual('NEO/BTC on Bitfinex: 11/10/17 00:00C 0.006228\n', contentList[1])


    def testControllerBugSpecifyTimeAfterAskedRT001(self):
        stdin = sys.stdin

        # The scenario below is not usable because if you run it between 0:01
        # and 3:44, the test will fail since the specified time (3:45) will be
        # after the current time, which causes the request to be performed for
        # the year before (request can not be for a< date/time in the future !)
        #
        # sys.stdin = StringIO('btc usd 0 all\n-t3:45\n-d0\nq\ny')

        sys.stdin = StringIO('btc usd 0 all\n-t00:01\nq\ny')

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:01M'.format(nowDayStr, nowMonthStr, nowYearStr), UtilityForTest.removePriceFromResult(contentList[3][:-1]))


    def testControllerBugSpecifyTimeAfterAskedRT001(self):
        stdin = sys.stdin

        # The scenario below is not usable because if you run it between 0:01
        # and 6:59, the test will fail since the specified time (7:00) will be
        # after the current time, which causes the request to be performed for
        # the year before (request can not be for a< date/time in the future !)
        #
        # sys.stdin = StringIO('btc usd 0 all\n-t7:00\n-d0\nq\ny')

        sys.stdin = StringIO('btc usd 0 all\n-t0:01\nq\ny')

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:01M'.format(nowDayStr, nowMonthStr, nowYearStr), UtilityForTest.removePriceFromResult(contentList[3][:-1]))


    def testControllerBugSpecifyTimeAfterAskedRT700ThenReaskRT(self):
        stdin = sys.stdin

        # The scenario below is not usable because if you run it between 0:01
        # and 6:59, the test will fail since the specified time (7:00) will be
        # after the current time, which causes the request to be performed for
        # the year before (request can not be for a< date/time in the future !)
        #
        # sys.stdin = StringIO('btc usd 0 all\n-t7:00\n-d0\nq\ny')

        sys.stdin = StringIO('btc usd 0 all\n-t0:01\n-d0\nq\ny')

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:01M'.format(nowDayStr, nowMonthStr, nowYearStr), UtilityForTest.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !


    def testControllerBugSpecifyDateAfterAskedRT2910(self):
        stdin = sys.stdin
        nextRequestDay = '29'
        nextRequestMonth = '10'
        sys.stdin = StringIO('btc usd 0 all\n-d{}/{}\nq\ny'.format(nextRequestDay, nextRequestMonth))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(nextRequestDay, nextRequestMonth, now.year - 2001), UtilityForTest.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year !'.format(nextRequestDay, nextRequestMonth, nowYearStr, nowHourStr, nowMinuteStr), contentList[4][:-1])


    def testControllerBugSpecifyDate10DaysBeforeAfterAskedRTThenAskRTAgain(self):
        stdin = sys.stdin
        oneDayBeforeNow = DateTimeUtil.localNow('Europe/Zurich').shift(days=-10)
        oneDayBeforeNowYearStr, oneDayBeforeNowMonthStr, oneDayBeforeNowDayStr, oneDayBeforeNowHourStr, oneDayBeforeNowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayBeforeNow)

        sys.stdin = StringIO('btc usd 0 all\n-d{}/{}/{}\n-d0\nq\ny'.format(oneDayBeforeNowDayStr, oneDayBeforeNowMonthStr, oneDayBeforeNow.year))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(oneDayBeforeNowDayStr, oneDayBeforeNowMonthStr, oneDayBeforeNowYearStr), UtilityForTest.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !


    def testControllerBugSpecifyFutureDateAfterAskedRTThenAskRTAgain(self):
        stdin = sys.stdin
        nextRequestDay = '29'
        nextRequestMonth = '10'
        sys.stdin = StringIO('btc usd 0 all\n-d{}/{}\n-d0\nq\ny'.format(nextRequestDay, nextRequestMonth))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(nextRequestDay, nextRequestMonth, now.year - 2001), UtilityForTest.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year !'.format(nextRequestDay, nextRequestMonth, nowYearStr, nowHourStr, nowMinuteStr), contentList[4][:-1])
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[6][:-1])) #removing \n from contentList entry !


    def testControllerBugChangeCryptoAfterAskedRT(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-ceth\nq\ny')

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
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[3][:-1]))

    def testControllerBugChangeCryptoAfterAskedRTThenAskRTAgain(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-ceth\n-d0\nq\ny')

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
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[5][:-1]))


    def testControllerBugAskRTTwice(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-d0\nq\ny')

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


    def testControllerInvalidYearThenValidDDMM(self):
        nextRequestDay = '30'
        nextRequestMonth = '9'
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 20/9/201 all\n-d{}/{}\nq\ny'.format(nextRequestDay, nextRequestMonth))

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - 201 not conform to accepted year format (YYYY, YY or '')\n", contentList[1])
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/0{}/{} 00:00C'.format(nextRequestDay, nextRequestMonth, now.year - 2001), UtilityForTest.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/0{}/{} 00:00 can not be in the future and was shifted back to last year !'.format(nextRequestDay, nextRequestMonth, now.year - 2000), contentList[4][:-1])


    def testControllerInvalidMonthThenValidDDMM(self):
        nextRequestDay = '30'
        nextRequestMonth = '9'
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 20/999 all\n-d{}/{}\nq\ny'.format(nextRequestDay, nextRequestMonth))

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - 999 not conform to accepted month format (MM or M)\n", contentList[1])
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/0{}/{} 00:00C'.format(nextRequestDay, nextRequestMonth, now.year - 2001), UtilityForTest.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/0{}/{} 00:00 can not be in the future and was shifted back to last year !'.format(nextRequestDay, nextRequestMonth, now.year - 2000), contentList[4][:-1])


    def testControllerInvalidMonthValue(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 20/13 all\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - month must be in 1..12\n", contentList[1])


    def testControllerInvalidDayValue(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 32/1 all\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - day is out of range for month\n", contentList[1])


    def testControllerInvalidHourValue(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 1/1 25:00 all\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - hour must be in 0..23\n", contentList[1])


    def testControllerInvalidMinuteValue(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 1/1 2:65 all\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - minute must be in 0..59\n", contentList[1])


    def testControllerInvalidCommandOnlyCryptoProvided(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - fiat missing or invalid\n", contentList[1])


    def testControllerInvalidCommandMissingFiatProvided(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc 1/1 2:00 all\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - fiat missing or invalid\n", contentList[1])


    def testControllerHistoDayPriceDiffOptParmsOrder(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 23/9/2017 2:56 bittrex\nbtc usd 2:56 23/9/17 bittrex\nbtc usd 2:56 bittrex 23/9/2017\nbtc usd bittrex 2:56 23/9/17\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[1])
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[3])
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[5])
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[7])


    def testControllerRTThenHistoMinuteThenRThenNewFiat(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        previousDate = now.shift(days = -2)
        previsousDateDay = previousDate.day
        previsousDateMonth = previousDate.month

        stdin = sys.stdin
        sys.stdin = StringIO('eth usd 0 bitfinex\n-d{}/{}\n-d0\n-fbtc\nq\ny'.format(previsousDateDay, previsousDateMonth))

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

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        yesterdayMinute = previousDate.minute

        if yesterdayMinute < 10:
            if yesterdayMinute > 0:
                yesterdayMinuteStr = '0' + str(yesterdayMinute)
            else:
                yesterdayMinuteStr = '00'
        else:
            yesterdayMinuteStr = str(yesterdayMinute)

        yesterdayHour = previousDate.hour

        if yesterdayHour < 10:
            if yesterdayHour > 0:
                yesterdayHourStr = '0' + str(yesterdayHour)
            else:
                yesterdayHourStr = '00'
        else:
            yesterdayHourStr = str(yesterdayHour)

        previsousDateDay = previousDate.day

        if previsousDateDay < 10:
            yesterdayDayStr = '0' + str(previsousDateDay)
        else:
            yesterdayDayStr = str(previsousDateDay)

        previsousDateMonth = previousDate.month

        if previsousDateMonth < 10:
            yesterdayMonthStr = '0' + str(previsousDateMonth)
        else:
            yesterdayMonthStr = str(previsousDateMonth)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(yesterdayDayStr, yesterdayMonthStr, previousDate.year - 2000, yesterdayHourStr, yesterdayMinuteStr), UtilityForTest.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removePriceFromResult(contentList[7][:-1])) #removing \n from contentList entry !


    def testControllerHistoDayPriceIncompleteCommandScenario(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        nextRequestDay = '23'
        nextRequestMonth = '9'
        stdin = sys.stdin
        sys.stdin = StringIO('btc 23/9 2:56 bittrex\n-fusd 2:56\n-d23/9\nq\ny')

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

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('ERROR - fiat missing or invalid\n', contentList[1])
            self.assertEqual('ERROR - invalid command -fusd 2:56\n', contentList[3])
            self.assertEqual('BTC/USD on BitTrex: ' + '{}/0{}/{} 00:00C'.format(nextRequestDay, nextRequestMonth, now.year - 2001), UtilityForTest.removePriceFromResult(contentList[5][:-1]))
            self.assertEqual('Warning - request date {}/0{}/{} 02:56 can not be in the future and was shifted back to last year !'.format(nextRequestDay, nextRequestMonth, nowYearStr, nowHourStr, nowMinuteStr), contentList[6][:-1])


    def testControllerHistoDayPriceWrongCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 23/9/17 2:56 bittrex\n-h22:21\nq\ny')

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[1])
            self.assertEqual('ERROR - invalid command -h22:21: -h not supported\n', contentList[3])


    def testControllerScenarioMissingFiatBadErrorMsg(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        stdin = sys.stdin
        sys.stdin = StringIO('btc\n-fusd\n-d0\n-ebittrex\nq\ny')

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

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual(
                'ERROR - fiat missing or invalid', contentList[1][:-1])
            self.assertEqual(
                'ERROR - invalid command -fusd', contentList[3][:-1]) #improve error msg
            self.assertEqual(
                'ERROR - exchange could not be parsed due to an error in your command', contentList[5][:-1])
            self.assertEqual(
                'BTC/USD on BitTrex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removePriceFromResult(contentList[7][:-1]))  # removing \n from contentList entry !


    def testControllerScenarioModel(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        yesterday = now.shift(days=-2)
        yesterdayDay = yesterday.day
        yesterdayMonth = yesterday.month

        stdin = sys.stdin
        sys.stdin = StringIO('eth usd 0 bitfinex\n-d{}/{}\n-d0\n-fbtc\nq\ny'.format(yesterdayDay, yesterdayMonth))

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

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual(
                'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removePriceFromResult(contentList[1][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(yesterdayDayStr, yesterdayMonthStr, yesterday.year - 2000,
                                                                yesterdayHourStr, yesterdayMinuteStr),
                UtilityForTest.removePriceFromResult(contentList[3][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removePriceFromResult(contentList[5][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removePriceFromResult(contentList[7][:-1]))  # removing \n from contentList entry !


    def testControllerBugSpecifyInvalTimeAfterAskedRT345(self):
        # should fail because error msg should signal invalid time
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-t03.45\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run() #will eat up what has been filled in stdin using StringIO above #will eat up what has been filled in stdin using StringIO above
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual(
                'BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                 nowMinuteStr),
                UtilityForTest.removePriceFromResult(contentList[1][:-1]))  # removing \n from contentList entry !
            self.assertEqual('ERROR - invalid command -t03.45: in -t03.45, 03.45 must respect 99:99 format !', contentList[3][:-1])


if __name__ == '__main__':
    unittest.main()