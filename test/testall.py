from unittest import TestLoader, TextTestRunner, TestSuite 

from testrequester import TestRequester

if __name__ == "__main__":
    loader = TestLoader() 
    suite = TestSuite((loader.loadTestsFromTestCase(TestRequester),
                       ))
    runner = TextTestRunner(verbosity = 2) 
    runner.run(suite)