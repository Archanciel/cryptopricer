from unittest import TestLoader, TextTestRunner, TestSuite 

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand
from testcommandquit import TestCommandQuit
from testcommanderror import TestCommandError

if __name__ == "__main__":
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand),
                       loader.loadTestsFromTestCase(TestCommandQuit),
                       loader.loadTestsFromTestCase(TestCommandError)
                      ))
    runner = TextTestRunner(verbosity = 2) 
    runner.run(suite)