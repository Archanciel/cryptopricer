import unittest
import os, sys, inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

from gui.guioutputformatter import GuiOutputFormatter
from resultdata import ResultData
from datetimeutil import DateTimeUtil
from configurationmanager import ConfigurationManager
from utilityfortest import UtilityForTest

class TestGuiOutputFormatter(unittest.TestCase):
	def setUp(self):
		if os.name == 'posix':
			FILE_PATH = '/sdcard/cryptopricer.ini'
		else:
			FILE_PATH = 'c:\\temp\\cryptopricer.ini'

		configMgr = ConfigurationManager(FILE_PATH)
		self.printer = GuiOutputFormatter(configMgr)


	def testPrintCryptoPriceHistorical(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'BitTrex'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


	def testPrintCryptoPriceHistoricalPriceValue(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'BitTrex'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01698205')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '70')

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('0.01698205 BTC/70 USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


	def testGetFullCommandStringYearDefinedDupl(self):
		crypto = 'ETH'
		unit = 'USD'

		resultData = ResultData()

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
							 'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})

		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual(fullCommandStringNoOptions, "eth usd 05/12/17 09:30 bittrex")


	def testPrintCryptoPriceHistoricalPriceValueDupl(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'BitTrex'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01698205')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '70')

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('0.01698205 BTC/70 USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


	def testPrintCryptoPriceHistoricalOptionValueGeneratedWarning(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'BitTrex'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, None)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, None)
		resultData.setWarning(ResultData.WARNING_TYPE_OPTION_VALUE,
							  "WARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD) -v option ignored")

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD on BitTrex: 12/09/17 00:00C 4122\nWARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD) -v option ignored\n', capturedStdout.getvalue())


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

		resultData = ResultData()

		recentDay = recent.day

		if recentDay < 10:
			recentDayStr = '0' + str(recentDay)
		else:
			recentDayStr = str(recentDay)

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122.09)

		dateTimeString = '{}/{}/{} 10:05'.format(recentDayStr, month, year - 2000)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD on BitTrex: {}M 4122.09\n'.format(dateTimeString), capturedStdout.getvalue())


	def testGetCryptoPriceHistoricalWrongExchange(self):
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'unknown'
		day = 12
		month = 9
		year = 2017
		hour = 10
		minute = 5

		resultData = ResultData()

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


	def testGetCryptoPriceRealTime(self):
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())


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

		resultData = ResultData()

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, None)
		resultData.setValue(resultData.RESULT_KEY_UNIT, None)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, None)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, None)
		resultData.setValue(resultData.RESULT_KEY_PRICE, None)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, None)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


	def testGetCryptoPriceRealTimeExchangeNotSupportPair(self):
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'BTC38'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - BTC38 market does not exist for this coin pair (BTC-USD)")
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		resultData.setValue(resultData.RESULT_KEY_PRICE, None)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, None)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual("ERROR - BTC38 market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


	def test_formatPriceFloatToStrRoundedFloat(self):
		y = round(5.59, 1)
		self.assertEqual('5.6', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))


	def test_formatPriceFloatToStrEmptystr(self):
		y = ''
		self.assertEqual('', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))


	def test_formatPriceFloatToStrNone(self):
		y = None
		self.assertEqual('', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))


	def test_formatPriceFloatToStrNineDigits(self):
		y = 	0.999999999
		self.assertEqual('1', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))


	def test_formatPriceFloatToStrFourDigits(self):
		y = 0.9084
		self.assertEqual('0.9084', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))


	def test_formatPriceFloatToStrinteger(self):
		y = 40
		self.assertEqual('40', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))


	def test_formatPriceFloatToStrNormal(self):
		y = 2000.085
		self.assertEqual('2000.085', self.printer._formatPriceFloatToStr(y, self.printer.PRICE_FLOAT_FORMAT))

	@unittest.skip
	def testToFromClipboard(self):
		'''
		Causes inomprensible error on Windows although clipboard works ok !

		:return:
		'''

		if os.name == 'posix':
			#causes an exception after updating all conda packages on 7.2.2018 !
			pass
		else:
			FILE_PATH = 'c:\\temp\\cryptopricer.ini'

			configMgr = ConfigurationManager(FILE_PATH)
			printer = GuiOutputFormatter(configMgr, activateClipboard=True)
			y = 2000.085
			printer.toClipboard(y)
			clipValue = printer.fromClipboard()
			self.assertTrue(str(y) == clipValue)


	def testGetFullCommandStringYearNone(self):
		now = DateTimeUtil.localNow('Europe/Zurich')

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		crypto = 'ETH'
		unit = 'USD'

		resultData = ResultData()

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': None, 'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None})
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
							 'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})

		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual(fullCommandStringNoOptions, "eth usd 05/12/17 09:30 bittrex")


	def testGetFullCommandStringYearDefined(self):
		crypto = 'ETH'
		unit = 'USD'

		resultData = ResultData()

		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
							 'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})

		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual(fullCommandStringNoOptions, "eth usd 05/12/17 09:30 bittrex")


	def testGetCryptoPriceRealTimeWithOptionValue(self):
		#correspond to command btc usd 0 bittrex -v0.01btc
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '160')
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': '0.01', 'OPTION_VALUE_SYMBOL': 'btc', 'OPTION_VALUE_SAVE': False,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('0.01 BTC/160 USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)
		self.assertEqual('btc usd 0 bittrex -v0.01btc', fullCommandStrWithOptions)


	def testGetCryptoPriceRealTimeWithOptionValueSave(self):
		#correspond to command btc usd 0 bittrex -vs0.01btc
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '160')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': '0.01', 'OPTION_VALUE_SYMBOL': 'btc', 'OPTION_VALUE_SAVE': True,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('0.01 BTC/160 USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -vs0.01btc', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)


	def testGetCryptoPriceRealTimeWithOptionValueGeneratedWarning(self):
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setWarning(ResultData.WARNING_TYPE_OPTION_VALUE,
							  "WARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD). -v option ignored !")

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD on BitTrex: {}R \nWARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD). -v option ignored !\n'.format(dateTimeString), capturedStdout.getvalue())


	def testGetCryptoPriceRealTimeOptionFiat(self):
		# btc usd 0 bittrex -fchf
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		fiat = 'CHF'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD/CHF.AVG on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())

	def testPrintCryptoPriceHistoricalOptionFiat(self):
		# btc usd 12/9/17 bittrex -feur
		crypto = 'BTC'
		unit = 'USD'
		fiat = 'EUR'
		exchange = 'BitTrex'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 3463.7166)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD/EUR.AVG on BitTrex: 12/09/17 00:00C 4122 3463.7166\n', capturedStdout.getvalue())

	def testPrintCryptoPriceHistoricalOptionFiatSave(self):
		# btc usd 12/9/17 bittrex -fseur
		crypto = 'BTC'
		unit = 'USD'
		fiat = 'EUR'
		exchange = 'BitTrex'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 3463.7166)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, True)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD/EUR.AVG on BitTrex: 12/09/17 00:00C 4122 3463.7166\n', capturedStdout.getvalue())

	def testPrintCryptoPriceHistoricalOptionFiatExchange(self):
		# mco eth 12/9/17 binance -fbtc.kraken
		crypto = 'MCO'
		unit = 'ETH'
		fiat = 'BTC'
		exchange = 'Binance'
		fiatExchange = 'Kraken'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 0.02802)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, fiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 0.001975)

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('MCO/ETH/BTC.Kraken on Binance: 12/09/17 00:00C 0.02802 0.001975\n', capturedStdout.getvalue())

	def testPrintCryptoPriceHistoricalOptionValueAndFiatExchange(self):
		# mco btc 12/9/17 binance -feth.kraken -v1eth
		# 34.39239 MCO/0.07047 BTC/1 ETH.Kraken on Binance: 12/09/17 00:00C 0.002049 0.029076
		crypto = 'MCO'
		unit = 'BTC'
		fiat = 'ETH'
		exchange = 'Binance'
		fiatExchange = 'Kraken'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
		resultData.setValue(resultData.RESULT_KEY_PRICE, 0.002049)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, 34.39238653001464)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, 0.07047)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, 1)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, fiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 0.02907620263942103)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': crypto, 'UNIT': unit, 'EXCHANGE': exchange, 'DAY': '12', 'MONTH': '9', 'YEAR': '17', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'HISTO', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': '1', 'OPTION_VALUE_SYMBOL': 'eth', 'OPTION_VALUE_SAVE': False})

		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('34.39238653 MCO/0.07047 BTC/1 ETH.Kraken on Binance: 12/09/17 00:00C 0.002049 0.0290762\n', capturedStdout.getvalue())

