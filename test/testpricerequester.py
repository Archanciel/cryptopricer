import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester
from priceresult import PriceResult
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
        priceResult = PriceResult()
        priceResult = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto,
                                                                          fiat,
                                                                          utcArrowDateTimeObj_endOfDay.timestamp,
                                                                          exchange,
                                                                          priceResult)
        self.assertEqual(1506729600, priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceResult.getValue(priceResult.RESULT_KEY_PRICE))


    def test_getHistoDayPriceAtUTCTimeStampMidOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj_midOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 12:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        priceResult = PriceResult()
        priceResult = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto,
                                                                          fiat,
                                                                          utcArrowDateTimeObj_midOfDay.timestamp,
                                                                          exchange,
                                                                          priceResult)
        self.assertEqual(1506729600, priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceResult.getValue(priceResult.RESULT_KEY_PRICE))


    def testGetHistoricalPriceAtUTCTimeStampEndOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        timeStampLocal = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 23:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             timeStampLocal,
                                                                             timeStampUtcNoHHMM,
                                                                             exchange)
        self.assertEqual(1506729600, priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceResult.getValue(priceResult.RESULT_KEY_PRICE))
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampMidOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        timeStampLocal = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             timeStampLocal,
                                                                             timeStampUtcNoHHMM,
                                                                             exchange)

        self.assertEqual(1506729600, priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceResult.getValue(priceResult.RESULT_KEY_PRICE))
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtTimeStampZurichMidOfDayUseTimeStamp(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        #time stamp is always UTC !
        timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             timeStampLocalMidDay,
                                                                             timeStampUtcNoHHMM,
                                                                             exchange)
        self.assertEqual(1506729600, priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TIME_STAMP),
                                                                       'UTC')
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceResult.getValue(priceResult.RESULT_KEY_PRICE))
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)

        # for histominute price,
        priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_CURRENT_OR_HISTO_MINUTE)
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetCurrentPrice(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        priceResult = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_CURRENT_OR_HISTO_MINUTE)
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDayWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)

        #here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
        priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_CURRENT_OR_HISTO_MINUTE)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), "ERROR - e param is not valid the market does not exist for this coin pair")
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetHistoricalPriceAtUTCTimeStampMidOfDayWrongExchange(self):
        crypto = 'BTC'

        fiat = 'USD'
        exchange = 'unknown'
        #time stamp is always UTC !
        timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                                "YYYY/MM/DD HH:mm:ss")
        timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
                                                                    "YYYY/MM/DD HH:mm:ss")
        priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
                                                                           fiat,
                                                                           timeStampLocalMidDay,
                                                                           timeStampUtcNoHHMM,
                                                                           exchange)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_HISTO_DAY)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), "ERROR - e param is not valid the market does not exist for this coin pair")
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


    def testGetCurrentPriceWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        priceResult = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE), priceResult.PRICE_TYPE_CURRENT_OR_HISTO_MINUTE)
        self.assertEqual(priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG), "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        self.assertEqual(crypto, priceResult.getValue(priceResult.RESULT_KEY_CRYPTO))
        self.assertEqual(fiat, priceResult.getValue(priceResult.RESULT_KEY_FIAT))
        self.assertEqual(exchange, priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE))


if __name__ == '__main__':
    unittest.main()
