import unittest
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester
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
        priceInfoList = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto, fiat,
                                                                            utcArrowDateTimeObj_endOfDay.timestamp,
                                                                            exchange)
        self.assertEqual(1506729600, priceInfoList[self.priceRequester.IDX_TIMESTAMP])
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[self.priceRequester.IDX_TIMESTAMP],
                                                                       'UTC')
        self.assertTrue(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])


    def test_getHistoDayPriceAtUTCTimeStampMidOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj_midOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 12:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        priceInfoList = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto, fiat,
                                                                            utcArrowDateTimeObj_midOfDay.timestamp,
                                                                            exchange)
        self.assertEqual(1506729600, priceInfoList[self.priceRequester.IDX_TIMESTAMP])
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[self.priceRequester.IDX_TIMESTAMP],
                                                                       'UTC')
        self.assertTrue(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])


    def testGetHistoricalPriceAtUTCTimeStampEndOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj_endOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                            utcArrowDateTimeObj_endOfDay.timestamp,
                                                                            exchange)
        self.assertEqual(1506729600, priceInfoList[self.priceRequester.IDX_TIMESTAMP])
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[self.priceRequester.IDX_TIMESTAMP],
                                                                       'UTC')
        self.assertTrue(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])


    def testGetHistoricalPriceAtUTCTimeStampMidOfDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        utcArrowDateTimeObj_midOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 12:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                            utcArrowDateTimeObj_midOfDay.timestamp,
                                                                            exchange)
        self.assertEqual(1506729600, priceInfoList[self.priceRequester.IDX_TIMESTAMP])
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[self.priceRequester.IDX_TIMESTAMP],
                                                                       'UTC')
        self.assertTrue(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])


    def testGetHistoricalPriceAtTimeStampZurichMidOfDayUseTimeStamp(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'
        #time stamp is always UTC !
        timeStampUtc = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
                                                              "YYYY/MM/DD HH:mm:ss")
        priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                            timeStampUtc,
                                                                            exchange)
        self.assertEqual(1506729600, priceInfoList[self.priceRequester.IDX_TIMESTAMP])
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[self.priceRequester.IDX_TIMESTAMP],
                                                                       'UTC')
        self.assertTrue(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
        self.assertEqual(4360.62, priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])


    def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDay(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)
        priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertFalse(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])


    def testGetCurrentPrice(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'CCCAGG'

        priceInfoList = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertFalse(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])


    def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDayWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
        utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)
        priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj.timestamp,
                                                                             exchange)
        self.assertFalse(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual("ERROR - e param is not valid the market does not exist for this coin pair", priceInfoList[self.priceRequester.IDX_ERROR_MSG])

    def testGetHistoricalPriceAtUTCTimeStampMidOfDayWrongExchange(self):
        crypto = 'BTC'

        fiat = 'USD'
        exchange = 'unknown'
        utcArrowDateTimeObj_midOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 12:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat,
                                                                             utcArrowDateTimeObj_midOfDay.timestamp,
                                                                             exchange)
        self.assertTrue(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual("ERROR - e param is not valid the market does not exist for this coin pair", priceInfoList[self.priceRequester.IDX_ERROR_MSG])


    def testGetCurrentPriceWrongExchange(self):
        crypto = 'BTC'
        fiat = 'USD'
        exchange = 'unknown'

        priceInfoList = self.priceRequester.getCurrentPrice(crypto, fiat, exchange)
        self.assertFalse(priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE])
        self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)", priceInfoList[self.priceRequester.IDX_ERROR_MSG])


if __name__ == '__main__':
    unittest.main()
