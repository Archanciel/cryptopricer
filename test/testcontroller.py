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
from configurationmanager import ConfigurationManager
from pricerequesterteststub import PriceRequesterTestStub
from utilityfortest import UtilityForTest

LOCAL_TIME_ZONE = 'Europe/Zurich'

class TestController(unittest.TestCase):
    '''
    This test class is launched from allcl.py (all command line), the class that runs
    all the tests in QPython on Android.

    Test the Controller using a ConsoleOutputFormaater in place of a GuiOuputFormater
    since ConsoleOutputFormaater runs on Android in QPython, but fails in Pydroid !
    '''
    def setUp(self):
        if os.name == 'posix':
            self.filePath = '/sdcard/cryptopricer_test.ini'
        else:
            self.filePath = 'c:\\temp\\cryptopricer_test.ini'

        configMgr = ConfigurationManager(self.filePath)

        #print('---- Instanciating Controller with ConsoleOutputFormater ----')
        self.controller = Controller(ConsoleOutputFormater(), configMgr, PriceRequesterTestStub())


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
        sys.stdin = StringIO('btc usd 30/9/2017 all\n-t\n-d\n-e\n-c\n-u\nq\ny')

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
            self.assertEqual('ERROR - invalid partial request -t\n', contentList[3])
            self.assertEqual('ERROR - invalid partial request -d\n', contentList[5])
            self.assertEqual('ERROR - invalid partial request -e\n', contentList[7])
            self.assertEqual('ERROR - invalid partial request -c\n', contentList[9])
            self.assertEqual('ERROR - invalid partial request -u\n', contentList[11])


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
            self.assertEqual('ERROR - exchange could not be parsed due to an error in your request (btc usd 23/9/2017 2.56 bittrex)\n', contentList[1])


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

        now = DateTimeUtil.localNow('Europe/Zurich')
        oneDayAfterNow = now.shift(days=+1)
        oneDayAfterNowYearStr, oneDayAfterNowMonthStr, oneDayAfterNowDayStr, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayAfterNow)

        oneYearBeforeArrowDate = now.shift(years=-1)
        oneYearBeforeYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        oneYearAfterArrowDate = now.shift(years=+1)
        oneYearAfterYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearAfterArrowDate)

        if oneDayAfterNowYearStr == oneYearAfterYearStr:
            # test is run on december 31st and so, the dd/mm request date will not be in the future,
            # but will be 01/01 and test will fail !
            return

        stdin = sys.stdin
        sys.stdin = StringIO('neo btc {}/{} bitfinex\nq\ny'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr))

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
            self.assertEqual('NEO/BTC on Bitfinex: ' + '{}/{}/{} 00:00C'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, now.year - 2001), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} 00:00 can not be in the future and was shifted back to last year'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, now.year - 2000), contentList[2][:-1])


    def testControllerBugSpecifyTimeAfterAskedRT0001(self):
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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:01M'.format(nowDayStr, nowMonthStr, nowYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))


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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:01M'.format(nowDayStr, nowMonthStr, nowYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))


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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:01M'.format(nowDayStr, nowMonthStr, nowYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !


    def testControllerBugSpecifyDateAfterAskedRT2910(self):
        stdin = sys.stdin

        now = DateTimeUtil.localNow('Europe/Zurich')
        oneDayAfterNow = now.shift(days=+1)
        oneDayAfterNowYearStr, oneDayAfterNowMonthStr, oneDayAfterNowDayStr, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayAfterNow)

        oneYearBeforeArrowDate = now.shift(years=-1)
        oneYearBeforeYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        oneYearAfterArrowDate = now.shift(years=+1)
        oneYearAfterYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearAfterArrowDate)

        if oneDayAfterNowYearStr == oneYearAfterYearStr:
            # test is run on december 31st and so, the dd/mm request date will not be in the future,
            # but will be 01/01 and test will fail !
            return

        sys.stdin = StringIO('btc usd 0 all\n-d{}/{}\nq\ny'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, now.year - 2001), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), contentList[4][:-1])


    def testControllerBugSpecifyDate10DaysBeforeAfterAskedRTThenAskRTAgain(self):
        stdin = sys.stdin
        tenDaysBeforeNow = DateTimeUtil.localNow('Europe/Zurich').shift(days=-10)
        tenDaysBeforeNowYearStr, tenDaysBeforeNowMonthStr, tenDaysBeforeNowDayStr, tenDaysBeforeNowHourStr, tenDaysBeforeNowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenDaysBeforeNow)

        sys.stdin = StringIO('btc usd 0 all\n-d{}/{}/{}\n-d0\nq\ny'.format(tenDaysBeforeNowDayStr, tenDaysBeforeNowMonthStr, tenDaysBeforeNow.year))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(tenDaysBeforeNowDayStr, tenDaysBeforeNowMonthStr, tenDaysBeforeNowYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !


    def testControllerBugSpecifyFutureDateAfterAskedRTThenAskRTAgain(self):
        stdin = sys.stdin

        now = DateTimeUtil.localNow('Europe/Zurich')
        oneDayAfterNow = now.shift(days=+1)
        oneDayAfterNowYearStr, oneDayAfterNowMonthStr, oneDayAfterNowDayStr, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayAfterNow)

        oneYearBeforeArrowDate = now.shift(years=-1)
        oneYearBeforeYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        oneYearAfterArrowDate = now.shift(years=+1)
        oneYearAfterYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearAfterArrowDate)

        if oneDayAfterNowYearStr == oneYearAfterYearStr:
            # test is run on december 31st and so, the dd/mm request date will not be in the future,
            # but will be 01/01 and test will fail !
            return

        sys.stdin = StringIO('btc usd 0 all\n-d{}/{}\n-d0\nq\ny'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, now.year - 2001), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), contentList[4][:-1])
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[6][:-1])) #removing \n from contentList entry !


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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[5][:-1]))


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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !


    def testControllerInvalidYearThenValidDDMMInFuture(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        oneDayAfterNow = now.shift(days=+1)
        oneDayAfterNowYearStr, oneDayAfterNowMonthStr, oneDayAfterNowDayStr, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayAfterNow)

        oneYearBeforeArrowDate = now.shift(years=-1)
        oneYearBeforeYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        oneYearAfterArrowDate = now.shift(years=+1)
        oneYearAfterYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearAfterArrowDate)

        if oneDayAfterNowYearStr == oneYearAfterYearStr:
            # test is run on december 31st and so, the dd/mm request date will not be in the future,
            # but will be 01/01 and test will fail !
            return

        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 20/9/201 all\n-d{}/{}\nq\ny'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, oneYearBeforeYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} 00:00 can not be in the future and was shifted back to last year'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, oneDayAfterNowYearStr), contentList[4][:-1])


    def testControllerInvalidMonthThenValidDDMMInFuture(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        oneDayAfterNow = now.shift(days=+1)
        oneDayAfterNowYearStr, oneDayAfterNowMonthStr, oneDayAfterNowDayStr, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayAfterNow)

        oneYearBeforeArrowDate = now.shift(years=-1)
        oneYearBeforeYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        oneYearAfterArrowDate = now.shift(years=+1)
        oneYearAfterYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearAfterArrowDate)

        if oneDayAfterNowYearStr == oneYearAfterYearStr:
            # test is run on december 31st and so, the dd/mm request date will not be in the future,
            # but will be 01/01 and test will fail !
            return

        stdin = sys.stdin

        sys.stdin = StringIO('btc usd 20/999 all\n-d{}/{}\nq\ny'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr))

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
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 00:00C'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, oneYearBeforeYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))
            self.assertEqual('Warning - request date {}/{}/{} 00:00 can not be in the future and was shifted back to last year'.format(oneDayAfterNowDayStr, oneDayAfterNowMonthStr, oneDayAfterNowYearStr), contentList[4][:-1])


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
            self.assertEqual("ERROR - unit missing or invalid\n", contentList[1])


    def testControllerInvalidCommandMissingUnitProvided(self):
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
            self.assertEqual("ERROR - unit missing or invalid\n", contentList[1])


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


    def testControllerRTThenHistoMinuteThenRThenNewUnit(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        previousDate = now.shift(days = -2)
        previsousDateDay = previousDate.day
        previsousDateMonth = previousDate.month

        stdin = sys.stdin
        sys.stdin = StringIO('eth usd 0 bitfinex\n-d{}/{}\n-d0\n-ubtc\nq\ny'.format(previsousDateDay, previsousDateMonth))

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
            self.assertEqual('ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(yesterdayDayStr, yesterdayMonthStr, previousDate.year - 2000, yesterdayHourStr, yesterdayMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), UtilityForTest.removeOneEndPriceFromResult(contentList[7][:-1])) #removing \n from contentList entry !


    def testControllerHistoDayPriceIncompleteCommandScenarioWithDateInFuture(self):
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            now)

        oneDaysAfterArrowDate = now.shift(days=1)

        oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

        oneYearBeforeArrowDate = now.shift(years=-1)

        oneYearBeforeYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

        stdin = sys.stdin
        multiRequestStr = 'btc {}/{} 2:56 bittrex\n-uusd 2:56\n-d{}/{}\nq\ny'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterMonthStr)
        sys.stdin = StringIO(multiRequestStr)

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
            self.assertEqual('ERROR - unit missing or invalid\n', contentList[1])
            self.assertEqual('ERROR - invalid partial request -uusd 2:56\n', contentList[3])

            if nowMonthStr == oneDaysAfterMonthStr:
            # this test can only be performed on a day which is not the last day of the mnnth.
            # othervise, the test which assumes that we try a full request with only day and time
            # specified, but with the day number set to tomorrow - in the future can not be
            # run.
                self.assertEqual('BTC/USD on BitTrex: ' + '{}/{}/{} 00:00C'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr), UtilityForTest.removeOneEndPriceFromResult(contentList[5][:-1]))
                self.assertEqual('Warning - request date {}/{}/{} 02:56 can not be in the future and was shifted back to last year'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, nowYearStr, nowHourStr, nowMinuteStr), contentList[6][:-1])


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
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[3])
            self.assertEqual('Warning - unsupported option -h22:21 in request -h22:21\n', contentList[4])


    def testControllerScenarioMissingUnitBadErrorMsg(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        stdin = sys.stdin
        sys.stdin = StringIO('btc\n-uusd\n-d0\n-ebittrex\nq\ny')

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
                'ERROR - unit missing or invalid', contentList[1][:-1])
            self.assertEqual(
                'ERROR - invalid partial request -uusd', contentList[3][:-1]) #improve error msg
            self.assertEqual(
                'ERROR - exchange could not be parsed due to an error in your request (-d0)', contentList[5][:-1])
            self.assertEqual(
                'BTC/USD on BitTrex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(contentList[7][:-1]))  # removing \n from contentList entry !


    def testControllerScenarioModel(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        yesterday = now.shift(days=-2)
        yesterdayDay = yesterday.day
        yesterdayMonth = yesterday.month

        stdin = sys.stdin
        sys.stdin = StringIO('eth usd 0 bitfinex\n-d{}/{}\n-d0\n-ubtc\nq\ny'.format(yesterdayDay, yesterdayMonth))

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
                UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(yesterdayDayStr, yesterdayMonthStr, yesterday.year - 2000,
                                                                yesterdayHourStr, yesterdayMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(contentList[3][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(contentList[5][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'ETH/BTC on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
                                                                nowMinuteStr),
                UtilityForTest.removeOneEndPriceFromResult(contentList[7][:-1]))  # removing \n from contentList entry !


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
                UtilityForTest.removeOneEndPriceFromResult(contentList[1][:-1]))  # removing \n from contentList entry !
            self.assertEqual('ERROR - invalid partial request -t03.45: in -t03.45, 03.45 must respect HH:mm format', contentList[3][:-1])


if __name__ == '__main__':
    unittest.main()