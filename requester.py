import re
from commandprice import CommandPrice
from commanderror import CommandError
from datetimeutil import DateTimeUtil

CURRENCY_SYMBOL_MIN_LENGTH = 3


class Requester:
	'''
	Reads in commands entered by the
	user, typically
	
	oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave

	and return a command filled with the command parsed parm data
	
	:seqdiag_note Parses the user requests, storing the request parms into the the appropriate Command.
	'''

	ENTER_COMMAND_PROMPT = 'Enter command (h for help, q to quit)\n'

	'''
	oo open order
	xo closed order
	lo lowest order or order at lowest price
	ho highest order or ordedr at highest price
	ro range orders
	va variation percents
	'''
	USER_COMMAND_GRP_PATTERN = r"(OO|XO|LO|HO|RO|VA) "

	'''
	Full price command parms pattern. Crypto symbol (mandatory, first position mandatory), unit symbol (optional,
	if provided, must be in second position), date (optional), time (optional) and exchange (optional). The three
	last parms can be provided in any order after the 2 first parms !
	
	Additionally, 2 request commands can be added to the regular full command. For example -vs12btc.

	Ex; btc usd 0 Kraken
		btc usd 10/9/17 12:45 Kraken
		btc usd 10/9/17 Kraken
		btc usd 10/9 Kraken
		btc usd 0 Kraken -v0.01btc
		btc usd 10/9/17 12:45 Kraken -v0.01btc
		btc usd 10/9/17 Kraken -v0.01btc
		btc usd 10/9 Kraken -v0.01btc

	Additional rules for the date and time parms. Those rules are enforced by the
	_buildFullCommandPriceOptionalParmsDic() method.
	
	° 0 is legal for date and means now, real time !
	° Date must be 0 or contain a '/'.
	° Time must be composed of two numerical groups separated by ':', the second group being a 2 digits
	  group. Note 0:00 or 00:00 does not mean now, but midnight !
	° Exchange name must start with a letter. May contain digits.

	Ex:
	Date can be: 0, accepted.
				 1, rejected.
				 10, rejected.
				 01, rejected.
				 0/0, accepted.
				 01/0, accepted.
				 01/1, accepted.
				 01/10, accepted.
				 1/1, accepted.
				 1/10, accepted.
				 01/12/16, accepted.
				 01/12/2015, accepted.
				 01/12/0, accepted.
	Hour minute can be: 0, rejected.
						1, rejected.
						10, rejected.
						01, rejected.
						01:1, rejected.
						01:01, accepted.
						01:10, accepted.
						1:10, accepted.
						00:00, accepted.
						0:00, accepted.
						0:0, rejected.
	'''

#	PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA = r"(\w+)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.]+))?(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.]+))?"

	# pattern modified to enable handling erroneous option specification with no option
	# data like in full request eth btc 0 binance -v or -vs or -f or -fs
	#PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA = r"(\w+)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.]*))?(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.]*))?"
	
	# modifying the full request pattern to handle the new -r option. This
	# option can be -r, -rs, -r999.999, -rs999.999, -r-1, -rs-1, -r-1-2-3-n,
	# -rs-1-2-3-n, -r-1:-n, -rs-1:-n
	# Here are the pythex test strings used to validate the new pattern
	'''
	btc usd 12/2/21 13:55 hitbtc
	btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -ps52012.45 -r-2:-3
	btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs -ps52012.45
	btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1-2-3
	btc usd 12/2/21 13:55 hitbtc -ps52012.45 -vs21.23btc -fschf.kraken -rs-1:-3
	btc usd 12/2/21 13:55 hitbtc -vs21.23btc -rs-1:-3 -fschf.kraken
	btc usd 12/2/21 13:55 hitbtc -rs-1:-3 -vs21.23btc -ps52012.45 -fschf.kraken
	btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -rs-1

	Those requests are unit tested by TestRequester.test_parseGroupsFullVariousResultOptions().
	'''

	# The full price request pattern is configured to parse 5 required full request
	# parameters (crypto, unit, date, time and exchange) as well as a maximum of 4 options
	# (-v value, -f fiat, -p price, and -r result). Adding a fifth -l limit option to the
	# 4 options makes no sense, so a full price request pattern with 9 (5 + 4) groups instead
	# of 10 is ok !
	#
	# Ex of biggest full request:
	#
	# btc usd 12/2/21 13:55 hitbtc -vs21.23btc -fschf.kraken -ps52012 -r-1-2
	PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA = r"(\w+)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: ([\w/:]+)|)(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.-]*))?(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.-]*))?(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.-]*))?(?: (-[a-zA-Z][a-zA-Z]?[\w/:\.-]*))?"

	'''
	Partial price command parms pattern. Grabs groups of kind -cbtc or -t12:54 or -d15/09 or -ebittrex
	or option groups sticking to the same format -<command letter> followed by 1 or
	more \w or \d or /. or - or : characters.

	Unlike with pattern 'full', the groups - option or not - can all occur in any order, reason for which
	all groups have the same pattern structure.
 
	The rules below apply to -d and -t values !
	
	Date can be: 0, accepted.
				 1, accepted.
				 10, accepted.
				 01, accepted.
				 01/0, accepted.
				 01/1, accepted.
				 01/10, accepted.
				 0/0, accepted.
				 1/0, accepted.
				 1/1, accepted.
				 1/10, accepted.
				 01/12/16, accepted.
				 01/12/2015, accepted.
				 01/12/0, accepted.
				 1 12:45, accepted.
	Hour minute can be: 0, rejected.
						1, rejected.
						10, rejected.
						01, rejected.
						01:1, accepted.
						01:01, accepted.
						01:10, accepted.
						1:10, accepted.
						00:00, accepted.
						0:00, accepted.
						0:0, accepted.
	'''
