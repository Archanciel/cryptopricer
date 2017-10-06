import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from datetimeutil import DateTimeUtil

DATE_TIME_FORMAT_ARROW = 'YYYY/MM/DD HH:mm:ss'
DATE_TIME_FORMAT_TZ_ARROW = DATE_TIME_FORMAT_ARROW + ' ZZ'

class TestDateTimeUtil(unittest.TestCase):
    def setUp(self):
        pass


    def testTimestampToLocalDate(self):
        timeStamp = 1506787315
        arrowObjIN = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("2017/09/30 21:31:55 +05:30",arrowObjIN.format(DATE_TIME_FORMAT_TZ_ARROW))


    def testSummerDateTimeStringToTimeStamp(self):
        dateStr = '2017/09/30 21:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, DATE_TIME_FORMAT_ARROW, 'Asia/Calcutta')
        self.assertEqual(1506787315, timeStamp)


    def testWinerDateTimeStringToTimeStamp(self):
        dateStr = '2017/11/30 21:31:55'
        timeStamp = DateTimeUtil.dateTimeStringToTimeStamp(dateStr, DATE_TIME_FORMAT_ARROW, 'Asia/Calcutta')
        self.assertEqual(1512057715, timeStamp)


if __name__ == '__main__':
    unittest.main()