# testing value option

	def testGetCryptoPriceRealTimeWithValueFlag(self):
		#correspond to command btc usd 0 bittrex -v0.01btc
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '160')
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': '0.01', 'OPTION_VALUE_SYMBOL': 'btc', 'OPTION_VALUE_SAVE': None,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('0.01 BTC/160 USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

	def testGetCryptoPriceRealTimeWithValueSaveFlag(self):
		#correspond to command btc usd 0 bittrex -vs0.01btc
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '160')
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': '0.01', 'OPTION_VALUE_SYMBOL': 'btc', 'OPTION_VALUE_SAVE': True,
							 'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('0.01 BTC/160 USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -vs0.01btc', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

# testing fiat option

	def testGetCryptoPriceRealTimeWithFiatFlag(self):
		#correspond to command btc usd 0 bittrex -fchf
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'Kraken')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None, 'OPTION_VALUE_SAVE': None,'OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': 'kraken', 'OPTION_FIAT_SAVE': None})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD/CHF.Kraken on BitTrex: {}R {} {}\n'.format(dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

	def testGetCryptoPriceRealTimeWithFiatSaveFlag(self):
		#correspond to command btc usd 0 bittrex -fschf
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'Kraken')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None, 'OPTION_VALUE_SAVE': None,'OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': 'kraken', 'OPTION_FIAT_SAVE': True})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('BTC/USD/CHF.Kraken on BitTrex: {}R {} {}\n'.format(dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -fschf.kraken', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

# testing value and fiat options

	def testGetCryptoPriceRealTimeWithValueAndFiatFlag(self):
		#correspond to command btc usd 0 bittrex -v1000chf -fchf
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionValueSymbol = 'chf'
		optionValueAmount = 1000 # 1000 chf
		optionValueCrypto = 0.118874
		optionValueUnit = 994.035785
		optionValueFiat = optionValueAmount
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, None)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'Kraken')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, None)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': None,'OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': 'kraken', 'OPTION_FIAT_SAVE': None})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('{} BTC/{} USD/{} CHF.Kraken on BitTrex: {}R {} {}\n'.format(optionValueCrypto, optionValueUnit, optionValueFiat, dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)
		self.assertEqual('btc usd 0 bittrex -v1000chf -fchf.kraken', fullCommandStrWithOptions)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, None)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': None,'OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': None, 'OPTION_FIAT_SAVE': None})
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual(None, fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)
		self.assertEqual('btc usd 0 bittrex -v1000chf -fchf', fullCommandStrWithOptions)

	def testGetCryptoPriceRealTimeWithValueSaveAndFiatFlag(self):
		#correspond to command btc usd 0 bittrex -vs1000chf -fchf.kraken
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionValueSymbol = 'chf'
		optionValueAmount = 1000 # 1000 chf
		optionValueCrypto = 0.118874
		optionValueUnit = 994.035785
		optionValueFiat = optionValueAmount
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'Kraken')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, None)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': 's','OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': 'kraken', 'OPTION_FIAT_SAVE': None})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('{} BTC/{} USD/{} CHF.Kraken on BitTrex: {}R {} {}\n'.format(optionValueCrypto, optionValueUnit, optionValueFiat, dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -vs1000chf', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

	def testGetCryptoPriceRealTimeWithValueSaveAndFiatFlagNoFiatExchange(self):
		#correspond to command btc usd 0 bittrex -vs1000chf -fchf
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionValueSymbol = 'chf'
		optionValueAmount = 1000 # 1000 chf
		optionValueCrypto = 0.118874
		optionValueUnit = 994.035785
		optionValueFiat = optionValueAmount
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, None)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': 's','OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': None, 'OPTION_FIAT_SAVE': None})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('{} BTC/{} USD/{} CHF.AVG on BitTrex: {}R {} {}\n'.format(optionValueCrypto, optionValueUnit, optionValueFiat, dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -vs1000chf', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

	def testGetCryptoPriceRealTimeWithValueAndFiatSaveFlag(self):
		#correspond to command btc usd 0 bittrex -vs1000chf -fschf.kraken
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionValueSymbol = 'chf'
		optionValueAmount = 1000 # 1000 chf
		optionValueCrypto = 0.118874
		optionValueUnit = 994.035785
		optionValueFiat = optionValueAmount
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, None)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'Kraken')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': None,'OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': 'kraken', 'OPTION_FIAT_SAVE': 's'})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('{} BTC/{} USD/{} CHF.Kraken on BitTrex: {}R {} {}\n'.format(optionValueCrypto, optionValueUnit, optionValueFiat, dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -fschf.kraken', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

	def testGetCryptoPriceRealTimeWithValueSaveAndFiatSaveFlag(self):
		#correspond to command btc usd 0 bittrex -vs1000chf -fschf.kraken
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionValueSymbol = 'chf'
		optionValueAmount = 1000 # 1000 chf
		optionValueCrypto = 0.118874
		optionValueUnit = 994.035785
		optionValueFiat = optionValueAmount
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'Kraken')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': 's','OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': 'kraken', 'OPTION_FIAT_SAVE': 's'})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('{} BTC/{} USD/{} CHF.Kraken on BitTrex: {}R {} {}\n'.format(optionValueCrypto, optionValueUnit, optionValueFiat, dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -vs1000chf -fschf.kraken', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)

	def testGetCryptoPriceRealTimeWithValueSaveAndFiatSaveFlagNoFiatExchange(self):
		#correspond to command btc usd 0 bittrex -vs1000chf -fschf
		now = DateTimeUtil.localNow('Europe/Zurich')
		crypto = 'BTC'
		unit = 'USD'
		unitPrice = 8362.07 # btc price in usd
		fiat = 'CHF'
		optionValueSymbol = 'chf'
		optionValueAmount = 1000 # 1000 chf
		optionValueCrypto = 0.118874
		optionValueUnit = 994.035785
		optionValueFiat = optionValueAmount
		optionFiatComputedAmount = 8412.24242 # btc price in chf
		exchange = 'bittrex'
		day = 0
		month = 0
		year = 0
		hour = 1
		minute = 1

		resultData = ResultData()

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

		#rt price not provided here !
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
		resultData.setValue(resultData.RESULT_KEY_PRICE, unitPrice)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
		dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatComputedAmount)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, True)
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
							{'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
							 'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
							 'OPTION_VALUE_AMOUNT': optionValueAmount, 'OPTION_VALUE_SYMBOL': optionValueSymbol, 'OPTION_VALUE_SAVE': 's','OPTION_FIAT_DATA': None,
							 'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': None, 'OPTION_FIAT_SAVE': 's'})
		stdout = sys.stdout
		capturedStdout = StringIO()
		sys.stdout = capturedStdout

		self.printer.printDataToConsole(resultData)
		sys.stdout = stdout
		self.assertEqual('{} BTC/{} USD/{} CHF.AVG on BitTrex: {}R {} {}\n'.format(optionValueCrypto, optionValueUnit, optionValueFiat, dateTimeString, unitPrice, optionFiatComputedAmount), capturedStdout.getvalue())
		fullCommandStringNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		self.assertEqual('btc usd 0 bittrex -vs1000chf -fschf', fullCommandStrWithSaveModeOptions)
		self.assertEqual('btc usd 0 bittrex', fullCommandStringNoOptions)
	
