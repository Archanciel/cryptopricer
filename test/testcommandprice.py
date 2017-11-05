import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import re
from datetimeutil import DateTimeUtil
from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester
from crypcompexchanges import CrypCompExchanges
from processor import Processor
from commandprice import  CommandPrice


class TestCommandPrice(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(FILE_PATH)
        self.priceRequester = PriceRequester()
        self.crypCompExchanges = CrypCompExchanges()
        self.processor = Processor(self.configMgr, self.priceRequester, self.crypCompExchanges)
        self.commandPrice = CommandPrice(self.processor, self.configMgr)


    def testExecuteHistoricalPriceFourDigitYear(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'bittrex'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '12'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '9'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '2017'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()

        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO), 'BTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_FIAT), 'USD')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE), 4122)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)

#        self.assertEqual("BTC/USD on BitTrex: 12/09/17 00:00 4122", priceResult)


    def testExecuteHistoricalPriceTwoDigitYear(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'bittrex'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '12'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '9'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '17'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()

        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO), 'BTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_FIAT), 'USD')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE), 4122)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)

#        self.assertEqual("BTC/USD on BitTrex: 12/09/17 00:00 4122", priceResult)


    def testExecuteHistoricalPriceNoYear(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'bittrex'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '12'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '9'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = None
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()

        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO), 'BTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_FIAT), 'USD')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE), 4122)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)

#        self.assertEqual("BTC/USD on BitTrex: 12/09/17 00:00 4122", priceResult)


    def testExecuteHistoricalPriceWrongExchange(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'Unknown'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '12'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '9'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '2017'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()

        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), "ERROR - Unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_FIAT), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP), None)

#        self.assertEqual("BTC/USD on Unknown: ERROR - Unknown market does not exist for this coin pair (BTC-USD)", priceResult)


    def removePriceFromResult(self, resultStr):
        match = re.match(r"(.*) ([\d\.]*)", resultStr)

        if match != None:
            return match.group(1)
        else:
            return ()


    def testExecuteRealTimePrice(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'bittrex'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()
#        priceResult = self.removePriceFromResult(priceResult)

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

        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO), 'BTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_FIAT), 'USD')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_CURRENT_OR_HISTO_MINUTE)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr))
#        self.assertEqual('BTC/USD on BitTrex: {}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr), priceResult)


    def testExecuteRealTimePriceWrongExchange(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'Unknown'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()


        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG),
                         "ERROR - Unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_FIAT), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP), None)
#        self.assertEqual("BTC/USD on Unknown: ERROR - Unknown market does not exist for this coin pair (BTC-USD)", priceResult)


    def testExecuteRealTimePriceInvalidYearOneDigit(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'bittrex'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '1'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()

        self.assertEqual("BTC/USD on bittrex: ERROR - 1 not conform to accepted year format (YYYY, YY, '' or 0)",
                         priceResult)


    def testExecuteRealTimePriceInvalidYearThreeDigit(self):
        self.commandPrice.parsedParmData[self.commandPrice.CRYPTO] = 'btc'
        self.commandPrice.parsedParmData[self.commandPrice.FIAT] = 'usd'
        self.commandPrice.parsedParmData[self.commandPrice.EXCHANGE] = 'bittrex'
        self.commandPrice.parsedParmData[self.commandPrice.DAY] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '0'
        self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '017'
        self.commandPrice.parsedParmData[self.commandPrice.HOUR] = '10'
        self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = '5'

        priceResult = self.commandPrice.execute()

        self.assertEqual("BTC/USD on bittrex: ERROR - 017 not conform to accepted year format (YYYY, YY, '' or 0)",
                         priceResult)


if __name__ == '__main__':
    unittest.main()
