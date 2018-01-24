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
        dateTimeObjDayStr = dateTimeObj.format('DD')
        dateTimeObjMonthStr = dateTimeObj.format('MM')
        dateTimeObjYearStr = dateTimeObj.format('YY')
        dateTimeObjHourStr = dateTimeObj.format('HH')
        dateTimeObjMinuteStr = dateTimeObj.format('mm')

        return dateTimeObjYearStr, dateTimeObjMonthStr, dateTimeObjDayStr, dateTimeObjHourStr, dateTimeObjMinuteStr


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