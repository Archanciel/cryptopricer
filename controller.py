import sys, os

from commandcrypto import CommandCrypto
from commanderror import CommandError
from commandprice import CommandPrice
from commandquit import CommandQuit
from crypcompexchanges import CrypCompExchanges
from processor import Processor
from requester import Requester


class Controller:
	"""
	Instanciate the app components and
	control the rep loop.
	
	:seqdiag_note Client in the GOF Command pattern. Entry point of the business layer. Instanciates the business layer classes.
	"""
	def __init__(self, printer, configMgr, priceRequester):
		self.configMgr = configMgr
		self.priceRequester = priceRequester
		self.crypCompTranslator = CrypCompExchanges()
		self.processor = Processor(self.configMgr, self.priceRequester, self.crypCompTranslator)
		self.requester = Requester(self.configMgr)

		self.commandPrice = CommandPrice(self.processor, self.configMgr)
		self.commandCrypto = CommandCrypto(self.processor)
		self.requester.commandPrice = self.commandPrice
		self.requester.commandCrypto = self.commandCrypto

		self.commandQuit = CommandQuit(sys)
		self.requester.commandQuit = self.commandQuit

		self.commandError = CommandError(None)
		self.requester.commandError = self.commandError

		self.printer = printer
		

	def commandLineLoop(self):
		"""
		Used essentially by the command line version of CryptoPricer.
		"""
		while True:
			command = self.requester.getCommandFromCommandLine()
			result = command.execute()

			if result != '':
				strToPrint = self.printer.getCommandOutputResult(result)
				print(strToPrint)


	def getPrintableResultForInput(self, inputStr):
		'''
		Return the printable request result, the full request command without any command option,
		the full request command with any specified NON save mode option (information used by
		the GUI to define the status bar content, which differs according to the type of the
		request, full or partial and finally the full request command with any specified save
		mode option (option which is to be saved in the	command history list. A detailed
		explanation of the usefulness of the returned values is availablein the
		GuiOutputFormatter.getFullCommandString(( method documentation.

		:param inputStr:
		:seqdiag_return printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar

		:return: 1/ printable request result
				 2/ full request command without any command option
				 3/ full request command with any non save command option(s)
				 4/ full request command with any specified save mode option(s), None if no save mode option
					is in effect
				 5/ full command string for status bar

				 Ex: 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ None (one command option with save mode in effect !)
					 4/ eth usd 0 bitfinex -vs0.1eth

					 1/ 0.1 ETH/36 USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ eth usd 0 bitfinex -v0.1eth
					 4/ None (no command save option in effect)

					 1/ ETH/USD on Bitfinex: 21/11/17 10:00 360
					 2/ eth usd 0 bitfinex
					 3/ None (no command option in effect)
					 4/ None (no command save option in effect)
		'''
		command = self.requester.getCommand(inputStr)
		resultData = command.execute()

		if resultData != '':
			commandOutputResult = self.printer.getCommandOutputResult(resultData)
			
			fullCommandStrNoOptions, \
			fullCommandStrWithNoSaveOptions, \
			fullCommandStrWithSaveOptionsForHistoryList, \
			fullCommandStrForStatusBar = self.printer.getFullCommandString(resultData)
			
			return commandOutputResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar


if __name__ == '__main__':
	import os
	from io import StringIO

	from consoleoutputformatter import ConsoleOutputFormatter

	stdin = sys.stdin
	sys.stdin = StringIO('btc usd 24/10/17 22:33 Bittrex' +
						 '\nbtc usd 24/10/017 22:33 Bittrex' +
						 '\nbtc usd 24/10/1 22:33 Bittrex' +
						 '\nbtc usd 23/10 2.56 bittrex' +
						 '\ngbyte btc 24/10/2017 22:33 Bittrex' +
						 '\ngbyte usd 24/10/2017 22:33 Bittrex' +
						 '\nbtc usd 0 Bittrex' +
						 '\ngbyte btc 0 Bittrex' +
						 '\nbtc usd 12/10/2017 12:00 Unknown' +
						 '\nbtc usd 12/10/2017 12:00 bittrex\nq\ny') #noticenq\ny to nicely quit the program

	# stdout = sys.stdout
	# if os.name == 'posix':
	#     FILE_PATH = '/sdcard/cryptoout.txt'
	# else:
	#     FILE_PATH = 'c:\\temp\\cryptoout.txt'
	# sys.stdout = open(FILE_PATH, 'w')

	c = Controller(ConsoleOutputFormatter())
	c.commandLineLoop()

	sys.stdin = stdin
	#sys.stdout = stdout
