from unittest import TestLoader, TextTestRunner, TestSuite 

from testrequester import TestRequester
from testabstractcommand import TestAbstractCommand

if __name__ == "__main__":
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       loader.loadTestsFromTestCase(TestAbstractCommand)
                       ))
    runner = TextTestRunner(verbosity = 2) 
    runner.run(suite)