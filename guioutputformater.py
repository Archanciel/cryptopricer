import os

from commandprice import CommandPrice
from abstractoutputformater import AbstractOutputFormater
from datetimeutil import DateTimeUtil


class GuiOutputFormater(AbstractOutputFormater):

	def __init__(self, configurationMgr, activateClipboard=False):
		'''
		Ctor. The parm activateClipboard with default value set to False was added to prevent SeqDiagBuilder
		unit tests in TestSeqDiagBuilder where the CryptoPricer Condtroller class were implied to crash the Pycharm
		unit test environment. This crask was due to an obscure problem in the Pycharm unit test framework. This
		failure only happened if the kivy clipboard class was imported.

		:param configurationMgr:
		:param activateClipboard:
		'''
		# commented code below does not run in Pydroid since Pydroid does not support
		# the sl4a lib
		# if os.name == 'posix':
		#     import android
		#     self._clipboard = android.Android()
		# else:
		self.activateClipboard = activateClipboard

		if self.activateClipboard:
			from kivy.core.clipboard import Clipboard
			self._clipboard = Clipboard

		self.configurationMgr = configurationMgr

	def printDataToConsole(self, resultData):
		'''
		print the result to the console and
		paste it to the clipboard
		'''
		outputStr = super(GuiOutputFormater, self).getPrintableData(resultData)

		print(outputStr)

	def getFullCommandString(self, resultData, copyResultToClipboard=True):
		'''
		Recreate the full command string corresponding to a full or partial price request entered by the user.

		The full command string no options contains a full date and time which is formatted according to the date time
		format as specified in the configuration file. Even if the request only contained partial date time info,
		the full command string no options contains a full date time specification.

		The full command string no options will be stored in the command history list so it can be replayed or saved to file.
		An empty string is returned if the command generated an error (empty string will not be added to history !

		In case an option to the command with save mode is in effect - for example -vs -, then the full
		command with the save mode option is returned as well. In the GUI, the full command with save mode will
		replace the full command string no options in the command history list. Otherwise, if no command option in save mode
		is in effect (no option or -v for example), then None is returned as second return value and
		no full command string no options will NOT have to be replaced in the command history list.

		:param copyResultToClipboard:
		:param resultData: result of the last full or partial request
		:param copyResultToClipboard: set to True by default. Whreplaying all requests
									  stored in history, set to False, which avoids
									  problem on Android
		:seqdiag_return printResult, fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar
		:return: 1/ full command string with no command option corresponding to a full or partial price request
					entered by the user or empty string if the command generated an error msg.
				 2/ full request command with any non save command option
				 3/ full command string with command option in save mode or none if no command option in save mode
					is in effect or if the command option generated a warning.

				 Ex: 1/ eth usd 0 bitfinex
					 2/ None
					 3/ eth usd 0 bitfinex -vs0.1eth

					 1/ eth usd 0 bitfinex
					 2/ eth usd 0 bitfinex -v0.1btc (even if warning generated !)
					 3/ None (-v0.1btc command was entered, which generated a warning)

					 1/ eth usd 0 bitfinex
					 2/ None (no value command in effect)
					 3/ None (no value command with save option in effect)
		'''
		if resultData.isError():
			return '', None, None, None

		commandDic = resultData.getValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS)
		priceType = resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE)

		if priceType == resultData.PRICE_TYPE_RT:
			fullCommandStrNoOptions = commandDic[CommandPrice.CRYPTO] + ' ' + \
												 commandDic[CommandPrice.UNIT] + ' 0 ' + \
												 commandDic[CommandPrice.EXCHANGE]
		else:
			requestDateDMY, requestDateHM = self._buildFullDateAndTimeStrings(commandDic,
																			  self.configurationMgr.localTimeZone)

			fullCommandStrNoOptions = commandDic[CommandPrice.CRYPTO] + ' ' + \
												 commandDic[CommandPrice.UNIT] + ' ' + \
												 requestDateDMY + ' ' + \
												 requestDateHM + ' ' + \
												 commandDic[CommandPrice.EXCHANGE]

		fullCommandStrWithSaveModeOptions = None
		fullCommandStrWithOptions = None
		fullCommandStrForStatusBar = None

		# handling option value

		if resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE):
			if not resultData.containsWarning(resultData.WARNING_TYPE_COMMAND_VALUE):
				# in case the value command generated a warning, if the value command data contains a crypto or unit
				# different from the crypto or unit of tthe request, the fullCommandStr remains
				# None and wont't be stored in the request history list of the GUI !
				fullCommandStrWithSaveModeOptions = fullCommandStrNoOptions + ' -vs{}{}'.format(commandDic[
					CommandPrice.OPTION_VALUE_AMOUNT], commandDic[CommandPrice.OPTION_VALUE_SYMBOL])
				fullCommandStrForStatusBar = fullCommandStrWithSaveModeOptions
		else:
			valueOptionAmountStr = commandDic[CommandPrice.OPTION_VALUE_AMOUNT]
			valueOptionSymbolStr = commandDic[CommandPrice.OPTION_VALUE_SYMBOL]
			if valueOptionAmountStr and valueOptionSymbolStr:
				# even in case the value command generated a warning, it will be displayed in the status bar !
				fullCommandStrWithOptions = fullCommandStrNoOptions + ' -v{}{}'.format(valueOptionAmountStr, valueOptionSymbolStr)
				fullCommandStrForStatusBar = fullCommandStrWithOptions

		# handling option fiat

		if resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE):
			if not resultData.containsWarning(resultData.WARNING_TYPE_COMMAND_VALUE):
				# in case the value command generated a warning, if the value command data contains a crypto or unit
				# different from the crypto or unit of tthe request, the fullCommandStr remains
				# None and wont't be stored in the request history list of the GUI !
				if fullCommandStrWithSaveModeOptions:
					# case when option value exist and is in save mode
					fullCommandStrWithSaveModeOptions = self._addFiatOptionInfoToFullCommandStr(commandDic,
																								fullCommandStrWithSaveModeOptions,
																								isOptionFiatSave=True)
				else:
					# case when no option value exist in save mode
					fullCommandStrWithSaveModeOptions = self._addFiatOptionInfoToFullCommandStr(commandDic,
																								fullCommandStrNoOptions,
																								isOptionFiatSave=True)

				fullCommandStrForStatusBar = fullCommandStrWithSaveModeOptions + self._buildUnitFiatComputationString(resultData)
		else:
			fiatOptionSymbol = commandDic[CommandPrice.OPTION_FIAT_SYMBOL]
			if not fullCommandStrWithOptions:
				if fiatOptionSymbol:
					fullCommandStrWithOptions = self._addFiatOptionInfoToFullCommandStr(commandDic,
																							fullCommandStrNoOptions,
																							isOptionFiatSave=False)
			else:
				if fiatOptionSymbol:
					fullCommandStrWithOptions = self._addFiatOptionInfoToFullCommandStr(commandDic,
																							fullCommandStrWithOptions,
																							isOptionFiatSave=False)

			if fullCommandStrWithOptions:
				fullCommandStrForStatusBar = fullCommandStrWithOptions + self._buildUnitFiatComputationString(resultData)

		from seqdiagbuilder import SeqDiagBuilder

		SeqDiagBuilder.recordFlow()

		return fullCommandStrNoOptions, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions, fullCommandStrForStatusBar
	
	def _addFiatOptionInfoToFullCommandStr(self,
										   commandDic,
										   fullCommandStr,
										   isOptionFiatSave):
		"""
		
		:param commandDic:
		:param fullCommandStr: full command string with or without value option
		:param isOptionFiatSave
		
		:return:
		"""
		if isOptionFiatSave:
			fiatOptionStr = ' -fs{}'
		else:
			fiatOptionStr = ' -f{}'

		requestFiatExchange = commandDic[CommandPrice.OPTION_FIAT_EXCHANGE]
		
		if requestFiatExchange:
			fullCommandStr = fullCommandStr + (fiatOptionStr + '.{}').format(
				commandDic[CommandPrice.OPTION_FIAT_SYMBOL],
				requestFiatExchange)
		else:
			fullCommandStr = fullCommandStr + fiatOptionStr.format(
				commandDic[CommandPrice.OPTION_FIAT_SYMBOL])
			
		return fullCommandStr
	
	def _buildUnitFiatComputationString(self, resultData):
		priceStr = self._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_PRICE), self.PRICE_FLOAT_FORMAT)
		fiatComputedAmountStr = self._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT), self.PRICE_FLOAT_FORMAT)
		fiatRateStr = self._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE), self.PRICE_FLOAT_FORMAT)

		return '\n({} * {} = {})'.format(priceStr,
										 fiatRateStr,
										 fiatComputedAmountStr)

	def _buildFullDateAndTimeStrings(self, commandDic, timezoneStr):
		'''
		This method ensures that the full command string is unified whatever the completness of the
		dated/time components specified in the request by the user.

		Ex: btc usd 1/1 bitfinex or btc usd 1/01/18 bitfinex or btc usd 1/1 12:23 bitfinex all return
			a full commaand of btc usd 01/01/18 00:00 bitfinex, btc usd 01/01/18 12:23 bitfinex
			respectively.

		This is important since the ful command string is what is stored in the command history list, with
		no duplicates. Otherwxise, btc usd 1/1 00:00 bitfinex and btc usd 01/01/18 00:00 bitfinex would
		be stored as 2 entries !

		:param commandDic:
		:param timezoneStr:
		:seqdiag_return requestDateDMY, requestDateHM
		:return:
		'''
		day = commandDic[CommandPrice.DAY]
		month = commandDic[CommandPrice.MONTH]
		year = commandDic[CommandPrice.YEAR]
		hour = commandDic[CommandPrice.HOUR]
		minute = commandDic[CommandPrice.MINUTE]

		requestDateDMY, requestDateHM = DateTimeUtil.formatPrintDateTimeFromStringComponents(day, month, year, hour,
																							 minute, timezoneStr,
																							 self.configurationMgr.dateTimeFormat)

		from seqdiagbuilder import SeqDiagBuilder
		SeqDiagBuilder.recordFlow()

		return requestDateDMY, requestDateHM

	def toClipboard(self, numericVal):
		if not self.activateClipboard:
			return

		self._clipboard.copy(str(numericVal))

	def fromClipboard(self):
		if not self.activateClipboard:
			return 'Clipboard not available since not activated at ConsoleOutputFormater initialisation'
		else:
			return self._clipboard.paste()


if __name__ == '__main__':
	pr = GuiOutputFormater()
	y = round(5.59, 1)
	y = 0.999999999
	y = 0.9084
	y = 40
	yFormatted = '%.8f' % y
	print()
	print('No formatting:                 ' + str(y))
	print('With formatting:               ' + yFormatted)
	print('With formatting no trailing 0: ' + pr._formatPriceFloatToStr(y))
	print()

	a = 12.56
	pr.toClipboard(a)
	print('Clipboard: ' + pr.fromClipboard())
