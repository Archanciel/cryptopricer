import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import re
from controller import Controller
from datetimeutil import DateTimeUtil
from guioutputformater import GuiOutputFormater
from testcontroller import TestController


class TestControllerGui(TestController):
    '''
    This test class is launched from allguy.py, the class that runs
    all the tests in Pydroid on Android.

    Test the Controller using a GuiOuputFormater in place of a ConsoleOutputFormaater
    since GuiOuputFormater runs on Android in Pydroid, but fails in QPython !

    All the test cases are defineed in the TestController parent to avoid code duplication
    '''
    def setUp(self):
        #print('---- Instanciating Controller with GuiOuputFormater ----')
        self.controller = Controller(GuiOutputFormater())


    @unittest.skip
    def testControllerAskRTWithValueSave(self):
        stdin = sys.stdin
        sys.stdin = StringIO('btc usd 0 all -vc0.01btc\nq\ny')

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptoout.txt'
        else:
            FILE_PATH = 'c:\\temp\\cryptoout.txt'

        stdout = sys.stdout

        # using a try/catch here prevent the test from failing  due to the run of CommandQuit !
        try:
            with open(FILE_PATH, 'w') as outFile:
                sys.stdout = outFile
                self.controller.run() #will eat up what has been filled in stdin using StringIO above
        except:
            pass

        sys.stdin = stdin
        sys.stdout = stdout

        now = DateTimeUtil.localNow('Europe/Zurich')
        nowMonthStr, nowDayStr, nowHourStr, nowMinuteStr = self.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        with open(FILE_PATH, 'r') as inFile:
            contentList = inFile.readlines()
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[1][:-1])) #removing \n from contentList entry !
            self.assertEqual('BTC/USD on CCCAGG: ' + '{}/{}/{} {}:{}R'.format(nowDayStr, nowMonthStr, now.year - 2000, nowHourStr, nowMinuteStr), self.removePriceFromResult(contentList[3][:-1])) #removing \n from contentList entry !


if __name__ == '__main__':
    unittest.main()
