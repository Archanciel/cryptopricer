import os,sys,inspect
import re

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from datetimeutil import DateTimeUtil

class UtilityForTest:
	'''
	This class contains static utility methods used by some unit test classes. It avoids code duplication.
	'''
	@staticmethod
	def getFormattedDateTimeComponentsForArrowDateTimeObj(dateTimeObj):
		'''
		Return dateTimeObjYearStr, dateTimeObjMonthStr, dateTimeObjDayStr, dateTimeObjHourStr,
		dateTimeObjMinuteStr corresponding to the passed Arrow date object
		:param dateTimeObj: passed Arrow date object
		:return:
		'''
		dateTimeObjDayStr = dateTimeObj.format('DD')
		dateTimeObjMonthStr = dateTimeObj.format('MM')
		dateTimeObjYearStr = dateTimeObj.format('YY')
		dateTimeObjHourStr = dateTimeObj.format('HH')
		dateTimeObjMinuteStr = dateTimeObj.format('mm')

		return dateTimeObjYearStr, dateTimeObjMonthStr, dateTimeObjDayStr, dateTimeObjHourStr, dateTimeObjMinuteStr


	@staticmethod
	def removeOneEndPriceFromResult(resultStr):
		'''
		Used to remove unique price from RT request results or variable date/time price request results
		:param resultStr:
		:return:
		'''
		patternNoWarning = r"(.*) ([\d\.]*)"
		patternOneWarning = r"(.*) ([\d\.]*)(\n.*)" #in raw string, \ must not be escaped (\\n not working !)
		match = re.match(patternOneWarning, resultStr)

		if (match):
			if len(match.groups()) == 3:
				# here, resultStr contains a warning like in
				# BTC/USD on CCCAGG: 30/01/18 01:51R 11248.28\nWarning - unsupported command -ebitfinex in request btc usd 0 all -ebitfinex !
				return match.group(1) + match.group(3)

		match = re.match(patternNoWarning, resultStr)

		if (match):
			if len(match.groups()) == 2:
				# the case for resultStr containing BTC/USD on CCCAGG: 30/01/18 01:49R 11243.72 for example !
				return match.group(1)

		return ()

	@staticmethod
	def removeTwoEndPricesFromResult(resultStr):
		'''
		Used to remove two prices from RT request results with -f (fiat) option or variable date/time price request
		results with -f (fiat) option
		:param resultStr:
		:return:
		'''
		patternNoWarning = r"(.*) (?:[\d\.]*) (?:[\d\.]*)"
		patternOneWarning = r"(.*) (?:[\d\.]*) (?:[\d\.]*)(\n.*)" #in raw string, \ must not be escaped (\\n not working !)
		match = re.match(patternOneWarning, resultStr)

		if (match):
			if len(match.groups()) == 2:
				# here, resultStr contains a warning like in
				# BTC/USD on CCCAGG: 30/01/18 01:51R 11248.28\nWarning - unsupported command -ebitfinex in request btc usd 0 all -ebitfinex !
				return match.group(1) + match.group(2)

		match = re.match(patternNoWarning, resultStr)

		if (match):
			if len(match.groups()) == 1:
				# the case for resultStr containing BTC/USD on CCCAGG: 30/01/18 01:49R 11243.72 for example !
				return match.group(1)

		return ()

	@staticmethod
	def removeAllPricesFromCommandValueResult(resultStr):
		'''
		Used to remove multiple prices from RT request results or variable date/time price request results
		:param resultStr:
		:return:
		'''
		patternNoWarning = r"(?:[\d\.]*) (\w*/)(?:[\d\.]*) (.*) (?:[\d\.]*)"
		patternOneWarning = r"(?:[\d\.]*) (\w*/)(?:[\d\.]*) (.*) (?:[\d\.]*(\n.*))"
		match = re.match(patternOneWarning, resultStr)

		if match != None:
			if len(match.groups()) == 3:
				return match.group(1) + match.group(2) + match.group(3)

		match = re.match(patternNoWarning, resultStr)

		if len(match.groups()) == 2:
			return match.group(1) + match.group(2)
		else:
			return ()

	@staticmethod
	def extractDateTimeStr(resultStr):
		dateTimePattern = r"(\d*/\d*/\d* \d*:\d*)"

		s = re.search(dateTimePattern, resultStr)
		
		if s != None:
			if len(s.groups()) == 1:
				group = s.group(1)
				return group
	
	@staticmethod
	def doAssertAcceptingOneMinuteDateTimeDifference(unitTest,
													 nowDayStr,
													 nowHourStr,
													 nowMinuteStr,
													 nowMonthStr,
													 nowYearStr,
													 requestResultNoEndPrice,
													 expectedPrintResultNoDateTimeNoEndPrice):
		"""
		This method verifies that the passed real time request result requestResultNoEndPrice
		date/time value correspond to now +/- 60 seconds. The purpose is to avoid a test
		failure due to the fact that the crypto price provider was requested at, say,
		11:54:59 (now value) and returns a result with time 11:55.
		
		:param unitTest:
		:param nowDayStr:
		:param nowHourStr:
		:param nowMinuteStr:
		:param nowMonthStr:
		:param nowYearStr:
		:param requestResultNoEndPrice:
		:param expectedPrintResultNoDateTimeNoEndPrice:
		:return:
		"""
		actualDateTimeStr = UtilityForTest.extractDateTimeStr(requestResultNoEndPrice)
		expectedDateTimeStr = '{}/{}/{} {}:{}'.format(nowDayStr, nowMonthStr, nowYearStr, nowHourStr,
													  nowMinuteStr)
		actualDateTimeStamp = DateTimeUtil.dateTimeStringToTimeStamp(actualDateTimeStr, 'Europe/Zurich',
																	 'DD/MM/YY HH:mm')
		expectedDateTimeStamp = DateTimeUtil.dateTimeStringToTimeStamp(expectedDateTimeStr, 'Europe/Zurich',
																	   'DD/MM/YY HH:mm')
		unitTest.assertAlmostEqual(actualDateTimeStamp, expectedDateTimeStamp, delta=60)
		unitTest.assertEqual(expectedPrintResultNoDateTimeNoEndPrice,
							 requestResultNoEndPrice.replace(actualDateTimeStr, ''))


if __name__ == '__main__':
	now = DateTimeUtil.localNow('Europe/Zurich')
	nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
	print("{}/{} {}:{}".format(nowDayStr, nowMonthStr, nowHourStr, nowMinuteStr))