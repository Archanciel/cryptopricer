import unittest
import os, sys, inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import re
from commandlineprinter import CommandLinePrinter
from resultdata import ResultData
from datetimeutil import DateTimeUtil

class TestCommandLinePrinter(unittest.TestCase):
    def setUp(self):
        self.printer = CommandLinePrinter()


    def testPrintCryptoPriceHistorical(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printData(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


    def testGetCryptoPriceHistoricalRecent(self):
        #here, requested date is less than 7 days ago
        now = DateTimeUtil.localNow('Europe/Zurich')
        recent = now.shift(days = -2)
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = recent.day
        month = recent.month
        year = recent.year
        hour = 10
        minute = 5

        resultData = ResultData()

        recentDay = recent.day

        if recentDay < 10:
            recentDayStr = '0' + str(recentDay)
        else:
            recentDayStr = str(recentDay)

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122.09)

        dateTimeString = '{}/{}/{} 10:05'.format(recentDayStr, month, year - 2000)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printData(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: {}M 4122.09\n'.format(dateTimeString), capturedStdout.getvalue())


    def testGetCryptoPriceHistoricalWrongExchange(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printData(resultData)
        sys.stdout = stdout
        self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


    def testGetCryptoPriceRealTime(self):    
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

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

        #rt price not provided here !
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printData(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())


    def testGetCryptoPriceRealTimeWrongExchange(self):    
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()
        
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, None)
        resultData.setValue(resultData.RESULT_KEY_FIAT, None)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, None)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printData(resultData)
        sys.stdout = stdout
        self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


    def testGetCryptoPriceRealTimeExchangeNotSupportPair(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'BTC38'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - BTC38 market does not exist for this coin pair (BTC-USD)")
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        resultData.setValue(resultData.RESULT_KEY_PRICE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, None)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printData(resultData)
        sys.stdout = stdout
        self.assertEqual("ERROR - BTC38 market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


    def testFormatFloatToStrRoundedFloat(self):
        y = round(5.59, 1)
        self.assertEqual('5.6', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrEmptystr(self):
        y = ''
        self.assertEqual('', self.printer.formatFloatToStr(y))


    def testFormatFloatToStrNone(self):
        y = None
        self.assertEqual('', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrNineDigits(self):
        y = 	0.999999999
        self.assertEqual('1', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrFourDigits(self):
        y = 0.9084   
        self.assertEqual('0.9084', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrinteger(self):
        y = 40 
        self.assertEqual('40', self.printer.formatFloatToStr(y))


    def testFormatFloatToStrNormal(self):
        y = 2000.085  
        self.assertEqual('2000.085', self.printer.formatFloatToStr(y)) 


    def testToFromClipboard(self):
        y = 2000.085
        self.printer.toClipboard(y)
        self.assertEqual(str(y), self.printer.fromClipboard())


if __name__ == '__main__':
    unittest.main()

