import arrow

class DateTimeUtil:
    SECONDS_PER_DAY = 86400

    @staticmethod
    def timeStampToArrowLocalDate(timeStamp, timeZoneStr):
        '''
        FGiven a UTC/GMT timezone independent timestamp and a timezone string specification,
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

        return arrowObj.timestamp  # timestamp is independant from timezone !


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
        return arrow.get(year, month, day, hour, minute, second).replace(tzinfo=timeZoneStr).timestamp


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
        return ((arrow.utcnow().timestamp - dateTimeArrowObject.to('UTC').timestamp) / dayNumberInt) > DateTimeUtil.SECONDS_PER_DAY


    @staticmethod
    def isAfter(dateArrowObjectAfter, dateArrowObjectBefore):
        '''
        Return True if dateArrowObjectAfter is after dateArrowObjectBefore, False if dateArrowObjectAfter
        is on or is before dateArrowObjectBefore
        :param dateArrowObjectAfter:
        :param dateArrowObjectBefore:
        :return: True or False
        '''
        return dateArrowObjectAfter.timestamp > dateArrowObjectBefore.timestamp


    @staticmethod
    def isTimeStampOlderThan(timeStamp, dayNumberInt):
        '''
        Return true if the passed time stamp is dayNumber days before UTC now.

        :param dateTimeArrowObject: arrow localized date time object.
        :param dayNumberInt: int day number
        :return: True or False
        '''
        return ((arrow.utcnow().timestamp - timeStamp) / dayNumberInt) > DateTimeUtil.SECONDS_PER_DAY


    @staticmethod
    def utcNowTimeStamp():
        '''
        Return the current UTC time stamp
        :return: current time zone independant (UTC) time stamp
        '''
        return arrow.utcnow().timestamp


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
        return endOfDayDateTimeArrowObject.timestamp


if __name__ == '__main__':
    utcArrowDateTimeObj_endOfPreviousDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/29 23:59:59", 'UTC',
                                                                      "YYYY/MM/DD HH:mm:ss")
    print('endOfPreviousDay.timestamp: ' + str(utcArrowDateTimeObj_endOfPreviousDay.timestamp) + ' ' + utcArrowDateTimeObj_endOfPreviousDay.format("YYYY/MM/DD HH:mm:ss ZZ"))
    utcArrowDateTimeObj_begOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 00:00:00", 'UTC',
                                                                      "YYYY/MM/DD HH:mm:ss")
    print('begOfCurrentDay.timestamp;  ' + str(utcArrowDateTimeObj_begOfCurrentDay.timestamp) + ' ' + utcArrowDateTimeObj_begOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

    utcArrowDateTimeObj_endOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC',
                                                                      "YYYY/MM/DD HH:mm:ss")
    print('endOfCurrentDay.timestamp:  ' + str(utcArrowDateTimeObj_endOfCurrentDay.timestamp) + ' ' + utcArrowDateTimeObj_endOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))
    utcArrowDateTimeObj_midOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 13:59:59", 'UTC',
                                                                      "YYYY/MM/DD HH:mm:ss")
    print('midOfCurrentDay.timestamp:  ' + str(utcArrowDateTimeObj_midOfCurrentDay.timestamp) + ' ' + utcArrowDateTimeObj_midOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

    utcArrowDateTimeObj_midOfCurrentDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/29 22:00:00", 'UTC',
                                                                      "YYYY/MM/DD HH:mm:ss")
    print('midOfCurrentDay.timestamp:  ' + str(utcArrowDateTimeObj_midOfCurrentDay.timestamp) + ' ' + utcArrowDateTimeObj_midOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

    print('essai                    :  ' + str(utcArrowDateTimeObj_midOfCurrentDay.timestamp) + ' ' + utcArrowDateTimeObj_midOfCurrentDay.format("YYYY/MM/DD HH:mm:ss ZZ"))

    tsEOD = DateTimeUtil.shiftTimeStampToEndOfDay(utcArrowDateTimeObj_begOfCurrentDay.timestamp)
    print('shifted:                    ' + str(tsEOD))