#	PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-[a-zA-Z])([\w/:\.]*))(?: (-[a-zA-Z])([\w/:\.]*))?(?: (-[a-zA-Z])([\w/:\.]*))?(?: (-[a-zA-Z])([\w/:\.]*))?(?: (-[a-zA-Z])([\w/:\.]*))?(?: (-[a-zA-Z])([\w/:\.]*))?(?: (-[a-zA-Z])([\w/:\.]*))?(?: (-[a-zA-Z])([\w/:\.]*))?"

	# The partial price request pattern is configured to parse a maximum of 9 parameters,
	# 5 basic request parameters (-c, -u, -d, -t and -e) and a maximum of 4 options,
	# (-v, -f, -p and -r). Adding a fifth limit -l option to the 4 options makes
	# no sense, so a partial price request pattern with 9 (5 + 4) groups instead of 10 is ok !
	#
	# The partial request specifications can be in any order.
	#
	# Ex: -ceth -ueur -d1 -t12:45 -ebittrex -vs34usd -fschf.kraken -rs-1:-2 -ebittrex -p1450
	PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-[a-zA-Z])([\w/:\.-]*))(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?(?: (-[a-zA-Z])([\w/:\.-]*))?"
	PATTERN_PARTIAL_PRICE_REQUEST_ERROR = r"({}([\d\w,\./]*))(?: .+|)"

	'''
	The next pattern splits the parameter data appended to the -v partial command option.
	
	Ex: -vs0.004325btc is splitted into 's', '0.00432', 'btc', None
		-v0.004325btc is splitted into '', '0.00432', 'btc', None
		-v0 is splitted into None, None, None, '0' and will mean 'erase previous -v parm specification
	'''
	OPTION_VALUE_PARM_DATA_PATTERN = r"([sS]?)([\d\.]+)(\w+)|(0)"

	'''
	The next pattern splits the parameter data appended to the -f partial command option.

	Ex: -fsusd.kraken is splitted into 's', 'usd', 'kraken', None
		-fusd.kraken is splitted into '', 'usd', 'kraken', None
		-fusd is splitted into '', 'usd', None, None
		-f0 is splitted into None, None, None, '0' and will mean 'erase previous -f parm
		specification
	'''
	OPTION_FIAT_PARM_DATA_PATTERN = r"(?:([sS]?)([a-zA-Z]+)(?:(?:\.)(\w+))?)|(0)"
	
	'''
	The next pattern splits the parameter data appended to the -p partial command option.

	Ex: -ps0.004325 is splitted into 's', '0.00432'
		-p0.004325 is splitted into '', '0.00432'
		-ps0.004325usd is splitted into '', '0.00432usd'    this invalid -ps option will generate an error msg
		-p0.004325usd is splitted into '', '0.00432usd'     this invalid -p option will generate an error msg
		-p0 is splitted into '', '0' and will mean 'erase previous -p parm specification
	'''
#	OPTION_PRICE_PARM_DATA_PATTERN = r"(?:([sS]?)([\d\.]+))"
	OPTION_PRICE_PARM_DATA_PATTERN = r"(?:([sS]?)([\w\.]*))" # \w instead of \d enables the generation
															 # of an error msg if a fiat symbol is appended
															 # to the price amount !
															 # uaing * insteadof + makes the generic
															 # Requester._validateOptionMandatoryComponents()
															 # method usefull

	'''
	The next pattern splits the parameter data appended to the -r partial command option.
	
	Ex: -rs is splitted into '', '', None   save option modifier is set to 's' in self._extractData()
		-r  is splitted into '', '', None   save option modifier is set to 's' in self._extractData()
		-rs-1 is splitted into '', '-1', None  save option modifier is set to 's' in self._extractData()
		-rs-1-2-3 is splitted into '', '-1-2-3', None  save option modifier is set to 's' in self._extractData()
		-r-1-2-3 is splitted into '', '-1-2-3', None
		-rs-1:-3 is splitted into '', '-1:-3', None  save option modifier is set to 's' in self._extractData()
		-r-1:-3 is splitted into '', '-1:-3', None
		-r0 is splitted into '', '0', None and will mean 'erase previous -r parm specification
	'''
#	OPTION_RESULT_PARM_DATA_PATTERN = r"([sS]?)([\d\.:-]+)|(0)"
#	OPTION_RESULT_PARM_DATA_PATTERN = r"([sS]?)([\d\.:-]+)|(s)"
	OPTION_RESULT_PARM_DATA_PATTERN = r"([sS]?)([\d\.:-]*)|(s)"

	'''
	The next pattern splits the parameter data appended to the -l partial command option.

	Ex: -ls16500usd.kraken is splitted into 's', '16500', 'usd', 'kraken', None
		-l16500usd.kraken is splitted into '', '16500', 'usd', 'kraken', None
		-l16500usd is splitted into '', '16500', 'usd', None, None
		-l0 is splitted into None, None, None, None, '0' and will mean 'erase previous -l parm
		specification
	'''
	OPTION_LIMIT_PARM_DATA_PATTERN = r"([sS]?)([\d\.]+)(\w+)(?:(?:\.)(\w+))?|(0)"

	REQUEST_TYPE_PARTIAL = 'PARTIAL'
	REQUEST_TYPE_FULL = 'FULL'

	def __init__(self, configMgr):
		self.configMgr = configMgr
		self.commandQuit = None
		self.commandError = None
		self.commandPrice = None
		self.commandCrypto = None
		self.commandTrade = None

		'''
		Sets correspondance between user input command parms and
		CommmandPrice.parsedParmData dictionary keys
		'''
		self.inputParmParmDataDicKeyDic = {'-C': CommandPrice.CRYPTO,
										   '-U': CommandPrice.UNIT,
										   '-D': CommandPrice.DAY_MONTH_YEAR,
										   '-T': CommandPrice.HOUR_MINUTE,
										   '-E': CommandPrice.EXCHANGE,
										   '-V': CommandPrice.OPTION_VALUE_DATA,
										   '-F': CommandPrice.OPTION_FIAT_DATA,
										   '-P': CommandPrice.OPTION_PRICE_DATA,
										   '-R': CommandPrice.OPTION_RESULT_DATA,
										   '-L': CommandPrice.OPTION_LIMIT_DATA}


	def getCommandFromCommandLine(self):
		"""
		Used essentially by the command line version of CryptoPricer.
		"""
		inputStr = input(Requester.ENTER_COMMAND_PROMPT)
		upperInputStr = inputStr.upper()

		while upperInputStr == 'H':
			self._printHelp()
			inputStr = input(Requester.ENTER_COMMAND_PROMPT)
			upperInputStr = inputStr.upper()
		
		if upperInputStr == 'Q':
			return self.commandQuit
		else: #here, neither help nor quit command entered. Need to determine which command
			  #is entered by the user finding unique pattern match that identify this command
			return self.getCommand(inputStr)


	def getCommand(self, inputStr):
		"""
		Used by the gui version of CryptoPricer.
		
		Parses the passed input string and return a Command concrete instance
		filled with the command specific data. May return a CommandError.
		
		:param inputStr: input string to parse
		:seqdiag_return AbstractCommand
		:seqdiag_return_note May return a CommandError in case of parsing problem.
		:return: Command concrete instance
		"""

		returnedCommand = None

		if inputStr == '' and self.commandPrice.isValid():
			#here, user entered RETURN to replay the last commannd
			self._alignCommandPriceDateTimeDataWithPriceType()
			
			# ensuring that no unsupported option is in effect which would cause
			# a warning to disturb the replay of the previous request execution.
			self.commandPrice.resetUnsupportedOptionData()
			returnedCommand = self.commandPrice
		else:
			upperInputStr = inputStr.upper()
			match = self._tryMatchCommandSymbol(upperInputStr)

			if match == None:
				#here, either full or partial historical/RT price request which has no command symbol
				#or user input error
				command = self._parseAndFillCommandPrice(inputStr)
				if command == self.commandPrice or command == self.commandError:
					returnedCommand = command
				else:
					# here, either invalid historical/RT price request which has no command symbol (for ex -t alone)
					# or other request with missing command symbol (for ex [btc 05/07 0.0015899] [usd-chf] -nosave)
					if '[' in inputStr:
						# command symbol missing
						self.commandError.parsedParmData[
							self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_INVALID_COMMAND
						self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.USER_COMMAND_MISSING_MSG

					else:
						# invalid partial command parm
						self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
						self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_MSG_KEY] = ''

					returnedCommand = self.commandError
			else:
				userCommandSymbol = match.group(1)

				if userCommandSymbol == "OO":
					upperInputStrWithoutUserCommand = upperInputStr[len(userCommandSymbol) + 1:]
					cryptoDataList, unitDataList, flag = self._parseOOCommandParms(inputStr, upperInputStrWithoutUserCommand)

					if cryptoDataList == self.commandError:
						returnedCommand = self.commandError
					else:
						self.commandCrypto.parsedParmData = {self.commandCrypto.CRYPTO_LIST : cryptoDataList, \
															 self.commandCrypto.UNIT_LIST : unitDataList, \
															 self.commandCrypto.FLAG : flag}

						returnedCommand = self.commandCrypto
				else:
					self.commandError.parsedParmData[
						self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_INVALID_COMMAND
					self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.USER_COMMAND_MISSING_MSG

					returnedCommand = self.commandError

		returnedCommand.requestInputString = inputStr

		return returnedCommand


	def _alignCommandPriceDateTimeDataWithPriceType(self):
		if self.commandPrice.parsedParmData[self.commandPrice.PRICE_TYPE] == self.commandPrice.PRICE_TYPE_RT:
			self.commandPrice.parsedParmData[self.commandPrice.YEAR] = '0'
			self.commandPrice.parsedParmData[self.commandPrice.MONTH] = '0'
			self.commandPrice.parsedParmData[self.commandPrice.DAY] = '0'
			self.commandPrice.parsedParmData[self.commandPrice.HOUR] = None
			self.commandPrice.parsedParmData[self.commandPrice.MINUTE] = None


	def _tryMatchCommandSymbol(self, upperInputStr):
		'''
		Try matching a command symbol like OO|XO|LO|HO|RO|VA in the command entered by the user.
		If the user entered a price command, no command symbol is used !
		:param upperInputStr:
		:return: None or a Match object
		'''
		return re.match(Requester.USER_COMMAND_GRP_PATTERN, upperInputStr)


	def _parseGroups(self, pattern, inputStr):
		'''
		Embedding this trivial code in a method enables to specifically test the correct
		functioning of the used patterns.

		:param pattern:     pattern to parse
		:param inputStr:    string to parse
		:return:
		'''
		match = re.match(pattern, inputStr)

		if match != None:
			return match.groups()
		else:
			return () # returning () instead of none since an iterator will be activated
					  # on the returned result !

	def _buildFullCommandPriceOrderFreeParmsDic(self, orderFreeParmList):
		'''
		This method is called only on full requests. A full request starts with 2 mandatory parameters,
		CRYPTO and UNIT provided in this mandatory order. The other full request mandatory parameters,
		date, time and exchange can be specified in any order. A full request can be ended by options
		whose order	is free as well.

		The purpose of this method is precisely to acquire the order free full request parameters.

		Since DAY_MONTH_YEAR, HOUR_MINUTE, EXCHANGE and additional OPTIONS can be provided in any order
		after CRYPTO and UNIT, this method differentiate them and build an order free command price parm
		data dictionary with the right key. This dictionary will then be added to the CommandPrice parmData
		dictionary.

		:seqdiag_return optionalParsedParmDataDic

		:param orderFreeParmList: contains the request parms entered after the CRYPTO and UNIT
								  specification aswell as any request option (namely -v, -f or -p).
		:return optionalParsedParmDataDic or None in case of syntax error.
		'''

		'''
		° 0 is legal for both date and time parms. Zero for either date or/and time means now, real time !
		° Date must be 0 or contain a '/'.
		° Time must be composed of two numerical groups separated by ':', the second group being a 2 digits
		  group. Note 00:00 does not mean now, but midnight !
		° Exchange name must start with a letter. May contain digits.

		Ex:
		Date can be 0, accepted. 1, rejected. 10, rejected. 01, rejected. 01/1, accepted. 01/10, accepted.
					1/1, accepted. 1/10, accepted. 01/12/16, accepted. 01/12/2015, accepted.
		Hour minute can be 0, rejected. 1, rejected. 10, rejected. 01, rejected. 01:1, rejected. 01:01, accepted.
						   01:10, accepted. 1:10, accepted. 00:00, accepted. 0:00, accepted. 0:0, rejected.
		'''

		OPTION_MODIFIER = 'optionModifier'
		UNSUPPORTED_OPTION = 'unsupportedOption'

		# changed r"\d+/\d+(?:/\d+)*|^0$" into r"\d+/\d+(?:/\d+)*|^\d+$" was required so
		# that a full request like btc usd 1 12:45 bitfinex does generate an ERROR - date not valid
		# in CommandPrice. With the old version of the pattern, CommandPrice.DAY_MONTH_YEAR was none,
		# which was considered like a valid full request with only the time provided, a feature which
		# was not supported before !
		#
		# So, allowing the user to provide only the time in the full request implied that we are
		# more permissive at the level of the Requester in order for CommandPrice to be able
		# to correctly identify the invalid date/time full request component in the form of
		# D HH:MM or DD HH:MM
		# pattern modified to enable handling erroneous option specification with no option
		# data like in full request eth btc 0 binance -v or -vs or -f or -fs
		patternCommandDic = {r"\d+/\d+(?:/\d+)*|^\d+$" : CommandPrice.DAY_MONTH_YEAR,
							 r"\d+:\d\d" : CommandPrice.HOUR_MINUTE,
							 r"[A-Za-z]+": CommandPrice.EXCHANGE,
							 r"(?:-[vV])([sS]?)([\w\.]*)": CommandPrice.OPTION_VALUE_DATA,
							 r"(?:-[vV])([sS]?)([\w\.]*)" + OPTION_MODIFIER: CommandPrice.OPTION_VALUE_SAVE,
							 r"(?:-[fF])([sS]?)([\w\.]*)": CommandPrice.OPTION_FIAT_DATA,
							 r"(?:-[fF])([sS]?)([\w\.]*)" + OPTION_MODIFIER: CommandPrice.OPTION_FIAT_SAVE,
							 r"(?:-[pP])([sS]?)([\w\.]*)": CommandPrice.OPTION_PRICE_DATA, # \w instead of \d enables the generation
															                               # of an error msg if a fiat symbol is appended
																						   # to the price amount !
							 r"(?:-[pP])([sS]?)([\w\.]*)" + OPTION_MODIFIER: CommandPrice.OPTION_PRICE_SAVE,
							 r"(?:-[rR])([sS]?)([\w\.:-]*)": CommandPrice.OPTION_RESULT_DATA,
							 r"(?:-[rR])([sS]?)([\w\.:-]*)" + OPTION_MODIFIER: CommandPrice.OPTION_RESULT_SAVE,
							 r"(?:-[lL])([sS]?)([\w\.]*)": CommandPrice.OPTION_LIMIT_DATA,
							 r"(?:-[lL])([sS]?)([\w\.]*)" + OPTION_MODIFIER: CommandPrice.OPTION_LIMIT_SAVE,
							 r"(-[^vVfFpPrRlL]{1})([sS]?)([\w\.]*)": CommandPrice.UNSUPPORTED_OPTION_DATA, # see scn capture https://pythex.org/ in Evernote for test of this regexp !
							 r"(-[^vVfFpPrRlL]{1})([sS]?)([\w\.]*)" + UNSUPPORTED_OPTION: CommandPrice.UNSUPPORTED_OPTION, # see scn capture https://pythex.org/ in Evernote for test of this regexp !
							 r"(-[^vVfFpPrRlL]{1})([sS]?)([\w\.]*)" + OPTION_MODIFIER: CommandPrice.UNSUPPORTED_OPTION_MODIFIER,}
		
		orderFreeParmList = list(orderFreeParmList)
		orderFreeParsedParmDataDic = {}
		
		# it does not make sense to parse the order free full request parms with a pattern combined with
		# OPTION_MODIFIER string !
		patternCommandDicKeysWithoutModifier = [x for x in patternCommandDic.keys() if OPTION_MODIFIER not in x]

		for pattern in patternCommandDicKeysWithoutModifier:
			for orderFreeParm in orderFreeParmList:
				if orderFreeParm and re.search(pattern, orderFreeParm):
					parsedParmDataDicKey = patternCommandDic[pattern]
					if parsedParmDataDicKey not in orderFreeParsedParmDataDic:
						# if for example DMY already found in optional full command parms,
						# it will not be overwritten ! Ex: 12/09/17 0: both token match DMY
						# pattern !
						data, option, optionModifier = self._extractData(pattern, orderFreeParm)
						if data != None:
							orderFreeParsedParmDataDic[parsedParmDataDicKey] = data
							patternOptionModifierKey = pattern + OPTION_MODIFIER
							if optionModifier != None and optionModifier != '':
								optionModifierParsedParmDataDicKey = patternCommandDic[patternOptionModifierKey]
								orderFreeParsedParmDataDic[optionModifierParsedParmDataDicKey] = optionModifier
							# elif patternOptionModifierKey in orderFreeParsedParmDataDic.keys():
							# This situation never happens when handling full request ! In fact,
							# orderFreeParsedParmDataDic is initialized to [] at the beginning of the method.
							# 	optionModifierParsedParmDataDicKey = patternCommandDic[patternOptionModifierKey]
							# 	orderFreeParsedParmDataDic[optionModifierParsedParmDataDicKey] = None
							orderFreeParmList.remove(orderFreeParm)
							if option:
								# here, handling an unsupported option. If handling a supported option, option
								# is None. For valid options, the correct option symbol will be set later in the
								# command price in _fillOptionValueInfo() like methods !
								patternUnsupportedOptionKey = pattern + UNSUPPORTED_OPTION
								orderFreeParsedParmDataDic[patternCommandDic[patternUnsupportedOptionKey]] = option
						else:
							#full command syntax error !
							return None


		from seqdiagbuilder import SeqDiagBuilder
		SeqDiagBuilder.recordFlow()

		return orderFreeParsedParmDataDic

	def _extractData(self, pattern, dataOrOptionStr):
		'''
		Applies the passed pattern to the passed dataOrOptionStr. If the passed dataOrOptionStr
		is an option of type -v0.1btc or -vs0.1btc, the passed pattern will extract the data part of the
		dataOrOptionStr, i.e. 0.01btc in this case and the option modifier part of the dataOrOptionStr,
		i.e. s in this case. The option itself is not extracted here since the pattern ignores the
		option symbol (like (?:-[vV]) in (?:-[vV])([sS]?)([\\w\\.]* for value option pattern. The option
		symbol will be set later in the command price in _fillOptionValueInfo() like methods !

		Else if the dataOrOptionStr does contain data only, without an option symbol, the passed
		pattern does not extract any group and the data is returned as is.

		:param pattern:
		:param dataOrOptionStr:
		:return: passed data or data part of the passed option + data aswell as the option modifier.
				 If -v0.1btc is passed as dataOrOptionStr, 0.1btc is returned. If -vs0.1btc is passed as
				 dataOrOptionStr, 0.1btc and s is returned.

				 In case of syntax error, None is returned
		'''
		match = re.match(pattern, dataOrOptionStr)

		if match == None:
			#denotes a syntax error !
			return None, None, None

		option = None
		optionModifier = None
		grpNumber = len(match.groups())

		if grpNumber == 1:
			data = match.group(1)
		elif grpNumber == 2:
			optionModifier = match.group(1)
			data = match.group(2)
		elif grpNumber == 3:
			# here, handling an unsupported option. If handling a supported option, option
			# is None. For valid options, the correct option symbol will be set later in the
			# command price in _fillOptionValueInfo() like methods !
			option = match.group(1)
			optionModifier = match.group(2)
			data = match.group(3)
		else:
			data = dataOrOptionStr

		return data, option, optionModifier

	def _parseAndFillCommandPrice(self, inputStr):
		'''
		This method parses either a full or a partial request.
		
		Here are 2 examples of a full request, one without any option and the second
		with 2 options:
		
		eth btc 0 binance
		eth btc 10/2/21 10:35 bittrex -v2eth -fusd.kraken
		
		The method first try to parse a full request. If no list of request elements was
		returned by the	parsing, it then try to parse a partial request.

		Here are 2 examples of a partial request, one with 1 option and the second
		with 2 options:
		
		-ebitfinex
		-d11/2 -fchf.kraken
		
		:param inputStr:
		:seqdiag_return CommandPrice or CommandError
		:return: self.commandPrice or self.commandError or None, which will cause an error to be raised
		'''
		# First, try to parse a full request partialRequestStr
		groupList = self._parseGroups(self.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

		if groupList == ():
			# Second, as full request pattern was not matched, try to parse a partial request partialRequestStr
			groupList = self._parseGroups(self.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)
			if groupList != ():
				# Partial request entered. Here, parm values are associated to parm tags
				# (i.e -c or -d). This means they have been entered in any order and are all
				# optional. Ensuring command price temporary data like unsupported command data
				# from the previous request are purged is necessary here when handling a partial
				# command(s) since, unlike when a full command is processed, the command price is not
				# reinitialized ! Otherwise, a warning signaling that an unsupported option is in
				# effect would be displayed in case such unsupported option was part of the preceeding
				# full or partial request !
				requestType = self.REQUEST_TYPE_PARTIAL
				
				# ensuring that no unsupported option is in effect which would cause
				# a warning to disturb the partial request execution.
				self.commandPrice.resetUnsupportedOptionData()

				keys = self.inputParmParmDataDicKeyDic.keys()
				it = iter(groupList)

				for command in it:
					value = next(it)
					if value != None:
						value = value
						commandUpper = command.upper()
						if commandUpper in keys:
							if value == '' or value.upper() == 'S':
								invalidPartialCommand, invalidValue = self._wholeParmAndInvalidValue(command, inputStr)
								self.commandError.parsedParmData[
									self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
								self.commandError.parsedParmData[
									self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.PARTIAL_REQUEST_EMPTY_VALUE_MSG.format(
									invalidPartialCommand, invalidPartialCommand)
								
								# remove invalid '' value from parsedParData to avoid polluting next partial
								# request !
								self.commandPrice.parsedParmData[self.inputParmParmDataDicKeyDic[commandUpper]] = None

								return self.commandError
							else:
								self.commandPrice.parsedParmData[self.inputParmParmDataDicKeyDic[commandUpper]] = value
						else:
							# unknown partial command symbol
							self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION] = command
							if value != '' and value[0].upper() == 'S':
								self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_DATA] = value[1:]
								self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_MODIFIER] = value[0]
							else:
								self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_DATA] = value
								self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_MODIFIER] = None


				if self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] == '0':
					# -d0 which means RT entered. In this case, the previous
					# date/time info are no longer relevant and must be erased!
					self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_RT
					hourMinute, dayMonthYear = self._wipeOutDateTimeInfoFromCommandPrice()
				elif self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] == None and self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] == None:
					# here, partial command(s) which aren't date/time related were entered: the previous request price type must be considered !
					if self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_RT:
						hourMinute, dayMonthYear = self._wipeOutDateTimeInfoFromCommandPrice()
					else:
						# here, since previous request was not RT, hourMinute and dayMonthYear must be rebuilt
						# from the date/time values of the previous request. Don't forget that OAY_MONTH_YEAR
						# and HOUR_MINUTE are set to None once date/time values have been acquired !
						if self._isMinimalDateTimeInfoFromPreviousRequestAvailable():
							dayMonthYear, hourMinute = self._rebuildPreviousRequestDateTimeValues()
						elif self._isPreviousFullRequestActive():
							return None # will cause an error. This occurs in a special situation when the previous request
										# was in error, which explains why the date/time info from previous request is
										# incoherent. Such a case is tested by TestController.
										# testControllerHistoDayPriceIncompleteCommandScenario
						else:
							# here, a partial request was entered before submitting any full request
							self.commandError.parsedParmData[
								self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST_WITH_NO_PREVIOUS_FULL_REQUEST
							
							# ensuring no previous error msg info are in effect which would pollute this error msg
							self.commandError.parsedParmData[
								self.commandError.COMMAND_ERROR_MSG_KEY] = ''
							
							return self.commandError
				else:
					# here, either commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
					# or commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] or both are
					# not None. Since the -d partial request value can be -d21/2/20 13:05,
					# which could not be parsed by the
					# self._parseGroups(self.PATTERN_PARTIAL_PRICE_REQUEST_DATA, partialRequestStr)
					# above, we have to try to extract a DMY and HM date/time value from the
					# partialRequestStr in case the -d partial request did contain a time element
					dayMonthYear, hourMinute = self._tryExtractDateTimeValueFromPartialRequest(inputStr)
					if dayMonthYear is None and hourMinute is None:
						# here, partial request -d contained no time value and so was parsed
						# by self._parseGroups(self.PATTERN_PARTIAL_PRICE_REQUEST_DATA, partialRequestStr)
						# above
						dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
						hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
			else: #neither full nor parrial pattern matched
				return None # will cause an error.
		else:
			# full request entered. Here, request parms were entered in an order reflected in the
			# pattern: crypto unit in this mandatory order, then date time exchange and options,
			# which can be entered in any order.
			requestType = self.REQUEST_TYPE_FULL
			self.commandPrice._initialiseParsedParmData()
			self.commandPrice.parsedParmData[CommandPrice.CRYPTO] = groupList[0] #mandatory crrypto parm, its order is fixed
			self.commandPrice.parsedParmData[CommandPrice.UNIT] = groupList[1] #mandatory unit parm, its order is fixed
			orderFreeParmDic = self._buildFullCommandPriceOrderFreeParmsDic(groupList[2:])

			if orderFreeParmDic != None:
				self.commandPrice.parsedParmData.update(orderFreeParmDic)
			else:
				# invalid full command format
				self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_FULL_REQUEST

				return self.commandError

			hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
			dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
			
		if hourMinute != None:
			hourMinuteList = hourMinute.split(':')
			if len(hourMinuteList) == 1:
				# supplied time is invalid: does not respect expected format of 0:10 or 12:01 etc
				# invalid time partial command format
				invalidPartialCommand, invalidValue = self._wholeParmAndInvalidValue('-t', inputStr)
				dtFormatDic = DateTimeUtil.getDateAndTimeFormatDictionary(self.configMgr.dateTimeFormat)
				timeFormat = dtFormatDic[DateTimeUtil.TIME_FORMAT_KEY]
				self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
				self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.PARTIAL_PRICE_COMMAND_TIME_FORMAT_INVALID_MSG.format(invalidPartialCommand, invalidValue, timeFormat)

				# remove invalid time specification from parsedParData to avoid polluting next partial
				# request !
				self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] = None

				return self.commandError
			else:
				minute = hourMinuteList[1]
				hour = hourMinuteList[0] #in both cases, first item in hourMinuteList is hour
		else:
			hour = self.commandPrice.parsedParmData[CommandPrice.HOUR]
			minute = self.commandPrice.parsedParmData[CommandPrice.MINUTE]

		self._fillHourMinuteInfo(hour, minute)

		if dayMonthYear != None:
			if dayMonthYear == '0':
				day = '0'
				month = '0'
				year = '0'
				self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_RT
			else:
				dayMonthYearList = dayMonthYear.split('/')
				if len(dayMonthYearList) == 1: #only day specified, the case for -d12 for example (12th of current month)
					day = dayMonthYearList[0]
					if CommandPrice.DAY in self.commandPrice.parsedParmData:
						month = self.commandPrice.parsedParmData[CommandPrice.MONTH]
						year = self.commandPrice.parsedParmData[CommandPrice.YEAR]
					else:
						month = None
						year = None
					self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_HISTO
				elif len(dayMonthYearList) == 2:
					day = dayMonthYearList[0]
					month = dayMonthYearList[1]
					if CommandPrice.YEAR in self.commandPrice.parsedParmData:
						year = self.commandPrice.parsedParmData[CommandPrice.YEAR]
					else:   # year not provided and not obtained from previous full price command input.
							# Will be set by PriceRequester which knows in which timezone we are
						year = None
					self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_HISTO
				elif len(dayMonthYearList) == 3:
					day = dayMonthYearList[0]
					month = dayMonthYearList[1]
					year = dayMonthYearList[2]
					self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_HISTO
				else: #invalid date format here !
					if CommandPrice.DAY in self.commandPrice.parsedParmData:
						day = self.commandPrice.parsedParmData[CommandPrice.DAY]
						month = self.commandPrice.parsedParmData[CommandPrice.MONTH]
						year = self.commandPrice.parsedParmData[CommandPrice.YEAR]
					else:
						day = None
						month = None
						year = None
		else:
			if CommandPrice.DAY in self.commandPrice.parsedParmData:
				day = self.commandPrice.parsedParmData[CommandPrice.DAY]
				month = self.commandPrice.parsedParmData[CommandPrice.MONTH]
				year = self.commandPrice.parsedParmData[CommandPrice.YEAR]

				if day == '0' and month == '0' and year == '0':
					self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_RT
				else:
					self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_HISTO
			else:
				day = None
				month = None
				year = None

		self._fillDayMonthYearInfo(day, month, year)

		command = None

		for optionType in CommandPrice.OPTION_TYPE_LIST:
			commandPriceOptionDataConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_DATA')
			optionData = self.commandPrice.parsedParmData[commandPriceOptionDataConstantValue]
			if optionData is not None:
				# optionData is None if the full request has no option for this option type
				# optionData == '' if the full request has an option with no data.
				# For example eth btc 0 binance -v or eth btc 0 binance -vs
				command = self._fillOptionValueInfo(optionType, optionData, requestType)
				if isinstance(command, CommandError):
					# in case an error was detected, we do not continue handling the options
					break

		if command:
			return command
		else:
			# here, no option -v, -f or -p specified !
			return self.commandPrice
	
	def _tryExtractDateTimeValueFromPartialRequest(self, partialRequestStr):
		"""
		Handles a -d partial request containing time component which could not
		be parsed sooner.
		
		:param partialRequestStr: partial request string
		
		:return: None, None if no time value or date and time components otherwise
		"""
		dateTimePattern = r"-d(\d+/\d+/\d+ \d+:\d+)|-d(\d+/\d+ \d+:\d+)|-d(\d+ \d+:\d+)|-d(\d+/\d+/\d+)|-d(\d+/\d+)|^-d(\d+)"
		dateTimeInputStr = ''

		for grps in re.finditer(dateTimePattern, partialRequestStr):
			for elem in grps.groups():
				if elem is not None:
					dateTimeInputStr = elem
		if ':' in dateTimeInputStr:
			dateTimeValueLst = dateTimeInputStr.split(' ')
			dayMonthYear = dateTimeValueLst[0]
			hourMinute = dateTimeValueLst[1]
			return dayMonthYear, hourMinute
		else:
			return None, None
	
	def _isPreviousFullRequestActive(self):
		"""
		Checks if a full request was entered before the currently handled partial request.
		Returns True if yes, False otherwise.
		
		:return: True or False
		"""
		return self.commandPrice.parsedParmData[CommandPrice.CRYPTO] and \
			   self.commandPrice.parsedParmData[CommandPrice.UNIT] and \
			   self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] and \
			   self.commandPrice.parsedParmData[CommandPrice.EXCHANGE]
			

	def _rebuildPreviousRequestDateTimeValues(self):
		hour = self.commandPrice.parsedParmData[CommandPrice.HOUR]
		minute = self.commandPrice.parsedParmData[CommandPrice.MINUTE]

		if hour and minute:
			hourMinute = hour + ':' + minute
		else:
			hourMinute = None

		year = self.commandPrice.parsedParmData[CommandPrice.YEAR]

		if year:
			dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY] + '/' + \
						   self.commandPrice.parsedParmData[CommandPrice.MONTH] + '/' + year
		else:
			dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY] + '/' + \
						   self.commandPrice.parsedParmData[CommandPrice.MONTH]

		return dayMonthYear, hourMinute


	def _fillHourMinuteInfo(self, hour, minute):
		'''
		Fill parsed parm data hour and minute fields and empty combined hour/minute field
		:param hour:
		:param minute:
		:return:
		'''
		self.commandPrice.parsedParmData[CommandPrice.HOUR] = hour
		self.commandPrice.parsedParmData[CommandPrice.MINUTE] = minute
		self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] = None


	def _fillDayMonthYearInfo(self, day, month, year):
		'''
		Fill parsed parm data day, month and year fields and empty combined daa/month/year field
		:param day:
		:param month:
		:param year:
		:return:
		'''
		self.commandPrice.parsedParmData[CommandPrice.DAY] = day
		self.commandPrice.parsedParmData[CommandPrice.MONTH] = month
		self.commandPrice.parsedParmData[CommandPrice.YEAR] = year
		self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None


	def _fillOptionValueInfo(self, optionType, optionData, requestType):
		'''
		This method is called in case of both full and partial request handling in order to
		complete filling the option value info in the CommandPrice parsed parm data dictionary.
		It fills the parsed parm data option value amount and option value symbol fields and
		erases the combined option value data field.

		:param optionData: the data following the -v partial command specification
		:param requestType: indicate if we are handling a full or a partial request
		:return: self.commandPrice or self.commandError in case the -v option is invalid
		'''
		optionSaveFlag = None
		optionErase = None
		optionSymbol = None
		optionAmount = None

		requesterOptionPattern = self._getRequesterOptionPattern(optionType)

		match = re.match(requesterOptionPattern, optionData)

		if match:
			# if len(match.groups()) == 5:
			# 	# case if OPTION_FIAT_PARM_DATA_PATTERN or OPTION_PRICE_PARM_DATA_PATTERN
			# 	optionSaveFlag = match.group(1)
			# 	optionAmount = match.group(2)
			# 	optionSymbol = match.group(3)
			# 	optionExchange = match.group(4)
			# 	optionErase = match.group(5)
			# else:
			# 	# case if OPTION_VALUE_PARM_DATA_PATTERN
			# 	optionSaveFlag = match.group(1)
			# 	optionAmount = match.group(2)
			# 	optionSymbol = match.group(3)
			# 	optionErase = match.group(4)
			
			groupNumber = len(match.groups())
			
			if optionType == 'VALUE':
				if groupNumber == 4:
					optionSaveFlag = match.group(1)
					optionAmount = match.group(2)
					optionSymbol = match.group(3)
					optionErase = match.group(4)
			elif optionType == 'FIAT':
				if groupNumber == 4:
					optionSaveFlag = match.group(1)
					optionSymbol = match.group(2)
					optionExchange = match.group(3)
					optionErase = match.group(4)
					self.commandPrice.parsedParmData[CommandPrice.OPTION_FIAT_EXCHANGE] = optionExchange
					if (optionErase == None and (optionSymbol == None or len(optionSymbol) < CURRENCY_SYMBOL_MIN_LENGTH)) or \
						(optionErase == '0' and optionSaveFlag == None and optionSymbol == None and optionData != '0'):
						# solving very difficult error message formatting for invalid -f option erase. -f0.01 in partial
						# and full requests or -fs0.01 in partial and full requests. I spent days solving it !
						return self._handleInvalidOptionFormat(optionData, optionType, requestType)
			elif optionType == 'PRICE':
				if groupNumber == 2:
					optionSaveFlag = match.group(1)
					optionAmount = match.group(2)
					if optionAmount == '0':
						optionErase = '0'
					else:
						optionErase = None
						if self._isNumber(optionAmount):
							self.commandPrice.parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT] = optionAmount
						else:
							optionAmount = None
			elif optionType == 'RESULT':
				if groupNumber == 3:
					optionSaveFlag = match.group(1)
					optionSymbol = None # not used for option result
					optionAmount = match.group(2)
					if optionAmount == '0':
						optionErase = '0'
					else:
						optionErase = None
						if '-' not in optionAmount and self._isNumber(optionAmount):
							# the case for -r20.45 for example
							return self._handleInvalidOptionFormat(optionData, optionType, requestType)
						else:
							self.commandPrice.parsedParmData[CommandPrice.OPTION_RESULT_AMOUNT] = optionAmount
			elif optionType == 'LIMIT':
				if groupNumber == 5:
					optionSaveFlag = match.group(1)
					optionAmount = match.group(2)
					optionSymbol = match.group(3)
					optionExchange = match.group(4)
					optionErase = match.group(5)
					self.commandPrice.parsedParmData[CommandPrice.OPTION_LIMIT_EXCHANGE] = optionExchange

			if optionErase == None:
				if optionSymbol and optionSymbol.isdigit():
					# case when no currency symbol entered, like -v0.01 or -vs0.01 instead of -v0.01btc/-vs0.01btc
					optionAmount += optionSymbol
					optionSymbol = ''

				if optionAmount != None:
					# if optionType == FIAT, optionAmount == None !
					commandPriceOptionAmountConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_AMOUNT')
					self.commandPrice.parsedParmData[commandPriceOptionAmountConstantValue] = optionAmount

				commandPriceOptionSymbolConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_SYMBOL')
				self.commandPrice.parsedParmData[commandPriceOptionSymbolConstantValue] = optionSymbol

				if requestType == self.REQUEST_TYPE_PARTIAL:
					# only in case of partial request containing a value command may the passed
					# optionValueData contain a s option.
					# for full requests containing a value command, the s option if present was parsed
					# in _buildFullCommandPriceOrderFreeParmsDic() and is not contained in the passed
					# optionValueData !
					commandPriceOptionSaveConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_SAVE')

					if optionSaveFlag.upper() == 'S':
						self.commandPrice.parsedParmData[commandPriceOptionSaveConstantValue] = True
					else:
						self.commandPrice.parsedParmData[commandPriceOptionSaveConstantValue] = None
			elif optionErase == '0':
				# here, -v0 was entered to deactivate option value calculation
				commandPriceOptionAmountConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_AMOUNT')
				self.commandPrice.parsedParmData[commandPriceOptionAmountConstantValue] = None

				commandPriceOptionSymbolConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_SYMBOL')
				self.commandPrice.parsedParmData[commandPriceOptionSymbolConstantValue] = None

				commandPriceOptionSaveConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_SAVE')
				self.commandPrice.parsedParmData[commandPriceOptionSaveConstantValue] = None

			# cleaning option value data which is no longer usefull
			command = self._validateOptionMandatoryComponents(requestType, optionType)
			commandPriceOptionDataConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType, optionComponent='_DATA')
			self.commandPrice.parsedParmData[commandPriceOptionDataConstantValue] = None

			return command
		else:
			#here, invalid option format
			return self._handleInvalidOptionFormat(optionData, optionType, requestType)

	def _isNumber(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False
		
	def _handleInvalidOptionFormat(self, optionData, optionType, requestType):
		optionKeyword = self.commandPrice.getCommandPriceOptionKeyword(optionType)
		if requestType == self.REQUEST_TYPE_PARTIAL:
			self.commandError.parsedParmData[
				self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
			optionData = self._correctOptionDataForErrorMessage(optionData, optionKeyword)
		else:
			self.commandError.parsedParmData[
				self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_FULL_REQUEST_OPTION
		self.commandError.parsedParmData[
			self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.OPTION_FORMAT_INVALID_MSG.format(
			optionKeyword, optionData, optionKeyword)

		return self.commandError

	def _validateOptionMandatoryComponents(self, requestType, optionType):
		commandPriceOptionDataConstantValue = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType,'_DATA')
		commandPriceOptionMandatoryComponentsList = self.commandPrice.getCommandPriceOptionComponentConstantValue(optionType,'_MANDATORY_COMPONENTS')
		returnedCommand = self.commandPrice
		optionData = self.commandPrice.parsedParmData[commandPriceOptionDataConstantValue]

		if optionData is not None and optionData != '0':    # in case option cancel like -v0, -f0 or -p0, checking
												# mandatory components has no sense
			for optionMandatoryComponentKey in commandPriceOptionMandatoryComponentsList:
				optionMandatoryComponentValue = self.commandPrice.parsedParmData[optionMandatoryComponentKey]
				if optionMandatoryComponentValue == None or optionMandatoryComponentValue == '':
					optionKeyword = self.commandPrice.getCommandPriceOptionKeyword(optionType)

					if requestType == self.REQUEST_TYPE_PARTIAL:
						self.commandError.parsedParmData[
							self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
						optionData = self._correctOptionDataForErrorMessage(optionData, optionKeyword)
					else:
						self.commandError.parsedParmData[
							self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_FULL_REQUEST_OPTION
					self.commandError.parsedParmData[
						self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.OPTION_FORMAT_INVALID_MSG.format(
						optionKeyword, optionData, optionKeyword)

					returnedCommand = self.commandError
					break

		return returnedCommand

	def _correctOptionDataForErrorMessage(self, optionData, optionKeyword):
		if 'S' in optionData.upper() and 'S' in optionKeyword.upper():
			optionData = optionData[1:]
		return optionData

	def _getRequesterOptionPattern(self, optionType):
		'''
		This method accepts as input an option type constant name part like 'VALUE', 'FIAT' or 'PRICE'. It
		returns the Requester corresponding pattern constant value which is used later for parsing the
		option components.

		This technique enables its _fillOptionValueInfo() caller method to be generalized to different option types.

		:param optionType: currently, 'VALUE', 'FIAT' or 'PRICE'
		:return:
		'''
		requesterOptionPatternConstantName = 'OPTION_' + optionType + '_PARM_DATA_PATTERN'
		requesterOptionPatternConstantValue = getattr(self, requesterOptionPatternConstantName)

		return requesterOptionPatternConstantValue

	def _wholeParmAndInvalidValue(self, parmSymbol, inputStr):
		'''
		Help improve error msg in case of invalid partial command parm value. For example,
		if partialRequestStr == -ceth -ebittrex -t6.45 -d21/12 and parmSymbol == -t, returns
		-t6.45 and 6.45 so that error msg for this invalid command can be meaningfull
		:param parmSymbol:
		:param inputStr:
		:return:
		'''
		#regexpStr = r"({}([\d\w,\./]+))(?: .+|)".format(parmSymbol)
		regexpStr = self.PATTERN_PARTIAL_PRICE_REQUEST_ERROR.format(parmSymbol)
		match = re.search(regexpStr, inputStr)

		if match:
			return match.group(1), match.group(2)


	def _wipeOutDateTimeInfoFromCommandPrice(self):
		'''
		Used to set to zero the date/time info stored
		from the previous request in the parsed parm data
		of the CommandPrice. This must be done if
		we request a RT price or if we provide a partial
		request whith parms neither date nor time AND
		the previour request was for a RT price.

		return None, None tuple used to fill the dayMonthYear
						  and hourMinute local variables
		'''
		self.commandPrice.parsedParmData[CommandPrice.DAY] = '0'
		self.commandPrice.parsedParmData[CommandPrice.MONTH] = '0'
		self.commandPrice.parsedParmData[CommandPrice.YEAR] = '0'
		self.commandPrice.parsedParmData[CommandPrice.HOUR] = '0'
		self.commandPrice.parsedParmData[CommandPrice.MINUTE] = '0'

		return (None, None)


	def _isMinimalDateTimeInfoFromPreviousRequestAvailable(self):
		'''
		Tests if at least a day and month from the previous request are available. For a request to be
		valid, it must be either RT with 0 for date/time info or have at least a day and month
		specification.
		:return: True if at least a day and month value are available from the previous request.
		'''
		return self.commandPrice.parsedParmData[CommandPrice.DAY] != None and \
			   self.commandPrice.parsedParmData[CommandPrice.MONTH] != None


	def _printHelp(self):
		print('\nCryptoPricer 2.0\n')
		print('Usage:\n')
		print('btc usd 21/11/17 9:08 bittrex  or')
		print('btc usd 21/11 bittrex          or')
		print('btc usd 0 bittrex (real time)  or')
		print('\nany of those commands, alone or combined:\n')
		print('   -cbtc')
		print('   -fusd')
		print('   -d21/11')
		print('   -t9:08')
		print('   -ebittrex')
#        print('[btc 5/7 0.0015899 6/7 0.00153] [usd-chf]')
#        print('Beware: IF YOU ENTER MORE THAN ONE UNIT CURRENCY, DO NOT FORGET TO SEPARATE THEM WITH A \'-\' !')
		inp = input('\nm for more or anything else to exit help\n')
		
		if inp.upper() == 'M':
			print("\n-ns or -nosave --> don't save retrieved prices")
			print("-rm [1, 3, 4] --> remove line numbers\n")


	def _parseUnit(self, inputStr):
		# convert "[usd-chf]"
		# into
		# ['usd', 'chf']
		# and return the unit list

		unitList = []
		patternUnit = r"((\w+)-)|((\w+)\])|(\[(w+)\])"

		for grp in re.finditer(patternUnit, inputStr):
			for elem in grp.groups():
				if elem != None and len(elem) == 3:
					unitList.append(elem)

		return unitList


	def _parseDatePrice(self, inputStr):
		# convert "[5/7 0.0015899 6/7 0.00153]"
		# into
		# ['5/7', '0.0015899', '6/7', '0.00153']
		# and return the date price pair list

		priceDateList = []
		patternDatePrice = r"(\d+/\d+) (\d+\.\d+)"

		for grp in re.finditer(patternDatePrice, inputStr):
			for elem in grp.groups():
				priceDateList.append(elem)

		return priceDateList


	def _parseOOCommandParms(self, inputStr, upperInputStr):
		# convert "btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
		# into
		# cryptoDataList = ['btc', '5/7', '0.0015899', '6/7', '0.00153']
		# unitDataList = ['usd', 'chf']
		# flag = '-nosave'
		#
		# in case the user input violates the awaited pattern, a CommandError object is
		# returned instead of the cryptoDataList
		pattern = r"(?:(\w+) (\[.*\]) (\[.*\]))|(-\w+)"

		unitDataList = []
		cryptoDataList = []
		flag = None
		grpNumber = 0

		for grp in re.finditer(pattern, upperInputStr):
			grpNumber += 1
			for elem in grp.groups():
				if elem is not None:
					if '[' in elem:
						if ' ' in elem:  # list of date/price pairs
							cryptoDataList += self._parseDatePrice(elem)
						else:  # list of unit currencies
							unitDataList = self._parseUnit(elem)
					else:  # crypto symbol like btc or flag like -nosave
						if '-' in elem:
							flag = elem
						else:  # crypto symbol at first position in input string
							cryptoDataList.append(elem)

		if (grpNumber == 0) or (grpNumber == 1 and flag != None):
			self.commandError.parsedParmData[
				self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_INVALID_COMMAND
			self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.UNIT_LIST_MISSING_MSG

			return self.commandError, unitDataList, flag
		else:
			return cryptoDataList, unitDataList, flag


if __name__ == '__main__':
	from configurationmanager import ConfigurationManager
	import os

	filePath = None

	if os.name == 'posix':
		filePath = '/sdcard/cryptopricer_test.ini'
	else:
		filePath = 'c:\\temp\\cryptopricer_test.ini'

	r = Requester(ConfigurationManager(filePath))
	
	r.commandPrice = CommandPrice()
	inputStr = "btc usd Kraken 10/9/17 12:45"
#    groupL = r._parseGroups(r.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, partialRequestStr)

#    print(groupL)
#    print(r._validateFullCommandPriceParsedGroupsOrder(groupL))
	print(r.getCommand(inputStr))

