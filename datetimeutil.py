import arrow

class DateTimeUtil:
    @staticmethod
    def timeStampToArrowLocalDate(timeStamp, timeZoneStr):
        '''
        From timestamp, returns a localized arrow object
        :param timeStamp: UTC/GMT timezone independent timestamp
        :param timeZoneStr: like 'Europe/Zurich' or 'US/Pacific'
        :return: arrow.Arrow instance
        '''
        return arrow.Arrow.utcfromtimestamp(timeStamp).to(timeZoneStr)

    @staticmethod
    def dateTimeStringToTimeStamp(dateTimeStr, dateTimeFormatArrow, timeZoneStr):
        arrowObj = arrow.get(dateTimeStr, dateTimeFormatArrow).replace(tzinfo=timeZoneStr)

        return arrowObj.timestamp  # timestamp is independant from timezone !


if __name__ == '__main__':
    pass