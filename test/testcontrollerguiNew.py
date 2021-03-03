import unittest
import os,sys,inspect

LOCAL_TIME_ZONE = 'Europe/Zurich'

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
							  # the test is executed standalone

import re
from controller import Controller
from datetimeutil import DateTimeUtil
from gui.guioutputformatter import GuiOutputFormatter
from configurationmanager import ConfigurationManager
from pricerequesterteststub import PriceRequesterTestStub
from utilityfortest import UtilityForTest


class TestControllerGuiNew(unittest.TestCase):
	'''
	New version of TestControllerGui since the original version already contains a lot of
	tests.

	Test the Controller using a GuiOuputFormater in place of a ConsoleOutputFormaater
	since GuiOuputFormatter runs on Android in Pydroid, but fails in QPython !

	All the test cases are defined in the TestController parent to avoid code duplication
	'''
	def setUp(self):
		if os.name == 'posix':
			FILE_PATH = '/sdcard/cryptopricer.ini'
		else:
			FILE_PATH = 'c:\\temp\\cryptopricer.ini'

		configMgr = ConfigurationManager(FILE_PATH)
		self.controller = Controller(GuiOutputFormatter(configMgr), configMgr, PriceRequesterTestStub())

	def testScenarioHistoDayFullThenPartialRequestsOptionFiatNoSave(self):
		'''
		This test verifies that the partial request fiat option remains active until new full
		request or option cancelling.
		'''
		# first entry: full request
		inputStr = 'chsb btc 20/12/20 hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# next entry: partial request option fiat no save
		inputStr = '-fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC/USD.Kraken on HitBTC: 20/12/20 00:00C 0.00001061 0.24913023', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fusd.kraken\n(0.00001061 CHSB/BTC * 23480.7 BTC/USD = 0.24913023 CHSB/USD)', fullCommandStrForStatusBar)

		# next  entry: partial request unit change
		inputStr = '-ueth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/ETH/USD.Kraken on HitBTC: 20/12/20 00:00C 0.0003938 0.25135466', printResult)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fusd.kraken\n(0.0003938 CHSB/ETH * 638.28 ETH/USD = 0.25135466 CHSB/USD)', fullCommandStrForStatusBar)

		# next entry: full request to cancel -f option
		inputStr = 'chsb btc 20/12/20 hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# next entry: again partial request option fiat no save
		inputStr = '-fusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC/USD.Kraken on HitBTC: 20/12/20 00:00C 0.00001061 0.24913023', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fusd.kraken', fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fusd.kraken\n(0.00001061 CHSB/BTC * 23480.7 BTC/USD = 0.24913023 CHSB/USD)', fullCommandStrForStatusBar)

		# next entry: partial request to remove option fiat no save
		inputStr = '-f0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

	def testScenarioHistoDayFullThenPartialRequestsOptionFiatSave(self):
		'''
		This test verifies that the partial request fiat option remains active until new full
		request or option cancelling.
		'''
		# first entry: full request
		inputStr = 'chsb btc 20/12/20 hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# next entry: partial request option fiat save
		inputStr = '-fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC/USD.Kraken on HitBTC: 20/12/20 00:00C 0.00001061 0.24913023', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken\n(0.00001061 CHSB/BTC * 23480.7 BTC/USD = 0.24913023 CHSB/USD)', fullCommandStrForStatusBar)
		
		# next  entry: partial request unit change
		inputStr = '-ueth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/ETH/USD.Kraken on HitBTC: 20/12/20 00:00C 0.0003938 0.25135466', printResult)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fsusd.kraken\n(0.0003938 CHSB/ETH * 638.28 ETH/USD = 0.25135466 CHSB/USD)', fullCommandStrForStatusBar)

		# next entry: full request to cancel -f option
		inputStr = 'chsb btc 20/12/20 hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)

		# next entry: again partial request option fiat save
		inputStr = '-fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC/USD.Kraken on HitBTC: 20/12/20 00:00C 0.00001061 0.24913023', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken\n(0.00001061 CHSB/BTC * 23480.7 BTC/USD = 0.24913023 CHSB/USD)', fullCommandStrForStatusBar)

		# next entry: partial request to remove option fiat save
		inputStr = '-f0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)
	
	def testScenarioHistoDayFullThenPartialRequestsOptionValueOptionFiatSave(self):
		'''
		This test verifies that the partial request fiat option remains active until new full
		request or option cancelling.
		'''
		# first entry: full request
		inputStr = 'chsb btc 20/12/20 hitbtc'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC on HitBTC: 20/12/20 00:00C 0.00001061', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual(None, fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(None, fullCommandStrForStatusBar)
		
		# next entry: partial request option fiat save
		inputStr = '-fsusd.kraken'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/BTC/USD.Kraken on HitBTC: 20/12/20 00:00C 0.00001061 0.24913023', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(
			'chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken\n(0.00001061 CHSB/BTC * 23480.7 BTC/USD = 0.24913023 CHSB/USD)',
			fullCommandStrForStatusBar)
		
		# next entry: partial request option value no save
		inputStr = '-v1000usd'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'4013.96495336 CHSB/0.04258817 BTC/1000 USD.Kraken on HitBTC: 20/12/20 00:00C 0.00001061 0.24913023', printResult)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -v1000usd', fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb btc 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(
			'chsb btc 20/12/20 00:00 hitbtc -v1000usd -fsusd.kraken\n(0.00001061 CHSB/BTC * 23480.7 BTC/USD = 0.24913023 CHSB/USD)',
			fullCommandStrForStatusBar)
		
		# next  entry: partial request unit change
		inputStr = '-ueth'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'3978.44219035 CHSB/1.56671053 ETH/1000 USD.Kraken on HitBTC: 20/12/20 00:00C 0.0003938 0.25135466', printResult)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -v1000usd', fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual(
			'chsb eth 20/12/20 00:00 hitbtc -v1000usd -fsusd.kraken\n(0.0003938 CHSB/ETH * 638.28 ETH/USD = 0.25135466 CHSB/USD)',
			fullCommandStrForStatusBar)

		# next entry: partial request to remove option value no save
		inputStr = '-v0'
		printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar = self.controller.getPrintableResultForInput(
			inputStr)
		self.assertEqual(
			'CHSB/ETH/USD.Kraken on HitBTC: 20/12/20 00:00C 0.0003938 0.25135466', printResult)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc', fullCommandStrNoOptions)
		self.assertEqual(None, fullCommandStrWithNoSaveOptions)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fsusd.kraken', fullCommandStrWithSaveOptionsForHistoryList)
		self.assertEqual('chsb eth 20/12/20 00:00 hitbtc -fsusd.kraken\n(0.0003938 CHSB/ETH * 638.28 ETH/USD = 0.25135466 CHSB/USD)', fullCommandStrForStatusBar)


if __name__ == '__main__':
#	unittest.main()
	tst = TestControllerGui()
	tst.setUp()
	tst.testGetPrintableResultForDayOnlyAndTimeFullRequestOn31st()
	tst.setUp()
	tst.testGetPrintableResultForUnsupportedPartialRequestOptionSaveAfterValidRealTimeRequest()
	tst.setUp()
	tst.testOptionValueOptionFiatFullRequestHistoDayPrice()
	tst.setUp()
	tst.testOptionValueOptionFiatFullRequestHistoDayPriceRequiredParmsOrderChanged()
	tst.testOptionValueOptionFiatFullRequestHistoDayPriceMandatoryParmsAndOptionOrderChanged()
	tst.setUp()
	tst.testGetPrintableResultForDayOnlyAndTimeFullRequestOn31st()
	tst.setUp()
	tst.testGetPrintableResultFullRequestNoDateNoTime()
	tst.setUp()
	tst.testOptionValueOptionFiatOptionPriceFullRequestHistoDayPrice()