# historical value and fiat option test
	
	def testGetFullCommandStringOptionValueSaveOptionFiatSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fschsb.hitbtc
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.00000746
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.016186335
		optionValueInFiat = 1525.5735155513667
		optionValueSave = 's'
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 94250.7068803016
		optionFiatCryptoInFiatRate = 0.7031102733270499
		optionFiatSave = 's'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)

		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)

		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)

		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc', fullCommandStrWithSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

	def testGetFullCommandStringOptionValueNoSaveOptionFiatSave(self):
		# krl btc 20/12/20 hitbtc -v2169.75krl -fschsb.hitbtc
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.00000746
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.016186335
		optionValueInFiat = 1525.5735155513667
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 94250.7068803016
		optionFiatCryptoInFiatRate = 0.7031102733270499
		optionFiatSave = 's'

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)

		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)

		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)

		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fschsb.hitbtc', fullCommandStrWithSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fschsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

	def testGetFullCommandStringOptionValueSaveOptionFiatNoSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fchsb.hitbtc
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.00000746
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.016186335
		optionValueInFiat = 1525.5735155513667
		optionValueSave = 's'
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 94250.7068803016
		optionFiatCryptoInFiatRate = 0.7031102733270499
		optionFiatSave = None

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)

		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)

		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)

		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fchsb.hitbtc', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl', fullCommandStrWithSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fchsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

	def testGetFullCommandStringOptionValueNoSaveOptionFiatNoSave(self):
		# krl btc 20/12/20 hitbtc -v2169.75krl -fchsb.hitbtc
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.00000746
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.016186335
		optionValueInFiat = 1525.5735155513667
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 94250.7068803016
		optionFiatCryptoInFiatRate = 0.7031102733270499
		optionFiatSave = None

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': None,
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': None,
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)

		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)

		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)

		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fchsb.hitbtc', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fchsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)


	def testGetFullCommandStringOptionValueNoSaveOptionFiatNoSaveOptionValueWarning(self):
		# krl btc 20/12/20 hitbtc -v2169.75usd -fchsb.hitbtc
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHF'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.00000746
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.016186335
		optionValueInFiat = 1525.5735155513667
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 94250.7068803016
		optionFiatCryptoInFiatRate = 0.7031102733270499
		optionFiatSave = None

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'usd',
																		  'OPTION_VALUE_SAVE': None,
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chf',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': None,
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.setWarning(resultData.WARNING_TYPE_OPTION_VALUE, "WARNING - currency value symbol USD differs from crypto (KRL), unit (BTC) and fiat (CHSB) -v option ignored"), None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)

		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)

		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)

		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75usd -fchf.hitbtc', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75usd -fchf.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHF = 0.70311027 KRL/CHF)', fullCommandStrForStatusBar)


	def testGetFullCommandStringOptionValueSaveOptionFiatSaveOptionValueWarning(self):
		# krl btc 20/12/20 hitbtc -vs2169.75usd -fschsb.hitbtc
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHF'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.00000746
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.016186335
		optionValueInFiat = 1525.5735155513667
		optionValueSave = True
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 94250.7068803016
		optionFiatCryptoInFiatRate = 0.7031102733270499
		optionFiatSave = True

		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'usd',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chf',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.setWarning(resultData.WARNING_TYPE_OPTION_VALUE, "WARNING - currency value symbol USD differs from crypto (KRL), unit (BTC) and fiat (CHSB) -v option ignored"), None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)

		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)

		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)

		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)

		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fschf.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHF = 0.70311027 KRL/CHF)', fullCommandStrForStatusBar)

