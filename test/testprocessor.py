import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

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

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)


    def testGetCryptoPriceHistoricalPriceValueCryptoToFiat(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        priceValueSymbol = 'BTC' # -v0.001BTC
        priceValueAmount = 0.001

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               priceValueSymbol,
                                               priceValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_CRYPTO), priceValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_FIAT), 4.122)


    def testGetCryptoPriceHistoricalPriceValueFromBadCryptoToFiat(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        priceValueSymbol = 'ETH' #-v0.001ETH
        priceValueAmount = 0.001

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               priceValueSymbol,
                                               priceValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_FIAT), None)
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - price value symbol ETH differs from both crypto (BTC) and unit (USD) of last request. -v parameter ignored")


    def testGetCryptoPriceHistoricalPriceValueFiatToCrypto(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        priceValueSymbol = 'USD' #-v70USD
        priceValueAmount = 70

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               priceValueSymbol,
                                               priceValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)

        try:
            from consoleoutputformater import ConsoleOutputFormater
            outputFormater = ConsoleOutputFormater()
        except ImportError:
            #ImportError is raised when running TestProcessor in Pydroid
            #since ConsoleOutputFormater is not compatible with Pydroid
            #because of Pydroid not supporting the sl4a lib imported
            #by ConsoleOutputFormater
            from guioutputformater import GuiOutputFormater
            outputFormater = GuiOutputFormater(self.configMgr)

        self.assertEqual(outputFormater.formatFloatToStr(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_CRYPTO)), outputFormater.formatFloatToStr(0.01698205))
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_FIAT), priceValueAmount)


    def testGetCryptoPriceHistoricalPriceValueFromBadFiatToCrypto(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        priceValueSymbol = 'EUR' #-v70EUR
        priceValueAmount = 70

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               priceValueSymbol,
                                               priceValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)      
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_FIAT), None)
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - price value symbol EUR differs from both crypto (BTC) and unit (USD) of last request. -v parameter ignored")


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

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        recentDay = recent.day

        if recentDay < 10:
            recentDayStr = '0' + str(recentDay)
        else:
            recentDayStr = str(recentDay)

        if month < 10:
            monthStr = '0' + str(month)
        else:
            monthStr = str(month)

        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '{}/{}/{} 10:05'.format(recentDayStr, monthStr, year - 2000))


    def testGetCryptoPriceHistoricalWrongExchange(self):    
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), None)


    def testGetCryptoPriceRealTime(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 0
        minute = 0

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)

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

        nowMonth = now.month

        if nowMonth < 10:
            nowMonthStr = '0' + str(nowMonth)
        else:
            nowMonthStr = str(nowMonth)

        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '{}/{}/{} {}:{}'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr))

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

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), None)


    def testGetCryptoPriceRealTimeExchangeNotSupportPair(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'BTC38'
        day = 0
        month = 0
        year = 0
        hour = 0
        minute = 0

        resultData = self.processor.getCryptoPrice(crypto,
                                               fiat,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)

        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - BTC38 market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_FIAT), fiat)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), None)


if __name__ == '__main__':
    unittest.main()
