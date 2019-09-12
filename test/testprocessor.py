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
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))


    def testGetCryptoPriceHistoricalOptionValueCryptoToUnit(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'BTC' # -v0.001BTC
        optionValueAmount = 0.001

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(4.122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))


    def testGetCryptoPriceHistoricalOptionValueFromBadCryptoToUnit(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'ETH' #-v0.001ETH
        optionValueAmount = 0.001

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - currency value option symbol ETH currently in effect differs from both crypto (BTC) and unit (USD) of last request. -v option ignored")


    def testGetCryptoPriceHistoricalOptionValueUnitToCrypto(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'USD' #-v70USD
        optionValueAmount = 70

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)

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

        self.assertEqual(outputFormater.formatFloatToStr(0.01698205), outputFormater.formatFloatToStr(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO)))
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueFromBadUnitToCrypto(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'EUR' #-v70EUR
        optionValueAmount = 70

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - currency value option symbol EUR currently in effect differs from both crypto (BTC) and unit (USD) of last request. -v option ignored")

    def testGetCryptoPriceHistoricalOptionValueSaveFromBadUnitToCrypto(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'EUR' #-vs70EUR
        optionValueAmount = 70

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount,
                                               optionValueSaveFlag=True)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - currency value option symbol EUR currently in effect differs from both crypto (BTC) and unit (USD) of last request. -vs option ignored")


    def testGetCryptoPriceHistoricalRecent(self):    
        #here, requested date is less than 7 days ago
        now = DateTimeUtil.localNow('Europe/Zurich')
        recent = now.shift(days = -2)
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = recent.day
        month = recent.month
        year = recent.year
        hour = 10
        minute = 5

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '{}/{}/{} 10:05'.format(recentDayStr, monthStr, year - 2000))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalWrongExchange(self):    
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'unknown'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), None)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))


    def testGetCryptoPriceRealTime(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 0
        minute = 0

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '{}/{}/{} {}:{}'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceRealTimeWrongExchange(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'unknown'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), None)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))


    def testGetCryptoPriceRealTimeExchangeNotSupportPair(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'BTC38'
        day = 0
        month = 0
        year = 0
        hour = 0
        minute = 0

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute)

        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - BTC38 market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), None)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionFiat(self):
        # full request: btc usd 12/09/17 10:05 bittrex -fCHF
        # exp result: BTC/USD/CHF on BitTrex: 12/09/17 00:00C 4122 4126.122
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionFiatSymbol = 'EUR' # -fEUR


        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol=None,
                                               optionValueAmount=None,
                                               requestInputString='',
                                               optionFiatSymbol=optionFiatSymbol)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(3463.7166, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('EUR', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueCryptoToUnitOptionFiat(self):
        # full request: btc usd 12/09/17 10:05 bittrex -v0.001BTC -fCHF
        # exp result: 0.001 BTC/4.122 USD/4.126122 CHF on BitTrex: 12/09/17 00:00C 4122 4126.122
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'BTC' # -v0.001BTC
        optionValueAmount = 0.001
        optionFiatSymbol = 'EUR' # -fEUR

        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount,
                                               requestInputString='',
                                               optionFiatSymbol=optionFiatSymbol)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(4.122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(3.4637166, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(3463.7166, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('EUR', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionFiatRateNotFound(self):
        # full request: btc usd 12/09/17 10:05 bittrex -fCHF
        # exp result: BTC/USD/CHF on BitTrex: 12/09/17 00:00C 4122 4126.122
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionValueSymbol = 'BTC'  # -v0.001BTC
        optionValueAmount = 0.001
        optionFiatSymbol = 'CHF' # -fCHF


        resultData = self.processor.getCryptoPrice(crypto,
                                               unit,
                                               exchange,
                                               day,
                                               month,
                                               year,
                                               hour,
                                               minute,
                                               optionValueSymbol,
                                               optionValueAmount,
                                               requestInputString='',
                                               optionFiatSymbol=optionFiatSymbol)
# in case of provider error: happened from 9 t0 11 sept 2019 !!
#        self.assertEqual('PROVIDER ERROR - Requesting USD/CHF price for date 12/09/17 10:05 returned invalid value 0', resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_OPTION_TIME_STAMP), 1505174400)
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(4.122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(4.126122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(4126.122, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

if __name__ == '__main__':
    unittest.main()
