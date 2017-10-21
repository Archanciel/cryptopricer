import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from datetimeutil import DateTimeUtil
import arrow

US_DATE_TIME_FORMAT_ARROW = 'YYYY/MM/DD HH:mm:ss'
US_YY_DATE_TIME_FORMAT_ARROW = 'YY/MM/DD HH:mm:ss'
US_DATE_TIME_FORMAT_TZ_ARROW = US_DATE_TIME_FORMAT_ARROW + ' ZZ'
US_YY_DATE_TIME_FORMAT_TZ_ARROW = US_YY_DATE_TIME_FORMAT_ARROW + ' ZZ'

FR_DATE_TIME_FORMAT_ARROW = 'DD/MM/YYYY HH:mm:ss'
FR_YY_DATE_TIME_FORMAT_ARROW = 'DD/MM/YY HH:mm:ss'
FR_DATE_TIME_FORMAT_TZ_ARROW = FR_DATE_TIME_FORMAT_ARROW + ' ZZ'
FR_YY_DATE_TIME_FORMAT_TZ_ARROW = FR_YY_DATE_TIME_FORMAT_ARROW + ' ZZ'

class TestDateTimeUtil(unittest.TestCase):
    def setUp(self):
        pass

    def testTimestampToSummerLocalDateUS(self):
        timeStamp = 1506787315

        arrowObjIN = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("17/09/30 21:31:55 +05:30", arrowObjIN.format(US_YY_DATE_TIME_FORMAT_TZ_ARROW))

        arrowObjZH = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Europe/Zurich')
        self.assertEqual("2017/09/30 18:01:55 +02:00", arrowObjZH.format(US_DATE_TIME_FORMAT_TZ_ARROW))

    def testTimestampToSummerLocalDateFR(self):
        timeStamp = 1506787315

        arrowObjIN = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("30/09/17 21:31:55 +05:30", arrowObjIN.format(FR_YY_DATE_TIME_FORMAT_TZ_ARROW))

        arrowObjZH = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Europe/Zurich')
        self.assertEqual("30/09/2017 18:01:55 +02:00", arrowObjZH.format(FR_DATE_TIME_FORMAT_TZ_ARROW))

    def testTimestampToWinterLocalDate(self):
        timeStamp = 1512057715
        
        arrowObjIN = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("17/11/30 21:31:55 +05:30", arrowObjIN.format(US_YY_DATE_TIME_FORMAT_TZ_ARROW))
        
        arrowObjZH = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Europe/Zurich')
        self.assertEqual("2017/11/30 17:01:55 +01:00", arrowObjZH.format(US_DATE_TIME_FORMAT_TZ_ARROW))


    def testSummerDateTimeStringToTimeStampUS(self):
        expTimeStamp = 1506787315

        dateStr = '17/09/30 21:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Asia/Calcutta', US_YY_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)

        dateStr = '2017/09/30 18:01:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Europe/Zurich', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)


    def testSummerDateTimeStringToTimeStampUS(self):
        expTimeStamp = 1506787315

        dateStr = '30/09/17 21:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Asia/Calcutta', FR_YY_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)

        dateStr = '30/09/2017 18:01:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Europe/Zurich', FR_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)


    def testWinterDateTimeStringToTimeStamp(self):
        expTimeStamp = 1512061315
        
        dateStr = '2017/11/30 22:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Asia/Calcutta', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)

        dateStr = '2017/11/30 18:01:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, 'Europe/Zurich', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, timeStamp)


    def testSummerDateTimeStringToArrowLocalDate(self):
        expTimeStamp = 1506787315

        dateStr = '2017/09/30 21:31:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Asia/Calcutta', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)

        dateStr = '2017/09/30 18:01:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Europe/Zurich', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)


    def testWinterDateTimeStringToArrowLocalDate(self):
        expTimeStamp = 1512061315

        dateStr = '2017/11/30 22:31:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Asia/Calcutta', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)

        dateStr = '2017/11/30 18:01:55'
        arrowDateObj = DateTimeUtil.dateTimeStringToArrowLocalDate(dateStr, 'Europe/Zurich', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual(expTimeStamp, arrowDateObj.timestamp)


    def testConvertToTimeZoneSummer(self):
        locDateStr = '2017/09/30 09:00:00'
        datetimeObjLA = DateTimeUtil.dateTimeStringToArrowLocalDate(locDateStr, 'US/Pacific', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual('2017/09/30 09:00:00 -07:00', datetimeObjLA.format(US_DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjZH = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Europe/Zurich')
        self.assertEqual('2017/09/30 18:00:00 +02:00', datetimeObjZH.format(US_DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjIN = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Asia/Calcutta')
        self.assertEqual('2017/09/30 21:30:00 +05:30', datetimeObjIN.format(US_DATE_TIME_FORMAT_TZ_ARROW))


    def testConvertToTimeZoneWinter(self):
        locDateStr = '2017/11/30 09:00:00'
        datetimeObjLA = DateTimeUtil.dateTimeStringToArrowLocalDate(locDateStr, 'US/Pacific', US_DATE_TIME_FORMAT_ARROW)
        self.assertEqual('2017/11/30 09:00:00 -08:00', datetimeObjLA.format(US_DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjZH = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Europe/Zurich')
        self.assertEqual('2017/11/30 18:00:00 +01:00', datetimeObjZH.format(US_DATE_TIME_FORMAT_TZ_ARROW))

        datetimeObjIN = DateTimeUtil.convertToTimeZone(datetimeObjLA, 'Asia/Calcutta')
        self.assertEqual('2017/11/30 22:30:00 +05:30', datetimeObjIN.format(US_DATE_TIME_FORMAT_TZ_ARROW))


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


    def testIsTimeStampOlderThanSevenDays(self):
        DAYS_BEFORE = -7
        dateBefore = arrow.utcnow().shift(days = DAYS_BEFORE).to('Europe/Zurich')
        self.assertFalse(DateTimeUtil.isTimeStampOlderThan(dateBefore.timestamp, abs(DAYS_BEFORE)))


    def testIsTimeStampOlderThanSevenDaysPlusOneSecond(self):
        DAYS_BEFORE = -7
        SECOND_BEFORE = -1
        dateBefore = arrow.utcnow().shift(days = DAYS_BEFORE, seconds = SECOND_BEFORE).to('Europe/Zurich')
        self.assertTrue(DateTimeUtil.isTimeStampOlderThan(dateBefore.timestamp, abs(DAYS_BEFORE)))


    def testIsTimeStampOlderThanSevenDaysMinusOneSecond(self):
        DAYS_BEFORE = -7
        SECOND_AFTER = 1
        dateBefore = arrow.utcnow().shift(days = DAYS_BEFORE, seconds = SECOND_AFTER).to('Europe/Zurich')
        self.assertFalse(DateTimeUtil.isTimeStampOlderThan(dateBefore.timestamp, abs(DAYS_BEFORE)))


    def testLocalNow(self):
        nowZH = arrow.utcnow().to('Europe/Zurich')
        datetimeObjZH = DateTimeUtil.localNow('Europe/Zurich')
        self.assertEqual(nowZH.format(FR_YY_DATE_TIME_FORMAT_TZ_ARROW), datetimeObjZH.format(FR_YY_DATE_TIME_FORMAT_TZ_ARROW))


    def testUtcNowTimeStamp(self):
        nowZHts = arrow.utcnow().to('Europe/Zurich').timestamp
        utcTimeStamp = DateTimeUtil.utcNowTimeStamp()
        self.assertEqual(nowZHts, utcTimeStamp)


    def testShiftTimeStampToEndOfDay(self):
        timeStamp = 1506787315 #30/09/2017 16:01:55 +00:00 or 30/09/2017 18:01:55 +02:00

        timeStampEndOfDay = DateTimeUtil.shiftTimeStampToEndOfDay(timeStamp)
        arrowObjUTCEndOfDay = DateTimeUtil.timeStampToArrowLocalDate(timeStampEndOfDay, 'UTC')
        self.assertEqual("2017/09/30 23:59:59 +00:00", arrowObjUTCEndOfDay.format(US_DATE_TIME_FORMAT_TZ_ARROW))

        arrowObjZHEndOfDay = DateTimeUtil.timeStampToArrowLocalDate(timeStampEndOfDay, 'Europe/Zurich')
        self.assertEqual("2017/10/01 01:59:59 +02:00", arrowObjZHEndOfDay.format(US_DATE_TIME_FORMAT_TZ_ARROW))

    def testShiftTimeStampToEndOfDay_alt(self):
        utcArrowDateTimeObj_begOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 00:00:00", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        timeStampBegDay = utcArrowDateTimeObj_begOfDay.timestamp
        utcArrowDateTimeObj_endOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC',
                                                                                   "YYYY/MM/DD HH:mm:ss")
        timeStampEndDay = utcArrowDateTimeObj_endOfDay.timestamp
        timeStampShifted = DateTimeUtil.shiftTimeStampToEndOfDay(timeStampBegDay)

        self.assertEqual(timeStampShifted, timeStampEndDay)


    def testDateTimeStringToArrowLocalDate(self):
        zhArrowDateTimeObj_begOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 02:00:00", 'Europe/Zurich',
                                                                                  "YYYY/MM/DD HH:mm:ss")
        self.assertEqual(1506729600, zhArrowDateTimeObj_begOfDay.timestamp)
        self.assertEqual("2017/09/30 02:00:00 +02:00", zhArrowDateTimeObj_begOfDay.format(US_DATE_TIME_FORMAT_TZ_ARROW))


    def testDateTimeStringToTimeStamp(self):
        absoluteTimeStamp = DateTimeUtil.dateTimeStringToTimeStamp("2017/09/30 02:00:00", 'Europe/Zurich',
                                                                   "YYYY/MM/DD HH:mm:ss")
        self.assertEqual(1506729600, absoluteTimeStamp)


    def testDateTimeComponentsToArrowLocalDate(self):
        zhArrowDateTimeObj_begOfDay = DateTimeUtil.dateTimeComponentsToArrowLocalDate(30, 9, 2017, 2, 0, 0, 'Europe/Zurich')
        self.assertEqual(1506729600, zhArrowDateTimeObj_begOfDay.timestamp)
        self.assertEqual("2017/09/30 02:00:00 +02:00", zhArrowDateTimeObj_begOfDay.format(US_DATE_TIME_FORMAT_TZ_ARROW))


    def testDateTimeComponentsToTimeStamp(self):
        absoluteTimeStamp = DateTimeUtil.dateTimeComponentsToTimeStamp(30, 9, 2017, 2, 0, 0, 'Europe/Zurich')

        self.assertEqual(1506729600, absoluteTimeStamp)


    def testDateTimeComponentsSecondNonZeroToTimeStamp(self):
        absoluteTimeStamp = DateTimeUtil.dateTimeComponentsToTimeStamp(30, 9, 2017, 2, 0, 1, 'Europe/Zurich')

        self.assertEqual(1506729601, absoluteTimeStamp)


if __name__ == '__main__':
    unittest.main()
