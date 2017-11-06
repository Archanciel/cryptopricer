import unittest
import os, sys, inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import re
from printer import Printer
from priceresult import PriceResult
from datetimeutil import DateTimeUtil

class TestPrinter(unittest.TestCase):
    def setUp(self):
        self.printer = Printer()

    def testPrintCryptoPriceHistorical(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'

        priceResult = PriceResult()
        priceResult.setValue(priceResult.RESULT_KEY_ERROR_MSG, None)
        priceResult.setValue(priceResult.RESULT_KEY_CRYPTO, crypto)
        priceResult.setValue(priceResult.RESULT_KEY_FIAT, fiat)
        priceResult.setValue(priceResult.RESULT_KEY_EXCHANGE, 'BitTrex')
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TYPE, priceResult.PRICE_TYPE_HISTO_DAY)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE, 4122)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.print(priceResult)
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

        priceResult = PriceResult()

        recentDay = recent.day

        if recentDay < 10:
            recentDayStr = '0' + str(recentDay)
        else:
            recentDayStr = str(recentDay)

        priceResult.setValue(priceResult.RESULT_KEY_ERROR_MSG, None)
        priceResult.setValue(priceResult.RESULT_KEY_CRYPTO, crypto)
        priceResult.setValue(priceResult.RESULT_KEY_FIAT, fiat)
        priceResult.setValue(priceResult.RESULT_KEY_EXCHANGE, 'BitTrex')
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TYPE, priceResult.PRICE_TYPE_HISTO_MINUTE)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE, 4122.09)

        dateTimeString = '{}/{}/{} 10:05'.format(recentDayStr, month, year - 2000)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.print(priceResult)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: {}M 4122.09\n'.format(dateTimeString), capturedStdout.getvalue())

'''
    def testGetCryptoPriceHistoricalWrongExchange(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        priceResult = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        priceResult.setValue(priceResult.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        priceResult.setValue(priceResult.RESULT_KEY_CRYPTO, None)
        priceResult.setValue(priceResult.RESULT_KEY_FIAT, None)
        priceResult.setValue(priceResult.RESULT_KEY_EXCHANGE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TYPE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP, None)


    def removePriceFromResult(self, resultStr):
        match = re.match(r"(.*) ([\d\.]*)", resultStr)

        if match != None:
            return match.group(1)
        else:
            return ()


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

        priceResult = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
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

        priceResult.setValue(priceResult.RESULT_KEY_ERROR_MSG, None)
        priceResult.setValue(priceResult.RESULT_KEY_CRYPTO, crypto)
        priceResult.setValue(priceResult.RESULT_KEY_FIAT, fiat)
        priceResult.setValue(priceResult.RESULT_KEY_EXCHANGE, 'BitTrex')
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TYPE, priceResult.PRICE_TYPE_RT)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr))
#        self.assertEqual('BTC/USD on BitTrex: {}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr,
#                                                                      nowMinuteStr), priceResult)


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

        priceResult = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        priceResult.setValue(priceResult.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        priceResult.setValue(priceResult.RESULT_KEY_CRYPTO, None)
        priceResult.setValue(priceResult.RESULT_KEY_FIAT, None)
        priceResult.setValue(priceResult.RESULT_KEY_EXCHANGE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TYPE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP, None)
#        self.assertEqual("BTC/USD on unknown: ERROR - unknown market does not exist for this coin pair (BTC-USD)", priceResult)


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

        priceResult = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)

        priceResult.setValue(priceResult.RESULT_KEY_ERROR_MSG, "ERROR - BTC38 market does not exist for this coin pair (BTC-USD)")
        priceResult.setValue(priceResult.RESULT_KEY_CRYPTO, crypto)
        priceResult.setValue(priceResult.RESULT_KEY_FIAT, fiat)
        priceResult.setValue(priceResult.RESULT_KEY_EXCHANGE, exchange)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TYPE, priceResult.PRICE_TYPE_RT)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        priceResult.setValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP, None)
#        self.assertEqual("BTC/USD on BTC38: ERROR - BTC38 market does not exist for this coin pair (BTC-USD)", priceResult)

'''
if __name__ == '__main__':
    unittest.main()
