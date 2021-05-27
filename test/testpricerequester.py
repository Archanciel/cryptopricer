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
		unit = 'USD'
		exchange = 'CCCAGG'
		utcArrowDateTimeObj_endOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC',
																				   "YYYY/MM/DD HH:mm:ss")
		resultData = ResultData()
		resultData = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto,
																		  unit,
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
		unit = 'USD'
		exchange = 'CCCAGG'
		utcArrowDateTimeObj_midOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 12:59:59", 'UTC',
																				   "YYYY/MM/DD HH:mm:ss")
		resultData = ResultData()
		resultData = self.priceRequester._getHistoDayPriceAtUTCTimeStamp(crypto,
																		  unit,
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
		unit = 'USD'
		exchange = 'CCCAGG'
		localTimeZone = 'Europe/Zurich'
		timeStampLocal = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 23:59:59", localTimeZone,
																"YYYY/MM/DD HH:mm:ss")
		timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
																	"YYYY/MM/DD HH:mm:ss")
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocal,
																		  localTimeZone,
																		  timeStampUtcNoHHMM,
																		  exchange)
		self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
		priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
																	   'UTC')
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
		self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
		self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampMidOfDay(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'CCCAGG'
		localTimeZone = 'Europe/Zurich'

		timeStampLocal = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", localTimeZone,
																"YYYY/MM/DD HH:mm:ss")
		timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
																	"YYYY/MM/DD HH:mm:ss")
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocal,
																		  localTimeZone,
																		  timeStampUtcNoHHMM,
																		  exchange)

		self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
		priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
																	   'UTC')
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
		self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
		self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtTimeStampZurichMidOfDayUseTimeStamp(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'CCCAGG'

		#time stamp is always UTC !
		timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", 'Europe/Zurich',
																"YYYY/MM/DD HH:mm:ss")
		timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
																	"YYYY/MM/DD HH:mm:ss")
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, unit,
																		  timeStampLocalMidDay,
																		  'Europe/Zurich',
																		  timeStampUtcNoHHMM,
																		  exchange)
		self.assertEqual(1506729600, resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP))
		priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(resultData.getValue(resultData.RESULT_KEY_PRICE_TIME_STAMP),
																	   'UTC')
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
		self.assertEqual('30/09/17', priceArrowUTCDateTime.format(self.configMgr.dateOnlyFormat))
		self.assertEqual(4360.62, resultData.getValue(resultData.RESULT_KEY_PRICE))
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDay(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'CCCAGG'
		utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
		utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)

		# for histominute price,
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalForHistoMinute=utcArrowDateTimeObj.timestamp,
																		  localTz=None,
																		  timeStampUTCNoHHMMForHistoDay=utcArrowDateTimeObj.timestamp,
																		  exchange=exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDay_USD_CHF(self):
		crypto = 'USD'
		unit = 'CHF'
		exchange = 'CCCAGG'
		now = DateTimeUtil.localNow('Europe/Zurich')
		oneDaysBeforeArrowDate = now.shift(days=-1).date()

		utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
		utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-1)
		utcArrowDateTimeStamp = DateTimeUtil.shiftTimeStampToEndOfDay(utcArrowDateTimeObj.timestamp)

		# for histominute price,
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalForHistoMinute=utcArrowDateTimeStamp,
																		  localTz=None,
																		  timeStampUTCNoHHMMForHistoDay=utcArrowDateTimeStamp,
																		  exchange=exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPrice(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'CCCAGG'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampLessThanSevenDayWrongExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'unknown'

		utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
		utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-2)

		#here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalForHistoMinute=utcArrowDateTimeObj.timestamp,
																		  localTz=None,
																		  timeStampUTCNoHHMMForHistoDay=utcArrowDateTimeObj.timestamp,
																		  exchange=exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampMoreThanSevenDayWrongExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'unknown'

		utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
		utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-12)

		#here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalForHistoMinute=utcArrowDateTimeObj.timestamp,
																		  localTz=None,
																		  timeStampUTCNoHHMMForHistoDay=utcArrowDateTimeObj.timestamp,
																		  exchange=exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampMoreThanSevenDayForCryptoUnitPairNotSupportedByExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'Binance'

		utcArrowDateTimeObj = DateTimeUtil.localNow('UTC')
		utcArrowDateTimeObj = utcArrowDateTimeObj.shift(days=-12)

		#here, since histominute price is fetched, time stamp UTC no HHMM for histoDay wil not be used !
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalForHistoMinute=utcArrowDateTimeObj.timestamp,
																		  localTz=None,
																		  timeStampUTCNoHHMMForHistoDay=utcArrowDateTimeObj.timestamp,
																		  exchange=exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - Binance market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))








	def testGetMinuteHistoricalPriceForCryptoUnitPairNotSupportedByExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'Binance'
		localTimeZone = 'Europe/Zurich'
		#time stamp is always UTC !
		now = DateTimeUtil.localNow(localTimeZone)
		timeStampLocalNow = now.timestamp
		timeStampUtcNow = DateTimeUtil.utcNowTimeStamp()
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalNow,
																		  localTimeZone,
																		  timeStampUtcNow,
																		  exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_MINUTE)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - Binance market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetHistoricalPriceAtUTCTimeStampMidOfDayWrongExchange(self):
		crypto = 'BTC'

		unit = 'USD'
		exchange = 'Binance'
		localTimeZone = 'Europe/Zurich'
		#time stamp is always UTC !
		timeStampLocalMidDay = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 12:59:59", localTimeZone,
																"YYYY/MM/DD HH:mm:ss")
		timeStampUtcNoHHMM = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 00:00:00", 'UTC',
																	"YYYY/MM/DD HH:mm:ss")
		resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto,
																		  unit,
																		  timeStampLocalMidDay,
																		  localTimeZone,
																		  timeStampUtcNoHHMM,
																		  exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_HISTO_DAY)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - Binance market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'unknown'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - unknown market does not exist for this coin pair (BTC/USD).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongCrypto(self):
		crypto = 'BBB'
		unit = 'USD'
		exchange = 'all'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual("PROVIDER ERROR - all market does not exist for this coin pair (BBB/USD).", resultData.getValue(resultData.RESULT_KEY_ERROR_MSG))
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongPair(self):
		crypto = 'BTA'
		unit = 'CHF'
		exchange = 'all'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - all market does not exist for this coin pair (BTA/CHF).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


	def testGetCurrentPriceWrongUnit(self):
		crypto = 'BTC'
		unit = 'USL'
		exchange = 'all'

		resultData = self.priceRequester.getCurrentPrice(crypto, unit, exchange)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE), resultData.PRICE_TYPE_RT)
		self.assertEqual(resultData.getValue(resultData.RESULT_KEY_ERROR_MSG), "PROVIDER ERROR - all market does not exist for this coin pair (BTC/USL).")
		self.assertEqual(crypto, resultData.getValue(resultData.RESULT_KEY_CRYPTO))
		self.assertEqual(unit, resultData.getValue(resultData.RESULT_KEY_UNIT))
		self.assertEqual(exchange, resultData.getValue(resultData.RESULT_KEY_EXCHANGE))


if __name__ == '__main__':
	# unittest.main()
	tst = TestPriceRequester()
	tst.setUp()
	tst.testGetHistoricalPriceAtUTCTimeStampLessThanSevenDay_USD_CHF()
