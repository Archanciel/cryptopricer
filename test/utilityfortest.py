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
        dateTimeObjMinute = dateTimeObj.minute

        if dateTimeObjMinute < 10:
            if dateTimeObjMinute > 0:
                dateTimeObjMinuteStr = '0' + str(dateTimeObjMinute)
            else:
                dateTimeObjMinuteStr = '00'
        else:
            dateTimeObjMinuteStr = str(dateTimeObjMinute)

        dateTimeObjHour = dateTimeObj.hour

        if dateTimeObjHour < 10:
            if dateTimeObjHour > 0:
                dateTimeObjHourStr = '0' + str(dateTimeObjHour)
            else:
                dateTimeObjHourStr = '00'
        else:
            dateTimeObjHourStr = str(dateTimeObjHour)

        dateTimeObjDay = dateTimeObj.day

        if dateTimeObjDay < 10:
            dateTimeObjDayStr = '0' + str(dateTimeObjDay)
        else:
            dateTimeObjDayStr = str(dateTimeObjDay)
        dateTimeObjMonth = dateTimeObj.month

        if dateTimeObjMonth < 10:
            dateTimeObjMonthStr = '0' + str(dateTimeObjMonth)
        else:
            dateTimeObjMonthStr = str(dateTimeObjMonth)

        return dateTimeObjMonthStr, dateTimeObjDayStr, dateTimeObjHourStr, dateTimeObjMinuteStr


    @staticmethod
    def removePriceFromResult(resultStr):
        '''
        Used to remove unique price from RT request results or variable date/time price request results
        :param resultStr:
        :return:
        '''
        match = re.match(r"(.*) ([\d\.]*)", resultStr)

        if match != None:
            return match.group(1)
        else:
            return ()


    @staticmethod
    def removeAllPricesFromCommandValueResult(resultStr):
        '''
        Used to remove multiple prices from RT request results or variable date/time price request results
        :param resultStr:
        :return:
        '''
        match = re.match(r"(?:[\d\.]*) (\w*/)(?:[\d\.]*) (.*) (?:[\d\.]*)", resultStr)

        if match != None:
            return match.group(1) + match.group(2)
        else:
            return ()


if __name__ == '__main__':
    now = DateTimeUtil.localNow('Europe/Zurich')
    nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)
    print("{}/{} {}:{}".format(nowDayStr, nowMonthStr, nowHourStr, nowMinuteStr))