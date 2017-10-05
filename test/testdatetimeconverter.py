import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from datetimeconverter import DateTimeConverter

DATE_TIME_FORMAT_ARROW = 'YYYY/MM/DD HH:mm:ss'
DATE_TIME_FORMAT_TZ_ARROW = DATE_TIME_FORMAT_ARROW + ' ZZ'

class TestDatetimeConverter(unittest.TestCase):
    def setUp(self):
        pass

    def testTimestampToLocalDate(self):
        timeStamp = 1506787315
        arrowObjIN = DateTimeConverter.timestampToLocalDate(timeStamp, 'Asia/Calcutta')
        self.assertEqual("2017/09/30 21:31:55 +05:30",arrowObjIN.format(DATE_TIME_FORMAT_TZ_ARROW))


if __name__ == '__main__':
    unittest.main()
