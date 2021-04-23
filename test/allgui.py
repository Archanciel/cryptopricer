'''
This test suite runs on Pydroid 3, but not on QPython 3 since it has a dependency on
Kivy resources which are not supported by QPython 3. It has no dependency on the sl4a
library, supported by QPython 3, but not by Pydroid 3. It can be executed in Pycharm on
pc !
'''

from unittest import TestLoader, TextTestRunner, TestSuite

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand
from testabstractoutputformater import TestAbstractOutputFormater
from testcommandquit import TestCommandQuit
from testcommanderror import TestCommandError
from testcontrollergui import TestControllerGui
from testcontrollerguiNew import TestControllerGuiNew
from testconfigurationmanager import TestConfigurationManager
from testpricerequester import TestPriceRequester
from testdatetimeutil import TestDateTimeUtil
from testcrypcompexchanges import TestCrypCompExchanges
from testprocessor import TestProcessor
from testcommandprice import TestCommandPrice
from testresultdata import TestResultData
from testcurrencypairtester import TestCurrencyPairTester
from testhelputil import TestHelpUtil
from testguioutputformatter import TestGuiOutputFormatter


if __name__ == "__main__":
    '''
    This test suite runs on Android in Pydroid, but fails in QPython !
    '''
    loader = TestLoader()
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand),
                       loader.loadTestsFromTestCase(TestAbstractOutputFormater),
                       loader.loadTestsFromTestCase(TestCommandQuit),
                       loader.loadTestsFromTestCase(TestCommandError),
                       loader.loadTestsFromTestCase(TestControllerGui),
                       loader.loadTestsFromTestCase(TestControllerGuiNew),
                       loader.loadTestsFromTestCase(TestConfigurationManager),
                       loader.loadTestsFromTestCase(TestDateTimeUtil),
                       loader.loadTestsFromTestCase(TestPriceRequester),
                       loader.loadTestsFromTestCase(TestCrypCompExchanges),
                       loader.loadTestsFromTestCase(TestProcessor),
                       loader.loadTestsFromTestCase(TestCommandPrice),
                       loader.loadTestsFromTestCase(TestResultData),
                       loader.loadTestsFromTestCase(TestCurrencyPairTester),
                       loader.loadTestsFromTestCase(TestHelpUtil),
                       loader.loadTestsFromTestCase(TestGuiOutputFormatter)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
