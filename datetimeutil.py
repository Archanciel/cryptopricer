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
    def isDateOlderThan(dateTimeArrowObject, dayNumber):
        '''
        Return true if the passed dateTimeArrowObject converted to the UTC time zone
        is dayNumber days before UTC now.

        :param dateTimeArrowObject: arrow localized date time object.
        :param dayNumber: int day number
        :return: True or False
        '''
        return ((arrow.utcnow().timestamp - dateTimeArrowObject.to('UTC').timestamp) / dayNumber) > DateTimeUtil.SECONDS_PER_DAY


    @staticmethod
    def isTimeStampOlderThan(timeStamp, dayNumber):
        '''
        Return true if the passed time stamp is dayNumber days before UTC now.

        :param dateTimeArrowObject: arrow localized date time object.
        :param dayNumber: int day number
        :return: True or False
        '''
        return ((arrow.utcnow().timestamp - timeStamp) / dayNumber) > DateTimeUtil.SECONDS_PER_DAY


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
        endOfDayDateTimeArrowObject = arrow.Arrow.utcfromtimestamp(inDayTimeStamp).replace(hour=24, minute=0, second=0)
        return endOfDayDateTimeArrowObject.timestamp


if __name__ == '__main__':
    pass