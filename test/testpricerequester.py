import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester
from resultdata import ResultData
from datetimeutil import DateTimeUtil


class TestPriceRequester(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(FILE_PATH)
        self.priceRequester = PriceRequester()


    def test_getHistoDayPriceAtUTCTimeStampEndOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj_endOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        resultData = ResultData()
        resultData = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto,
                                                                          fiat,
                                                                          utcArrowDateTimeObj_endOfDay.timestamp,
                                                                          exchange,
                                                                          resultData)
        self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))


    def test_getHistoDayPriceAtUTCTimeStampMidOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj_midOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 12:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        resultData = ResultData()
        resultData = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto,
                                                                          fiat,
                                                                          utcArrowDateTimeObj_midOfDay.timestamp,
                                                                          exchange,
                                                                          resultData)
        self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))


    def testGetHistoricalPriceAtUTCTimeStampEndOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        timeStampLocal = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 23:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             timeStampLocal,
                                                                             timeStampUtcNoHHMM,
                                                                             exchange)
        self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampMidOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        timeStampLocal = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             timeStampLocal,
                                                                             timeStampUtcNoHHMM,
                                                                             exchange)

        self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtTimeStampZurichMidOfDayUseTimeStamp(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        #time stamp is always UTC !
        timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             timeStampLocalMidDay,
                                                                             timeStampUtcNoHHMM,
                                                                             exchange)
        self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)

        # for histominute price,
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetCurrentPrice(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        resultData = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDayWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)

        #here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampMoreThanSevenDayWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-12)

        #here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampMoreThanSevenDayForCryptoFiatPairNotSupportedByExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'Binance'

        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-12)

        #here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))








    def testGetMinuteHistoricalPriceForCryptoFiatPairNotSupportedByExchange(self):
        crypto = 'BTC'

        fiat = 'USD'
        exchange = 'Binance'
        #time stamp is always UTC !
        LOCAL_TIME_ZONE = 'Europe/Zurich'
        now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
        timeStampLocalNow = now.timestamp
        timeStampUtcNow = DateTimeUtil.utcNowTimeStamp()
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
                                                                           fiat,
                                                                           timeStampLocalNow,
                                                                           timeStampUtcNow,
                                                                           exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - Binance market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampMidOfDayWrongExchange(self):
        crypto = 'BTC'

        fiat = 'USD'
        exchange = 'Binance'
        #time stamp is always UTC !
        timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
                                                                           fiat,
                                                                           timeStampLocalMidDay,
                                                                           timeStampUtcNoHHMM,
                                                                           exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetCurrentPriceWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        resultData = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetCurrentPriceWrongCrypto(self):
        crypto = 'BTa'
        fiat = 'USD'
        exchange = 'all'

        resultData = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - There is no data for the symbol BTa")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


    def testGetCurrentPriceWrongFiat(self):
        crypto = 'BTC'
        fiat = 'USL'
        exchange = 'all'

        resultData = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
        self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - There is no data for any of the toSymbols USL")
        self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, resultData.getValue(resultData.RESULT_KEY_FIAT))
        self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


if __name__ == '__main__':
    unittest.main()
