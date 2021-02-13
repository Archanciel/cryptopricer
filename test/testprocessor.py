import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from processor import Processor
from configurationmanager import ConfigurationManager
from pricerequesterteststub import PriceRequesterTestStub
from crypcompexchanges import CrypCompExchanges
from datetimeutil import DateTimeUtil

class TestProcessor(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(FILE_PATH)
        self.priceRequester = PriceRequesterTestStub()
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
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
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - currency value option symbol ETH currently in effect differs from both crypto (BTC) and unit (USD) of request. -v option ignored.")


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

        self.assertEqual(outputFormater._formatPriceFloatToStr(0.01698205, outputFormater.PRICE_FLOAT_FORMAT),
                         outputFormater._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), outputFormater.PRICE_FLOAT_FORMAT))
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
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
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - currency value option symbol EUR currently in effect differs from both crypto (BTC) and unit (USD) of request. -v option ignored.")

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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))

        # The save flag is set in the ResultData in CommandPrice.execute()
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), "WARNING - currency value option symbol EUR currently in effect differs from both crypto (BTC) and unit (USD) of request. -vs option ignored.")


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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '{}/{}/{} 10:05'.format(recentDayStr, monthStr, year - 2000))
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist or is not yet supported by the application.")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), None)
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '{}/{}/{} {}:{}'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr))
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist or is not yet supported by the application.")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), None)
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


    def testGetCryptoPriceRealTimeInvalidExchangeNotSupportPair(self):
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

        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - BTC38 market does not exist for this coin pair (BTC/USD).")
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), None)
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

    def testGetCryptoPriceHistoDayValidExchangeHandlingInvertedCryptoUnit(self):
        '''
        Tests correct working of a request where the crypto/unit pair is not supported
        by the fiat exchange and so causes an inverted unit/crypto pair request.

        btc (crypto) eth (unit) on binance is not supported. So eth/btc is requested
        and its result is inverted ((1/returned price)
        :return:
        '''
        # full request btc eth 12/9/17 binance
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'ETH'
        exchange = 'Binance'
        day = 12
        month = 9
        year = 2017
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

        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit,resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(14.164305949008499, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/17 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1505174400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
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
        # full request: btc usd 12/09/17 10:05 bittrex -feur
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        value = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT)
        self.assertTrue(value >= 3440.2212 and value <= 3463.7166)
        self.assertEqual('EUR', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.8346, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionFiatHandlingInvertedUnitFiat(self):
        '''
        Tests correct working of a fiat option where the unit/fiat pair is not supported
        by the fiat exchange and so causes an inverted fiat/unit pair request.

        btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
        and its result is inverted ((1/returned price)
        :return:
        '''
        # mco btc 12/09/17 00:00 binance -fseth.binance
        crypto = 'MCO'
        unit = 'BTC'
        exchange = 'binance'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5
        optionFiatSymbol = 'ETH' # -fsETH
        optionFiatExchange = 'binance'


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
                                               optionFiatSymbol=optionFiatSymbol,
                                               optionFiatExchange=optionFiatExchange,
                                               optionValueSaveFlag='s')
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual('Binance', resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(0.002049, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/17 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1505174400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        value = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT)
        self.assertEqual(0.029022662889518415, value)
        self.assertEqual('ETH', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('Binance', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(14.164305949008499, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueCryptoToUnitOptionFiat(self):
        # full request: btc usd 12/09/17 10:05 bittrex -v0.001BTC -feur
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
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(4.122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        value = resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT)
        self.assertTrue(value >= 3.440221 and value <= 3.463717)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        value = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT)
        self.assertTrue(value >= 3440.2212 and value <= 3463.7166)
        self.assertEqual('EUR', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.8346, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueCryptoToUnitOptionFiatSave(self):
        # full request: btc usd 12/09/17 10:05 bittrex -v0.001BTC -fseur
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
        optionFiatSymbol = 'EUR' # -fseur
        optionFiatSave = 's'

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
                                               optionFiatSymbol=optionFiatSymbol,
                                               optionFiatSaveFlag=optionFiatSave)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), None)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(4.122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        value = resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT)
        self.assertTrue(value >= 3.440221 and value <= 3.463717)
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        value = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT)
        self.assertTrue(value >= 3440.2212 and value <= 3463.7166)
        self.assertEqual('EUR', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.8346, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))

        # The save flag is set in the ResultData in CommandPrice.execute()
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


        if resultData.getValue(resultData.RESULT_KEY_PRICE) == 0:
            # in case of provider error: happened from 9 t0 11 sept 2019 !!
            errorMsg = resultData.getValue(resultData.RESULT_KEY_ERROR_MSG)
            print(errorMsg)
            self.assertEqual('PROVIDER ERROR - Requesting fiat option coin pair USD/CHF or CHF/USD price for date 12/09/17 10:05 on exchange CCCAGG returned invalid value 0',
                             errorMsg)
        else:
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_CRYPTO), crypto)
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_UNIT), unit)
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_EXCHANGE), 'BitTrex')
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE), 4122)
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING), '12/09/17 00:00')
            self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP), 1505174400)
            self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
            self.assertEqual(4.122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
            self.assertEqual(4.126122, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
            self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
            self.assertEqual(4126.121999999999, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
            self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
            self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
            self.assertEqual(1.001, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))
            self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
            self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
            self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
            self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
            self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueCryptoToUnitOptionFiatCHF(self):
        # full request: eth usd 12/09/18 all -v10eth -fchf
        # exp result: 10 ETH/1830.3 USD/1780.51584 CHF.CCCAGG on CCCAGG: 12/09/18 00:00C 183.03 178.051584
        crypto = 'ETH'
        unit = 'USD'
        exchange = 'all'
        day = 12
        month = 9
        year = 2018
        hour = 0
        minute = 0
        optionValueSymbol = 'ETH'
        optionValueAmount = 10
        optionFiatSymbol = 'CHF'

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
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertFalse(resultData.getValue(resultData.RESULT_KEY_WARNINGS_DIC))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(183.03, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/18 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1536710400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(1830.3, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(1780.51584, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(178.051584, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.9728, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))

        # The save flag is set in the ResultData in CommandPrice.execute()
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueUnitToCryptoOptionFiatCHF(self):
        # full request: eth usd 12/09/18 all -v10usd -fchf
        # exp result: 0.05463585204611266 ETH/10 USD/9.728 CHF.CCCAGG on CCCAGG: 12/09/18 00:00C 183.03 178.051584
        crypto = 'ETH'
        unit = 'USD'
        exchange = 'all'
        day = 12
        month = 9
        year = 2018
        hour = 0
        minute = 0
        optionValueSymbol = 'USD'
        optionValueAmount = 10
        optionFiatSymbol = 'CHF'

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
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertFalse(resultData.getValue(resultData.RESULT_KEY_WARNINGS_DIC))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(183.03, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/18 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1536710400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        self.assertEqual(0.05463585204611266, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(9.728, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(178.051584, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.9728, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))

        # The save flag is set in the ResultData in CommandPrice.execute()
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueFiatOptionFiatCHF(self):
        # full request: eth usd 12/09/18 all -v10chf -fchf
        # exp result: 0.056163499225033574 ETH/10.279605263157896 USD/10 CHF.CCCAGG on CCCAGG: 12/09/18 00:00C 183.03 178.051584
        crypto = 'ETH'
        unit = 'USD'
        exchange = 'all'
        day = 12
        month = 9
        year = 2018
        hour = 0
        minute = 0
        optionValueSymbol = 'CHF'
        optionValueAmount = 10
        optionFiatSymbol = 'CHF'

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
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertFalse(resultData.getValue(resultData.RESULT_KEY_WARNINGS_DIC))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(183.03, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/18 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1536710400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        self.assertEqual(0.056163499225033574, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(10.279605263157896, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(optionValueAmount, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(178.051584, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.9728, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))

        # The save flag is set in the ResultData in CommandPrice.execute()
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueNotCryptoNotUnitNotFiatFiatOptionFiatCHF(self):
        # full request: eth usd 12/09/18 all -v10btc -fchf
        # exp result: WARNING - currency value option symbol BTC currently in effect differs from crypto (ETH), unit (USD) and fiat (CHF) of request. -v option ignored.'
        crypto = 'ETH'
        unit = 'USD'
        exchange = 'all'
        day = 12
        month = 9
        year = 2018
        hour = 0
        minute = 0
        optionValueSymbol = 'BTC'
        optionValueAmount = 10
        optionFiatSymbol = 'CHF'

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
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), 'WARNING - currency value option symbol BTC currently in effect differs from crypto (ETH), unit (USD) and fiat (CHF) of request. -v option ignored.')
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(183.03, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/18 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1536710400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(178.051584, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.9728, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))

        # The save flag is set in the ResultData in CommandPrice.execute()
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

    def testGetCryptoPriceHistoricalOptionValueNotCryptoNotUnitNotFiatFiatOptionFiatCHFSave(self):
        # full request: eth usd 12/09/18 all -v10btc -fchf
        # exp result: WARNING - currency value option symbol BTC currently in effect differs from crypto (ETH), unit (USD) and fiat (CHF) of request. -v option ignored.'
        crypto = 'ETH'
        unit = 'USD'
        exchange = 'all'
        day = 12
        month = 9
        year = 2018
        hour = 0
        minute = 0
        optionValueSymbol = 'BTC'
        optionValueAmount = 10
        optionFiatSymbol = 'CHF'

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
                                               optionFiatSymbol=optionFiatSymbol,
                                               optionValueSaveFlag='S' )
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
        self.assertEqual(resultData.getWarningMessage(resultData.WARNING_TYPE_COMMAND_VALUE), 'WARNING - currency value option symbol BTC currently in effect differs from crypto (ETH), unit (USD) and fiat (CHF) of request. -vs option ignored.')
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
        self.assertEqual(resultData.PRICE_TYPE_HISTO_DAY, resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE))
        self.assertEqual(183.03, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual('12/09/18 00:00', resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING))
        self.assertEqual(1536710400, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE))
        self.assertEqual(178.051584, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT))
        self.assertEqual('CHF', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
        self.assertEqual('CCCAGG', resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE))
        self.assertEqual(0.9728, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE))

        # The save flag is set in the ResultData in CommandPrice.execute()
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SYMBOL))
        self.assertEqual(None, resultData.getValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE))

if __name__ == '__main__':
    unittest.main()
