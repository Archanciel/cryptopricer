import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requester import Requester
from configurationmanager import ConfigurationManager
from commandprice import CommandPrice
from commandcrypto import CommandCrypto
from commandquit import CommandQuit
from commanderror import CommandError
from resultdata import ResultData


class TestRequester(unittest.TestCase):
	'''
	-teste input crypto + unit avec ou sans
	nosave ou ns
	
	-teste input crypto avec 0 price/oate,
	1 price/date, n price/date
	
	-idem 0, 1, n units
	
	-varie order crypto list/unit list/
	nosave command
	'''
	def setUp(self):
		if os.name == 'posix':
			FILE_PATH = '/sdcard/cryptopricer.ini'
		else:
			FILE_PATH = 'c:\\temp\\cryptopricer.ini'

		configMgr = ConfigurationManager(FILE_PATH)

		requester = Requester(configMgr)
		self.commandPrice = CommandPrice(None)
		requester.commandPrice = self.commandPrice
		requester.commandCrypto = CommandCrypto(None)
		requester.commandQuit = CommandQuit(sys)
		self.commandError = CommandError(None)
		requester.commandError = self.commandError
		self.requester = requester


	def test_parseUnitTwoUnitsNoUnitSep(self):
		inputStr = "[usd chf]"
		unitList = self.requester._parseUnit(inputStr.upper())
		self.assertEqual(unitList, ['CHF'])


	def test_parseUnitTwoUnits(self):
		inputStr = "[usd-chf]"
		unitList = self.requester._parseUnit(inputStr.upper())
		self.assertEqual(unitList, ['USD', 'CHF'])


	def test_parseUnitEmptyUnitList(self):
		inputStr = "[]"
		unitList = self.requester._parseUnit(inputStr.upper())
		self.assertEqual(unitList, [])


	def test_parseUnitOneUnit(self):
		inputStr = "[usd]"
		unitList = self.requester._parseUnit(inputStr.upper())
		self.assertEqual(unitList, ['USD'])


	def test_parseUnitThreeUnits(self):
		inputStr = "[usd-chf-eur]"
		unitList = self.requester._parseUnit(inputStr.upper())
		self.assertEqual(unitList, ['USD', 'CHF', 'EUR'])


	def test_parseUnitNoUnitList(self):
		inputStr = ""
		unitList = self.requester._parseUnit(inputStr.upper())
		self.assertEqual(unitList, [])


	def test_getUserCommandCommandMissingOtherCommand(self):
		inputStr = "[btc 05/07 0.0015899] [usd-chf] -nosave"
		cryptoData = self.requester.getCommand(inputStr)
		self.assertEqual(cryptoData, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid request [btc 05/07 0.0015899] [usd-chf] -nosave: user command missing.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def testGetCommandInvalidC(self):
		# valid full request so that next invalid partial request does not cause
		# a "ERROR - no full request executed before partial request -c. Partial
		# request ignored" error msg
		inputStr = "eth btc 0 all"
		self.requester.getCommand(inputStr)
		
		# invalid partial request
		inputStr = "-c"
		cryptoData = self.requester.getCommand(inputStr)
		self.assertEqual(cryptoData, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid partial request -c: -c with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def testGetCommandInvalidF(self):
		# valid full request so that next invalid partial request does not cause
		# a "ERROR - no full request executed before partial request -c. Partial
		# request ignored" error msg
		inputStr = "eth btc 0 all"
		self.requester.getCommand(inputStr)
		
		# invalid partial request
		inputStr = "-u"
		cryptoData = self.requester.getCommand(inputStr)
		self.assertEqual(cryptoData, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid partial request -u: -u with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def testGetCommandInvalidD(self):
		# valid full request so that next invalid partial request does not cause
		# a "ERROR - no full request executed before partial request -c. Partial
		# request ignored" error msg
		inputStr = "eth btc 0 all"
		self.requester.getCommand(inputStr)
		
		# invalid partial request
		inputStr = "-d"
		cryptoData = self.requester.getCommand(inputStr)
		self.assertEqual(cryptoData, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid partial request -d: -d with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def testGetCommandInvalidT(self):
		# valid full request so that next invalid partial request does not cause
		# a "ERROR - no full request executed before partial request -c. Partial
		# request ignored" error msg
		inputStr = "eth btc 0 all"
		self.requester.getCommand(inputStr)
		
		# invalid partial request
		inputStr = "-t"
		cryptoData = self.requester.getCommand(inputStr)
		self.assertEqual(cryptoData, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid partial request -t: -t with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def testGetCommandInvalidE(self):
		# valid full request so that next invalid partial request does not cause
		# a "ERROR - no full request executed before partial request -c. Partial
		# request ignored" error msg
		inputStr = "eth btc 0 all"
		self.requester.getCommand(inputStr)
		
		# invalid partial request
		inputStr = "-e"
		cryptoData = self.requester.getCommand(inputStr)
		self.assertEqual(cryptoData, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid partial request -e: -e with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def test_parseDatePriceTwoPairs(self):
		inputStr = "[5/7 0.0015899 6/7 0.00153]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, ['5/7', '0.0015899', '6/7', '0.00153'])


	def test_parseDatePriceOnePair(self):
		inputStr = "[5/7 0.0015899]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, ['5/7', '0.0015899'])


	def test_parseDatePriceOnePriceOnlyNoDateNoOtherCommand(self):
		inputStr = "[btc 0.0015899] [usd-chf]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, [])


	def test_parseDatePriceOnePriceNoDateOtherCommand(self):
		inputStr = "[0.0015899]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, [])


	def test_parseDatePriceOneDateMissing(self):
		inputStr = "[0.0015899 6/7 0.00153]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, ['6/7', '0.00153'])


	def test_parseDatePriceOnePriceMissing(self):
		inputStr = "[5/7 6/7 0.00153]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, ['6/7', '0.00153'])


	def test_parseDatePriceOnePriceTwoDigitsDateOnlyOtherCommand(self):
		inputStr = "[15/12 0.0015899]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, ['15/12', '0.0015899'])


	def test_parseDatePriceOnePriceTwoDigitsWithZeroeDate(self):
		inputStr = "[05/02 0.0015899]"
		datePriceList = self.requester._parseDatePrice(inputStr.upper())
		self.assertEqual(datePriceList, ['05/02', '0.0015899'])


	def test_parseOOCommandParmsUnitListMissingNoOtherCommand(self):
		inputStr = "btc [5/7 0.0015899 6/7 0.00153]"
		cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
		self.assertEqual(cryptoDataList, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid request : unit list missing.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def test_parseOOCommandParmsUnitListMissingWithOtherCommand(self):
		inputStr = "btc [5/7 0.0015899 6/7 0.00153] -nosave"
		cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
		self.assertEqual(cryptoDataList, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid request : unit list missing.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


	def test_parseOOCommandParms(self):
		inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
		cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
		self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(unitDataList, ['USD', 'CHF'])
		self.assertEqual(flag, '-NOSAVE')


	def test_parseOOCommandParmsNoOtherCommand(self):
		inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf]"
		cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
		self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(unitDataList, ['USD', 'CHF'])
		self.assertEqual(flag, None)


	def test_parseOOCommandParmsEmptyUnitListNoOtherCommand(self):
		inputStr = "btc [5/7 0.0015899 6/7 0.00153] []"
		cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
		self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(unitDataList, [])
		self.assertEqual(flag, None)


	def testGetCommand(self):
		inputStr = "oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
		cryptoCommand = self.requester.getCommand(inputStr)

		self.assertIsInstance(cryptoCommand, CommandCrypto)
		parsedParmData = cryptoCommand.parsedParmData
		self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], ['USD', 'CHF'])
		self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')


	def testRequestOOCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave")
		cryptoCommand = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(cryptoCommand, CommandCrypto)
		parsedParmData = cryptoCommand.parsedParmData
		self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], ['USD', 'CHF'])
		self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')

		sys.stdin = stdin


	def testRequestOOCommandNoFlag(self):
		stdin = sys.stdin
		sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf]")
		cryptoCommand = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(cryptoCommand, CommandCrypto)
		parsedParmData = cryptoCommand.parsedParmData
		self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], ['USD', 'CHF'])
		self.assertEqual(parsedParmData[cryptoCommand.FLAG], None)

		sys.stdin = stdin


	def testRequestOOCommandEmptyUnit(self):
		stdin = sys.stdin
		sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [] -nosave")
		cryptoCommand = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(cryptoCommand, CommandCrypto)
		parsedParmData = cryptoCommand.parsedParmData
		self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
		self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], [])
		self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')

		sys.stdin = stdin


	def testRequestOOCommandNoUnit(self):
		stdin = sys.stdin
		sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] -nosave")
		command = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(command, CommandError)

		sys.stdin = stdin


	def testRequestUserCommandNoCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc [5/7 0.0015899 6/7 0.00153] -nosave")
		command = self.requester.getCommandFromCommandLine()

		#now that you changed command price full pattern to render all parms except the first one optional,
		#this input is interpreted as a CommandPrice
		self.assertIsInstance(command, CommandPrice)

		sys.stdin = stdin


	def test_parseGroupsFullDayMonthHHMM(self):
		inputStr = "btc usd 10/9 12:45 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken', None, None, None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMValueOption(self):
		inputStr = "btc usd 10/9 12:45 Kraken -v100usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken', '-v100usd', None, None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMValueOptionIncomplete(self):
		inputStr = "btc usd 10/9 12:45 Kraken -v100"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken', '-v100', None, None, None), groupList)

	def test_parseGroupsFullExchangeFirst(self):
		inputStr = "btc usd Kraken 10/9/17 12:45"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', 'Kraken', '10/9/17', '12:45', None, None, None, None), groupList)


	def test_parseGroupsFullDayMonthYearHMM(self):
		inputStr = "btc usd 10/9/2017 1:45 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '10/9/2017', '1:45', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDayMonthZeroYearHMM(self):
		inputStr = "btc usd 10/9/0 1:45 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '10/9/0', '1:45', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDH(self):
		inputStr = "btc usd 1 2 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '1', '2', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDDDMH(self):
		inputStr = "btc usd 111/9 2 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '111/9', '2', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDMH(self):
		inputStr = "btc usd 1/9 2 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '1/9', '2', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDayHH(self):
		inputStr = "btc usd 10 12 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '10', '12', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDMYearHMM(self):
		inputStr = "btc usd 1/2/17 1:25 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', 'usd', '1/2/17', '1:25', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDHH(self):
		inputStr = "btc usd 1 12 Kraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', 'usd', '1', '12', 'Kraken', None, None, None, None), groupList)


	def test_parseGroupsFullDMHHMMNoExchange(self):
		inputStr = "btc usd 1/9 12:05"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', 'usd', '1/9', '12:05', None, None, None, None, None), groupList)


	def test_parseGroupsFullNoUnitDMHHMMNoExchange(self):
		inputStr = "btc 1/9 12:05"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', '1/9', '12:05', None, None, None, None, None, None), groupList)


	def test_parseGroupsFullNoUnitDHHMMNoExchange(self):
		inputStr = "btc 1 12:05"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', '1', '12:05', None, None, None, None, None, None), groupList)


	def test_parseGroupsFullNoUnitNoDMHHMMNoExchange(self):
		inputStr = "btc 12:05"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', '12:05', None, None, None, None, None, None, None), groupList)


	def test_parseGroupsFullNoUnitDMNoTimeNoExchange(self):
		inputStr = "btc 1/9"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', '1/9', None, None, None, None, None, None, None), groupList)


	def test_parseGroupsFullNoUnitNoDateNoTimeNoExchange(self):
		inputStr = "btc"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
		self.assertEqual(('btc', None, None, None, None, None, None, None, None), groupList)

	def test_parseGroupsFullVariousResultOptions(self):
		'''
btc usd 12/2/21 13:55 hitbtc
btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -ps52012.45 -r-2:-3
btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs -ps52012.45
btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1-2-3
btc usd 12/2/21 13:55 hitbtc -ps52012.45 -vs21.23btc -fschf.kraken -rs-1:-3
btc usd 12/2/21 13:55 hitbtc -vs21.23btc -rs-1:-3 -fschf.kraken
btc usd 12/2/21 13:55 hitbtc -rs-1:-3 -vs21.23btc -ps52012.45 -fschf.kraken
btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1
btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -r
		
		:return:
		'''
		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -ps52012.45 -r-2:-3'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-fschf.kraken', '-ps52012.45', '-r-2:-3'), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs -ps52012.45'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-fschf.kraken', '-rs', '-ps52012.45'), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1-2-3'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-fschf.kraken', '-rs-1-2-3', None), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -ps52012.45 -vs21.23btc -fschf.kraken -rs-1:-3'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-ps52012.45', '-vs21.23btc', '-fschf.kraken', '-rs-1:-3'), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1:-3'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-fschf.kraken', '-rs-1:-3', None), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -rs-1:-3 -fschf.kraken'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-rs-1:-3', '-fschf.kraken', None), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -rs-1:-3 -vs21.23btc -ps52012.45 -fschf.kraken'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-rs-1:-3', '-vs21.23btc', '-ps52012.45', '-fschf.kraken'), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-fschf.kraken', '-rs-1', None), groupList)

		inputStr = 'btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -r'
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'usd', '12/2/21', '13:55', 'hitbtc', '-vs21.23btc', '-fschf.kraken', '-r', None), groupList)

	def test_buildFullCommandPriceOptionalParmsDic(self):
		'''
		° 0 is legal for date, not for time parms. Zero for either date means now, real time !
		° Date must be 0 or contain a '/'.
		° Time must be composed of two numerical groups separated by ':', the second group being a
		° 2 digits group. Note 00:00 or 0:00 does not mean now, but midnight !
		° Exchange name must start with a letter. May contain digits.

		Ex:
		Date can be 0, accepted. 1, rejected. 10, rejected. 01, rejected. 01/1, accepted.
					01/10, accepted. 1/1, accepted. 1/10, accepted. 01/12/16, accepted.
					01/12/2015, accepted.
		Hour minute can be 0, rejected. 1, rejected. 10, rejected. 01, rejected. 01:1, rejected.
						   01:01, accepted.
						   01:10, accepted. 1:10, accepted. 00:00, accepted. 0:00, accepted. 0:0, rejected.
		 '''
		optionalParmList = ['01:10', 'Kraken', '10/9/17']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10/9/17')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '01:10')
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'Kraken')

		optionalParmList = ['1', 'kraken', '10/9/2017']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

		optionalParmList = ['1', 'kraken', '1']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

		optionalParmList = ['kraken', '0', '10:12']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '10:12')
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

		optionalParmList = ['kraken', '0', '1']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

		optionalParmList = [ '1', 'kraken', '0']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

		optionalParmList = ['10', '10:09']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '10:09')

		optionalParmList = ['01', '1:09']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '01')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '1:09')

		optionalParmList = ['01/1', '00:00']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '01/1')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '00:00')

		optionalParmList = ['1/1', '00:00']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/1')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '00:00')

		optionalParmList = ['1/10', '0:00']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/10')
		self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '0:00')

		optionalParmList = ['1/10', '0:0']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/10')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)

	def test_buildFullCommandPriceOptionalParmsDicExoticExchangeName(self):
		optionalParmList = [ '1', 'BTC38', '0']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'BTC38')

		optionalParmList = ['1', 'Bit2C', '0']
		optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
		self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
		self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
		self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'Bit2C')

	def test_parseGroupsPartialDDZeroMonth(self):
		inputStr = "-ceth -ugbp -d11/0 -t22:46 -ekraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialDayZeroMonth(self):
		inputStr = "-ceth -ugbp -d1/0 -t22:46 -ekraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialZeroDayZeroMonth(self):
		inputStr = "-ceth -ugbp -d0/0 -t22:46 -ekraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '0/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialDayMonthHHMM(self):
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -ekraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDayMonthYearHMM(self):
		inputStr = "-ceth -ugbp -d11/8/17 -t2:46 -ekraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8/17', '-t', '2:46', '-e', 'kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDayMonthYearHHMM(self):
		inputStr = "-ceth -ugbp -d11/8/17 -t12:46 -ebtc38 -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8/17', '-t', '12:46', '-e', 'btc38', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDayMonthZeroYearHHMM(self):
		inputStr = "-ceth -ugbp -d11/8/0 -t12:46 -ebtc38 -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8/0', '-t', '12:46', '-e', 'btc38', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDH(self):
		inputStr = "-ceth -ugbp -d1 -t2 -ekraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1', '-t', '2', '-e', 'kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDHH(self):
		inputStr = "-ceth -ugbp -d1 -t2:5 -ebit2c -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1', '-t', '2:5', '-e', 'bit2c', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDayHH(self):
		inputStr = "-ceth -ugbp -d11 -t22 -eKraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11', '-t', '22', '-e', 'Kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDMHH(self):
		inputStr = "-ceth -ugbp -d1/2 -t22 -eKraken -v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1/2', '-t', '22', '-e', 'Kraken', '-v', '700usd', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDDDMHHValue(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -v0.0044235btc"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-v', '0.0044235btc', None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDDDMHHNoValue(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDayMonthHHMMNoExchangeNoValue(self):
		inputStr = "-ceth -ugbp -d11/8 -t22:46"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8', '-t', '22:46', None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialDayMonthNoTimeNoExchangeNoValue(self):
		inputStr = "-ceth -ugbp -d11/8"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialNoDateNoTimeNoExchangeNoValue(self):
		inputStr = "-ceth -ugbp"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialNoUnitNoDateNoTimeNoExchangeNoValue(self):
		inputStr = "-ceth"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialNoCryptoNoDateNoTimeNoExchangeNoValue(self):
		inputStr = "-ugbp"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-u', 'gbp', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialValueFloatNoCryptoNoUnitNoDateNoTimeNoExchange(self):
		inputStr = "-v700.05usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-v', '700.05usd', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialValueIntNoCryptoNoUnitNoDateNoTimeNoExchange(self):
		inputStr = "-v700usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-v', '700usd', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


	def test_parseGroupsPartialNoCryptoNoDateNoExchangeNoValue(self):
		inputStr = "-ugbp -t3:45"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-u', 'gbp', '-t', '3:45', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)

