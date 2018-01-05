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
        print('---- Instanciating Controller with GuiOuputFormater ----')
        self.controller = Controller(GuiOutputFormater())


if __name__ == '__main__':
    unittest.main()