# historical value, fiat and price option test

# price save
	
	def testGetFullCommandStringOptionValueSaveOptionFiatSaveOptionPriceSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fschsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = 's'
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = 's'
		optionPricePrice = 0.0000075
		optionPriceSave = 's'
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc -ps0.0000075', fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc -ps0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)
	
	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueNoSaveOptionFiatSaveOptionPriceSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fschsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = 's'
		optionPricePrice = 0.0000075
		optionPriceSave = 's'
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fschsb.hitbtc -p0.0000075', fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fschsb.hitbtc -ps0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)
	
	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueSaveOptionFiatNoSaveOptionPriceSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fchsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = 's'
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = None
		optionPricePrice = 0.0000075
		optionPriceSave = 's'
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fchsb.hitbtc', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -ps0.0000075', fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fchsb.hitbtc -ps0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)
	
	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueNoSaveOptionFiatNoSaveOptionPriceSave(self):
		# krl btc 20/12/20 hitbtc -v2169.75krl -fchsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = None
		optionPricePrice = 0.0000075
		optionPriceSave = 's'
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fchsb.hitbtc', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -ps0.0000075', fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fchsb.hitbtc -ps0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)

# price no save
	
	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueSaveOptionFiatSaveOptionPriceNoSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fschsb.hitbtc -p0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = 's'
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = 's'
		optionPricePrice = 0.0000075
		optionPriceSave = None
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -p0.0000075', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc',
						 fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc -p0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)
	
	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueNoSaveOptionFiatSaveOptionPriceNoSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fschsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = 's'
		optionPricePrice = 0.0000075
		optionPriceSave = None
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -p0.0000075', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fschsb.hitbtc', fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fschsb.hitbtc -p0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)
	
	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueSaveOptionFiatNoSaveOptionPriceNoSave(self):
		# krl btc 20/12/20 hitbtc -vs2169.75krl -fchsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = 's'
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = None
		optionPricePrice = 0.0000075
		optionPriceSave = None
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fchsb.hitbtc -p0.0000075', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl', fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fchsb.hitbtc -p0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)

	@unittest.skip # skipping while handling price option in GuiOutputFormatter not yet implemented
	def testGetFullCommandStringOptionValueNoSaveOptionFiatNoSaveOptionPriceNoSave(self):
		# krl btc 20/12/20 hitbtc -v2169.75krl -fchsb.hitbtc -ps0.0000075
		crypto = 'KRL'
		unit = 'BTC'
		fiat = 'CHSB'
		cryptoUnitExchange = 'HitBTC'
		requestDateStr = '20/12/20 00:00'
		requestTimeStamp = 1608422400
		cryptoPriceInUnit = 0.0000075
		priceType = ResultData.PRICE_TYPE_HISTO_DAY
		optionValueInCrypto = 2169.75
		optionValueInUnit = 0.01627312
		optionValueInFiat = 382.10436619
		optionValueSave = None
		optionFiatExchange = 'HitBTC'
		optionFiatUnitInFiatRate = 23480.7
		optionFiatCryptoInFiatRate = 0.17610525
		optionFiatSave = None
		optionPricePrice = 0.0000075
		optionPriceSave = None
		
		resultData = ResultData()
		resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'krl',
																		  'UNIT': 'btc',
																		  'EXCHANGE': 'hitbtc',
																		  'DAY': '20',
																		  'MONTH': '12',
																		  'YEAR': '20',
																		  'HOUR': '00',
																		  'MINUTE': '00',
																		  'DMY': None,
																		  'HM': None,
																		  'PRICE_TYPE': 'HISTO',
																		  'OPTION_VALUE_DATA': None,
																		  'OPTION_VALUE_AMOUNT': '2169.75',
																		  'OPTION_VALUE_SYMBOL': 'krl',
																		  'OPTION_VALUE_SAVE': 's',
																		  'OPTION_FIAT_DATA': None,
																		  'OPTION_FIAT_SYMBOL': 'chsb',
																		  'OPTION_FIAT_EXCHANGE': 'hitbtc',
																		  'OPTION_FIAT_AMOUNT': None,
																		  'OPTION_FIAT_SAVE': 's',
																		  'OPTION_PRICE_DATA': None,
																		  'OPTION_PRICE_AMOUNT': None,
																		  'OPTION_PRICE_SYMBOL': None,
																		  'OPTION_PRICE_EXCHANGE': None,
																		  'OPTION_PRICE_SAVE': None,
																		  'UNSUPPORTED_OPTION': None,
																		  'UNSUPPORTED_OPTION_MODIFIER': None,
																		  'UNSUPPORTED_OPTION_DATA': None})
		resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
		resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
		resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
		resultData.setValue(resultData.RESULT_KEY_EXCHANGE, cryptoUnitExchange)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, priceType)
		resultData.setValue(resultData.RESULT_KEY_PRICE, cryptoPriceInUnit)
		resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestDateStr)
		resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, requestTimeStamp)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueInCrypto)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueInUnit)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueInFiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, optionFiatExchange)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, optionFiatCryptoInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, optionFiatUnitInFiatRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, optionFiatSave)
		
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_AMOUNT, optionPricePrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_PRICE_SAVE, optionPriceSave)
		
		fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptions, fullCommandStrForStatusBar = self.printer.getFullCommandString(
			resultData)
		
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fchsb.hitbtc -p0.0000075', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptions)
		self.assertEqual(
			'krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fchsb.hitbtc -p0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/CHSB = 0.17610525 KRL/CHSB)',
			fullCommandStrForStatusBar)


