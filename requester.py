import re
from commandprice import CommandPrice
from commanderror import CommandError
from datetimeutil import DateTimeUtil

class Requester:
    '''
    Read in commands entered by the
    user, typically
    
    oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave

    and return a command filled with the command parsed parm data
    :seqdiag_note Parses the user commands
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

    PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA = r"(\w+)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: (-\w\w?[\w\d/:\.]+))?(?: (-\w\w?[\w\d/:\.]+))?"

    '''
    Partial price command parms pattern. Grabs one group of kind -cbtc or -t12:54 or -d15/09 or -ebittrex or -v0.00432btc 
    followed by several OPTIONAL groups sticking to the same format -<command letter> followed by 1 or 
    more \w or \d or / . or : characters.

    Unlike with pattern 'full', the groups can all occur in any order, reason for which all groups have the same
    structure
     
    Additionally, 2 request commands can be added to the regular partial commands. For example -vs12btc.
   
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
                        
    Ex: -ceth -fgbp -d13/9 -t23:09 -eKraken -v0.0044543eth
    '''
    PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:\.]+))(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?"

    '''
    The next pattern splits the parameter data appended to the -v partial command.
    
    Ex: -v0.004325btc is splitted into 0.00432, btc, None
        -v0 is splitted into None, None, 0 and will mean 'erase previous -v parm specification
    '''
    OPTION_VALUE_PARM_DATA_PATTERN = r"([sS]?)([\d\.]+)(\w+)|(0)"
    OPTION_FIAT_PARM_DATA_PATTERN = r"([sS]?)([\d\.]+)(\w+)|(0)"

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
                                           '-V': CommandPrice.OPTION_VALUE_DATA}


    def request(self):
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
        '''
        Parses the paased input string and return a Command concrete instance
        filled with the command specific data. May return a CommandError.
        :param inputStr: input string to parse
        :seqdiag_return AbstractCommand
        :seqdiag_return_note May return a CommandError in case of parsing problem.
        :return: Command concrete instance
        '''

        returnedCommand = None

        if inputStr == '' and self.commandPrice.isValid():
            #here, user entered RETURN to replay the last commannd
            self._alignCommandPriceDateTimeDataWithPriceType()
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
                        # invakid partial command parm
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
        CRYPTO and UNIT provided in this mandatory order. The other full request parameters, date, time,
        exchange and any additional options can be specified in any order.

        The purpose of this method is precisely to acquire those order free full request parameters.

        Since DAY_MONTH_YEAR, HOUR_MINUTE, EXCHANGE and additional OPTIONS can be provided in any order
        after CRYPTO and UNIT, this method differentiate them build an optional command price parm data
        dictionary with the right key. This dictionary will be added to the CommandPrice parmData dictionary.

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
        # in CommandPrice. With the old versionk of th pattern, CommandPrice.DAY_MONTH_YEAR was none,
        # which was considered like a valid full request with only the time providded, a feature which
        # was not supported before !
        #
        # So, allowing the user to provide only the time in the full request implied that we are
        # more permissive at the level of the Requester in order for CommandPrice to be able
        # to correctly identify the invalid date/time full request component in the form of
        # D HH:MM or DD HH:MM
        patternCommandDic = {r"\d+/\d+(?:/\d+)*|^\d+$" : CommandPrice.DAY_MONTH_YEAR,
                             r"\d+:\d\d" : CommandPrice.HOUR_MINUTE,
                             r"[A-Za-z]+": CommandPrice.EXCHANGE,
                             r"(?:-[vV])([sS]?)([\w\d/:\.]+)": CommandPrice.OPTION_VALUE_DATA,
                             r"(?:-[vV])([sS]?)([\w\d/:\.]+)" + OPTION_MODIFIER: CommandPrice.OPTION_VALUE_SAVE,
                             r"(-[^vVfFpP]{1})([sS]?)([\w\d/:\.]+)": CommandPrice.UNSUPPORTED_OPTION_DATA,  # see scn capture https://pythex.org/ in Evernote for test of this regexp !
                             r"(-[^vVfFpP]{1})([sS]?)([\w\d/:\.]+)" + UNSUPPORTED_OPTION: CommandPrice.UNSUPPORTED_OPTION,  # see scn capture https://pythex.org/ in Evernote for test of this regexp !
                             r"(-[^vVfFpP]{1})([sS]?)([\w\d/:\.]+)" + OPTION_MODIFIER: CommandPrice.UNSUPPORTED_OPTION_MODIFIER,
                             r"(?:-[fF])([sS]?)([\w\d/:\.]+)": CommandPrice.OPTION_FIAT_DATA,
                             r"(?:-[fF])([sS]?)([\w\d/:\.]+)" + OPTION_MODIFIER: CommandPrice.OPTION_FIAT_SAVE,
                             r"(?:-[pP])([sS]?)([\w\d/:\.]+)": CommandPrice.OPTION_PRICE_DATA,
                             r"(?:-[pP])([sS]?)([\w\d/:\.]+)" + OPTION_MODIFIER: CommandPrice.OPTION_PRICE_SAVE}

        optionalParsedParmDataDic = {}

        for pattern in patternCommandDic.keys():
            for group in orderFreeParmList:
                if group and re.search(pattern, group):
                    if patternCommandDic[pattern] not in optionalParsedParmDataDic:
                        # if for example DMY already found in optional full command parms,
                        # it will not be overwritten ! Ex: 12/09/17 0: both token match DMY
                        # pattern !
                        data, option, optionModifier = self._extractData(pattern, group)
                        if data != None:
                            optionalParsedParmDataDic[patternCommandDic[pattern]] = data
                            patternCommandModifierKey = pattern + OPTION_MODIFIER
                            if optionModifier != None and optionModifier != '':
                                optionalParsedParmDataDic[patternCommandDic[patternCommandModifierKey]] = optionModifier
                            elif patternCommandModifierKey in optionalParsedParmDataDic.keys():
                                optionalParsedParmDataDic[patternCommandDic[patternCommandModifierKey]] = None
                            if option:
                                # here, handling an unsupported option. If handling a supported option, option
                                # is None. For valid options, the correct option symbol will be set later in the
                                # command price in _fillOptionValueInfo() like methods !
                                patternUnsupportedOptionKey = pattern + UNSUPPORTED_OPTION
                                optionalParsedParmDataDic[patternCommandDic[patternUnsupportedOptionKey]] = option
                        else:
                            #full command syntax error !
                            return None


        from seqdiagbuilder import SeqDiagBuilder
        SeqDiagBuilder.recordFlow()

        return optionalParsedParmDataDic


    def _extractData(self, pattern, dataOrOptionStr):
        '''
        Applies the passed pattern to the passed dataOrOptionStr. If the passed dataOrOptionStr
        is an option of type -v0.1btc or -vs0.1btc, the passed pattern will extract the data part of the
        dataOrOptionStr, i.e. 0.01btc in this case and the option modifier part of the dataOrOptionStr,
        i.e. s in this case.

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
            option = match.group(1)
            optionModifier = match.group(2)
            data = match.group(3)
        else:
            data = dataOrOptionStr

        return data, option, optionModifier

    def _parseAndFillCommandPrice(self, inputStr):
        '''
        This method try parsing a full or a partial request.

        :param inputStr:
        :seqdiag_return CommandPrice or CommandError
        :return: self.commandPrice or self.commandError or None, which will cause an error to be raised
        '''
        groupList = self._parseGroups(self.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        requestType = None

        if groupList == ():
            # full command pattern not matched --> try match partial command pattern
            groupList = self._parseGroups(self.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)
            if groupList != ():
                # partial request entered. Here, parms are associated to parrm tag (i.e -c or -d).
                # Means they have been entered in any order and are all optional ensuring
                # command price temporary data like unsupported command data from previous
                # request are purged. Necessary here when handling partial command(s) since, unlike
                # when a full command is processed, the command price is not reinitialized !
                requestType = self.REQUEST_TYPE_PARTIAL
                self.commandPrice.resetTemporaryData()

                keys = self.inputParmParmDataDicKeyDic.keys()
                it = iter(groupList)

                for command in it:
                    value = next(it)
                    if value != None:
                        commandUpper = command.upper()
                        if commandUpper in keys:
                            self.commandPrice.parsedParmData[self.inputParmParmDataDicKeyDic[commandUpper]] = value
                        else:
                            # unknown partial command symbol
                            self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION] = command
                            if value[0].upper() == 'S':
                                self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_DATA] = value[1:]
                                self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_MODIFIER] = value[0]
                            else:
                                self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_DATA] = value
                                self.commandPrice.parsedParmData[self.commandPrice.UNSUPPORTED_OPTION_MODIFIER] = None


                if self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] == '0':
                    #-d0 which means RT entered. In this case, the previous
                    #date/time info are no longer relevant !
                    self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_RT
                    hourMinute, dayMonthYear = self._wipeOutDateTimeInfoFromCommandPrice()
                elif self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] == None and self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] == None:
                    #here, partial command(s) which aren't date/time related were entered: the previous request price type must be considered !
                    if self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_RT:
                        hourMinute, dayMonthYear = self._wipeOutDateTimeInfoFromCommandPrice()
                    else:
                        #here, since previous request was not RT, hourMinute and dayRonthYear must be rebuilt
                        #from the date/time values of the previous request. Don't forget that OAY_MONTH_YEAR
                        #and HOUR_MINUTE are set to None once date/time values have been acquired !
                        if self._isMinimalDateTimeInfoFromPreviousRequestAvailable():
                            dayMonthYear, hourMinute = self._rebuildPreviousRequestDateTimeValues()
                        else:
                            return None # will cause an error. This occurs in a special situation when the previous request
                                        # was in error, which explains why the date/time info from previous request is
                                        # incoherent. Such a case is tested by TestController.
                                        # testControllerHistoDayPriceIncompleteCommandScenario
                else:           
                    hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
                    dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
                    
            else: #neither full nor parrial pattern matched
                return None # will cause an error.
        else:
            # full request entered. Here, parms were entered in an order reflected in the
            # pattern: crypto unit in this mandatory order, then date time exchange, of which order
            # can be different.
            requestType = self.REQUEST_TYPE_FULL
            self.commandPrice.initialiseParsedParmData()
            self.commandPrice.parsedParmData[CommandPrice.CRYPTO] = groupList[0] #mandatory crrypto parm, its order is fixed
            self.commandPrice.parsedParmData[CommandPrice.UNIT] = groupList[1] #mandatory unit parm, its order is fixed
            optionalParsedParmDataDic = self._buildFullCommandPriceOrderFreeParmsDic(groupList[2:])

            if optionalParsedParmDataDic != None:
                self.commandPrice.parsedParmData.update(optionalParsedParmDataDic)
            else:
                # invalid full command format
                self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_FULL_REQUEST

                return self.commandError

            hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
            dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
            
        if hourMinute != None:
            hourMinuteList = hourMinute.split(':')
            if len(hourMinuteList) == 1:
                #supplied time is invalid: does not respect expected format of 0:10 or 12:01 etc
                # invalid time partial command format
                invalidPartialCommand, invalidValue = self._wholeParmAndInvalidValue('-t', inputStr)
                dtFormatDic = DateTimeUtil.getDateAndTimeFormatDictionary(self.configMgr.dateTimeFormat)
                timeFormat = dtFormatDic[DateTimeUtil.TIME_FORMAT_KEY]
                self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
                self.commandError.parsedParmData[self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.PARTIAL_PRICE_COMMAND_TIME_FORMAT_INVALID_MSG.format(invalidPartialCommand, invalidValue, timeFormat)

                # remove invalid time specification form parsedParData to avoid polluting next partial
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

        optionTypeList = ['VALUE']
        command = None

        for optionType in optionTypeList:
            commandPriceOptionDataConstantValue = self.getCommandPricePattern(optionType, optionComponent='_DATA')
            optionData = self.commandPrice.parsedParmData[commandPriceOptionDataConstantValue]
            if optionData:
                command = self._fillOptionValueInfo(optionType, optionData, requestType)
                if isinstance(command, CommandError):
                    # in case an error was detected, we do not continue handling the options
                    break

        if command:
            return command
        else:
            # here, no option -v, -f or -p specified !
            return self.commandPrice

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

        :param optionData: the data following thce -v partial command specification
        :param requestType: indicate if we are handling a full or a partial request
        :return: self.commandPrice or self.commandError in case the -v option is invalid
        '''

        requesterOptionPattern = self.getRequesterOptionPattern(optionType)

        match = re.match(requesterOptionPattern, optionData)

        if match:
            optionSaveFlag = match.group(1)
            optionAmount = match.group(2)
            optionSymbol = match.group(3)
            optionErase =  match.group(4)
            if optionErase == None:
                if optionSymbol.isdigit():
                    # case when no currency synbol entered, like -v100 instead of -v100usd
                    optionAmount += optionSymbol
                    optionSymbol = ''

                commandPriceOptionAmountConstantValue = self.getCommandPricePattern(optionType, optionComponent='_AMOUNT')
                self.commandPrice.parsedParmData[commandPriceOptionAmountConstantValue] = optionAmount

                commandPriceOptionSymbolConstantValue = self.getCommandPricePattern(optionType, optionComponent='_SYMBOL')
                self.commandPrice.parsedParmData[commandPriceOptionSymbolConstantValue] = optionSymbol

                if requestType == self.REQUEST_TYPE_PARTIAL:
                    # only in case of partial request containing a value command may the passed
                    # optionValueData contain a s option.
                    # for full requests containing a value command, the s option if present was parsed
                    # in _buildFullCommandPriceOrderFreeParmsDic() and is not contained in the passed
                    # optionValueData !
                    commandPriceOptionSaveConstantValue = self.getCommandPricePattern(optionType, optionComponent='_SAVE')

                    if optionSaveFlag.upper() == 'S':
                        self.commandPrice.parsedParmData[commandPriceOptionSaveConstantValue] = True
                    else:
                        self.commandPrice.parsedParmData[commandPriceOptionSaveConstantValue] = None
            elif optionErase == '0':
                # here, -v0 was entered to deactivate option value calculation
                commandPriceOptionAmountConstantValue = self.getCommandPricePattern(optionType, optionComponent='_AMOUNT')
                self.commandPrice.parsedParmData[commandPriceOptionAmountConstantValue] = None

                commandPriceOptionSymbolConstantValue = self.getCommandPricePattern(optionType, optionComponent='_SYMBOL')
                self.commandPrice.parsedParmData[commandPriceOptionSymbolConstantValue] = None

                commandPriceOptionSaveConstantValue = self.getCommandPricePattern(optionType, optionComponent='_SAVE')
                self.commandPrice.parsedParmData[commandPriceOptionSaveConstantValue] = None

            # cleaning option value data which is no longer usefull
            commandPriceOptionDataConstantValue = self.getCommandPricePattern(optionType, optionComponent='_DATA')
            self.commandPrice.parsedParmData[commandPriceOptionDataConstantValue] = None

            return self.commandPrice
        else:
            #here, invalid option format
            if requestType == self.REQUEST_TYPE_PARTIAL:
                self.commandError.parsedParmData[
                    self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_PARTIAL_REQUEST
                optionSaveModifier = self.getCommandPriceOptionKeyword(optionType)
                if 'S' in optionData.upper() and 'S' in optionSaveModifier.upper():
                    optionData = optionData[1:]
            else:
                self.commandError.parsedParmData[
                    self.commandError.COMMAND_ERROR_TYPE_KEY] = self.commandError.COMMAND_ERROR_TYPE_FULL_REQUEST_OPTION
                optionSaveModifier = self.getCommandPriceOptionKeyword(optionType)

            self.commandError.parsedParmData[
                self.commandError.COMMAND_ERROR_MSG_KEY] = self.commandError.OPTION_FORMAT_INVALID_MSG.format(
                optionSaveModifier, optionData, optionSaveModifier)

            return self.commandError

    def getCommandPricePattern(self, optionType, optionComponent):
        '''
        This method accepts as input an option type constant name part like 'VALUE', 'FIAT' or 'PRICE' as well as
        an option component constant name part like '_DATA', '_AMOUNT' or '_SAVE'. It returns the CommandPrice
        corresponding constant value which is used later as key for the CommandPrice parsed parm data dictionary.

        This technique enables its _fillOptionValueInfo() caller method to be generalized to different option types
        and option components.

        :param optionType: currently, 'VALUE', 'FIAT' or 'PRICE'
        :param optionComponent: currently, '_DATA', '_AMOUNT' '_SYMBOL' or '_SAVE'
        :return:
        '''
        commandPriceOptionComponentConstantName = 'OPTION_' + optionType + optionComponent
        commandPriceOptionComponentConstantValue = CommandPrice.__getattribute__(CommandPrice,
                                                                              commandPriceOptionComponentConstantName)
        return commandPriceOptionComponentConstantValue

    def getCommandPriceOptionKeyword(self, optionType):
        '''
        This method is used as helper when building an invalid full request error msg. Unlike when building such
        an error msg when handling an invalid  partial request, in a full request context, the faulty option
        keyword is not available and so must be rebuilt. The method accepts as input an option type constant name
        part like 'VALUE', 'FIAT' or 'PRICE'.

        :param optionType: currently, 'VALUE', 'FIAT' or 'PRICE'
        :return: -v or -vs or -f or -fs or -p or -ps
        '''
        optionKeywordDic = {'VALUE':'-v', 'FIAT':'-f', 'PRICE':'-p'}
        commandPriceOptionSaveConstantName = 'OPTION_' + optionType + '_SAVE'
        commandPriceOptionSaveValue = self.commandPrice.parsedParmData[commandPriceOptionSaveConstantName]

        if commandPriceOptionSaveValue:
            commandPriceOptionSaveValue = 's'
        else:
            commandPriceOptionSaveValue = ''

        return optionKeywordDic[optionType] + commandPriceOptionSaveValue

    def getRequesterOptionPattern(self, optionType):
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
        if inputStr == -ceth -ebittrex -t6.45 -d21/12 and parmSymbol == -t, returns
        -t6.45 and 6.45 so that error msg for this invalid command can be meaningfull
        :param parmSymbol:
        :param inputStr:
        :return:
        '''
        regexpStr = r"({}([\d\w,\./]+))(?: .+|)".format(parmSymbol)
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
#    groupL = r._parseGroups(r.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

#    print(groupL)
#    print(r._validateFullCommandPriceParsedGroupsOrder(groupL))
    print(r.getCommand(inputStr))

