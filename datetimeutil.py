import arrow
import re


class DateTimeUtil:
	SECONDS_PER_DAY = 86400

	SHORT_DATE_FORMAT_KEY = 'SHORT_DATE_FORMAT'
	LONG_DATE_FORMAT_KEY = 'LONG_DATE_FORMAT'
	TIME_FORMAT_KEY = 'TIME_FORMAT'

	@staticmethod
	def timeStampToArrowLocalDate(timeStamp, timeZoneStr):
		'''
		Given a UTC/GMT timezone independent timestamp and a timezone string specification,
		returns a localized arrow object.

		:param timeStamp: UTC/GMT timezone independent timestamp
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		:return: arrow localized date time object
		'''
		return arrow.Arrow.utcfromtimestamp(timeStamp).to(timeZoneStr)


	@staticmethod
	def dateTimeStringToTimeStamp(dateTimeStr, timeZoneStr, dateTimeFormatArrow):
		'''
		Given a datetime string which format abide to to the passed arrow format and
		a timezone string specification, return a UTC/GMT timezone independent timestamp.

		:param dateTimeStr:
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		:param dateTimeFormatArrow: example YYYY/MM/DD HH:mm:ss --> 2017/09/12 15:32:21
		:return: int UTC/GMT timezone independent timestamp
		'''
		arrowObj = arrow.get(dateTimeStr, dateTimeFormatArrow).replace(tzinfo=timeZoneStr)

		return arrowObj.int_timestamp  # timestamp is independant from timezone !


	@staticmethod
	def dateTimeStringToArrowLocalDate(dateTimeStr, timeZoneStr, dateTimeFormatArrow):
		'''
		Given a datetime string which format abide to to the passed arrow format and
		a timezone string specification, return an arrow localized date time object.

		:param dateTimeStr:
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		:param dateTimeFormatArrow: example YYYY/MM/DD HH:mm:ss --> 2017/09/12 15:32:21
		:return: arrow localized date time object
		'''
		return arrow.get(dateTimeStr, dateTimeFormatArrow).replace(tzinfo=timeZoneStr)


	@staticmethod
	def dateTimeComponentsToArrowLocalDate(dayInt, monthInt, yearInt, hourInt, minuteInt, secondInt, timeZoneStr):
		'''
		Given the passed date/time components and a timezone string specification,
		return an arrow localized date time object.

		:param dayInt:
		:param monthInt:
		:param yearInt:
		:param hourInt:
		:param minuteInt:
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		
		:return: arrow localized date time object.
		'''
		return arrow.get(yearInt, monthInt, dayInt, hourInt, minuteInt, secondInt).replace(tzinfo=timeZoneStr)


	@staticmethod
	def dateTimeComponentsToTimeStamp(day, month, year, hour, minute, second, timeZoneStr):
		'''
		Given the passed date/time components and a timezone string specification,
		return a UTC/GMT timezone independent timestamp.

		:param day:
		:param month:
		:param year:
		:param hour:
		:param minute:
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		:return: UTC/GMT timezone independent timestamp.
		'''
		return arrow.get(year, month, day, hour, minute, second).replace(tzinfo=timeZoneStr).int_timestamp


	@staticmethod
	def convertToTimeZone(dateTimeArrowObject, timeZoneStr):
		'''
		Return the passed dateTimeArrowObject converted to the passed timeZoneStr.
		The passed dateTimeArrowObject remains unchanged !

		:param dateTimeArrowObject: arrow localized date time object.
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		:return: arrow date time object localized  to passed timeZoneStr
		'''
		return dateTimeArrowObject.to(timeZoneStr)


	@staticmethod
	def isDateOlderThan(dateTimeArrowObject, dayNumberInt):
		'''
		Return true if the passed dateTimeArrowObject converted to the UTC time zone
		is dayNumber days before UTC now.

		:param dateTimeArrowObject: arrow localized date time object.
		:param dayNumberInt: int day number
		:return: True or False
		'''
		return ((arrow.utcnow().int_timestamp - dateTimeArrowObject.to('UTC').int_timestamp) / dayNumberInt) > DateTimeUtil.SECONDS_PER_DAY


	@staticmethod
	def isAfter(dateArrowObjectAfter, dateArrowObjectBefore):
		'''
		Return True if dateArrowObjectAfter is after dateArrowObjectBefore, False if dateArrowObjectAfter
		is on or is before dateArrowObjectBefore
		:param dateArrowObjectAfter:
		:param dateArrowObjectBefore:
		:return: True or False
		'''
		return dateArrowObjectAfter.int_timestamp > dateArrowObjectBefore.int_timestamp


	@staticmethod
	def isTimeStampOlderThan(timeStamp, timeZoneStr, dayNumberInt):
		'''
		Return true if the passed time stamp is dayNumber days before UTC now if
		no timezone is passed or local now if a timezone is passed.

		:param timeZoneStr timezone os the passed timeStamp
		:param dateTimeArrowObject: arrow localized date time object.
		:param dayNumberInt: int day number
		:return: True or False
		'''
		
		if timeZoneStr is None:
			return ((arrow.utcnow().int_timestamp - timeStamp) / dayNumberInt) > DateTimeUtil.SECONDS_PER_DAY
		else:
			return ((arrow.utcnow().to(timeZoneStr).int_timestamp - timeStamp) / dayNumberInt) > DateTimeUtil.SECONDS_PER_DAY

	@staticmethod
	def utcNowTimeStamp():
		'''
		Return the current UTC time stamp
		:return: current time zone independant (UTC) time stamp
		'''
		return arrow.utcnow().int_timestamp


	@staticmethod
	def localNow(timeZoneStr):
		'''
		Return a localised current dateTimeArrowObject
		:param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
		:return: current arrow localized date time object
		'''
		return arrow.now(timeZoneStr)


	@staticmethod
	def shiftTimeStampToEndOfDay(inDayTimeStamp):
		'''
		Return the time stamp of midnight of the day including the passed inDayTimeStamp
		:param inDayTimeStamp:
		:return: time stamp of the day containing inDayTimeStamp, but at midnight precisely
		'''
		endOfDayDateTimeArrowObject = arrow.Arrow.utcfromtimestamp(inDayTimeStamp).replace(hour=23, minute=59, second=59)
		return endOfDayDateTimeArrowObject.int_timestamp


	@staticmethod
	def getFormattedDateTimeComponents(arrowDateTimeObj, dateTimeformat):
		'''
		Returns 3 lists, one containing the date/time components symbols in the order they are used in the
		passed dateTimeFormat, the second containing 2 elements: the date and the time separator, and the
		third containing the corresponding formated values.

		Ex: for dateTimeformat = 'DD/MM/YY HH:mm' and 24/1/2018 4:41, returns
			['DD', 'MM', 'YY', 'HH', 'mm']
			['/', ':'] and
			['24', '01', '18', '04', '41']

			for dateTimeformat = 'YYYY-MM-DD HH.mm' and 24-1-2018 4.41, returns
			['YYYY', 'MM', 'DD', 'HH', 'mm']
			['-', '.'] and
			['2018', '01', '24', '04', '41']


		:param arrowDateTimeObj:
		:param dateTimeformat: in the format used by Arrow dates
		:return: dateTimeComponentSymbolList, separatorsList and dateTimeComponentValueList
		'''
		dateTimeComponentSymbolList, separatorsList = DateTimeUtil._extractDateTimeFormatComponentFromDateTimeFormat(
			dateTimeformat)
		dateTimeComponentValueList = []

		for dateTimeSymbol in dateTimeComponentSymbolList:
			dateTimeComponentValueList.append(arrowDateTimeObj.format(dateTimeSymbol))

		return dateTimeComponentSymbolList, separatorsList, dateTimeComponentValueList


	@staticmethod
	def _extractDateTimeFormatComponentFromDateTimeFormat(dateTimeformat):
		'''
		Returns 2 lists, the first containing the date/time components symbols in the order
		they are used in the passed dateTimeFormat, the second containing 2 elements:
		the date and the time separator.

		Ex: for dateTimeformat = 'DD/MM/YY HH:mm', returns
			['DD', 'MM', 'YY', 'HH', 'mm']
			['/', ':'] and

			for dateTimeformat = 'YYYY-MM-DD HH.mm', returns
			['YYYY', 'MM', 'DD', 'HH', 'mm']
			['-', '.'] and

		:param dateTimeformat: in the format used by Arrow dates
		:return: dateTimeComponentSymbolList, separatorsList
		'''
		# find the separators in 'DD/MM/YY HH:mm' - ['/', '/', ':'] or 'YYYY.MM.DD HH.mm' - ['.', '.', '.']
		dateTimeSeparators = re.findall(r"[^\w^ ]", dateTimeformat)
		# build the split pattern '/| |:' or '\.| |\.'
		# if a separator is a dot, must be escaped !
		if dateTimeSeparators[0] == '.':
			dateTimeSeparators[0] = r'\.'
		if dateTimeSeparators[-1] == '.':
			dateTimeSeparators[-1] = r'\.'
		separatorsList = [dateTimeSeparators[0], dateTimeSeparators[-1]]
		dateTimeComponentsSplitPattern = '{}| |{}'.format(dateTimeSeparators[0], dateTimeSeparators[-1])
		dateTimeComponentSymbolList = re.split(dateTimeComponentsSplitPattern, dateTimeformat)
		return dateTimeComponentSymbolList, separatorsList


	@staticmethod
	def getDateAndTimeFormatDictionary(dateTimeformat):
		'''
		Returns a dictonary containing the date and time formats corresponding to the
		passed Arrow dateTimeformat

		Ex: for dateTimeformat = 'DD/MM/YY HH:mm', returns
			['DD', 'MM', 'YY', 'HH', 'mm']
			['/', ':'] and

			for dateTimeformat = 'YYYY-MM-DD HH.mm', returns
			['YYYY', 'MM', 'DD', 'HH', 'mm']
			['-', '.'] and

		:param dateTimeformat: in the format used by Arrow dates
		:return: formatDic: dictionary containing the date and time formats
		'''
		dateTimeComponentSymbolList, separatorsList = DateTimeUtil._extractDateTimeFormatComponentFromDateTimeFormat(dateTimeformat)
		separatorsList = [(lambda x : x.strip('\\'))(x) for x in separatorsList]
		formatDic = {}

		# handling date formats
		dateSep = separatorsList[0]

		if 'Y' in dateTimeComponentSymbolList[0].upper():
			#date start with year
			formatDic[DateTimeUtil.LONG_DATE_FORMAT_KEY] = '{}{}{}{}{}'.format(dateTimeComponentSymbolList[0],
																  dateSep,
																  dateTimeComponentSymbolList[1],
																  dateSep,
																  dateTimeComponentSymbolList[2])
			formatDic[DateTimeUtil.SHORT_DATE_FORMAT_KEY] = '{}{}{}'.format(dateTimeComponentSymbolList[1],
										   dateSep,
										   dateTimeComponentSymbolList[2])
		elif 'D' in dateTimeComponentSymbolList[0].upper():
			#date start with day
			formatDic[DateTimeUtil.LONG_DATE_FORMAT_KEY] = '{}{}{}{}{}'.format(dateTimeComponentSymbolList[0],
																  dateSep,
																  dateTimeComponentSymbolList[1],
																  dateSep,
																  dateTimeComponentSymbolList[2])
			formatDic[DateTimeUtil.SHORT_DATE_FORMAT_KEY] = '{}{}{}'.format(dateTimeComponentSymbolList[0],
												dateSep,
												dateTimeComponentSymbolList[1])
		elif 'M' in dateTimeComponentSymbolList[0].upper():
			# date start with month
			formatDic[DateTimeUtil.LONG_DATE_FORMAT_KEY] = '{}{}{}{}{}'.format(dateTimeComponentSymbolList[0],
																			   dateSep,
																			   dateTimeComponentSymbolList[1],
																			   dateSep,
																			   dateTimeComponentSymbolList[2])
			formatDic[DateTimeUtil.SHORT_DATE_FORMAT_KEY] = '{}{}{}'.format(dateTimeComponentSymbolList[0],
																			dateSep,
																			dateTimeComponentSymbolList[1])
		else:
			#unsupported date format
			pass

		# handling time formats
		timeSep = separatorsList[1]

		formatDic[DateTimeUtil.TIME_FORMAT_KEY] = '{}{}{}'.format(dateTimeComponentSymbolList[3],
									   timeSep,
									   dateTimeComponentSymbolList[4])

		return formatDic


	@staticmethod
	def _unescape(str):
		return str.strip('\\')

	@staticmethod
	def formatPrintDateTimeFromStringComponents(dayStr,
												monthStr,
												yearStr,
												hourStr,
												minuteStr,
												timezoneStr,
												dateTimeFormat):
		'''
		Accept string date/time components and return them as formatted date and time
		according to the passed dateTimeFormat (comes from the ConfigurationManager).

		:param dayStr:
		:param monthStr:
		:param yearStr:
		:param hourStr:
		:param minuteStr:
		:param timezoneStr:
		:param dateTimeFormat:
		:return:
		'''
		dayInt = int(dayStr)
		monthInt = int(monthStr)

		if yearStr == None:
			now = DateTimeUtil.localNow(timezoneStr)
			yearInt = now.year
		else:
			yearInt = int(yearStr)

		if hourStr != None and minuteStr != None:
			# hour can not exist without minute and vice versa !
			hourInt = int(hourStr)
			minuteInt = int(minuteStr)
		else:
			hourInt = 0
			minuteInt = 0

		dateDMY, dateHM = DateTimeUtil.formatPrintDateTimeFromIntComponents(dayInt, monthInt, yearInt, hourInt,
																			minuteInt, timezoneStr, dateTimeFormat)

		return dateDMY, dateHM

	@staticmethod
	def formatPrintDateTimeFromIntComponents(dayInt,
											 monthInt,
											 yearInt,
											 hourInt,
											 minuteInt,
											 timezoneStr,
											 dateTimeFormat):
		'''
		Accept integer date/time components and return them as formatted date and time
		according to the passed dateTimeFormat (comes from the ConfigurationManager).

		In case all passed date components are 0, which is the case in real time request
		context, returns the local now DMY and HM string values.

		:param dayInt:
		:param monthInt:
		:param yearInt:
		:param hourInt:
		:param minuteInt:
		:param timezoneStr:
		:param dateTimeFormat:
		
		:return: DMY and HM string values
		'''
		if yearInt == 0 and monthInt == 0 and dayInt == 0 and hourInt == 0:
			# the case if formatPrintDateTimeFromIntComponents called in the context of
			# a real time request
			arrowDate = DateTimeUtil.localNow(timezoneStr)
		else:
			arrowDate = DateTimeUtil.dateTimeComponentsToArrowLocalDate(dayInt,
																	monthInt,
																	yearInt,
																	hourInt,
																	minuteInt,
																	0,
																	timezoneStr)
			
		dateTimeComponentSymbolList, separatorsList, dateTimeComponentValueList = DateTimeUtil.getFormattedDateTimeComponents(
			arrowDate, dateTimeFormat)
		dateSeparator = separatorsList[0]
		timeSeparator = separatorsList[1]

		dateDMY = dateTimeComponentValueList[0] + dateSeparator + dateTimeComponentValueList[1] + dateSeparator + \
				  dateTimeComponentValueList[2]
		dateHM = dateTimeComponentValueList[3] + timeSeparator + dateTimeComponentValueList[4]

		return dateDMY, dateHM


