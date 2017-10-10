import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from datetimeutil import DateTimeUtil
import arrow

DATE_TIME_FORMAT_ARROW = 'YYYY/MM/DD HH:mm:ss'
DATE_TIME_FORMAT_TZ_ARROW = DATE_TIME_FORMAT_ARROW + ' ZZ'

class TestDateTimeUtil(unittest.TestCase):
    def setUp(self):
        pass


    def testTimestampToSummerLocalDate(self):
        timeStamp = 1506787315
        
        arrowObjIN = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("2017/09/30 21:31:55 +05:30",arrowObjIN.format(DATE_TIME_FORMAT_TZ_ARROW))
        
        arrowObjZH = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Europe/Zurich')
        self.assertEqual("2017/09/30 18:01:55 +02:00",arrowObjZH.format(DATE_TIME_FORMAT_TZ_ARROW))


    def testTimestampToWinterLocalDate(self):
        timeStamp = 1512057715
        
        arrowObjIN = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("2017/11/30 21:31:55 +05:30",arrowObjIN.format(DATE_TIME_FORMAT_TZ_ARROW))
        
        arrowObjZH = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Europe/Zurich')
        self.assertEqual("2017/11/30 17:01:55 +01:00",arrowObjZH.format(DATE_TIME_FORMAT_TZ_ARROW))


    def testSummerDateTimeStringToTimeStamp(self):
        expTimeStamp = 1506787315

        dateStr = '2017/09/30 21:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Asia/Calcutta', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)

        dateStr = '2017/09/30 18:01:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Europe/Zurich', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)


    def testWinterDateTimeStringToTimeStamp(self):
        expTimeStamp = 1512061315
        
        dateStr = '2017/11/30 22:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Asia/Calcutta', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)

        dateStr = '2017/11/30 18:01:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Europe/Zurich', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)


    def testSummerDateTimeStringToArrowLocalDate(self):
        expTimeStamp = 1506787315

        dateStr = '2017/09/30 21:31:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Asia/Calcutta', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)

        dateStr = '2017/09/30 18:01:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Europe/Zurich', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)


    def testWinterDateTimeStringToArrowLocalDate(self):
        expTimeStamp = 1512061315

        dateStr = '2017/11/30 22:31:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Asia/Calcutta', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)

        dateStr = '2017/11/30 18:01:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Europe/Zurich', DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)


    def testConvertToTimeZoneSummer(self):
        locDateStr = '2017/09/30 09:00:00'
        datetimeObjLA = DateTimeUtil.dateTimeStringToArrowLocalDate(locDateStr, 'US/Pacific', DATE_TIME_FORMAT_ARROW)
        self.assertEqual('2017/09/30 09:00:00 -07:00', datetimeObjLA.format(DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjZH = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Europe/Zurich')
        self.assertEqual('2017/09/30 18:00:00 +02:00', datetimeObjZH.format(DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjIN = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Asia/Calcutta')
        self.assertEqual('2017/09/30 21:30:00 +05:30', datetimeObjIN.format(DATE_TIME_FORMAT_TZ_ARROW))


    def testConvertToTimeZoneWinter(self):
        locDateStr = '2017/11/30 09:00:00'
        datetimeObjLA = DateTimeUtil.dateTimeStringToArrowLocalDate(locDateStr, 'US/Pacific', DATE_TIME_FORMAT_ARROW)
        self.assertEqual('2017/11/30 09:00:00 -08:00', datetimeObjLA.format(DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjZH = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Europe/Zurich')
        self.assertEqual('2017/11/30 18:00:00 +01:00', datetimeObjZH.format(DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjIN = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Asia/Calcutta')
        self.assertEqual('2017/11/30 22:30:00 +05:30', datetimeObjIN.format(DATE_TIME_FORMAT_TZ_ARROW))


    def testIsDateOlderThanSevenDays(self):
        DAYS_BEFORE = 7
        dateBefore = arrow.utcnow().shift(days = -DAYS_BEFORE).to('Europe/Zurich')
        self.assertFalse(DateTimeUtil.isDateOlderThan(dateBefore, DAYS_BEFORE))


    def testIsDateOlderThanSevenDaysPlusOneSecond(self):
        DAYS_BEFORE = 7
        SECOND_BEFORE = 1
        dateBefore = arrow.utcnow().shift(days = -DAYS_BEFORE, seconds = -SECOND_BEFORE).to('Europe/Zurich')
        self.assertTrue(DateTimeUtil.isDateOlderThan(dateBefore, DAYS_BEFORE))


    def testIsDateOlderThanSevenDaysMinusOneSecond(self):
        DAYS_BEFORE = 7
        SECOND_BEFORE = 1
        dateBefore = arrow.utcnow().shift(days = -DAYS_BEFORE, seconds = SECOND_BEFORE).to('Europe/Zurich')
        self.assertFalse(DateTimeUtil.isDateOlderThan(dateBefore, DAYS_BEFORE))


if __name__ == '__main__':
    unittest.main()
