'''
This test suite (named allcl for Command Line) runs on QPython 3, but not on Pydroid 3
since it has a dependency on the sl4a library which are not supported by Pydroid 3.
It has no dependency on Kivy ressources, supported by Pydroid 3, but not by QPython 3.
It can be executed in Pycharm on pc !
'''
from unittest import TestLoader, TextTestRunner, TestSuite

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand
from testabstractoutputformater import TestAbstractOutputFormater
from testcommandquit import TestCommandQuit
from testcommanderror import TestCommandError
from testcontroller import TestController
from testconfigurationmanager import TestConfigurationManager
from testpricerequester import TestPriceRequester
from testdatetimeutil import TestDateTimeUtil
from testcrypcompexchanges import TestCrypCompExchanges
from testprocessor import TestProcessor
from testcommandprice import TestCommandPrice
from testresultdata import TestResultData
from testcurrencypairtester import TestCurrencyPairTester
from testconsoleoutputformatter import TestConsoleOutputFormatter


if __name__ == "__main__":
    '''
    This test suite runs on Android in QPython, but fails in Pydroid !
    '''
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand),
                       loader.loadTestsFromTestCase(TestAbstractOutputFormater),
                       loader.loadTestsFromTestCase(TestCommandQuit),
                       loader.loadTestsFromTestCase(TestCommandError),
                       loader.loadTestsFromTestCase(TestController),
                       loader.loadTestsFromTestCase(TestConfigurationManager),
                       loader.loadTestsFromTestCase(TestDateTimeUtil),
                       loader.loadTestsFromTestCase(TestPriceRequester),
                       loader.loadTestsFromTestCase(TestCrypCompExchanges),
                       loader.loadTestsFromTestCase(TestProcessor),
                       loader.loadTestsFromTestCase(TestCommandPrice),
                       loader.loadTestsFromTestCase(TestResultData),
                       loader.loadTestsFromTestCase(TestCurrencyPairTester),
                       loader.loadTestsFromTestCase(TestConsoleOutputFormatter)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)