if __name__ == '__main__':
	utcArrowDateTimeObj_endOfPreviousDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/29 23:59:59", 'UTC',
																	  "YYYY/MM/DD HH:mm:ss")
	print('endOfPreviousDay.timestamp: ' + str(utcArrowDateTimeObj_endOfPreviousDay.int_timestamp) + ' ' + utcArrowDateTimeObj_endOfPreviousDay.format("YYYY/MM/DD HH:mm:ss ZZ"))
	utcArrowDateTimeObj_begOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 00:00:00", 'UTC',
																	  "YYYY/MM/DD HH:mm:ss")
	print('begOfCurrentDay.timestamp;  ' + str(utcArrowDateTimeObj_begOfCurrentDay.int_timestamp) + ' ' + utcArrowDateTimeObj_begOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

	utcArrowDateTimeObj_endOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC',
																	  "YYYY/MM/DD HH:mm:ss")
	print('endOfCurrentDay.timestamp:  ' + str(utcArrowDateTimeObj_endOfCurrentDay.int_timestamp) + ' ' + utcArrowDateTimeObj_endOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))
	utcArrowDateTimeObj_midOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 13:59:59", 'UTC',
																	  "YYYY/MM/DD HH:mm:ss")
	print('midOfCurrentDay.timestamp:  ' + str(utcArrowDateTimeObj_midOfCurrentDay.int_timestamp) + ' ' + utcArrowDateTimeObj_midOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

	utcArrowDateTimeObj_midOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/29 22:00:00", 'UTC',
																	  "YYYY/MM/DD HH:mm:ss")
	print('midOfCurrentDay.timestamp:  ' + str(utcArrowDateTimeObj_midOfCurrentDay.int_timestamp) + ' ' + utcArrowDateTimeObj_midOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

	print('essai                    :  ' + str(utcArrowDateTimeObj_midOfCurrentDay.int_timestamp) + ' ' + utcArrowDateTimeObj_midOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

	tsEOD = DateTimeUtil.shiftTimeStampToEndOfDay(utcArrowDateTimeObj_begOfCurrentDay.int_timestamp)
	print('shifted:                    ' + str(tsEOD))

	timezoneStr = 'Europe/Zurich'
	now = DateTimeUtil.localNow(timezoneStr)
	dateTimeformat = 'DD/MM/YY HH:mm'
	dateTimeComponentSymbolList, separatorsList, dateTimeComponentValueList = DateTimeUtil.getFormattedDateTimeComponents(now, dateTimeformat)
	print(dateTimeComponentSymbolList)
	print(separatorsList)
	print(dateTimeComponentValueList)
	dateTimeformat = 'YYYY.MM.DD HH.mm'
	dateTimeComponentSymbolList, separatorsList, dateTimeComponentValueList = DateTimeUtil.getFormattedDateTimeComponents(now, dateTimeformat)
	print(dateTimeComponentSymbolList)
	print(separatorsList)
	print(dateTimeComponentValueList)

	gmtPlusList = []
	gmtMinusList = []

	for i in range(24):
		tz = 'GMT+' + str(i)
		gmtPlusList.append(tz)
		tzTime = DateTimeUtil.localNow(tz)
		print("{}: {}".format(tz, tzTime))

	for i in range(24):
		tz = 'GMT-' + str(i)
		gmtMinusList.append(tz)
		tzTime = DateTimeUtil.localNow(tz)
		print("{}: {}".format(tz, tzTime))

	gmtPlusList.append(gmtMinusList)

	print(gmtPlusList)

	print('\nBug\n')
	print(DateTimeUtil.formatPrintDateTimeFromIntComponents(12, 11, 20, 15, 2, 'Europe/Zurich', 'DD/MM/YY HH:mm'))
	print(DateTimeUtil.formatPrintDateTimeFromStringComponents('01','01','20','18','48','Europe/Zurich','DD/MM/YY HH:mm'))
