from unittest import TestLoader, TextTestRunner, TestSuite 

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand
from testabstractprinter import TestAbstractPrinter
from testcommandquit import TestCommandQuit
from testcommanderror import TestCommandError
from testcontrollergui import TestControllerGui
from testconfigurationmanager import TestConfigurationManager
from testpricerequester import TestPriceRequester
from testdatetimeutil import TestDateTimeUtil
from testcrypcompexchanges import TestCrypCompExchanges
from testprocessor import TestProcessor
from testcommandprice import TestCommandPrice
from testresultdata import TestResultData
from testcurrencypairtester import TestCurrencyPairTester
from testguiprinter import TestGuiPrinter


if __name__ == "__main__":
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand),
                       loader.loadTestsFromTestCase(TestAbstractPrinter),
                       loader.loadTestsFromTestCase(TestCommandQuit),
                       loader.loadTestsFromTestCase(TestCommandError),
                       loader.loadTestsFromTestCase(TestControllerGui),
                       loader.loadTestsFromTestCase(TestConfigurationManager),
                       loader.loadTestsFromTestCase(TestDateTimeUtil),
                       loader.loadTestsFromTestCase(TestPriceRequester),
                       loader.loadTestsFromTestCase(TestCrypCompExchanges),
                       loader.loadTestsFromTestCase(TestProcessor),
                       loader.loadTestsFromTestCase(TestCommandPrice),
                       loader.loadTestsFromTestCase(TestResultData),
                       loader.loadTestsFromTestCase(TestCurrencyPairTester),
                       loader.loadTestsFromTestCase(TestGuiPrinter)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
