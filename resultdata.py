class ResultData:
	RESULT_KEY_CRYPTO = 'CRYPTO'
	RESULT_KEY_UNIT = 'UNIT'
	RESULT_KEY_EXCHANGE = 'EXCHANGE'
	RESULT_KEY_PRICE_TIME_STAMP = 'PRICE_TIMESTAMP'
	RESULT_KEY_PRICE_DATE_TIME_STRING = 'PRICE_DATE_TIME_STR'
	RESULT_KEY_PRICE = 'PRICE'
	RESULT_KEY_PRICE_TYPE = 'PRICE_TYPE'
	RESULT_KEY_ERROR_MSG = 'ERROR_MSG'
	RESULT_KEY_WARNINGS_DIC = 'WARNING_MSG'
	RESULT_KEY_INITIAL_COMMAND_PARMS = 'INIT_COMMAND_PARMS' # command parm dic denoting the user requesr

	RESULT_KEY_OPTION_VALUE_CRYPTO = 'OPTION_VALUE_CRYPTO'  # store the crypto price returned for -v option
	RESULT_KEY_OPTION_VALUE_UNIT = 'OPTION_VALUE_UNIT'      # store the unit price returned for -v option
	RESULT_KEY_OPTION_VALUE_FIAT = 'OPTION_VALUE_FIAT'      # store the fiat price returned for -v option
															# provided the -f fiat option is specified
	RESULT_KEY_OPTION_VALUE_SAVE = 'OPTION_VALUE_SAVE'      # store True or False to indicate if the value option is to be stored in history (-vs) or not (-v)

	RESULT_KEY_OPTION_FIAT_RATE = 'OPTION_FIAT_RATE'                      # store the unit to fiat exchange rate (ex: eth btc 0 all -fusd ==> btc/usd rate)
	RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT = 'OPTION_FIAT_COMPUTED_AMOUNT'# store the crypto price in unit converted to fiat returned for the -f option
	RESULT_KEY_OPTION_FIAT_SYMBOL = 'OPTION_FIAT_SYMBOL'                  # store the fiat symbol of the -f option
	RESULT_KEY_OPTION_FIAT_EXCHANGE = 'OPTION_FIAT_EXCHANGE'              # store the fiat exchange of the -f option
	RESULT_KEY_OPTION_FIAT_SAVE = 'OPTION_FIAT_SAVE'                      # store True or False to indicate if the fiat option is to be stored in history (-fs) or not (-f)

	RESULT_KEY_OPTION_PRICE_AMOUNT = 'OPTION_PRICE_AMOUNT'   # store the crypto/unit value the user entered for -p option. Ex: 0.1 if -p0.1btc
	RESULT_KEY_OPTION_PRICE_SAVE = 'OPTION_PRICE_SAVE'       # store True or False to indicate if the price option is to be stored in history (-ps) or not (-p)

	RESULT_KEY_OPTION_RESULT_COMPUTED_AMOUNT_UNIT = 'OPTION_RESULT_COMPUTED_AMOUNT_UNIT'    # store result computed amount in unit
	RESULT_KEY_OPTION_RESULT_COMPUTED_PERCENT_UNIT = 'OPTION_RESULT_COMPUTED_AMOUNT_UNIT'   # store result computed percent for unit
	RESULT_KEY_OPTION_RESULT_COMPUTED_AMOUNT_FIAT = 'OPTION_RESULT_COMPUTED_AMOUNT_FIAT'    # store result computed amount in fiat
	RESULT_KEY_OPTION_RESULT_COMPUTED_PERCENT_FIAT = 'OPTION_RESULT_COMPUTED_AMOUNT_FIAT'   # store result computed percent for fiat
	RESULT_KEY_OPTION_RESULT_SAVE = 'OPTION_RESULT_SAVE'                                    # store True or False to indicate if the result option is to be stored in history (-rs) or not (-r)

	
	RESULT_KEY_OPTION_LIMIT_AMOUNT = 'OPTION_LIMIT_AMOUNT'                              # store the value the user entered for -l option. Ex: 300 if -l300usd.kraken
	RESULT_KEY_OPTION_LIMIT_COMPUTED_UNIT_AMOUNT = 'OPTION_LIMIT_COMPUTED_UNIT_AMOUNT'  # store the limit in unit corresponding to the amount specified in the option synbol specified
																						# for the -l option. Ex: if crypto is eth and unit is btc and option is -l300usd,
																						# store the price in btc if 1 eth is 300 usd (see help for more info !)
	RESULT_KEY_OPTION_LIMIT_SYMBOL = 'OPTION_LIMIT_SYMBOL'      # store the currency symbol of the -l option. Ex: usd if -l300usd.kraken
	RESULT_KEY_OPTION_LIMIT_EXCHANGE = 'OPTION_LIMIT_EXCHANGE'  # store the limit exchange of the -l option. Ex: kraken if -l300usd.kraken
	RESULT_KEY_OPTION_LIMIT_SAVE = 'OPTION_LIMIT_SAVE'          # store True or False to indicate if the limit option is to be stored in history (-ls) or not (-l)

	WARNING_TYPE_FUTURE_DATE = 'FUTURE_DATE'    # signals that request date is in the future
	WARNING_TYPE_OPTION_VALUE = 'OPTION_VALUE'  # signals that value option currency not possible
	WARNING_TYPE_OPTION_PRICE = 'OPTION_PRICE'  # signals that option price not compatible with RT request
	WARNING_TYPE_OPTION_UNSUPPORTED = 'OPTION_UNSUPPORTED'

	PRICE_TYPE_HISTO_DAY = 'HISTO_DAY'
	PRICE_TYPE_HISTO_MINUTE = 'HISTO_MINUTE'
	PRICE_TYPE_RT = 'REAL_TIME'
	PRICE_TYPE_EFFECTIVE = 'EFFECTIVE' # buy or sell transaction price set by the -p price option

	def __init__(self, resultDataDic=None):
		if not resultDataDic:
			self._resultDataDic = {}
			self._resultDataDic[self.RESULT_KEY_CRYPTO] = None
			self._resultDataDic[self.RESULT_KEY_UNIT] = None
			self._resultDataDic[self.RESULT_KEY_EXCHANGE] = None
			self._resultDataDic[self.RESULT_KEY_PRICE_TIME_STAMP] = None
			self._resultDataDic[self.RESULT_KEY_PRICE_DATE_TIME_STRING] = None
			self._resultDataDic[self.RESULT_KEY_PRICE] = None
			self._resultDataDic[self.RESULT_KEY_PRICE_TYPE] = None
			self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None
			self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] = {}
			self._resultDataDic[self.RESULT_KEY_INITIAL_COMMAND_PARMS] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_CRYPTO] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_UNIT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_FIAT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_SAVE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_RATE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_SYMBOL] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_EXCHANGE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_SAVE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_PRICE_AMOUNT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_PRICE_SAVE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_RESULT_COMPUTED_AMOUNT_UNIT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_RESULT_COMPUTED_PERCENT_UNIT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_RESULT_COMPUTED_AMOUNT_FIAT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_RESULT_COMPUTED_PERCENT_FIAT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_RESULT_SAVE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_LIMIT_AMOUNT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_LIMIT_COMPUTED_UNIT_AMOUNT] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_LIMIT_SYMBOL] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_LIMIT_EXCHANGE] = None
			self._resultDataDic[self.RESULT_KEY_OPTION_LIMIT_SAVE] = None
		else:
			self._resultDataDic = resultDataDic

		self.requestInputString = ''
	
	def setValue(self, key, value):
		self._resultDataDic[key] = value


	def getValue(self, key):
		return self._resultDataDic[key]


	def setError(self, errorMessage):
		'''
		Set the error msg entry in the ResultData
		:param errorMessage:
		'''
		self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = errorMessage


	def getErrorMessage(self):
		'''
		Returns the error msg entry in the ResultData
		'''
		return self._resultDataDic[self.RESULT_KEY_ERROR_MSG]


	def noError(self):
		return self._resultDataDic[self.RESULT_KEY_ERROR_MSG] == None


	def containsWarning(self, warningType):
		'''
		Return True if the ResultData contains a warning msg
		'''
		warningDic = self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC]

		if warningDic == {}:
			return False
		else:
			return warningType in warningDic.keys()


	def containsWarnings(self):
		'''
		Return True if the ResultData contains a warning msg
		'''
		return self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] != {}


	def getWarningMessage(self, warningType):
		'''
		Return the warning msg contained in the ResultData
		:param warningType:
		'''
		return self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC][warningType]


	def setWarning(self, warningType, warningMessage):
		'''
		Set the warning msg entry in the ResultData
		:param warningType:
		'''
		warningsDic = self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC]
		warningsDic[warningType] = warningMessage


	def getAllWarningMessages(self):
		'''
		Return a list of warning messages.
		:return: list containing the warning msg strings
		'''

		return list(self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC].values())


	def __str__(self):
		strRepr = ''

		for key in self._resultDataDic.keys():
			val = self._resultDataDic.get(key)
			if val != None:
				strRepr += key + ': ' + str(val) + ' '
			else:
				strRepr += key + ': None '

		return strRepr

if __name__ == '__main__':
	pass