# result groups
	
	def test_parseGroupsPartialVariousResultOptions(self):
		inputStr = '-ceth -ueur -vs34usd -fschf -ebittrex -d1 -t12:45 -rs32.45 -ebittrex -p23usd.kraken'
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'eur', '-v', 's34usd', '-f', 'schf', '-e', 'bittrex', '-d', '1', '-t', '12:45', '-r', 's32.45', '-e', 'bittrex', '-p', '23usd.kraken'), groupList)

		inputStr = '-ceth -ueur -vs34usd -fschf -ebittrex -d1 -t12:45 -rs -ebittrex -p23usd.kraken'
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'eur', '-v', 's34usd', '-f', 'schf', '-e', 'bittrex', '-d', '1', '-t', '12:45', '-r', 's', '-e', 'bittrex', '-p', '23usd.kraken'), groupList)

		inputStr = '-ceth -ueur -vs34usd -fschf -ebittrex -d1 -t12:45 -rs-1 -ebittrex -p23usd.kraken'
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'eur', '-v', 's34usd', '-f', 'schf', '-e', 'bittrex', '-d', '1', '-t', '12:45', '-r', 's-1', '-e', 'bittrex', '-p', '23usd.kraken'), groupList)

		inputStr = '-ceth -ueur -vs34usd -fschf -ebittrex -d1 -t12:45 -rs-1-2-3 -ebittrex -p23usd.kraken'
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'eur', '-v', 's34usd', '-f', 'schf', '-e', 'bittrex', '-d', '1', '-t', '12:45', '-r', 's-1-2-3', '-e', 'bittrex', '-p', '23usd.kraken'), groupList)

		inputStr = '-ceth -ueur -vs34usd -fschf -ebittrex -d1 -t12:45 -ebittrex -p23usd.kraken -rs-1:-3'
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'eur', '-v', 's34usd', '-f', 'schf', '-e', 'bittrex', '-d', '1', '-t', '12:45', '-e', 'bittrex', '-p', '23usd.kraken', '-r', 's-1:-3'), groupList)

		inputStr = '-rs-1:-3 -ceth -ueur -vs34usd -fschf -ebittrex -d1 -t12:45 -ebittrex'
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-r', 's-1:-3', '-c', 'eth', '-u', 'eur', '-v', 's34usd', '-f', 'schf', '-e', 'bittrex', '-d', '1', '-t', '12:45', '-e', 'bittrex', None, None), groupList)


	def test_parseAndFillFullCommandPrice(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceWithVariousOptions(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -vs2btc -fschf.kraken -rs"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10',parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('2', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('chf', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillFullCommandPriceInvalDate1(self):
		inputStr = "btc usd 1 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceInvalDate2(self):
		inputStr = "btc usd 10 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceInvalDate3(self):
		inputStr = "btc usd 01 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceInvalMonthAccepted(self):
		inputStr = "btc usd 01/0 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceInvalDayAccepted(self):
		inputStr = "btc usd 0/0 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceValidDate1(self):
		inputStr = "btc usd 01/1 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '1')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceValidDate2(self):
		inputStr = "btc usd 1/01 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '01')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceValidDate3(self):
		inputStr = "btc usd 1/1 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '1')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceValidDate4(self):
		inputStr = "btc usd 1/10 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '10')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceValidDate5(self):
		inputStr = "btc usd 01/10 12:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '10')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDate(self):
		#means current date !
		inputStr = "btc usd 0 2:45 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '2')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime1(self):
		#means current date !
		inputStr = "btc usd 0 2:4 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime2(self):
		#means current date !
		inputStr = "btc usd 0 2: Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime3(self):
		#means current date !
		inputStr = "btc usd 0 20 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime4(self):
		#means current date !
		inputStr = "btc usd 0 2 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime5(self):
		#means current date !
		inputStr = "btc usd 0 01 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime6(self):
		#means current date !
		inputStr = "btc usd 0 10 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime7(self):
		inputStr = "btc usd 10/9/2017 01:1 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateInvalidTime8(self):
		inputStr = "btc usd 10/9/2017 0:0 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateValidTime1(self):
		inputStr = "btc usd 10/9/2017 00:00 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '00')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '00')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateValidTime2(self):
		inputStr = "btc usd 10/9/2017 0:00 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '00')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceDateBeforeZeroTime(self):
		inputStr = "btc usd 10/9/17 0 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroTimeBeforeDate(self):
		#zero time is rejected. Instead, it is interrpreted as date == 0
		#means current date !
		inputStr = "btc usd 0 10/9/17 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceZeroDateZeroTime(self):
		#first zero means current date. Second zero for 0 time is not acceptable for time !
		inputStr = "btc usd 0 0 Kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceExchangeBeforeDateTime(self):
		inputStr = "btc usd Kraken 10/9/17 12:45"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceNoYearTimeBeforeDate(self):
		inputStr = "btc usd Kraken 12:45 10/9"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceNoYearNoExchange(self):
		inputStr = "btc usd 10/9 12:45"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceNoTimeNoYearNoExchange(self):
		inputStr = "btc usd 10/9"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceNoDateNoTimeNoExchange(self):
		inputStr = "btc usd"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], None)
		self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


	def test_parseAndFillFullCommandPriceNoUnitNoDateNoTimeNoExchange(self):
		inputStr = "btc"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY], None)
		self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

	def test_parseAndFillPartialCommandPriceWithInitYearWithPartialYear(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '17'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8/16 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceWithInitYearNoPartialYear(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '15'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceWithInitYearWithPartialDateDayOnly(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '17'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearNoExchange(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearNoExchangeNoTime(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearNoExchangeNoMinute(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t5"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : in -t5, 5 must respect HH:mm format.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceNoInitYearNoMinuteInvalidTime(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ebittrex -t6.45 -d21/12"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : in -t6.45, 6.45 must respect HH:mm format.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceWithInitYear(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceWrongCommand(self):
		commandError = self.requester.commandPrice

		parsedParmData = commandError.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -h22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_OPTION], '-h')
		self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA], '22:46')
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceCommandNoHiphen(self):
		commandError = self.requester.commandPrice

		parsedParmData = commandError.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_DATA] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = None
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = None

		inputStr = "-ceth fgbp -d11/8 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def testCommandPriceFullRequest(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestDateZero(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 0 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin


	def testCommandPriceFullRequestDateBeforeTimeZero(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/2017 0 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin


	def testCommandPriceFullRequestTimeZeroBeforeDate(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 0 10/9/2017 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin


	def testCommandPriceFullRequestDateZeroTimeZero(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 0 0 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestDateZeroNoTime(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 0 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testRequestCommandPricePartialCryptoExchange(self):
		#first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		#then, enter partial command price
		sys.stdin = StringIO("-cbtc -eKraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testRequestCommandPricePartialDate(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-d10/9")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testRequestCommandPricePartialDateZeroMeansCurent(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		# then, enter partial command price
		sys.stdin = StringIO("-d0")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testRequestCommandPricePartialUnitTime(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-uusd -t0:15")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '15')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testRequestCommandPricePartialUnitTimeZeroRejected(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price. -t0 means we want current price
		sys.stdin = StringIO("-uusd -t0")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - invalid partial request -uusd -t0: in -t0, 0 must respect HH:mm format.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def test_fillOptionValueInfoRequestTypeFullAmountIntegerCurrencySymbolOk(self):
		optionType = 'VALUE'
		tstOptionValueData = '100usd'
		requestType = Requester.REQUEST_TYPE_FULL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypePartialAmountIntegerCurrencySymbolOk(self):
		optionType = 'VALUE'
		tstOptionValueData = '100usd'
		requestType = Requester.REQUEST_TYPE_PARTIAL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypeFullAmountFloatCurrencySymbolOk(self):
		optionType = 'VALUE'
		tstOptionValueData = '10.55usd'
		requestType = Requester.REQUEST_TYPE_FULL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('10.55', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypePartialAmountFloatCurrencySymbolOk(self):
		optionType = 'VALUE'
		tstOptionValueData = '10.55usd'
		requestType = Requester.REQUEST_TYPE_PARTIAL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('10.55', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypeFullCancelValueOption(self):
		optionType = 'VALUE'
		tstOptionValueData = '0'
		requestType = Requester.REQUEST_TYPE_FULL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypePartialCancelValueOption(self):
		optionType = 'VALUE'
		tstOptionValueData = '0'
		requestType = Requester.REQUEST_TYPE_PARTIAL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypeFullAmountIntegerCurrencySymbolMissing(self):
		optionType = 'VALUE'
		tstOptionValueData = '100'
		requestType = Requester.REQUEST_TYPE_FULL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypePartialAmountIntegerCurrencySymbolMissing(self):
		optionType = 'VALUE'
		tstOptionValueData = '100'
		requestType = Requester.REQUEST_TYPE_PARTIAL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypeFullAmountFloatIncompleteCurrencySymbolMissing(self):
		optionType = 'VALUE'
		tstOptionValueData = '12.'
		requestType = Requester.REQUEST_TYPE_FULL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('12', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypePartialAmountFloatIncompleteCurrencySymbolMissing(self):
		optionType = 'VALUE'
		tstOptionValueData = '12.'
		requestType = Requester.REQUEST_TYPE_PARTIAL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('12', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypeFullAmountFloatCurrencySymbolMissing(self):
		optionType = 'VALUE'
		tstOptionValueData = '12.5'
		requestType = Requester.REQUEST_TYPE_FULL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('12.5', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

	def test_fillOptionValueInfoRequestTypePartialAmountFloatCurrencySymbolMissing(self):
		optionType = 'VALUE'
		tstOptionValueData = '12.5'
		requestType = Requester.REQUEST_TYPE_PARTIAL
		commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

		self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual('12.5', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

# test new FIAT -f and PRICE -p options

	def test_parseGroupsFullDayMonthHHMMFiatValueOption(self):
		inputStr = "btc eth 10/9 12:45 Kraken -fusd -v100usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-fusd', '-v100usd', None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMFiatValueOptionIncomplete(self):
		inputStr = "btc eth 10/9 12:45 Kraken -fusd -v100"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-fusd', '-v100', None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMPriceOption(self):
		inputStr = "btc eth 10/9 12:45 Kraken -p200.453usd "
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200.453usd', None, None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMPriceOptionIncomplete(self):
		inputStr = "btc eth 10/9 12:45 Kraken -p200"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200', None, None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMOptionPrice(self):
		inputStr = "btc eth 10/9 12:45 Kraken -p200.453usd -v100.675usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200.453usd', '-v100.675usd', None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMOptionPriceIncomplete(self):
		inputStr = "btc eth 10/9 12:45 Kraken -p200usd -v100"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200usd', '-v100', None, None), groupList)

	def test_parseGroupsFullDayMonthHHMMPriceIncompleteValueOption(self):
		inputStr = "btc eth 10/9 12:45 Kraken -p200 -v100usd"
		groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200', '-v100usd', None, None), groupList)

	def test_parseGroupsPartialDDDMHHFiatValueOptions(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -fusd -v0.0044235btc"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-f', 'usd', '-v', '0.0044235btc', None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialDDDMHHFiatValueIncompleteOptions(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -fusd -v0.0044235"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-f', 'usd', '-v', '0.0044235', None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialDDDMHHPriceValueOptions(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -p300.567usd -v0.0044235btc"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-p', '300.567usd', '-v', '0.0044235btc', None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialDDDMHHPriceValueIncompleteOptions(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -p500usd -v0.0044235"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-p', '500usd', '-v', '0.0044235', None, None, None, None, None, None), groupList)

	def test_parseGroupsPartialDDDMHHPriceIncompleteValueIncompleteOptions(self):
		inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -p500 -v0.0044235"
		groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

		self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-p', '500', '-v', '0.0044235', None, None, None, None, None, None), groupList)

# test full request options

# value full

	def testCommandPriceFullRequestWithOptionValueSaveCommandInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -vs0.01btc 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -vs0.01btc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionValueSaveCommandInInvalidPosThreeAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -vs0.01btc 10/9/17 12:45 Kraken -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -vs0.01btc 10/9/17 12:45 Kraken -zunsupported violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionValueSaveCommandInInvalidPosFour(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 -vs0.01btc 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 -vs0.01btc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionValueSaveCommandInInvalidPosFive(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 -vs0.01btc Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 -vs0.01btc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], None)
		self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithUnsupportedOptionWithSaveModifier(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -zsunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], None)
		self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithValueOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0.01btc")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionValueSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01btc")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionValueSaveCommandAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01btc -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithPriceUnsupportedOptionAndValueSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -zunsupported -vs0.01btc")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestWithValueOptionInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -v0.01btc 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - full request btc usd -v0.01btc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithValueOptionInInvalidPosFour(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 -v0.01btc 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - full request btc usd 10/9/17 -v0.01btc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithValueOptionInInvalidPosFive(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 -v0.01btc Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - full request btc usd 10/9/17 12:45 -v0.01btc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionValueSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vsooo")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -vsooo: -vsooo option violates the -vs option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionValueCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vooo")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -vooo: -vooo option violates the -v option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionValueSaveSpec(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -vs: -vs option violates the -vs option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionValueSaveNoFiatWithAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -vs0.01: -vs0.01 option violates the -vs option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionValueNoFiatWithAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0.01")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -v0.01: -v0.01 option violates the -v option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionValueEraseCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin


	def testCommandPriceFullRequestEndingWithInvalidOptionValueNoAmountNoFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 Kraken -v: -v option violates the -v option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

# fiat full

	def testCommandPriceFullRequestWithOptionFiatSaveCommandInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -fsbtc 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -fsbtc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionFiatSaveCommandInInvalidPosThreeAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -fsbtc 10/9/17 12:45 Kraken -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -fsbtc 10/9/17 12:45 Kraken -zunsupported violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionFiatSaveCommandInInvalidPosFour(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 -fsbtc 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 -fsbtc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionFiatSaveCommandInInvalidPosFive(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 -fsbtc Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 -fsbtc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithFiatOptionCrypto(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fbtc")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithFiatOptionExchange(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fbtc.bittrex")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual('bittrex', parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithFiatOptionSaveExchange(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fsbtc.bittrex")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual('bittrex', parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionFiatSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fsbtc")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionFiatSaveCommandAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fsbtc -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithPriceUnsupportedOptionAndFiatSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -zunsupported -fsbtc")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestWithFiatOptionInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -fbtc 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - full request btc usd -fbtc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithFiatOptionInInvalidPosFour(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 -fbtc 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - full request btc usd 10/9/17 -fbtc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithFiatOptionInInvalidPosFive(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 -fbtc Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual("ERROR - full request btc usd 10/9/17 12:45 -fbtc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionFiatSaveSpec(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fs")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -fs: -fs option violates the -fs option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionFiatNoFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -f")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 Kraken -f: -f option violates the -f option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithFiatOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -fusd")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithFiatOptionSave(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -fsusd")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionFiatErase(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -f0")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionFiatWithAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -f0.01")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -f0.01: -f0.01 option violates the -f option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionFiatSaveWithAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fs0.01")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -fs0.01: -fs0.01 option violates the -fs option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

# value fiat full

	def testCommandPriceFullRequestEndingWithInvalidOptionValueNoAmountInvalidOptionFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v -f")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 Kraken -v -f: -v option violates the -v option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

# price full

	def testCommandPriceFullRequestWithOptionPriceSaveCommandInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -ps0.02btc 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -ps0.02btc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionPriceSaveCommandInInvalidPosThreeAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -ps0.02btc 10/9/17 12:45 Kraken -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -ps0.02btc 10/9/17 12:45 Kraken -zunsupported violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionPriceSaveCommandInInvalidPosFour(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 -ps0.02btc 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 -ps0.02btc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithOptionPriceSaveCommandInInvalidPosFive(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 -ps0.02btc Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 -ps0.02btc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithPriceOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -p0.01")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin
		
	def testCommandPriceFullRequestEndingWithPriceOptionSave(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ps0.01")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_EXCHANGE])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionPriceSaveCommandAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ps0.02 -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.02', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithPriceUnsupportedOptionAndPriceSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -zunsupported -ps0.02")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.02', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestWithPriceOptionInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -p0.01btc 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -p0.01btc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithPriceOptionInInvalidPosFour(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 -p0.01btc 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 -p0.01btc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestWithPriceOptionInInvalidPosFive(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 -p0.01btc Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 -p0.01btc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceSaveCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -psooo")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -psooo: -psooo option violates the -ps option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -pooo")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -pooo: -pooo option violates the -p option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceSaveSpec(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ps")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -ps: -ps option violates the -ps option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceNoSaveAmountWithFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -p0.01usd")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -p0.01usd: -p0.01usd option violates the -p option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceNoSaveNoAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -p")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -p: -p option violates the -p option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceSaveNoAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ps")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -ps: -ps option violates the -ps option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceSaveAmountWithFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ps0.01usd")
		commandError = self.requester.getCommandFromCommandLine()

		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()

		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -ps0.01usd: -ps0.01usd option violates the -ps option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithOptionPriceEraseCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -p0")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

		sys.stdin = stdin

	def testCommandPriceFullRequestEndingWithInvalidOptionPriceNoAmountNoFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -p")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 Kraken -p: -p option violates the -p option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

		sys.stdin = stdin
		
# result full
	
	def test_parseAndFillFullCommandPriceWithOptionResultSaveNoData(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultSaveData_1(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1:-3"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1:-3', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultSaveData_2(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1-2"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1-2', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultSaveData_3(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultNoSaveNoData(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -r"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultNoSaveData_1(self):
		inputStr = "btc usd 10/9/2017 12:45 Kraken -r-1:-3"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1:-3', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultNoSaveData_2(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -r-1-2"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1-2', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultNoSaveData_3(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -r-1"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithOptionResultErase(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -r0"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithInvalidRSDataOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/2017 12:45 Kraken -rs23.55")
		commandError = self.requester.getCommandFromCommandLine()
		
		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/2017 12:45 Kraken -rs23.55: -rs23.55 option violates the -rs option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin
	
	def test_parseAndFillFullCommandPriceWithInvalidRDataOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/2017 12:45 Kraken -r23.55")
		commandError = self.requester.getCommandFromCommandLine()
		
		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/2017 12:45 Kraken -r23.55: -r23.55 option violates the -r option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin
	
	def test_parseAndFillFullCommandPriceWithRSMinusOneOption(self):
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithRSMinusOneMinusTwoOption(self):
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1-2"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1-2', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithRSMinusNOption(self):
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1-2-3"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1-2-3', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillFullCommandPriceWithRSMinusOneToMinusThreeOption(self):
		'''
		This test is identical to calling Requester.getCommandFromCommandLine()
		used as shown bellow in other unit tests !

		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		'''
		inputStr = "btc usd 10/9/2017 12:45 Kraken -rs-1:-3"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('btc', parsedParmData[CommandPrice.CRYPTO])
		self.assertEqual('usd', parsedParmData[CommandPrice.UNIT])
		self.assertEqual('10', parsedParmData[CommandPrice.DAY])
		self.assertEqual('9', parsedParmData[CommandPrice.MONTH])
		self.assertEqual('2017', parsedParmData[CommandPrice.YEAR])
		self.assertEqual('12', parsedParmData[CommandPrice.HOUR])
		self.assertEqual('45', parsedParmData[CommandPrice.MINUTE])
		self.assertEqual('Kraken', parsedParmData[CommandPrice.EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.HOUR_MINUTE])
		self.assertEqual(None, parsedParmData[CommandPrice.DAY_MONTH_YEAR])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1:-3', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
# limit full
	
	def testCommandPriceFullRequestWithOptionLimitSaveCommandInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc -ls1500usd.kraken 10/9/17 12:45 binance")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request eth btc -ls1500usd.kraken 10/9/17 12:45 binance violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		
		sys.stdin = stdin
	
	def testCommandPriceFullRequestWithOptionLimitSaveCommandInInvalidPosThreeAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc -ls1500usd.kraken 10/9/17 12:45 binance -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request eth btc -ls1500usd.kraken 10/9/17 12:45 binance -zunsupported violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithOptionLimitNoSave(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -l1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'binance')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithOptionLimitNoSaveNoExchange(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -l1500usd")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'binance')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithOptionLimitSave(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'binance')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithOptionLimitSaveNoExchange(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'binance')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithOptionLimitSaveCommandAndUnsupportedOption(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -ls1500usd.kraken -zunsupported")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'binance')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual('s', parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])

		sys.stdin = stdin
	
	def testCommandPriceFullRequestWithOptionLimitInInvalidPosThree(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd -ls1500usd.kraken 10/9/17 12:45 Kraken")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd -ls1500usd.kraken 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithInvalidOptionLimitSaveNoFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ls1500")
		commandError = self.requester.getCommandFromCommandLine()
		
		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -ls1500: -ls1500 option violates the -ls option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithInvalidOptionLimitSaveNoAmount(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -lsusd")
		commandError = self.requester.getCommandFromCommandLine()
		
		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -lsusd: -lsusd option violates the -ls option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithInvalidOptionLimitSaveSpec(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -ls")
		commandError = self.requester.getCommandFromCommandLine()
		
		self.assertEqual(self.commandError, commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			'ERROR - full request btc usd 10/9/17 12:45 Kraken -ls: -ls option violates the -ls option format. See help for more information.',
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithOptionLimitEraseCommand(self):
		stdin = sys.stdin
		sys.stdin = StringIO("eth btc 10/9/17 12:45 binance -l0")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'btc')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'binance')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		
		sys.stdin = stdin
	
	def testCommandPriceFullRequestEndingWithInvalidOptionLimitNoAmountNoFiat(self):
		stdin = sys.stdin
		sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -l")
		commandPrice = self.requester.getCommandFromCommandLine()
		
		self.assertIsInstance(commandPrice, CommandError)
		self.assertEqual(commandPrice, self.commandError)
		resultData = self.commandError.execute()
		self.assertEqual(
			"ERROR - full request btc usd 10/9/17 12:45 Kraken -l: -l option violates the -l option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		
		sys.stdin = stdin
	
	# test partial request options

# value partial

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValue(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -v0.0044256btc"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionValue(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-V0.0044256btc -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionValue(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -v500gbp -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceOptionValuePreviouslySet(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'

		inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceIneffectiveOptionValueSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

		inputStr = "-ceth -v -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValueSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -vs0.0044256btc"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValueSaveAndUnsupportedOptionWithSaveOptionModifier(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -vs0.0044256btc -zsunsupported"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValueSaveAndUnsupportedOption(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -vs0.0044256btc -zunsupported100"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported100', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionValueSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-VS0.0044256btc -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionValueSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -vs500gbp -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceOptionValueSavePreviouslySet(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceEraseOptionValueSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -v0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceInvalidOptionValueSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'

		inputStr = "-ceth -vooo -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -vooo option violates the -v option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceInvalidOptionValueSaveSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -vsooo -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -vsooo option violates the -vs option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceInvalidOptionValueSaveSpecNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -vs0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -vs0.01 option violates the -vs option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceInvalidOptionValueNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -v0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -v0.01 option violates the -v option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceEraseOptionValue(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'

		inputStr = "-ceth -v0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceEmptyOptionValueSaveSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

		inputStr = "-ceth -vs -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -vs with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceIneffectiveOptionValueSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

		inputStr = "-ceth -v35 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -v35 option violates the -v option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceIneffectiveOptionValueSaveSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

		inputStr = "-ceth -vs35 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -vs35 option violates the -vs option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

# fiat partial

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiat(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fbtc"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertIsInstance(commandPrice, CommandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiatExchange(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fbtc.binance"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertIsInstance(commandPrice, CommandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual('binance', parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiatExchange(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fbtc.bittrex"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertIsInstance(commandPrice, CommandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual('bittrex', parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiatSaveExchange(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fsbtc.bittrex"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertIsInstance(commandPrice, CommandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual('bittrex', parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionFiat(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-Fbtc -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionFiat(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -fbtc -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceOptionFiatPreviouslySet(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL] = 'btc'

		inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceIneffectiveOptionFiatSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL] = 'btc'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

		inputStr = "-ceth -f -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandError)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('-f with no value is not valid. Partial request ignored', parsedParmData[CommandError.COMMAND_ERROR_MSG_KEY])
		self.assertEqual(CommandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST, parsedParmData[CommandError.COMMAND_ERROR_TYPE_KEY])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiatSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fsbtc"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiatSaveAndUnsupportedOptionWithSaveOptionModifier(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fsbtc -zsunsupported"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionFiatSaveAndUnsupportedOption(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -fsbtc -zunsupported100"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported100', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionFiatSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-FSbtc -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionFiatSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		#prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

		inputStr = "-ceth -fsbtc -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceOptionFiatSavePreviouslySet(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL] = 'btc'
		parsedParmData[CommandPrice.OPTION_FIAT_SAVE] = True

		inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceEraseOptionFiatSave(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL] = 'btc'
		parsedParmData[CommandPrice.OPTION_FIAT_SAVE] = True

		inputStr = "-ceth -fs0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -fs0 option violates the -fs option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceInvalidOptionFiatSaveSpecNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -fs0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -fs0.01 option violates the -f option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceInvalidOptionFiatNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

		inputStr = "-ceth -f0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -f0.01 option violates the -f option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

	def test_parseAndFillPartialCommandPriceEraseOptionFiat(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL] = 'btc'

		inputStr = "-ceth -f0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

	def test_parseAndFillPartialCommandPriceIneffectiveOptionFiatSaveSpec(self):
		commandPrice = self.requester.commandPrice

		parsedParmData = commandPrice.parsedParmData

		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

		inputStr = "-ceth -fs -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()

		#formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual("ERROR - invalid partial request : -fs with no value is not valid. Partial request ignored.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
		
# price partial
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionPrice(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -p0.0044256"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionPriceExchange(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -p0.0044256"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionPrice(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-P0.0044256 -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionPrice(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -p500 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceOptionPricePreviouslySet(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL] = None
		
		inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -p300 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('300', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceIneffectiveOptionPriceSpec(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False
		
		inputStr = "-ceth -p -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandError)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual('-p with no value is not valid. Partial request ignored',
						 parsedParmData[CommandError.COMMAND_ERROR_MSG_KEY])
		self.assertEqual(CommandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST,
						 parsedParmData[CommandError.COMMAND_ERROR_TYPE_KEY])
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionPriceSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -ps0.0044256"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_EXCHANGE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionPriceSaveAndUnsupportedOptionWithSaveOptionModifier(
			self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -ps0.0044256 -zsunsupported"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionPriceSaveAndUnsupportedOption(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -ps0.004425 -zunsupported100"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported100', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.004425', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionPriceSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-PS0.0044256 -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionPriceSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ps500 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceOptionPriceSavePreviouslySet(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_PRICE_SAVE] = True
		
		inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertTrue(parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceEraseOptionPriceSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_PRICE_SAVE] = True
		
		inputStr = "-ceth -p0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceInvalidOptionPriceSpec(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -pooo -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -pooo option violates the -p option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
	
	def test_parseAndFillPartialCommandPriceInvalidOptionPriceSaveSpec(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -psooo -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -psooo option violates the -ps option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
	
	def test_parseAndFillPartialCommandPriceInvalidOptionPriceSaveSpecNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = None
		parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL] = None
		parsedParmData[CommandPrice.OPTION_PRICE_SAVE] = None
		
		inputStr = "-ceth -ps0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceInvalidOptionPriceNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True
		
		inputStr = "-ceth -p0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceEraseOptionPrice(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL] = 'gbp'
		
		inputStr = "-ceth -p0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
	
	def test_parseAndFillPartialCommandPriceIneffectiveOptionPriceSaveSpec(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = '16'
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False
		
		inputStr = "-ceth -ps -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -ps with no value is not valid. Partial request ignored.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
	
# result partial
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionResult(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -rs-1-2-3"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1-2-3', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionResult(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-Ceth -Ugbp -D11/8 -T22:46 -EKraken -Rs-1-2"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1-2', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceOptionResultPreviouslySet(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT] = '-1'
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -rs-1:-2"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1:-2', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceOptionResultSaveNoAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'Kraken'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT] = '-2-4'
		
		inputStr = "-ceth -ugbp -d0 -rs"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceOptionResultNoAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'Kraken'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT] = '-2-4'
		parsedParmData[CommandPrice.OPTION_RESULT_SAVE] = True

		inputStr = "-ceth -ugbp -d0 -r"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionResultSaveAndUnsupportedOptionWithSaveOptionModifier(
			self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -zsunsupported -rs-1:-2"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual('-1:-2', parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
	
	def test_parseAndFillPartialCommandPriceEraseOptionResultSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'Kraken'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT] = '-2-4'
		parsedParmData[CommandPrice.OPTION_RESULT_SAVE] = True
		
		inputStr = "-ceth -ugbp -d0 -r0"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_RESULT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	# limit partial
		
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionLimit(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -l1500usd.kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

	def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionLimit(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-Ceth -Ugbp -D11/8 -T22:46 -EKraken -Ls1500usd.kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceOptionLimitPreviouslySet(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL] = 'gbp'
		
		inputStr = "-Ceth -Ugbp -D11/8 -T22:46 -EKraken -Ls1500usd.kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('1500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceOptionLimitNoAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL] = 'gbp'
		
		inputStr = "-Ceth -Ugbp -D11/8 -T22:46 -EKraken -Ls"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -Ls with no value is not valid. Partial request ignored.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionLimitSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -ls2500usd.kraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('2500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceNoInitYearThenOptionLimitSaveAndUnsupportedOptionWithSaveOptionModifier(
			self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -ls2500usd.kraken -zsunsupported"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual('2500', parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual('kraken', parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(True, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
		self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
	
	def test_parseAndFillPartialCommandPriceEraseOptionLimitSave(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL] = 'gbp'
		parsedParmData[CommandPrice.OPTION_LIMIT_SAVE] = True
		
		inputStr = "-ceth -l0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceInvalidOptionLimitSaveSpecNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ls0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -ls0.01 option violates the -ls option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
	
	def test_parseAndFillPartialCommandPriceInvalidOptionLimitNoFiatWithAmount(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -l0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -l0.01 option violates the -l option format. See help for more information.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
	
	def test_parseAndFillPartialCommandPriceEraseOptionLimit(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT] = '500'
		parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL] = 'gbp'
		
		inputStr = "-ceth -l0 -ugbp -d11/8/15 -t22:46 -eKraken"
		commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
		self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_DATA])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_AMOUNT])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SYMBOL])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE])
		self.assertEqual(None, parsedParmData[CommandPrice.OPTION_LIMIT_SAVE])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
		self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
	
	def test_parseAndFillPartialCommandPriceEmptyOptionLimitSaveSpec(self):
		commandPrice = self.requester.commandPrice
		
		parsedParmData = commandPrice.parsedParmData
		
		# prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
		parsedParmData[CommandPrice.CRYPTO] = 'btc'
		parsedParmData[CommandPrice.UNIT] = 'usd'
		parsedParmData[CommandPrice.DAY] = '10'
		parsedParmData[CommandPrice.MONTH] = '9'
		parsedParmData[CommandPrice.YEAR] = None
		parsedParmData[CommandPrice.HOUR] = '12'
		parsedParmData[CommandPrice.MINUTE] = '45'
		parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
		parsedParmData[CommandPrice.HOUR_MINUTE] = None
		parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
		
		inputStr = "-ceth -ls -ugbp -d11/8/15 -t22:46 -eKraken"
		commandError = self.requester._parseAndFillCommandPrice(inputStr)
		self.assertEqual(commandError, self.commandError)
		resultData = self.commandError.execute()
		
		# formatting of request input string has been moved to end of Requester.getCommand !
		self.assertEqual(
			"ERROR - invalid partial request : -ls with no value is not valid. Partial request ignored.",
			resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

#  other partial
	
	def testRequestCommandPricePartialDateTimeDMYYYY(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-d10/9/2020 12:22")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2020')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

	def testRequestCommandPricePartialDateTime0D0MYYYY(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-d01/09/2020 12:22")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '09')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '2020')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

	def testRequestCommandPricePartialDateTimeDMYY(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-d10/9/20 12:22")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '20')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

	def testRequestCommandPricePartialDateTimeDM(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-d10/9 12:22")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

	def testRequestCommandPricePartialDateTimeD(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price
		sys.stdin = StringIO("-d10 12:22")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

	def testRequestCommandPricePartialValueOptionDateTimeD(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price with value option before -d
		sys.stdin = StringIO("-v10eth -d10 12:22")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

	def testRequestCommandPricePartialDateTimeDValueOption(self):
		# first, enter full command price
		stdin = sys.stdin
		sys.stdin = StringIO("eth usd 1/8/16 13:46 kraken")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		# then, enter partial command price with value option after -d
		sys.stdin = StringIO("-d10 12:22 -v10eth")
		commandPrice = self.requester.getCommandFromCommandLine()

		self.assertIsInstance(commandPrice, CommandPrice)
		self.assertEqual(commandPrice, self.commandPrice)
		parsedParmData = commandPrice.parsedParmData
		self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
		self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
		self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
		self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
		self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
		self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
		self.assertEqual(parsedParmData[CommandPrice.MINUTE], '22')
		self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'kraken')
		self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
		self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

		sys.stdin = stdin

if __name__ == '__main__':
#	unittest.main()
	t = TestRequester()
	t.setUp()
	#t.testCommandPriceFullRequestEndingWithOptionValueSaveCommand()
	t.test_parseAndFillPartialCommandPriceOptionResultNoAmount()