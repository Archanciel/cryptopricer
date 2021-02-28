from commandprice import CommandPrice
from abstractoutputformater import AbstractOutputFormater
from datetimeutil import DateTimeUtil


class GuiOutputFormatter(AbstractOutputFormater):
	"""
	:seqdiag_note Formats the result data printed to the output zone of the application and to the status bar.
	"""

	def __init__(self, configurationMgr):
		"""
		Ctor. The parm activateClipboard with default value set to False was added to prevent SeqDiagBuilder
		unit tests in TestSeqDiagBuilder where the CryptoPricer Condtroller class were implied to crash the Pycharm
		unit test environment. This crash was due to an obscure problem in the Pycharm unit test framework. This
		failure only happened if the kivy clipboard class was imported.
		
		:param configurationMgr:
		"""
		
		super().__init__()
		self.configurationMgr = configurationMgr

	def printDataToConsole(self, resultData):
		'''
		print the result to the console and
		paste it to the clipboard
		'''
		outputStr = super(GuiOutputFormatter, self).getCommandOutputResult(resultData)

		print(outputStr)

	def getFullCommandString(self, resultData):
		'''
		Recreate the full command string corresponding to a full or partial price request entered by the user.

		The full command string no options contains a full date and time which is formatted according to the date time
		format as specified in the configuration file. Even if the request only contained partial date time info,
		the full command string no options contains a full date time specification.

		The full command string no options will be stored in the command history list so it can be replayed or
		saved to file. An empty string is returned if the command generated an error (an empty string will not
		be added to the history list !)

		In case an option with save mode is added to the command - for example -vs -, then the full
		command with the save mode option is returned as well (fullCommandStrWithSaveOptionsForHistoryList).
		In the GUI, the full command with save mode option will	replace the corresponding full command string
		no options (fullCommandStrNoOptions) in the command history list. If the added command option is not
		in save mode (no option or -v... or -f... for example), then None is returned for
		fullCommandStrWithSaveOptionsForHistoryList	and	the corresponding full command string no options
		(fullCommandStrNoOptions) will NOT have	to be replaced in the command history list.
		
		Finally, what is the usefulness of the fullCommandStrWithNoSaveOptions returned string ? It
		serves to differentiate a partial request with option(s) without save mode from a full request
		with with option(s) without save mode. In case of partial request, the status bar content is
		different from in the case of a full request.
		
		:param copyResultToClipboard:
		:param resultData: result of the last full or partial request
		:seqdiag_return printResult, fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar

		:return: 1/ full command string with no command option corresponding to a full or partial price request
					entered by the user or empty string if the command generated an error msg.
				 2/ full request command with any non save command option
				 3/ full command string with command option in save mode or none if no command option in save mode
					is in effect or if the command option generated a warning.
				 4/ full command string for status bar

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
		if not resultData.noError():
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

		fullCommandStrWithSaveOptionsForHistoryList = None
		fullCommandStrWithNoSaveOptions = None
		fullCommandStrForStatusBar = None

		# handling value option

		valueOptionStr = ''
		
		if resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO):
			fullCommandStrWithNoSaveOptions, \
			fullCommandStrWithSaveOptionsForHistoryList, \
			fullCommandStrForStatusBar, \
			valueOptionStr = self._addOptionValueInfo(resultData,
													  commandDic,
													  fullCommandStrNoOptions,
													  fullCommandStrWithNoSaveOptions,
													  fullCommandStrWithSaveOptionsForHistoryList,
													  fullCommandStrForStatusBar,
													  valueOptionStr)
		
		# handling fiat option

		fiatOptionSymbol = commandDic[CommandPrice.OPTION_FIAT_SYMBOL]

		if fiatOptionSymbol:
			fullCommandStrWithNoSaveOptions, \
			fullCommandStrWithSaveOptionsForHistoryList, \
			fullCommandStrForStatusBar = self._addOptionFiatInfo(resultData,
																 commandDic,
																 valueOptionStr,
																 fiatOptionSymbol,
																 fullCommandStrNoOptions,
																 fullCommandStrWithNoSaveOptions,
																 fullCommandStrWithSaveOptionsForHistoryList,
																 fullCommandStrForStatusBar)

		# handling price option

		from seqdiagbuilder import SeqDiagBuilder

		SeqDiagBuilder.recordFlow()
		# import logging
		# logging.info('fullCommandStrWithNoSaveOptions: {}'.format(fullCommandStrWithNoSaveOptions))
		# logging.info('fullCommandStrWithSaveOptionsForHistoryList: {}'.format(fullCommandStrWithSaveOptionsForHistoryList))
		# logging.info('fullCommandStrForStatusBar: {}'.format(fullCommandStrForStatusBar))

		return fullCommandStrNoOptions, fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar
	
	def _addOptionValueInfo(self,
							resultData,
							commandDic,
							fullCommandStrNoOptions,
							fullCommandStrWithNoSaveOptions,
							fullCommandStrWithSaveOptionsForHistoryList,
							fullCommandStrForStatusBar,
							valueOptionStr):
		"""
		Adds the value option information to
			1/ the request full command string with no save	option (result ex:
			   btc usd 20/12/20 00:00 binance -v1500usd)
			2/ the request full command string with save option used to fill the GUI request
			   history list (result ex: btc usd 20/12/20 00:00 binance -vs1500usd)
			3/ the request full command string for status bar (result ex:
			   btc usd 20/12/20 00:00 binance -v1500usd or
			   btc usd 20/12/20 00:00 binance -vs1500usd)

		:param resultData: stores the on-line request results
		:param commandDic: stores the currently active command parms
		:param fullCommandStrNoOptions: contains the current request full command without any option
		:param fullCommandStrWithNoSaveOptions: empty str output result
		:param fullCommandStrWithSaveOptionsForHistoryList: empty str output result
		:param fullCommandStrForStatusBar: empty str output result
		:param valueOptionStr: empty str output result
		
		:return: fullCommandStrWithNoSaveOptions,
				 fullCommandStrWithSaveOptionsForHistoryList,
				 fullCommandStrForStatusBar,
				 valueOptionStr
		"""
		valueOptionAmountStr = commandDic[CommandPrice.OPTION_VALUE_AMOUNT]
		valueOptionSymbolStr = commandDic[CommandPrice.OPTION_VALUE_SYMBOL]

		if resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE):
			if not resultData.containsWarning(resultData.WARNING_TYPE_OPTION_VALUE):
				# in case the value command generated a warning, if the value option refers a
				# currency different from the crypto, unit or fiat of the request, the fullCommandStr
				# remains None which results that it will not be stored in the request history list
				# of the GUI !
				valueOptionStr = ' -vs{}{}'.format(valueOptionAmountStr, valueOptionSymbolStr)
				fullCommandStrWithSaveOptionsForHistoryList = fullCommandStrNoOptions + valueOptionStr
				fullCommandStrForStatusBar = fullCommandStrWithSaveOptionsForHistoryList
		else:
			if valueOptionAmountStr and valueOptionSymbolStr:
				# even in case the value command generated a warning, it will be displayed in the
				# status bar !
				valueOptionStr = ' -v{}{}'.format(valueOptionAmountStr, valueOptionSymbolStr)
				fullCommandStrWithNoSaveOptions = fullCommandStrNoOptions + valueOptionStr
				fullCommandStrForStatusBar = fullCommandStrWithNoSaveOptions

		return fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar, valueOptionStr
	
	def _addOptionFiatInfo(self,
						   resultData,
						   commandDic,
						   valueOptionStr,
						   fiatOptionSymbol,
						   fullCommandStrNoOptions,
						   fullCommandStrWithNoSaveOptions,
						   fullCommandStrWithSaveOptionsForHistoryList,
						   fullCommandStrForStatusBar):
		"""
		Adds the fiat option information to
			1/ the request full command string with no save	option (result ex:
			   btc usd 12/09/17 00:00 bittrex -feur)
			2/ the request full command string with save option used to fill the GUI request
			   history list (result ex: btc usd 12/09/17 00:00 bittrex -fseur)
			3/ the request full command string  for status bar (result ex:
			   btc usd 12/09/17 00:00 bittrex -feur (4122 BTC/USD " 0.8346 USD/EUR = 3440.2212 BTC/EUR)
			
		If the valueOptionStr is not empty, it is added before the fiat option info.
		
		:param resultData: stores the on-line request results
		:param commandDic: stores the currently active command parms
		:param valueOptionStr: empty if no value option or contains the value option information
		:param fiatOptionSymbol:
		:param fullCommandStrNoOptions: contains the current request full command string without any option
		:param fullCommandStrWithNoSaveOptions: empty if no no save value option or contains the full command string
												with the no save value option information
		:param fullCommandStrWithSaveOptionsForHistoryList: empty if no save value option or contains the full command
															string with the save value option information
		:param fullCommandStrForStatusBar: empty if no value option (no save or save) or contains the request full
										   command string plus the value option for status bar.
										   Ex: btc usd 20/12/20 00:00 binance -v1500usd
										   
		:return: fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar
		"""
		if resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE):
			# save mode is active
			if not resultData.containsWarning(resultData.WARNING_TYPE_OPTION_VALUE):
				# in case the value command generated a warning, if the value option refers a
				# currency different from the crypto, unit or fiat of the request, the fullCommandStr
				# remains None which results that it will not be stored in the request history list
				# of the GUI !
				fiatOptionInfo = self._buildFiatOptionInfo(commandDic,
														   fiatOptionSymbol,
														   isOptionFiatSave=True)
				if fullCommandStrWithSaveOptionsForHistoryList:
					# case when option value exist and is in save mode
					fullCommandStrWithSaveOptionsForHistoryList += fiatOptionInfo
				else:
					# case when no option value exist in save mode
					fullCommandStrWithSaveOptionsForHistoryList = fullCommandStrNoOptions + fiatOptionInfo
				
				fullCommandStrForStatusBar = fullCommandStrNoOptions + valueOptionStr + fiatOptionInfo + \
											 self._buildUnitFiatComputationString(resultData)
		else:
			# save mode is not active
			fiatOptionInfo = self._buildFiatOptionInfo(commandDic,
													   fiatOptionSymbol,
													   isOptionFiatSave=False)
			if fullCommandStrWithNoSaveOptions:
				# case when option value exist and is not in save mode
				if fiatOptionSymbol:
					fullCommandStrWithNoSaveOptions += fiatOptionInfo
			else:
				# case when no option value exist
				if fiatOptionSymbol:
					fullCommandStrWithNoSaveOptions = fullCommandStrNoOptions + fiatOptionInfo
			
			fullCommandStrForStatusBar = fullCommandStrNoOptions + valueOptionStr + fiatOptionInfo + \
										 self._buildUnitFiatComputationString(resultData)

		return fullCommandStrWithNoSaveOptions, fullCommandStrWithSaveOptionsForHistoryList, fullCommandStrForStatusBar
	
	def _buildFiatOptionInfo(self,
							 commandDic,
							 fiatOptionSymbol,
							 isOptionFiatSave):
		"""

		:param commandDic:
		:param fiatOptionInfo: full command string with or without value option
		:param fiatOptionSymbol
		:param isOptionFiatSave

		:return:
		"""
		if isOptionFiatSave:
			fiatOptionStr = ' -fs{}'
		else:
			fiatOptionStr = ' -f{}'
		
		requestFiatExchange = commandDic[CommandPrice.OPTION_FIAT_EXCHANGE]
		
		if requestFiatExchange:
			fiatOptionInfo = (fiatOptionStr + '.{}').format(fiatOptionSymbol, requestFiatExchange)
		else:
			fiatOptionInfo = fiatOptionStr.format(fiatOptionSymbol)
		
		return fiatOptionInfo
	
	def _buildUnitFiatComputationString(self, resultData):
		priceStr = self._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_PRICE), self.PRICE_FLOAT_FORMAT)
		fiatComputedAmountStr = self._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT), self.PRICE_FLOAT_FORMAT)
		fiatRateStr = self._formatPriceFloatToStr(resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE), self.PRICE_FLOAT_FORMAT)
		cryptoUnitPair = '{}/{}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
										resultData.getValue(resultData.RESULT_KEY_UNIT))
		unitFiatPair = '{}/{}'.format(resultData.getValue(resultData.RESULT_KEY_UNIT),
									  resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
		cryptoFiatPair = '{}/{}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
									  resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))

		
		return '\n({} {} * {} {} = {} {})'.format(priceStr,
												  cryptoUnitPair,
												  fiatRateStr,
												  unitFiatPair,
												  fiatComputedAmountStr,
												  cryptoFiatPair)

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


if __name__ == '__main__':
	pr = GuiOutputFormatter()
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
