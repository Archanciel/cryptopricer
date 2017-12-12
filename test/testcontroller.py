import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import re
from controller import Controller
from datetimeutil import DateTimeUtil
from consoleoutputformater import ConsoleOutputFormater


class TestController(unittest.TestCase):
    def setUp(self):
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
        stdin = sys.stdin
        sys.stdin = StringIO('neo btc 11/10 bitfinex\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
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
            self.assertEqual('NEO/BTC on Bitfinex: 11/10/17 00:00C 0.006228\n', contentList[1])


    def testControllerBugSpecifyTimeAfterAskedRT345(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-t03:45\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 03:45M'.format(nowDayStr, now.month, now.year - 2000), self.removePriceFromResult(contentList[3][:-1]))


    def testControllerBugSpecifyTimeAfterAskedRT700(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-t7:00\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 07:00M'.format(nowDayStr, now.month, now.year - 2000), self.removePriceFromResult(contentList[3][:-1]))


    def testControllerBugSpecifyTimeAfterAskedRT700ThenReaskRT(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-t7:00\n-d0\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} 07:00M'.format(nowDayStr, now.month, now.year - 2000), self.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !


    def testControllerBugSpecifyDateAfterAskedRT2910(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-d29/10\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '29/10/17 00:00C 6147.52', contentList[3][:-1])


    def testControllerBugSpecifyDateAfterAskedRT2910ThenAskRTAgain(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all\n-d29/10\n-d0\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '29/10/17 00:00C 6147.52', contentList[3][:-1])
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !


    def removePriceFromResult(self, resultStr):
        match = re.match(r"(.*) ([\d\.]*)", resultStr)

        if match != None:
            return match.group(1)
        else:
            return ()


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
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[3][:-1]))

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
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[3][:-1]))
            self.assertEqual('ETH/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[5][:-1]))


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
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !


    def testControllerInvalidYearThenValidDDMM(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 20/9/201 all\n-d30/9\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - 201 not conform to accepted year format (YYYY, YY or '')\n", contentList[1])
            self.assertEqual('BTC/USD on CCCAGG: 30/09/17 00:00C 4360.62\n', contentList[3])


    def testControllerInvalidMonthThenValidDDMM(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 20/999 all\n-d30/9\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual("ERROR - 999 not conform to accepted month format (MM or M)\n", contentList[1])
            self.assertEqual('BTC/USD on CCCAGG: 30/09/17 00:00C 4360.62\n', contentList[3])


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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
                self.controller.run()
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
        yesterday = now.shift(days = -2)
        yesterdayDay = yesterday.day
        yesterdayMonth = yesterday.month

        stdin = sys.stdin
        sys.stdin = StringIO('mcap usd 0 ccex\n-d{}/{}\n-d0\n-fbtc\nq\ny'.format(yesterdayDay, yesterdayMonth))

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('MCAP/USD on Ccex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('MCAP/USD on Ccex: ' + '{}/{}/{} {}:{}M'.format(yesterdayDayStr, yesterday.month, yesterday.year - 2000, yesterdayHourStr, yesterdayMinuteStr), self.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !
            self.assertEqual('MCAP/USD on Ccex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[5][:-1])) #removing \n from contentList entry !
            self.assertEqual('MCAP/BTC on Ccex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[7][:-1])) #removing \n from contentList entry !


    def testControllerHistoDayPriceIncompleteCommandScenario(self):
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
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('ERROR - fiat missing or invalid\n', contentList[1])
            self.assertEqual('ERROR - invalid command -fusd 2:56\n', contentList[3])
            self.assertEqual('BTC/USD on BitTrex: 23/09/17 00:00C 3773\n', contentList[5])


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
                self.controller.run()
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
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual(
                'ERROR - fiat missing or invalid', contentList[1][:-1])
            self.assertEqual(
                'ERROR - invalid command -fusd', contentList[3][:-1]) #improve error msg
            self.assertEqual(
                'ERROR - exchange could not be parsed due to an error in your command', contentList[5][:-1])
            self.assertEqual(
                'BTC/USD on BitTrex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr,
                                                                nowMinuteStr),
                self.removePriceFromResult(contentList[7][:-1]))  # removing \n from contentList entry !


    def testControllerScenarioModel(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        yesterday = now.shift(days=-2)
        yesterdayDay = yesterday.day
        yesterdayMonth = yesterday.month

        stdin = sys.stdin
        sys.stdin = StringIO('mcap usd 0 ccex\n-d{}/{}\n-d0\n-fbtc\nq\ny'.format(yesterdayDay, yesterdayMonth))

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run()
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

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

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual(
                'MCAP/USD on Ccex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr,
                                                                nowMinuteStr),
                self.removePriceFromResult(contentList[1][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'MCAP/USD on Ccex: ' + '{}/{}/{} {}:{}M'.format(yesterdayDayStr, yesterday.month, yesterday.year - 2000,
                                                                yesterdayHourStr, yesterdayMinuteStr),
                self.removePriceFromResult(contentList[3][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'MCAP/USD on Ccex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr,
                                                                nowMinuteStr),
                self.removePriceFromResult(contentList[5][:-1]))  # removing \n from contentList entry !
            self.assertEqual(
                'MCAP/BTC on Ccex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, now.month, now.year - 2000, nowHourStr,
                                                                nowMinuteStr),
                self.removePriceFromResult(contentList[7][:-1]))  # removing \n from contentList entry !


if __name__ == '__main__':
    unittest.main()