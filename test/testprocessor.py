import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import re
from processor import Processor
from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester
from crypcompexchanges import CrypCompExchanges
from datetimeutil import DateTimeUtil

class TestProcessor(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(FILE_PATH)
        self.priceRequester = PriceRequester()
        self.crypCompExchanges = CrypCompExchanges()
        self.processor = Processor(self.configMgr, self.priceRequester, self.crypCompExchanges)


    def testGetCryptoPriceHistorical(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5

        result = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual('BTC/USD on BitTrex: 12/09/17 4122', result)


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

        result = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        result = self.removePriceFromResult(result)
        self.assertEqual('BTC/USD on BitTrex: {}/{}/{} 10:05'.format(day, month, year - 2000), result)


    def testGetCryptoPriceHistoricalWrongExchange(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        result = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual("BTC/USD on unknown: ERROR - unknown market does not exist for this coin pair (BTC-USD)", result)


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

        result = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        result = self.removePriceFromResult(result)
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

        self.assertEqual('BTC/USD on BitTrex: {}/{}/{} {}:{}'.format(now.day, now.month, now.year - 2000, nowHourStr,
                                                                      nowMinuteStr), result)


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

        result = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual("BTC/USD on unknown: ERROR - unknown market does not exist for this coin pair (BTC-USD)", result)


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

        result = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual("BTC/USD on BTC38: ERROR - BTC38 market does not exist for this coin pair (BTC-USD)", result)


if __name__ == '__main__':
    unittest.main()
