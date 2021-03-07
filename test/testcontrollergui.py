import unittest
import os,sys,inspect

LOCAL_TIME_ZONE = 'Europe/Zurich'

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

import re
from controller import Controller
from datetimeutil import DateTimeUtil
from gui.guioutputformatter import GuiOutputFormatter
from configurationmanager import ConfigurationManager
from pricerequesterteststub import PriceRequesterTestStub
from utilityfortest import UtilityForTest


class TestControllerGui(unittest.TestCase):
	'''
	This test class is launched from allguy.py, the class that runs
	all the tests in Pydroid on Android.

	Test the Controller using a GuiOuputFormater in place of a ConsoleOutputFormaater
	since GuiOuputFormatter runs on Android in Pydroid, but fails in QPython !

	All the test cases are defined in the TestController parent to avoid code duplication
	'''
	def setUp(self):
		if os.name == 'posix':
			FILE_PATH = '/sdcard/cryptopricer.ini'
		else:
			FILE_PATH = 'c:\\temp\\cryptopricer.ini'

		configMgr = ConfigurationManager(FILE_PATH)
		self.controller = Controller(GuiOutputFormatter(configMgr), configMgr, PriceRequesterTestStub())


	def testControllerBugSpecifyDateBegOfYear(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		requestYearStr = nowYearStr
		requestDayStr = '1'
		requestMonthStr = '1'
		requestArrowDate = DateTimeUtil.dateTimeComponentsToArrowLocalDate(int(requestDayStr), int(requestMonthStr), now.year, 0, 0, 0, timezoneStr)
		inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(requestArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = '00'
			minuteStr = '00'
			priceType = 'M'

		self.assertEqual(
			'MCO/BTC on AVG: ' + '0{}/0{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('mco btc 0{}/0{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultFullRequestNoDateNoTime(self):
		inputStr = 'mco btc all'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - date not valid.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testGetPrintableResultForReplayRealTime(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
		# 													   nowMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
			
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForReplayHistoDay(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		eightDaysBeforeArrowDate = now.shift(days=-8)
		
		if eightDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testGetPrintableResultForReplayHistoDay()', now))
			return
		
		eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

		requestDayStr = eightDaysBeforeDayStr
		requestMonthStr = eightDaysBeforeMonthStr
		requestYearStr = eightDaysBeforeYearStr
		inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = eightDaysBeforeHourStr
			minuteStr = eightDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'MCO/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'MCO/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForReplayHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForReplayHistoMinuteDayMonthOnly(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-2)
		
		if fiveDaysBeforeArrowDate.year < now.year:
			print(
				'{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format(
					'testGetPrintableResultForReplayHistoMinuteDayMonthOnly()', now))
			return
		
		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{} binance'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = '00'
			minuteStr = '00'
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForRealThenChangeTimeThenChangeCrypto(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
		# 													   nowMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		tenMinutesBeforeArrowDate = now.shift(minutes=-10)

		tenMinutesBeforeYearStr, tenMinutesBeforeMonthStr, tenMinutesBeforeDayStr, tenMinutesBeforeHourStr, tenMinutesBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenMinutesBeforeArrowDate)

		requestHourStr = tenMinutesBeforeHourStr
		requestMinuteStr = tenMinutesBeforeMinuteStr

		if DateTimeUtil.isDateOlderThan(tenMinutesBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = requestHourStr
			minuteStr = requestMinuteStr
			priceType = 'M'

		#next command: '-t' 10 minutes before
		inputStr = '-t{}:{}'.format(hourStr, minuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
															   minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '-ceth'
		inputStr = '-ceth'.format(hourStr, minuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(tenMinutesBeforeDayStr, tenMinutesBeforeMonthStr, tenMinutesBeforeYearStr, hourStr,
															   minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInvalidDayFormatAfterHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: -d with invalid date format
		inputStr = '-d10:01'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: 10:01 violates format for day (DD/MM).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInvalidMonthFormatAfterHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: -d with invalid date format
		inputStr = '-d10/O1'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: O1 violates format for month (DD/MM).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInvalidYearFormatAfterHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: -d with invalid date format
		inputStr = '-d1/1/20O1'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: 20O1 violates format for year (DD/MM/YY).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInvalidMinuteFormatAfterHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: -t with invalid time format
		inputStr = '-t10:O1'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: O1 violates format for minute (HH:mm).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInvalidMinuteValueAfterHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: -t with invalid time format
		inputStr = '-t10:61'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - minute must be in 0..59.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInvalidHourFormatAfterHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: -t with invalid time format
		inputStr = '-t1O:01'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: 1O violates format for hour (HH:mm).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForReplayRealTimeThenOneDigitDateSpec(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowBegOfMonth = now.replace(day=1)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
		nowBegOfMonthYearStr, nowBegOfMonthMonthStr, nowBegOfMonthDayStr, nowBegOfMonthHourStr, nowBegOfMonthMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonth)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '-d1'
		inputStr = '-d1'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(nowBegOfMonth, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = nowBegOfMonthHourStr
			minuteStr = nowBegOfMonthMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForReplayRealTimeThenTwoPartDateSpec(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowBegOfMonth = now.replace(day = 1, month = 1)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
		nowBegOfMonthYearStr, nowBegOfMonthMonthStr, nowBegOfMonthDayStr, nowBegOfMonthHourStr, nowBegOfMonthMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonth)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '-d1'
		inputStr = '-d1/1'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(nowBegOfMonth, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = nowBegOfMonthHourStr
			minuteStr = nowBegOfMonthMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthDayStr, nowBegOfMonthMonthStr, nowBegOfMonthYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForReplayRealTimeThenThreePartDateSpec(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowBegOfMonthLastYear = now.replace(day = 1, month = 1, year = now.year - 1)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
		nowBegOfMonthLastYearYearStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearHourStr, nowBegOfMonthLastYearMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(nowBegOfMonthLastYear)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '-d1'
		inputStr = '-d1/1/{}'.format(nowBegOfMonthLastYearYearStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(nowBegOfMonthLastYear, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = nowBegOfMonthLastYearHourStr
			minuteStr = nowBegOfMonthLastYearMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(nowBegOfMonthLastYearDayStr, nowBegOfMonthLastYearMonthStr, nowBegOfMonthLastYearYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInputScenarioWithInvalidOption(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 all -ebitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
			
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on AVG: R\nWarning - unsupported option -ebitfinex in request btc usd 0 all -ebitfinex - option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc usd 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		# then replay same request with no error
		inputStr = 'btc usd 0 all'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on AVG: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc usd 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForInputScenarioWithInvalidOptionInFullAndPartialRequests(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 all -zooo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on AVG: R\nWarning - unsupported option -zooo in request btc usd 0 all -zooo - option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc usd 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		# then enter partial request with same unsupported option
		inputStr = '-ueth -zooo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on AVG: R\nWarning - unsupported option -zooo in request -ueth -zooo - option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc eth 0 all', fullCommandStrNoOptions) #empty string since request caused an error !
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultWithInvalidDateCommandAfterInvalidTimeCommandFollowingRealTimeRequest(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next: invalid time command '-t12.56'
		inputStr = '-t12.56'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid partial request -t12.56: in -t12.56, 12.56 must respect HH:mm format.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next: invalid time command '-t12.56'
		inputStr = '-d23:11'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: 23:11 violates format for day (DD/MM).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultWithInvalidTimeCommandAfterInvalidDateCommandFollowingRealTimeRequest(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next: invalid time command '-t12.56'
		inputStr = '-d23:11'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: 23:11 violates format for day (DD/MM).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next: invalid time command '-t12.56'
		inputStr = '-t12.56'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid partial request -t12.56: in -t12.56, 12.56 must respect HH:mm format.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next: valid -e command
		inputStr = '-eall'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: 23:11 violates format for day (DD/MM).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultWithInvalidDateAndTimePartialRequestCommandsFollowingRealTimeRequest(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-d{}:{} -t00.01'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid partial request -d{}:{} -t00.01: in -t00.01, 00.01 must respect HH:mm format.'.format(requestDayStr, requestMonthStr), printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-t00:01'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - invalid value: {}:{} violates format for day (DD/MM).'.format(requestDayStr, requestMonthStr), printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-d{}/{}'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} 00:01M'.format(requestDayStr, requestMonthStr, requestYearStr,
															   requestHourStr,
															   requestMinuteStr),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} 00:01 bitfinex'.format(requestDayStr, requestMonthStr, requestYearStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForRealThenAddVSCommandAndChangeExchangeTimeCryptoDate(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
		# 													   nowMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		threeDaysBeforeArrowDate = now.shift(days=-3)
		
		if threeDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testGetPrintableResultForRealThenAddVSCommandAndChangeExchangeTimeCryptoDate()', now))
			return
		
		threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

		requestHourStr = threeDaysBeforeHourStr
		requestMinuteStr = threeDaysBeforeMinuteStr
		requestDayStr = threeDaysBeforeDayStr
		requestMonthStr = threeDaysBeforeMonthStr
		requestYearStr = threeDaysBeforeYearStr

		if DateTimeUtil.isDateOlderThan(threeDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = requestHourStr
			minuteStr = requestMinuteStr
			priceType = 'M'

		inputStr = '-vs100usd -eall -t{}:{} -ceth -d{}/{}'.format(requestHourStr, requestMinuteStr, requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth usd {}/{}/{} {}:{} all -vs100usd'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForRealThenChangeUnitExchangeTimeAddVSCommandAndChangeCryptoDate(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)


		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		threeDaysBeforeArrowDate = now.shift(days=-3)
		
		if threeDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testGetPrintableResultForRealThenChangeUnitExchangeTimeAddVSCommandAndChangeCryptoDate()', now))
			return
		
		threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

		requestHourStr = threeDaysBeforeHourStr
		requestMinuteStr = threeDaysBeforeMinuteStr
		requestDayStr = threeDaysBeforeDayStr
		requestMonthStr = threeDaysBeforeMonthStr
		requestYearStr = threeDaysBeforeYearStr

		if DateTimeUtil.isDateOlderThan(threeDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = requestHourStr
			minuteStr = requestMinuteStr
			priceType = 'M'

		inputStr = '-ubtc -eall -t{}:{} -vs100eth -ceth -d{}/{}'.format(requestHourStr, requestMinuteStr, requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth btc {}/{}/{} {}:{} all -vs100eth'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr), fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForHistoMinuteWithMarketNotExistForCoinPairAndInvalidOptionCausingErrorAndWarning(self):
		#first command: RT price request with invalid option
		inputStr = 'btc eth 0 binance -eall'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -eall in request btc eth 0 binance -eall - option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
														  
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		threeDaysBeforeArrowDate = now.shift(days=-3)
		
		if threeDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testGetPrintableResultForHistoMinuteWithMarketNotExistForCoinPairAndInvalidOptionCausingErrorAndWarning()', now))
			return
		
		threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

		requestDayStr = threeDaysBeforeDayStr
		requestMonthStr = threeDaysBeforeMonthStr

		#second command: histo minute price request with invalid option
		inputStr = 'btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/ETH on Binance: {}/{}/{} 00:00M\nWarning - unsupported option -eall in request btc eth {}/{} binance -eall - option ignored.'.format(requestDayStr, requestMonthStr, threeDaysBeforeYearStr, requestDayStr, requestMonthStr), UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc eth {}/{}/{} 00:00 binance'.format(requestDayStr, requestMonthStr, threeDaysBeforeYearStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForHistoDayWithInvalidOptionCausingErrorAndWarning(self):
		#first full request: RT price request with invalid option
		inputStr = 'btc eth 0 binance -eall'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -eall in request btc eth 0 binance -eall - option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		tenDaysBeforeArrowDate = now.shift(days=-10)
		
		if tenDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testGetPrintableResultForHistoDayWithMarketNotExistForCoinPairAndInvalidOptionCausingErrorAndWarning()', now))
			return
		
		tenDaysBeforeYearStr, tenDaysBeforeMonthStr, tenDaysBeforeDayStr, tenDaysBeforeHourStr, tenDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenDaysBeforeArrowDate)

		requestDayStr = tenDaysBeforeDayStr
		requestMonthStr = tenDaysBeforeMonthStr

		#second full request: histo day price request with invalid option
		inputStr = 'btc eth {}/{} binance -eall'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/ETH on Binance: {}/{}/{} 00:00C\nWarning - unsupported option -eall in request btc eth {}/{} binance -eall - option ignored.'.format(requestDayStr, requestMonthStr, tenDaysBeforeYearStr, requestDayStr, requestMonthStr), UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc eth {}/{}/{} 00:00 binance'.format(requestDayStr, requestMonthStr, tenDaysBeforeYearStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
	
	def testGetPrintableResultForHistoDayWithInvalidOptionThenPartialRequestOk(self):
		"""
		This test ensures that a partial request with no unsupported option submitted
		after a full request with an unsupported option obtains a result with no warning.
		This validates the fact that, in Requester, CommandPrice.resetUnsupportedOptionData()
		is called when handling a partial request.
		:return:
		"""
		# first command: RT price request with invalid option
		inputStr = 'btc eth 0 binance -eall'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -eall in request btc eth 0 binance -eall - option ignored.'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		tenDaysBeforeArrowDate = now.shift(days=-10)
		
		if tenDaysBeforeArrowDate.year < now.year:
			print(
				'{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format(
					'testGetPrintableResultForHistoDayWithMarketNotExistForCoinPairAndInvalidOptionCausingErrorAndWarning()',
					now))
			return
		
		tenDaysBeforeYearStr, tenDaysBeforeMonthStr, tenDaysBeforeDayStr, tenDaysBeforeHourStr, tenDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			tenDaysBeforeArrowDate)
		
		requestDayStr = tenDaysBeforeDayStr
		requestMonthStr = tenDaysBeforeMonthStr
		
		# second command: partial histo day price request without invalid option
		inputStr = '-d{}/{}'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		self.assertEqual(
			'BTC/ETH on Binance: {}/{}/{} 00:00C'.format(
				requestDayStr, requestMonthStr, tenDaysBeforeYearStr),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc eth {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, tenDaysBeforeYearStr, nowHourStr, nowMinuteStr),
						 fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
	
	def testGetPrintableResultForUnsupportedPartialRequestOptionAfterValidRealTimeRequest(self):
		"""
		This test ensures that a partial request with an unsupported option submitted
		after a valid RT full request gets a result with a warning.
		:return:
		"""
		# first command: valid RT price request
		inputStr = 'btc eth 0 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		# second command: partial request with unsupported option
		inputStr = '-zooo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -zooo in request -zooo - option ignored.'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
	
	def testGetPrintableResultForUnsupportedPartialRequestOptionSaveAfterValidRealTimeRequest(self):
		"""
		This test ensures that a partial request with an unsupported option submitted
		after a valid RT full request gets a result with a warning.
		:return:
		"""
		# first command: valid RT price request
		inputStr = 'btc eth 0 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		# second command: partial request with unsupported option
		inputStr = '-zs'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -z in request -zs - option ignored.'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testGetPrintableResultForReturnPressedAfterUnsupportedPartialRequestOptionAfterValidRealTimeRequest(self):
		"""
		This test execute three requests:
		
		1/ Valid RT request
		2/ Invalid partial request with an unsupported option
		3/ Replaying the last request by pressing the Return key
		
		It ensures the last request does not cause any warning since the unsupported option
		which was ignored was removed from the options in effect.
		"""
		# first command: valid RT price request
		inputStr = 'btc eth 0 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		# second command: partial request with unsupported option
		inputStr = '-zooo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -zooo in request -zooo - option ignored.'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		# third command: return pressed to repeat the last request.
		# The warning displayed above must disappear !
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
	
	def testGetPrintableResultForPartialRequestValidOptionAfterUnsupportedPartialRequestOptionAfterValidRealTimeRequest(self):
		"""
		This test execute three requests:

		1/ Valid RT request
		2/ Invalid partial request with an unsupported option
		3/ Valid partial request with a valid option

		It ensures the last partial request does not cause any warning since the
		unsupported option which was ignored was removed from the options in effect.
		"""
		# first command: valid RT price request
		inputStr = 'btc eth 0 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		# second command: partial request with unsupported option
		inputStr = '-zooo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R\nWarning - unsupported option -zooo in request -zooo - option ignored.'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		
		# third command: return pressed to repeat the last request.
		# The warning displayed above must disappear !
		inputStr = '-fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH/USD.Kraken on Binance: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self,
																	nowDayStr,
																	nowHourStr,
																	nowMinuteStr,
																	nowMonthStr,
																	nowYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
	
	def testGetPrintableResultForTimeOnlyWithoutDateFullRequest(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#here, even if we request a price at now hour and now minute, the price returned is
		#not a RT price, but a histo minute price. We may request a price at 12:55 and we are
		#at 12:55:01 !
		inputStr = 'btc usd {}:{} bitfinex'.format(nowHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: M'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
															   nowMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForDayOnlyAndTimeFullRequest_3daysBefore(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		threeDaysBeforeArrowDate = now.shift(days=-3)

		threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

		inputStr = 'btc usd {} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if nowMonthStr == threeDaysBeforeMonthStr:
			# this test can only be performed after the 3rd day of the mnnth,
			# othervise, the test which assumes that we try a full request with only day and time
			# specified, but with the day number set to 3 days before today - so, in the future
			# if we are between the 1st and the 3rd since the month is not specified, can not be run.
			self.assertEqual(
				'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr),
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForDayOnlyAndTimeFullRequestOn31st(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		day = 31
		inputStr = 'btc usd {} {}:{} bitfinex'.format(day, nowHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		try:
			_ = DateTimeUtil.dateTimeComponentsToArrowLocalDate(day, now.month, now.year, now.hour, now.minute, 0,
																				   LOCAL_TIME_ZONE)
		except ValueError:
			# only if the request is for a month which does not have a 31st is the test valid !
			self.assertEqual(
				'ERROR - day is out of range for month: day 31, month {}.'.format(now.month), printResult)
			self.assertEqual('', fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForDayOnlyAndTimeFullRequest_8daysBefore(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		eightDaysBeforeArrowDate = now.shift(days=-8)

		eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

		inputStr = 'btc usd {} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if nowMonthStr == eightDaysBeforeMonthStr:
			# this test can only be performed after the 8th day of the month,
			# otherwise, the test which assumes that we try a full request with only day and time
			# specified, but with the day number set to 8 days before today - so, in the future
			# if we are between the 1st and the 8th since the month is not specified, can not be run.
			self.assertEqual(
				'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr),
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForDayOnlyAndTimeFullRequest_1daysAfter(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		oneDaysAfterArrowDate = now.shift(days=1)

		oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

		oneYearBeforeArrowDate = now.shift(years=-1)

		oneYearBeforeYearStr, oneYearBeforeMonthStr, oneYearBeforeDayStr, oneYearBeforeHourStr, oneYearBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

		inputStr = 'btc usd {} {}:{} bitfinex'.format(oneDaysAfterDayStr, oneDaysAfterHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if nowMonthStr == oneDaysAfterMonthStr:
			# this test can only be performed on a day which is not the last day of the mnnth.
			# othervise, the test which assumes that we try a full request with only day and time
			# specified, but with the day number set to tomorrow - in the future can not be
			# run.
			self.assertEqual(
				'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year.'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr, oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterYearStr, nowHourStr, nowMinuteStr),
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysAfterDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForDayOnlyAndTimePartialRequest_3daysBefore(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		threeDaysBeforeArrowDate = now.shift(days=-3)

		threeDaysBeforeYearStr, threeDaysBeforeMonthStr, threeDaysBeforeDayStr, threeDaysBeforeHourStr, threeDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(threeDaysBeforeArrowDate)

		#here, even if we request a price at now hour and now minute, the price returned is
		#not a RT price, but a histo minute price. We may request a price at 12:55 and we are
		#at 12:55:01 !
		inputStr = 'btc usd {} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if nowMonthStr == threeDaysBeforeMonthStr:
			# this test can only be performed after the 3rd day of the mnnth,
			# othervise, the test which assumes that we try a full request with only day and time
			# specified, but with the day number set to 3 days before today - so, in the future
			# if we are between the 1st and the 3rd since the month is not specified, can not be run.
			self.assertEqual(
				'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr),
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(threeDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForDayOnlyAndTimePartialRequest_8daysBefore(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		eightDaysBeforeArrowDate = now.shift(days=-8)

		eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

		inputStr = 'btc usd {} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if nowMonthStr == eightDaysBeforeMonthStr:
			# this test can only be performed after the 8th day of the mnnth,
			# othervise, the test which assumes that we try a full request with only day and time
			# specified, but with the day number set to 8 days before today - so, in the future
			# if we are between the 1st and the 8th since the month is not specified, can not be run.
			self.assertEqual(
				'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr),
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(eightDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForDayOnlyAndTimePartialRequest_1daysAfter(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		oneDaysAfterArrowDate = now.shift(days=1)

		oneDaysAfterYearStr, oneDaysAfterMonthStr, oneDaysAfterDayStr, oneDaysAfterHourStr, oneDaysAfterMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysAfterArrowDate)

		oneYearBeforeArrowDate = now.shift(years=-1)

		oneYearBeforeYearStr, oneYearBeforeMonthStr, oneYearBeforeDayStr, oneYearBeforeHourStr, oneYearBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneYearBeforeArrowDate)

		inputStr = 'btc usd {} {}:{} bitfinex'.format(oneDaysAfterDayStr, oneDaysAfterHourStr, nowMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if nowMonthStr == oneDaysAfterMonthStr:
			# this test can only be performed on a day which is not the last day of the mnnth.
			# othervise, the test which assumes that we try a full request with only day and time
			# specified, but with the day number set to tomorrow - in the future can not be
			# run.
			self.assertEqual(
				'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year.'.format(oneDaysAfterDayStr, oneDaysAfterMonthStr, oneYearBeforeYearStr, oneDaysAfterDayStr, oneDaysAfterMonthStr, oneDaysAfterYearStr, nowHourStr, nowMinuteStr),
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysAfterDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
			self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testBtcEthBinanceInvertedCryptoUnitBug(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		inputStr = 'eth btc 0 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC on Binance: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		invertedInputStr = 'btc eth 0 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			invertedInputStr)
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Binance: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc eth 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	# testing option value scenario

	def testGetPrintableResultForInputScenarioWithInvalidOptionValueSaveAndWarning(self):
		inputStr = 'eth usd 0 bitfinex -vs100'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ERROR - full request eth usd 0 bitfinex -vs100: -vs100 option violates the -vs option format. See help for more information.',
			printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testControllerBugSpecifyOptionValueAfterAskHistoDay(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		eightDaysBeforeArrowDate = now.shift(days=-8)
		
		if eightDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testControllerBugSpecifyOptionValueAfterAskHistoDay()', now))
			return
		
		eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

		requestDayStr = eightDaysBeforeDayStr
		requestMonthStr = eightDaysBeforeMonthStr
		requestYearStr = eightDaysBeforeYearStr
		inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = eightDaysBeforeHourStr
			minuteStr = eightDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'MCO/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-v12mco'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'MCO/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testControllerBugSpecifyOptionValueSaveAfterAskHistoDay(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		eightDaysBeforeArrowDate = now.shift(days=-8)
		
		if eightDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testControllerBugSpecifyOptionValueSaveAfterAskHistoDay()', now))
			return
		
		eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

		requestYearStr = eightDaysBeforeYearStr
		requestDayStr = eightDaysBeforeDayStr
		requestMonthStr = eightDaysBeforeMonthStr
		inputStr = 'mco btc {}/{} all'.format(requestDayStr, requestMonthStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = eightDaysBeforeHourStr
			minuteStr = eightDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'MCO/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-vs12mco'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'MCO/BTC on AVG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('mco btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('mco btc {}/{}/{} {}:{} all -vs12mco'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)


	def testControllerBugSpecifyOptionValueAfterAskHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)
		
		if fiveDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testControllerBugSpecifyOptionValueAfterAskHistoMinute()', now))
			return
		
		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestYearStr = fiveDaysBeforeYearStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-v12eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testControllerBugSpecifyOptionValueSaveAfterAskHistoMinute(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)
		
		if fiveDaysBeforeArrowDate.year < now.year:
			print('{} skipped due to current date {} which causes the test case to generate a warning \"request date can not be in the future ...\"'.format('testControllerBugSpecifyOptionValueSaveAfterAskHistoMinute()', now))
			return
		
		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestYearStr = fiveDaysBeforeYearStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-vs12eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth btc {}/{}/{} {}:{} binance -vs12eth'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)


	def testControllerBugSpecifyOptionValueAfterAskHistoMinuteYearSupplied(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestYearStr = fiveDaysBeforeYearStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-v12eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testControllerBugSpecifyOptionValueSaveAfterAskHistoMinuteYearSupplied(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestYearStr = fiveDaysBeforeYearStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = fiveDaysBeforeHourStr
			minuteStr = fiveDaysBeforeMinuteStr
			priceType = 'M'

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-vs12eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/BTC on Binance: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth btc {}/{}/{} {}:{} binance'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth btc {}/{}/{} {}:{} binance -vs12eth'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInputScenarioWithOptionValueAtWrongPosition(self):
		# first command: RT price request
		inputStr = 'btc usd 0 -vs10btc bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ERROR - full request btc usd 0 -vs10btc bitfinex violates format <crypto> <unit> <date|time> <exchange> <options>.',
			printResult)
		self.assertEqual('', fullCommandStrNoOptions)  # empty string since request caused an error !
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForInputScenarioWithOptionValue(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#second command: value option
		inputStr = '-v10eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#third command: value save option
		inputStr = '-vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#fourth command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#fifth command: change crypto
		inputStr = '-cneo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#sixth command: remove value option
		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecified(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs0.1btc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.1 BTC/414.94 USD on Bitfinex: 12/09/17 00:00C 4149.4',printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs0.1btc', fullCommandStrWithSaveOptionsForHistoryList)

	# here
	def testGetPrintableResultForInputScenarioWithOptionValueV0InFullRequest(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		yesterday = now.shift(days=-2)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price full command with save value option
		inputStr = 'eth usd 0 bitfinex -vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#second command: RT price full command with remove value option. This is not usefull since
		#each time you enter a full command, you wioe out any previously entered command, as tested
		#by testGetPrintableResultForInputScenarioWithValueSaveCommandWipedOutByFullCommand() !
		inputStr = 'eth usd 0 bitfinex -v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInputScenarioWithOptionValueSaveWipedOutByFullRequest(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		yesterday = now.shift(days=-2)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price full command with save value option
		inputStr = 'eth usd 0 bitfinex -vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#second command: RT price full command with remove value option. This is not usefull since
		#each time you enter a full command, you wioe out any previously entered command !
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForInputScenarioWithOptionValueAndError(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 bitfinex -vs10btc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 0 bitfinex -vs10btc', fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-ueth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc eth 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc eth 0 bitfinex -vs10btc', fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-cxmr'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'PROVIDER ERROR - Bitfinex market does not exist for this coin pair (XMR/ETH).', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-cbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/ETH on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc eth 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc eth 0 bitfinex -vs10btc', fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-uusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 0 bitfinex -vs10btc', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForInputScenarioWithOptionValueVAfterOptionValueVS(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		inputStr = 'eth usd 0 bitfinex -vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-v100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -v100usd', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -v100usd', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForReplayHistoMinuteThenOptionValue(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		fiveDaysBeforeArrowDate = now.shift(days=-5)

		fiveDaysBeforeYearStr, fiveDaysBeforeMonthStr, fiveDaysBeforeDayStr, fiveDaysBeforeHourStr, fiveDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(fiveDaysBeforeArrowDate)

		requestDayStr = fiveDaysBeforeDayStr
		requestMonthStr = fiveDaysBeforeMonthStr
		requestYearStr = fiveDaysBeforeYearStr
		requestHourStr = fiveDaysBeforeHourStr
		requestMinuteStr = fiveDaysBeforeMinuteStr
		inputStr = 'eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, requestHourStr, requestMinuteStr)

		if DateTimeUtil.isDateOlderThan(fiveDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = requestHourStr
			minuteStr = requestMinuteStr
			priceType = 'M'

		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: value option
		inputStr = '-v10eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: value save option
		inputStr = '-vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: change crypto
		inputStr = '-cneo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: remove value option
		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
															   requestMinuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, fiveDaysBeforeYearStr, hourStr, minuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForReplayHistoDayThenOptionValue(self):
		timezoneStr = LOCAL_TIME_ZONE
		now = DateTimeUtil.localNow(timezoneStr)
		eightDaysBeforeArrowDate = now.shift(days=-8)

		eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

		requestDayStr = eightDaysBeforeDayStr
		requestMonthStr = eightDaysBeforeMonthStr
		requestYearStr = eightDaysBeforeYearStr
		requestHourStr = eightDaysBeforeHourStr
		requestMinuteStr = eightDaysBeforeMinuteStr
		inputStr = 'eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr)

		if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
			hourStr = '00'
			minuteStr = '00'
			priceType = 'C'
		else:
			hourStr = requestHourStr
			minuteStr = requestMinuteStr
			priceType = 'M'

		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, hourStr, minuteStr, priceType),
														UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: value option
		inputStr = '-v10eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: value save option
		inputStr = '-vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual('eth usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: change crypto
		inputStr = '-cneo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex -vs100usd'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrWithSaveOptionsForHistoryList)

		#next command: remove value option
		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
															   minuteStr, priceType),
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('neo usd {}/{}/{} {}:{} bitfinex'.format(requestDayStr, requestMonthStr, eightDaysBeforeYearStr, requestHourStr, requestMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForReplayRealTimeThenOptionValue(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		requestYearStr, requestMonthStr, requestDayStr, requestHourStr, requestMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: value option
		inputStr = '-v10eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: value save option
		inputStr = '-vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'ETH/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#next command: change crypto
		inputStr = '-cneo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeAllPricesFromCommandValueResult(printResult))
		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('neo usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		#next command: remove value option
		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#next command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, requestDayStr,
																	requestHourStr,
																	requestMinuteStr,
																	requestMonthStr,
																	requestYearStr,
																	requestResultNoEndPrice,
																	expectedPrintResultNoDateTimeNoEndPrice)
		# self.assertEqual(
		# 	'NEO/USD on Bitfinex: ' + '{}/{}/{} {}:{}R'.format(requestDayStr, requestMonthStr, requestYearStr, requestHourStr,
		# 													   requestMinuteStr),
		# 	UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForInputScenarioWithOptionValueAndInvalidOption(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request with invalid option
		inputStr = 'btc usd 0 all -vs100.2usd -ebitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on AVG: R\nWarning - unsupported option -ebitfinex in request btc usd 0 all -vs100.2usd -ebitfinex - option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc usd 0 all', fullCommandStrNoOptions)
		self.assertEqual('btc usd 0 all -vs100.2usd', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForInputScenarioWithOptionValueSaveAndWarning(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		inputStr = 'eth usd 0 bitfinex -vs100usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-cxmr'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeAllPricesFromCommandValueResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'XMR/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('xmr usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('xmr usd 0 bitfinex -vs100usd', fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-ubtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'XMR/BTC on Bitfinex: R\nWARNING - currency value option symbol USD currently in effect differs from both crypto (XMR) and unit (BTC) of request. -vs option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('xmr btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-ceth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC on Bitfinex: R\nWARNING - currency value option symbol USD currently in effect differs from both crypto (ETH) and unit (BTC) of request. -vs option ignored.'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveUnitAmountSpecified(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs70usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.01686991 BTC/70 USD on Bitfinex: 12/09/17 00:00C 4149.4',printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs70usd', fullCommandStrWithSaveOptionsForHistoryList)

# testing option fiat scenario

	def testGetPrintableResultForFullRequestWithOptionFiatNoExchange(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth btc 0 bitfinex -fusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC/USD.AVG on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth btc 0 bitfinex -fusd', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForPartialRequestWithOptionFiatNoExchange(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth btc 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#second command: fiat option
		inputStr = '-fusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC/USD.AVG on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth btc 0 bitfinex -fusd', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForPartialRequestWithOptionFiatExchangeSpecified(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth btc 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#second command: fiat option
		inputStr = '-fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC/USD.Kraken on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth btc 0 bitfinex -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForFullRequestWithOptionFiatExchangeSpecified(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth btc 0 bitfinex -fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/BTC/USD.Kraken on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth btc 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth btc 0 bitfinex -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForInputScenarioWithOptionFiat(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#second command: fiat option
		inputStr = '-fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD/CHF.AVG on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -fchf', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#third command: value save option
		inputStr = '-fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD/CHF.AVG on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

		#fourth command: '' to replay lst command
		inputStr = ''
		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD/CHF.AVG on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('eth usd 0 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

		#fifth command: change crypto
		inputStr = '-cneo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD/CHF.AVG on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('neo usd 0 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

		#sixth command: remove fiat save option
		inputStr = '-f0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'NEO/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('neo usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs0.1btc -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.1 BTC/414.94 USD/415.35494 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs0.1btc', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs0.1btc -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.1 BTC/414.94 USD/415.35494 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs0.1btc -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveCryptoAmountSpecifiedOptionFiatSaveExchange(self):
		inputStr = 'eth usd 12/09/17 all -vs0.1btc -fsbtc.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'1.41910915 ETH/417.36 USD/0.1 BTC.Kraken on AVG: 12/09/17 00:00C 294.1 0.07046674', printResult)
		self.assertEqual('eth usd 12/09/17 00:00 all', fullCommandStrNoOptions)
		self.assertEqual('eth usd 12/09/17 00:00 all -vs0.1btc -fsbtc.kraken', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueCryptoAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v0.1btc -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.1 BTC/414.94 USD/415.35494 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueCryptoAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v0.1btc -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.1 BTC/414.94 USD/415.35494 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveUnitAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs1000usd -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.2409987 BTC/1000 USD/1001 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000usd', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveUnitAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs1000usd -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.2409987 BTC/1000 USD/1001 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000usd -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueUnitAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v1000usd -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.2409987 BTC/1000 USD/1001 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueUnitAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v1000usd -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.2409987 BTC/1000 USD/1001 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)


	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveFiatAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs1000chf -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.24075794 BTC/999.000999 USD/1000 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveFiatAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs1000chf -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.24075794 BTC/999.000999 USD/1000 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionFiatSaveOptionValueSaveFiatAmountSpecified(self):
		# inverting value and fiat options compared to previous tst
		inputStr = 'btc usd 12/09/17 bitfinex -fschf -vs1000chf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.24075794 BTC/999.000999 USD/1000 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueFiatAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v1000chf -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.24075794 BTC/999.000999 USD/1000 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueFiatAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v1000chf -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.24075794 BTC/999.000999 USD/1000 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveFiatOptionSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs1000chf -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.24075794 BTC/999.000999 USD/1000 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs1000chf -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSavedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs10btc -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'10 BTC/41494 USD/41535.494 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fchf', fullCommandStrWithNoSaveOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -vs10btc', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v10btc -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'10 BTC/41494 USD/41535.494 CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -v10btc', fullCommandStrWithNoSaveOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueSaveInvalidCurrencyAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -vs1000eth -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'BTC/USD/CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494\nWARNING - currency value option symbol ETH currently in effect differs from crypto (BTC), unit (USD) and fiat (CHF) of request. -vs option ignored.', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueInvalidCurrencyAmountSpecifiedOptionFiatSave(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v1000eth -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'BTC/USD/CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494\nWARNING - currency value option symbol ETH currently in effect differs from crypto (BTC), unit (USD) and fiat (CHF) of request. -v option ignored.', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForHistoricalRequestWithOptionValueInvalidCurrencyAmountSpecifiedOptionFiat(self):
		inputStr = 'btc usd 12/09/17 bitfinex -v1000eth -fchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'BTC/USD/CHF.AVG on Bitfinex: 12/09/17 00:00C 4149.4 4153.5494\nWARNING - currency value option symbol ETH currently in effect differs from crypto (BTC), unit (USD) and fiat (CHF) of request. -v option ignored.', printResult)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex', fullCommandStrNoOptions)
		self.assertEqual('btc usd 12/09/17 00:00 bitfinex -fchf', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testControllerBugSpecifyOptionValueSaveThenFiatSaveAfterAskHistoDay(self):
		inputStr = 'btc eth 12/9/17 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('BTC/ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
		self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		# adding value save option
		inputStr = '-vs10eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('0.706 BTC/10 ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
		self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('btc eth 12/09/17 00:00 binance -vs10eth', fullCommandStrWithSaveOptionsForHistoryList)

		# adding fiat save option
		inputStr = '-fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('0.706 BTC/10 ETH/2947.7 CHF.AVG on Binance: 12/09/17 00:00C 14.16430595 4175.21246459', printResult)
		self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('btc eth 12/09/17 00:00 binance -vs10eth -fschf', fullCommandStrWithSaveOptionsForHistoryList)

	def testOptionFiatValueComputationIsCorrectFullRequestHistoDayPrice(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: btc usd histo day on kraken price request
		inputStr = 'btc usd 1/1/19 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
		self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

		#second command: eth btc histo day price request with usd fiat option
		inputStr = 'eth btc 1/1/19 binance -fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
		self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken\n(0.03663 ETH/BTC * 3820.1 BTC/USD = 139.930263 ETH/USD)', fullCommandStrForStatusBar)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
		fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

		#ensure fiat value of eth is correct
		self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

	def testOptionFiatValueComputationIsCorrectFullRequestCurrentPrice(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: eth usd histo day on kraken price request
		inputStr = 'btc usd 0 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('btc usd 0 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0])

		#second command: eth btc current price request with usd fiat option
		inputStr = 'eth btc 0 binance -fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('eth btc 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 0 binance -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0])
		ethUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1])

		#ensure fiat value of eth is correct
		self.assertAlmostEqual(round(ethBtcRate * btcUsdRate, GuiOutputFormatter.PRICE_FLOAT_ROUNDING), ethUsdRate, delta=0.5)

	def testOptionFiatValueComputationIsCorrectPartialRequestHistoDayPrice(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: btc usd histo day on kraken price request
		inputStr = 'btc usd 1/1/19 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
		self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

		#second command: eth btc histo day price request
		inputStr = 'eth btc 1/1/19 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC on Binance: 01/01/19 00:00C 0.03663', printResult)
		self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#second command: usd fiat save option
		inputStr = '-fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
		self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fsusd.kraken\n(0.03663 ETH/BTC * 3820.1 BTC/USD = 139.930263 ETH/USD)', fullCommandStrForStatusBar)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
		fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

		#ensure fiat value of eth is correct
		self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

	def testOptionFiatValueComputationIsCorrectPartialRequestCurrentPrice(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: eth usd histo day on kraken price request
		inputStr = 'btc usd 0 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0])

		#second command: eth btc current price request
		inputStr = 'eth btc 0 binance'
		_, _, _, _, _ = self.controller.getPrintableResultForInput(inputStr)

		#third command: usd fiat save option
		inputStr = '-fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('eth btc 0 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 0 binance -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0])
		ethUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1])

		#ensure fiat value of eth is correct
		self.assertAlmostEqual(round(ethBtcRate * btcUsdRate, GuiOutputFormatter.PRICE_FLOAT_ROUNDING), ethUsdRate, delta=0.5)

	def testOptionFiatValueComputationIsCorrectFullRequestHistoDayPriceNoSave(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: btc usd histo day on kraken price request
		inputStr = 'btc usd 1/1/19 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
		self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

		#second command: eth btc histo day price request with usd fiat option
		inputStr = 'eth btc 1/1/19 binance -fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
		self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fusd.kraken\n(0.03663 ETH/BTC * 3820.1 BTC/USD = 139.930263 ETH/USD)', fullCommandStrForStatusBar)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
		fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

		#ensure fiat value of eth is correct
		self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

	def testOptionFiatValueComputationIsCorrectPartialRequestHistoDayPriceNoSave(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: btc usd histo day on kraken price request
		inputStr = 'btc usd 1/1/19 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/USD on Kraken: 01/01/19 00:00C 3820.1', printResult)
		self.assertEqual('btc usd 01/01/19 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		btcUsdRate = float(re.findall(r".* ([\d\.]+)", printResult)[0]) # 3820.1

		#second command: eth btc histo day price request
		inputStr = 'eth btc 1/1/19 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC on Binance: 01/01/19 00:00C 0.03663', printResult)
		self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		#second command: usd fiat save option
		inputStr = '-fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC/USD.Kraken on Binance: 01/01/19 00:00C 0.03663 139.930263', printResult)
		self.assertEqual('eth btc 01/01/19 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 01/01/19 00:00 binance -fusd.kraken\n(0.03663 ETH/BTC * 3820.1 BTC/USD = 139.930263 ETH/USD)', fullCommandStrForStatusBar)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0]) # 0.03663
		fiatComputedEthUsdRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1]) # 139.930263

		#ensure fiat value of eth is correct
		self.assertEqual(ethBtcRate * btcUsdRate, fiatComputedEthUsdRate)

	def testOptionFiatFullRequestHistoDayPriceFullCommandStrForStatusBarFormat(self):
		inputStr = 'eth btc 12/9/17 binance -fschf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC/CHF.AVG on Binance: 12/09/17 00:00C 0.0706 293.854144', printResult)
		self.assertEqual('eth btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 12/09/17 00:00 binance -fschf', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 12/09/17 00:00 binance -fschf\n(0.0706 ETH/BTC * 4162.24 BTC/CHF = 293.854144 ETH/CHF)', fullCommandStrForStatusBar)

	def testGetCryptoPriceHistoricalOptionFiatHandlingInvertedUnitFiat(self):
		'''
		Tests correct working of a fiat option where the unit/fiat pair is not supported
		by the fiat exchange and so causes an inverted fiat/unit pair request.

		btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
		and its result is inverted ((1/returned price)
		:return:
		'''
		# mco btc 12/09/17 00:00 binance -fseth.binance
		#first command: mco btc 12/09/17 00:00 binance -fseth.binance
		inputStr = 'mco btc 12/09/17 00:00 binance -fseth.binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'MCO/BTC/ETH on Binance: 12/09/17 00:00C 0.002049 0.02902266', printResult)
		self.assertEqual('mco btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance\n(0.002049 MCO/BTC * 14.16430595 BTC/ETH = 0.02902266 MCO/ETH)', fullCommandStrForStatusBar)

	def testGetCryptoPriceHistoricalOptionFiatScenarioSettingUnitEqualToFiat(self):
		'''
		Tests correct working of a fiat option where the unit/fiat pair is not supported
		by the fiat exchange and so causes an inverted fiat/unit pair request.

		btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
		and its result is inverted ((1/returned price)
		:return:
		'''
		# mco btc 12/09/17 00:00 binance -fseth.binance
		#first command: mco btc 12/09/17 00:00 binance -fseth.binance
		inputStr = 'mco btc 12/09/17 00:00 binance -fseth.binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'MCO/BTC/ETH on Binance: 12/09/17 00:00C 0.002049 0.02902266', printResult)
		self.assertEqual('mco btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance\n(0.002049 MCO/BTC * 14.16430595 BTC/ETH = 0.02902266 MCO/ETH)', fullCommandStrForStatusBar)

		#second command: -cbtc -ueth Here, unit is equal to fiat
		inputStr = '-cbtc -ueth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'BTC/ETH/ETH on Binance: 12/09/17 00:00C 14.16430595 14.16430595', printResult)
		self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('btc eth 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('btc eth 12/09/17 00:00 binance -fseth.binance\n(14.16430595 BTC/ETH * 1 ETH/ETH = 14.16430595 BTC/ETH)', fullCommandStrForStatusBar)

		#third command: -cbtc -ueth with cancelling fiat option
		inputStr = '-cbtc -ueth -f0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'BTC/ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
		self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetCryptoPriceHistoricalOptionFiatScenarioSettingCryptoEqualToFiat(self):
		'''
		Tests correct working of a fiat option where the unit/fiat pair is not supported
		by the fiat exchange and so causes an inverted fiat/unit pair request.

		btc (unit) eth (fiat) on binance is not supported. So eth/btc is requested
		and its result is inverted ((1/returned price)
		:return:
		'''
		# mco btc 12/09/17 00:00 binance -fseth.binance
		#first command: mco btc 12/09/17 00:00 binance -fseth.binance
		inputStr = 'mco btc 12/09/17 00:00 binance -fseth.binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'MCO/BTC/ETH on Binance: 12/09/17 00:00C 0.002049 0.02902266', printResult)
		self.assertEqual('mco btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('mco btc 12/09/17 00:00 binance -fseth.binance\n(0.002049 MCO/BTC * 14.16430595 BTC/ETH = 0.02902266 MCO/ETH)', fullCommandStrForStatusBar)

		inputStr = '-ceth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ETH/BTC/ETH on Binance: 12/09/17 00:00C 0.0706 1', printResult)
		self.assertEqual('eth btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 12/09/17 00:00 binance -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 12/09/17 00:00 binance -fseth.binance\n(0.0706 ETH/BTC * 14.16430595 BTC/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

		#third command: add -vs10eth
		inputStr = '-vs10eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'10 ETH/0.706 BTC/10 ETH on Binance: 12/09/17 00:00C 0.0706 1', printResult)
		self.assertEqual('eth btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 12/09/17 00:00 binance -vs10eth -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 12/09/17 00:00 binance -vs10eth -fseth.binance\n(0.0706 ETH/BTC * 14.16430595 BTC/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

		#fourth command: add -vs10btc
		inputStr = '-vs10btc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'141.64305949 ETH/10 BTC/141.64305949 ETH on Binance: 12/09/17 00:00C 0.0706 1', printResult)
		self.assertEqual('eth btc 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 12/09/17 00:00 binance -vs10btc -fseth.binance', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth btc 12/09/17 00:00 binance -vs10btc -fseth.binance\n(0.0706 ETH/BTC * 14.16430595 BTC/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

	def testGetCryptoPriceHistoDayValidExchangeHandlingInvertedCryptoUnit(self):
		'''
		Tests correct working of a request where the crypto/unit pair is not supported
		by the fiat exchange and so causes an inverted unit/crypto pair request.

		btc (crypto) eth (unit) on binance is not supported. So eth/btc is requested
		and its result is inverted ((1/returned price)
		:return:
		'''
		# btc eth 12/09/17 00:00 binance
		#first command: mco btc 12/09/17 00:00 binance -fseth.binance
		inputStr = 'btc eth 12/09/17 00:00 binance'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual(
			'BTC/ETH on Binance: 12/09/17 00:00C 14.16430595', printResult)
		self.assertEqual('btc eth 12/09/17 00:00 binance', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testOptionFiatSaveFullRequestHistoDayPriceAfterRemovingSaveModeOfOptionValue(self):
		# first request where both value and fiat options are saved
		inputStr = 'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/1525.57351555 CHSB on HitBTC: 20/12/20 00:00C 0.00000746 0.70311027', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

		# second request where the value option is no longer saved
		inputStr = 'krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fschsb.hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/1525.57351555 CHSB on HitBTC: 20/12/20 00:00C 0.00000746 0.70311027', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fschsb.hitbtc', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fschsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

	def testOptionFiatSaveFullRequestHistoDayPriceAfterRemovingSaveModeOfOptionFiat(self):
		# first request where both value and fiat options are saved
		inputStr = 'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/1525.57351555 CHSB on HitBTC: 20/12/20 00:00C 0.00000746 0.70311027', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fschsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

		# second request where the value option is no longer saved
		inputStr = 'krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fchsb.hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/1525.57351555 CHSB on HitBTC: 20/12/20 00:00C 0.00000746 0.70311027', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -fchsb.hitbtc', fullCommandStrWithNoSaveOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -vs2169.75krl -fchsb.hitbtc\n(0.00000746 KRL/BTC * 94250.7068803 BTC/CHSB = 0.70311027 KRL/CHSB)', fullCommandStrForStatusBar)

	def testOptionValueOptionFiatFullRequestHistoDayPrice(self):
		inputStr = 'krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/380.06647623 USD.Kraken on HitBTC: 20/12/20 00:00C 0.00000746 0.17516602', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken\n(0.00000746 KRL/BTC * 23480.7 BTC/USD = 0.17516602 KRL/USD)', fullCommandStrForStatusBar)

	def testOptionValueOptionFiatFullRequestHistoDayPriceRequiredParmsOrderChanged(self):
		'''
		A full request is composed of two mandatory order required elements, i.e. crypto
		and	unit plus three order free required elements, i.e. date, time and exchange.
		This test verifies that the three required full request order free elements can
		be set in any order. This is purely for validating the app. In fact, the required
		elements are always set in this order: <crypto> <unit> <date|time> <exchange> !
		'''
		# first changed order
		inputStr = 'krl btc hitbtc 00:00 20/12/20 -v2169.75krl -fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/380.06647623 USD.Kraken on HitBTC: 20/12/20 00:00C 0.00000746 0.17516602', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken\n(0.00000746 KRL/BTC * 23480.7 BTC/USD = 0.17516602 KRL/USD)', fullCommandStrForStatusBar)

		# second changed order
		inputStr = 'krl btc 00:00 hitbtc 20/12/20 -v2169.75krl -fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/380.06647623 USD.Kraken on HitBTC: 20/12/20 00:00C 0.00000746 0.17516602', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken\n(0.00000746 KRL/BTC * 23480.7 BTC/USD = 0.17516602 KRL/USD)', fullCommandStrForStatusBar)

		# third changed order
		inputStr = 'krl btc 00:00 20/12/20 hitbtc -v2169.75krl -fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01618633 BTC/380.06647623 USD.Kraken on HitBTC: 20/12/20 00:00C 0.00000746 0.17516602', printResult)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 00:00 hitbtc -v2169.75krl -fusd.kraken\n(0.00000746 KRL/BTC * 23480.7 BTC/USD = 0.17516602 KRL/USD)', fullCommandStrForStatusBar)

	def testOptionValueOptionFiatFullRequestHistoDayPriceMandatoryParmsAndOptionOrderChanged(self):
		inputStr = 'krl btc 00:00 20/12/20 -fusd.kraken -v2169.75krl hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'ERROR - full request krl btc 00:00 20/12/20 -fusd.kraken -v2169.75krl hitbtc violates format <crypto> <unit> <date|time> <exchange> <options>.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testOptionValueOptionFiatFullRequestHistoDayPriceFiatEqualsUnit(self):
		inputStr = 'eth usd 19/02/18 kraken -v0.3821277eth -fusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/359.44459973 USD/359.44459973 USD on Kraken: 19/02/18 00:00C 940.64 940.64', printResult)
		self.assertEqual('eth usd 19/02/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -v0.3821277eth -fusd', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -v0.3821277eth -fusd\n(940.64 ETH/USD * 1 USD/USD = 940.64 ETH/USD)', fullCommandStrForStatusBar)

	def testOptionValueOptionFiatFullRequestHistoDayPriceFiatEqualsCrypto(self):
		inputStr = 'eth usd 19/02/18 kraken -v0.3821277eth -feth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/359.44459973 USD/0.3821277 ETH on Kraken: 19/02/18 00:00C 940.64 1', printResult)
		self.assertEqual('eth usd 19/02/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -v0.3821277eth -feth', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -v0.3821277eth -feth\n(940.64 ETH/USD * 0.00106311 USD/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

	def testOptionValueSaveOptionFiatSaveFullRequestHistoDayPriceFiatEqualsUnit(self):
		# first request where both value and fiat options are saved
		inputStr = 'eth usd 19/02/18 kraken -vs0.3821277eth -fsusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/359.44459973 USD/359.44459973 USD on Kraken: 19/02/18 00:00C 940.64 940.64', printResult)
		self.assertEqual('eth usd 19/02/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -vs0.3821277eth -fsusd', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -vs0.3821277eth -fsusd\n(940.64 ETH/USD * 1 USD/USD = 940.64 ETH/USD)', fullCommandStrForStatusBar)

	def testOptionValueSaveOptionFiatSaveFullRequestHistoDayPriceFiatEqualsCrypto(self):
		inputStr = 'eth usd 19/02/18 kraken -vs0.3821277eth -fseth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/359.44459973 USD/0.3821277 ETH on Kraken: 19/02/18 00:00C 940.64 1', printResult)
		self.assertEqual('eth usd 19/02/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -vs0.3821277eth -fseth', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -vs0.3821277eth -fseth\n(940.64 ETH/USD * 0.00106311 USD/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

	def testOptionValueNoSaveOptionFiatSaveFullRequestHistoDayPriceFiatEqualsUnit(self):
		# first request
		inputStr = 'eth usd 19/02/18 kraken -v0.3821277eth -fsusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/359.44459973 USD/359.44459973 USD on Kraken: 19/02/18 00:00C 940.64 940.64', printResult)
		self.assertEqual('eth usd 19/02/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -fsusd', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -v0.3821277eth', fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -v0.3821277eth -fsusd\n(940.64 ETH/USD * 1 USD/USD = 940.64 ETH/USD)', fullCommandStrForStatusBar)

	def testOptionValueSaveOptionFiatNoSaveFullRequestHistoDayPriceFiatEqualsCrypto(self):
		# first request
		inputStr = 'eth usd 19/02/18 kraken -vs0.3821277eth -feth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/359.44459973 USD/0.3821277 ETH on Kraken: 19/02/18 00:00C 940.64 1', printResult)
		self.assertEqual('eth usd 19/02/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -vs0.3821277eth', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -feth', fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 19/02/18 00:00 kraken -vs0.3821277eth -feth\n(940.64 ETH/USD * 0.00106311 USD/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

	def testPartialRequestHistoDayPriceSettingUnitToUnsupportedPairAtThisDate(self):
		# full request where pairs ok
		inputStr = 'eth usd 19/01/18 00:00 kraken -vs0.3821277eth -feth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/400.4698296 USD/0.3821277 ETH on Kraken: 19/01/18 00:00C 1048 1', printResult)
		self.assertEqual('eth usd 19/01/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/01/18 00:00 kraken -vs0.3821277eth', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth usd 19/01/18 00:00 kraken -feth', fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 19/01/18 00:00 kraken -vs0.3821277eth -feth\n(1048 ETH/USD * 0.0009542 USD/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

		# partial request pair not supported at this date
		inputStr = '-uchf'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual('PROVIDER ERROR - Requesting ETH/CHF price for date 19/01/18 00:00 on exchange Kraken returned invalid value 0', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testPartialRequestHistoDayPriceSettingDateCausingUnsupportedFiatPairAtThisDate(self):
		# full request where pairs ok
		inputStr = 'eth usd 01/01/21 00:00 kraken -vs0.3821277eth -fschf.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/279.27802955 USD/248.36195167 CHF on Kraken: 01/01/21 00:00C 730.85 649.944905', printResult)
		self.assertEqual('eth usd 01/01/21 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 01/01/21 00:00 kraken -vs0.3821277eth -fschf.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 01/01/21 00:00 kraken -vs0.3821277eth -fschf.kraken\n(730.85 ETH/USD * 0.8893 USD/CHF = 649.944905 ETH/CHF)', fullCommandStrForStatusBar)

		# partial request changing date so that pair not supported
		inputStr = '-d1/1/18'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual('PROVIDER ERROR - fiat option coin pair CHF/USD or USD/CHF not supported by exchange Kraken on date 01/01/18 00:00', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testPartialRequestHistoDayPriceSettingFiatToUnsupportedUnitFiatPairAtThisDate(self):
		# full request pair ok
		inputStr = 'eth usd 19/01/18 00:00 kraken -vs0.3821277eth -feth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'0.3821277 ETH/400.4698296 USD/0.3821277 ETH on Kraken: 19/01/18 00:00C 1048 1', printResult)
		self.assertEqual('eth usd 19/01/18 00:00 kraken', fullCommandStrNoOptions)
		self.assertEqual('eth usd 19/01/18 00:00 kraken -vs0.3821277eth', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('eth usd 19/01/18 00:00 kraken -feth', fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth usd 19/01/18 00:00 kraken -vs0.3821277eth -feth\n(1048 ETH/USD * 0.0009542 USD/ETH = 1 ETH/ETH)', fullCommandStrForStatusBar)

		# partial request changing fiat so pair not supported at this date
		inputStr = '-fchf.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual('PROVIDER ERROR - fiat option coin pair CHF/USD or USD/CHF not supported by exchange Kraken on date 19/01/18 00:00', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrForStatusBar)
	
	def testRealTimeFullRequestOptionOptionFiatWithFiatPairUnsupportedError(self):
		'''
		This test verifies that the partial request fiat save option remains active until
		new full request or option cancelling.
		'''
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)
		
		# first entry: full request
		inputStr = 'btc usdc 0 all -fchf.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		self.assertEqual(
			'PROVIDER ERROR - fiat option coin pair CHF/USDC or USDC/CHF not supported by exchange Kraken on date {}/{}/{} {}:{}'.format(
				nowDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr), printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)
		
		# next  entry: partial request unit change
		inputStr = '-uusd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		
		requestResultNoEndPrice = UtilityForTest.removeTwoEndPricesFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD/CHF.Kraken on AVG: R'
		
		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
		                                                            nowHourStr,
		                                                            nowMinuteStr,
		                                                            nowMonthStr,
		                                                            nowYearStr,
		                                                            requestResultNoEndPrice,
		                                                            expectedPrintResultNoDateTimeNoEndPrice)
		
		self.assertEqual('btc usd 0 all', fullCommandStrNoOptions)
		self.assertEqual('btc usd 0 all -fchf.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
	
	def testFiatAndValueOptionComputationFullRequestCurrentPriceFiatEqualsUnit(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: eth btc current price on kraken request
		inputStr = 'eth btc 0 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('eth btc 0 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcCurrentPrice = float(re.findall(r".* ([\d\.]+)", printResult)[0])

		#second command: eth btc current price request with eth fiat option
		inputStr = 'eth btc 0 kraken -vs3eth -fseth.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('eth btc 0 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 0 kraken -vs3eth -fseth.kraken', fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0])
		ethEthFiatRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1])

		#ensure fiat value of eth in eth is correct
		self.assertAlmostEqual(round(ethBtcRate * ethEthFiatRate, GuiOutputFormatter.PRICE_FLOAT_ROUNDING), ethBtcCurrentPrice, delta=0.4)

		#'eth btc 0 kraken -vs3eth -fseth.kraken
		#(0.03835 ETH/BTC * 26.0756193 BTC/ETH = 1 ETH/ETH)'
		fullCommandStrForStatusBar = fullCommandStrForStatusBar.replace('\n', ' ').replace('(', '')
		
		ethBtcRateInStatusBarStr = float(re.findall(r"(\d+\.\d+|\d)", fullCommandStrForStatusBar)[2])
		btcEthRateInStatusBarStr = float(re.findall(r"(\d+\.\d+|\d)", fullCommandStrForStatusBar)[3])
		ethEthRateInStatusBarStr = float(re.findall(r"(\d+\.\d+|\d)", fullCommandStrForStatusBar)[4])

		self.assertAlmostEqual(ethBtcRateInStatusBarStr, ethBtcCurrentPrice, delta=0.1)
		self.assertAlmostEqual(btcEthRateInStatusBarStr, 1 / ethBtcCurrentPrice, delta=0.1)
		self.assertEqual(ethEthRateInStatusBarStr, 1)

	def testFiatAndValueOptionComputationFullRequestCurrentPriceFiatEqualsCrypto(self):
		'''
		This test verifies that the fiat computed amount is correct
		:return:
		'''
		#first command: eth btc current price on kraken request
		inputStr = 'eth btc 0 kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('eth btc 0 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcCurrentPrice = float(re.findall(r".* ([\d\.]+)", printResult)[0])

		#second command: eth btc current price request with eth fiat option
		inputStr = 'eth btc 0 kraken -vs3eth -fsbtc.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('eth btc 0 kraken', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('eth btc 0 kraken -vs3eth -fsbtc.kraken', fullCommandStrWithSaveOptionsForHistoryList)

		ethBtcRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][0])
		ethBtcFiatRate = float(re.findall(r".* ([\d\.]+) ([\d\.]+)", printResult)[0][1])

		#ensure fiat value of eth in btc is correct
		self.assertAlmostEqual(round(ethBtcRate, GuiOutputFormatter.PRICE_FLOAT_ROUNDING), ethBtcFiatRate, delta=0.4)
		
		# 'eth btc 0 kraken -vs3eth -fsbtc.kraken
		# (0.03835 ETH/BTC * 1 BTC/BTC = 0.03835 ETH/BTC)'
		fullCommandStrForStatusBar = fullCommandStrForStatusBar.replace('\n', ' ').replace('(', '')
		
		ethBtcRateInStatusBarStr = float(re.findall(r"(\d+\.\d+|\d)", fullCommandStrForStatusBar)[2])
		btcEthRateInStatusBarStr = float(re.findall(r"(\d+\.\d+|\d)", fullCommandStrForStatusBar)[3])
		ethBtcFiatRateInStatusBarStr = float(re.findall(r"(\d+\.\d+|\d)", fullCommandStrForStatusBar)[4])
		
		self.assertAlmostEqual(ethBtcRateInStatusBarStr, ethBtcCurrentPrice, delta=0.1)
		self.assertEqual(btcEthRateInStatusBarStr, 1)
		self.assertAlmostEqual(ethBtcFiatRateInStatusBarStr, ethBtcCurrentPrice, delta=0.1)


	def testGetPrintableResultForDayOnlyRequest_1dayBefore(self):
		"""
		In this day only full request test, a minute price is returned,
		except if the test is run on the first day of month
		"""
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		oneDaysBeforeArrowDate = now.shift(days=-1)

		oneDaysBeforeYearStr, oneDaysBeforeMonthStr, oneDaysBeforeDayStr, oneDaysBeforeHourStr, oneDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDaysBeforeArrowDate)

		inputStr = 'btc usd {} bitfinex'.format(oneDaysBeforeDayStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if 'Warning - request date' in printResult:
			# we are on the first day of current month. So, the day number of 1 day 
			# before now  will generate a request date in the future. Ex: 1 day before
			# April 1st is March 31st, so 31/04/current year, a date in the future !
			nowLastYear = DateTimeUtil.localNow(LOCAL_TIME_ZONE).shift(years=-1)
			nowLastYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
				nowLastYear)
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year.'
			expectedPrintResult = expectedPrintResult.format(oneDaysBeforeDayStr, nowMonthStr, nowLastYearStr, oneDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr)
		else:
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} {}:{}M'
			expectedPrintResult = expectedPrintResult.format(oneDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr)

		if not 'ERROR' in printResult:
			self.assertEqual(expectedPrintResult,
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(oneDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
		else:
			# if test is run on February 1st for example
			self.assertEqual('ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')), printResult)

		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForDayOnlyRequest_10daysBefore(self):
		"""
		In this day only full request test, a close price is returned.
		"""
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)
		nowYearStr, nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
			now)

		tenDaysBeforeArrowDate = now.shift(days=-10)

		tenDaysBeforeYearStr, tenDaysBeforeMonthStr, tenDaysBeforeDayStr, tenDaysBeforeHourStr, tenDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(tenDaysBeforeArrowDate)

		inputStr = 'btc usd {} bitfinex'.format(tenDaysBeforeDayStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if 'Warning - request date' in printResult:
			# we are between 1 and 10 of current month. So, the day number of now minus
			# 10 days will generate a request date in the future. Ex: 10 days before
			# April 9th is March 30th, so 30/04/current year, a date in the future !
			nowLastYear = DateTimeUtil.localNow(LOCAL_TIME_ZONE).shift(years=-1)
			nowLastYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
				nowLastYear)
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} {}:{} can not be in the future and was shifted back to last year.'
			expectedPrintResult = expectedPrintResult.format(tenDaysBeforeDayStr, nowMonthStr, nowLastYearStr, tenDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr, nowMinuteStr)
		else:
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'
			expectedPrintResult = expectedPrintResult.format(tenDaysBeforeDayStr, nowMonthStr, nowYearStr)

		self.assertEqual(expectedPrintResult,
			UtilityForTest.removeOneEndPriceFromResult(printResult))
		self.assertEqual('btc usd {}/{}/{} {}:{} bitfinex'.format(tenDaysBeforeDayStr, nowMonthStr, nowYearStr, nowHourStr,
															   nowMinuteStr), fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

	def testGetPrintableResultForPartialRequestsWithNoPreviousFullRequest(self):
		"""
		Test the error msg generated when a valid or invalid partial request is
		entered before any full request was submitted.
		"""
		#partial request with no previous full request
		inputStr = '-v100eth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - no full request executed before partial request -v100eth. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertIsNone(fullCommandStrWithNoSaveOptions)
		self.assertIsNone(fullCommandStrWithSaveOptionsForHistoryList)
		self.assertIsNone(fullCommandStrForStatusBar)

		#invalid partial request with no previous full request
		inputStr = '-vs'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request -vs: -vs with no value is not valid. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertIsNone(fullCommandStrWithNoSaveOptions)
		self.assertIsNone(fullCommandStrWithSaveOptionsForHistoryList)
		self.assertIsNone(fullCommandStrForStatusBar)

		#invalid partial request with no previous full request
		inputStr = '-zooo'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - no full request executed before partial request -zooo. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertIsNone(fullCommandStrWithNoSaveOptions)
		self.assertIsNone(fullCommandStrWithSaveOptionsForHistoryList)
		self.assertIsNone(fullCommandStrForStatusBar)

		#invalid partial request with no previous full request
		inputStr = '-z'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - no full request executed before partial request -z. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertIsNone(fullCommandStrWithNoSaveOptions)
		self.assertIsNone(fullCommandStrWithSaveOptionsForHistoryList)
		self.assertIsNone(fullCommandStrForStatusBar)

		#invalid partial request with no previous full request
		inputStr = '-v'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request -v: -v with no value is not valid. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertIsNone(fullCommandStrWithNoSaveOptions)
		self.assertIsNone(fullCommandStrWithSaveOptionsForHistoryList)
		self.assertIsNone(fullCommandStrForStatusBar)

		#command: '' to replay lst command
		inputStr = ''
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request .', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertIsNone(fullCommandStrWithNoSaveOptions)
		self.assertIsNone(fullCommandStrWithSaveOptionsForHistoryList)
		self.assertIsNone(fullCommandStrForStatusBar)

	def testGetPrintableResultForInputScenarioPartialRequestDateTime(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		#first command: RT price request
		inputStr = 'btc usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'BTC/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)

		self.assertEqual('btc usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)

		twoDaysBeforeArrowDate = now.shift(days=-2)

		twoDaysBeforeYearStr, twoDaysBeforeMonthStr, twoDaysBeforeDayStr, twoDaysBeforeHourStr, twoDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(twoDaysBeforeArrowDate)

		#second command: partial date -d and time -t request
		inputStr = '-d{}/{}/{} -t12:45'.format(twoDaysBeforeDayStr, twoDaysBeforeMonthStr, twoDaysBeforeYearStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 12:45M'
		expectedPrintResult = expectedPrintResult.format(twoDaysBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)

		if not 'ERROR' in printResult:
			self.assertEqual(expectedPrintResult,
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} 12:45 bitfinex'.format(twoDaysBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
		else:
			# if test is run on March 1st for example
			self.assertEqual('ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')), printResult)

		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		#third command: partial date -d with time request
		inputStr = '-d{} 11:34'.format(twoDaysBeforeDayStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if 'Warning - request date' in printResult:
			# we are on the first day of current month. So, the day number of 2 days
			# before now  will generate a request date in the future. Ex: 2 days before
			# April 1st is March 30st, so 30/04/current year, a date in the future !
			nowLastYear = DateTimeUtil.localNow(LOCAL_TIME_ZONE).shift(years=-1)
			nowLastYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
				nowLastYear)
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} 11:34 can not be in the future and was shifted back to last year.'
			expectedPrintResult = expectedPrintResult.format(twoDaysBeforeDayStr, nowMonthStr, nowLastYearStr, twoDaysBeforeDayStr, nowMonthStr, nowYearStr)
		else:
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 11:34M'
			expectedPrintResult = expectedPrintResult.format(twoDaysBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)

		if not 'ERROR' in printResult:
			self.assertEqual(expectedPrintResult,
				UtilityForTest.removeOneEndPriceFromResult(printResult))
			self.assertEqual('btc usd {}/{}/{} 11:34 bitfinex'.format(twoDaysBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr, nowHourStr,
																   nowMinuteStr), fullCommandStrNoOptions)
		else:
			# if test is run on February 1st for example
			self.assertEqual('ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')), printResult)

		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		#fourth command: partial date -d with time request
		oneDayBeforeArrowDate = now.shift(days=-1)
		oneDayBeforeYearStr, oneDayBeforeMonthStr, oneDayBeforeDayStr, oneDayBeforeHourStr, oneDayBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(oneDayBeforeArrowDate)

		inputStr = '-d{} 16:34'.format(oneDayBeforeDayStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if 'Warning - request date' in printResult:
			# we are on the first day of current month. So, the day number of 2 days
			# before now  will generate a request date in the future. Ex: 2 days before
			# April 1st is March 30st, so 30/04/current year, a date in the future !
			nowLastYear = DateTimeUtil.localNow(LOCAL_TIME_ZONE).shift(years=-1)
			nowLastYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
				nowLastYear)
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} 16:34 can not be in the future and was shifted back to last year.'
			expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, nowMonthStr, nowLastYearStr, oneDayBeforeDayStr, nowMonthStr, nowYearStr)
		else:
			if oneDayBeforeDayStr == '2' and twoDaysBeforeMonthStr == '3':
				# tst run on Marth 2nd
				expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'
				expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)
			
				if not 'ERROR' in printResult:
					self.assertEqual(expectedPrintResult,
					                 UtilityForTest.removeOneEndPriceFromResult(printResult))
					self.assertEqual(
						'btc usd {}/{}/{} 16:34 bitfinex'.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr),
						fullCommandStrNoOptions)
				else:
					# if test is run on February 1st for example
					self.assertEqual(
						'ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')),
						printResult)
			else:
				expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 16:34M'
				expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)

				if 'ERROR' not in printResult:
					self.assertEqual(expectedPrintResult,
						UtilityForTest.removeOneEndPriceFromResult(printResult))
					self.assertEqual('btc usd {}/{}/{} 16:34 bitfinex'.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr), fullCommandStrNoOptions)
				else:
					# if test is run on February 1st for example
					self.assertEqual('ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')), printResult)


		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		#fifth command: partial same day date -d with time different request
		inputStr = '-d{} 18:34'.format(oneDayBeforeDayStr)
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		if 'Warning - request date' in printResult:
			# we are on the first day of current month. So, the day number of 2 days
			# before now  will generate a request date in the future. Ex: 2 days before
			# April 1st is March 30st, so 30/04/current year, a date in the future !
			nowLastYear = DateTimeUtil.localNow(LOCAL_TIME_ZONE).shift(years=-1)
			nowLastYearStr, _, _, _, _ = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
				nowLastYear)
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C\nWarning - request date {}/{}/{} 18:34 can not be in the future and was shifted back to last year.'
			expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, nowMonthStr, nowLastYearStr, oneDayBeforeDayStr, nowMonthStr, nowYearStr)
		else:
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'
			expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)
		
		if oneDayBeforeDayStr == '2' and twoDaysBeforeMonthStr == '3':
			# tst run on Marth 2nd
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 00:00C'
			expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)
			
			if not 'ERROR' in printResult:
				self.assertEqual(expectedPrintResult,
				                 UtilityForTest.removeOneEndPriceFromResult(printResult))
				self.assertEqual(
					'btc usd {}/{}/{} 18:34 bitfinex'.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr),
					fullCommandStrNoOptions)
			else:
				# if test is run on February 1st for example
				self.assertEqual(
					'ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')),
					printResult)
		else:
			expectedPrintResult = 'BTC/USD on Bitfinex: ' + '{}/{}/{} 18:34M'
			expectedPrintResult = expectedPrintResult.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr)
			
			if 'ERROR' not in printResult:
				self.assertEqual(expectedPrintResult,
				                 UtilityForTest.removeOneEndPriceFromResult(printResult))
				self.assertEqual(
					'btc usd {}/{}/{} 18:34 bitfinex'.format(oneDayBeforeDayStr, twoDaysBeforeMonthStr, nowYearStr),
					fullCommandStrNoOptions)
			else:
				# if test is run on February 1st for example
				self.assertEqual(
					'ERROR - day is out of range for month: day 31, month {}.'.format(nowMonthStr.replace('0', '')),
					printResult)
		
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testGetPrintableResultForInputScenarioWithInvalidOptionValue(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		# first command: full request no option
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# second command: partial request invalid -v option
		inputStr = '-v'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request -v: -v with no value is not valid. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# third command: partial request invalid -vs option
		inputStr = '-vs'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request -vs: -vs with no value is not valid. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testGetPrintableResultForInputScenarioWithInvalidOptionFiat(self):
		now = DateTimeUtil.localNow(LOCAL_TIME_ZONE)

		nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

		# first command: full request no option
		inputStr = 'eth usd 0 bitfinex'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		requestResultNoEndPrice = UtilityForTest.removeOneEndPriceFromResult(printResult)
		expectedPrintResultNoDateTimeNoEndPrice = 'ETH/USD on Bitfinex: R'

		UtilityForTest.doAssertAcceptingOneMinuteDateTimeDifference(self, nowDayStr,
														  nowHourStr,
														  nowMinuteStr,
														  nowMonthStr,
														  nowYearStr,
														  requestResultNoEndPrice,
														  expectedPrintResultNoDateTimeNoEndPrice)
		self.assertEqual('eth usd 0 bitfinex', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# second command: partial request invalid -v option
		inputStr = '-f'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request -f: -f with no value is not valid. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# third command: partial request invalid -vs option
		inputStr = '-fs'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)

		self.assertEqual('ERROR - invalid partial request -fs: -fs with no value is not valid. Partial request ignored.', printResult)
		self.assertEqual('', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testOptionValueOptionFiatOptionPriceFullRequestHistoDayPrice(self):
		inputStr = 'krl btc 20/12/20 20:35 hitbtc -v2169.75krl -fusd.kraken -p0.0000075'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'2169.75 KRL/0.01627312 BTC/382.10436619 USD.Kraken on HitBTC: 20/12/20 20:35P 0.0000075 0.17610525', printResult)
		self.assertEqual('krl btc 20/12/20 20:35 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('krl btc 20/12/20 20:35 hitbtc -v2169.75krl -fusd.kraken -p0.0000075', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('krl btc 20/12/20 20:35 hitbtc -v2169.75krl -fusd.kraken -p0.0000075\n(0.0000075 KRL/BTC * 23480.7 BTC/USD = 0.17610525 KRL/USD)', fullCommandStrForStatusBar)

if __name__ == '__main__':
#	unittest.main()
	tst = TestControllerGui()
	tst.setUp()
	tst.testGetPrintableResultForDayOnlyAndTimeFullRequestOn31st()
	tst.setUp()
	tst.testGetPrintableResultForUnsupportedPartialRequestOptionSaveAfterValidRealTimeRequest()
	tst.setUp()
	tst.testOptionValueOptionFiatFullRequestHistoDayPrice()
	tst.setUp()
	tst.testOptionValueOptionFiatFullRequestHistoDayPriceRequiredParmsOrderChanged()
	tst.testOptionValueOptionFiatFullRequestHistoDayPriceMandatoryParmsAndOptionOrderChanged()
	tst.setUp()
	tst.testGetPrintableResultForDayOnlyAndTimeFullRequestOn31st()
	tst.setUp()
	tst.testGetPrintableResultFullRequestNoDateNoTime()
	tst.setUp()
	tst.testOptionValueOptionFiatOptionPriceFullRequestHistoDayPrice()
	tst.setUp()
	tst.testGetPrintableResultForInputScenarioPartialRequestDateTime()