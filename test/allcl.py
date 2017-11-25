from unittest import TestLoader, TextTestRunner, TestSuite 

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand
from testabstractprinter import TestAbstractPrinter
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
from testcommandlineprinter import TestCommandLinePrinter


if __name__ == "__main__":
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand),
                       loader.loadTestsFromTestCase(TestAbstractPrinter),
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
                       loader.loadTestsFromTestCase(TestCommandLinePrinter)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)