if __name__ == '__main__':
	#	unittest.main()
	tst = TestGuiOutputFormatter()
	tst.setUp()
	tst.testGetFullCommandStringOptionValueSaveOptionFiatSave()
	tst.setUp()
	tst.testGetFullCommandStringOptionValueNoSaveOptionFiatSave()
	tst.setUp()
	tst.testGetFullCommandStringOptionValueSaveOptionFiatNoSave()
	tst.setUp()
	tst.testGetFullCommandStringOptionValueNoSaveOptionFiatNoSave()
	tst.setUp()
	tst.testPrintCryptoPriceHistoricalOptionValueGeneratedWarning()
	tst.setUp()
	tst.testGetFullCommandStringOptionValueNoSaveOptionFiatNoSaveOptionValueWarning()
	tst.setUp()
	tst.testGetFullCommandStringOptionValueSaveOptionFiatSaveOptionValueWarning()

# tst.setUp()
	# tst.testGetFullCommandStringOptionValueSaveOptionFiatSaveOptionPriceSave()
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueNoSaveOptionFiatSaveOptionPriceSave()
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueSaveOptionFiatNoSaveOptionPriceSave()
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueNoSaveOptionFiatNoSaveOptionPriceSave()
	#
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueSaveOptionFiatSaveOptionPriceNoSave()
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueNoSaveOptionFiatSaveOptionPriceNoSave()
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueSaveOptionFiatNoSaveOptionPriceNoSave()
	# tst.setUp()
	# tst.testGetFullCommandStringOptionValueNoSaveOptionFiatNoSaveOptionPriceNoSave()
