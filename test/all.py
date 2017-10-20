from unittest import TestLoader, TextTestRunner, TestSuite 

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand
from testcommandquit import TestCommandQuit
from testcommanderror import TestCommandError
from testcontroller import TestController
from testconfigurationmanager import TestConfigurationManager
from testpricerequester import TestPriceRequester
from testdatetimeutil import TestDateTimeUtil
from testcrypcompexchanges import TestCrypCompExchanges


if __name__ == "__main__":
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand),
                       loader.loadTestsFromTestCase(TestCommandQuit),
                       loader.loadTestsFromTestCase(TestCommandError),
                       loader.loadTestsFromTestCase(TestController),
                       loader.loadTestsFromTestCase(TestConfigurationManager),
                       loader.loadTestsFromTestCase(TestDateTimeUtil),
                       loader.loadTestsFromTestCase(TestPriceRequester),
                       loader.loadTestsFromTestCase(TestCrypCompExchanges)
    ))
    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)