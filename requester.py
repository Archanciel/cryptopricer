import re
from commandprice import CommandPrice


class Requester:
    '''
    Read in commands entered by the
    user, typically
    
    oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave

    and return a command filled with the command parsed parm data
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
    Full price command parms pattern. Crypto symbol (mandatory, first position mandatory), fiat symbol (optional, 
    if provided, must be in second position), date (optional), time (optional) and exchange (optional). The four
    last parms can be provided in any order after the 2 first parms !

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

    PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA = r"(\w+)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: (-\w[\w\d/:\.]+))?"

    '''
    Partial price command parms pattern. Grabs one group of kind -cbtc or -t12:54 or -d15/09 or -ebittrex or -v0.00432btc 
    followed by several OPTIONAL groups sticking to the same format -<command letter> followed by 1 or 
    more \w or \d or / . or : characters.

    Unlike with pattern 'full', the groups can all occur in any order, reason for which all groups have the same
    structure
    
    The rules below apply to -d and -t values !
    
    Date can be: 0, accepted. 
                 1, rejected. 
                 10, rejected. 
                 01, rejected. 
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
    PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:\.]+))(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?(?: (-\w)([\w\d/:\.]+))?"

    '''
    The next pattern splits the parameter data appended to the -v partial command.
    
    Ex: -v0.004325btc is splitted into 0.00432, btc, None
        -v0 is splitted into None, None, 0 and will mean 'erase previous -v parm specification
    '''
    PRICE_VALUE_PARM_DATA_PATTERN = r"([\d\.]+)(\w+)|(0)"

    def __init__(self):
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
                                           '-F': CommandPrice.FIAT,
                                           '-D': CommandPrice.DAY_MONTH_YEAR,
                                           '-T': CommandPrice.HOUR_MINUTE,
                                           '-E': CommandPrice.EXCHANGE,
                                           '-V': CommandPrice.PRICE_VALUE_DATA}


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
        :return: Command concrete instance
        '''
        upperInputStr = inputStr.upper()
        match = self._tryMatchCommandSymbol(upperInputStr)

        if match == None:
            #here, either full or partial historical/RT price request which has no command symbol
            #or user input error
            command = self._parseAndFillCommandPrice(inputStr)
            if command == self.commandPrice or command == self.commandError:
                return command
            else:
                # here, either invalid historical/RT price request which has no command symbol (for ex -t alone)
                # or other request with missing command symbol (for ex [btc 05/07 0.0015899] [usd-chf] -nosave)
                self.commandError.rawParmData = inputStr
                if '[' in inputStr:
                    # command symbol missing
                    self.commandError.parsedParmData = [self.commandError.USER_COMMAND_MISSING_MSG]
                else:
                    # invakid partial command parm
                    self.commandError.parsedParmData = ['']
                return self.commandError

        userCommand = match.group(1)

        if userCommand == "OO":
            upperInputStrWithoutUserCommand = upperInputStr[len(userCommand) + 1:]
            cryptoDataList, fiatDataList, flag = self._parseOOCommandParms(inputStr, upperInputStrWithoutUserCommand)

            if cryptoDataList == self.commandError:
                return self.commandError

            self.commandCrypto.parsedParmData = {self.commandCrypto.CRYPTO_LIST : cryptoDataList, \
                                                 self.commandCrypto.FIAT_LIST : fiatDataList, \
                                                 self.commandCrypto.FLAG : flag}

            return self.commandCrypto
        else:
            self.commandError.rawParmData = inputStr
            self.commandError.parsedParmData = [self.commandError.USER_COMMAND_MISSING_MSG]

            return self.commandError


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
        Embeding this trivial code in a method enables to
        specifically test the correct functioning of the
        used patterns
        :param pattern:     pattern to parse
        :param inputStr:    string to parse
        :return:
        '''
        match = re.match(pattern, inputStr)

        if match != None:
            return match.groups()
        else:
            return ()


    def _buildFullCommandPriceOptionalParmsDic(self, optionalParmList):
        '''
        Since DAY_MONTH_YEAR, HOUR_MINUTE and EXCHANGE can be provided in any order after CRYPTO
        and FIAT, this method differentiate them build an optional command price parm data dictionary
        with the right key. This dictionary will be added to the CommandPrice parmData dictionary.

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
        patternCommandDic = {r"\d+/\d+(?:/\d+)*|^0$" : CommandPrice.DAY_MONTH_YEAR,
                             r"\d+:\d\d" : CommandPrice.HOUR_MINUTE,
                             r"[A-Za-z]+": CommandPrice.EXCHANGE,
                             r"(?:-[vV])([\w\d/:\.]+)": CommandPrice.PRICE_VALUE_DATA}

        optionalParsedParmDataDic = {}

        for pattern in patternCommandDic.keys():
            for group in optionalParmList:
                if group and re.search(pattern, group):
                    if patternCommandDic[pattern] not in optionalParsedParmDataDic:
                        #if for example DMY already found in optional full command parms,
                        #it will not be overwritten ! Ex: 12/09/17 0: both token match DMY
                        #pattern !
                        data = self._extractData(pattern, group)
                        if data != None:
                            optionalParsedParmDataDic[patternCommandDic[pattern]] = data
                        else:
                            #full command syntax error !
                            return None

        return optionalParsedParmDataDic


    def _extractData(self, pattern, dataOrCommandStr):
        '''
        Applies the passed pattern to the passed dataOrCommandStr. If the pasaed dataOrCommandStr
        is a command of type -v0.1btc, the passed pattern will extract the data part of the
        dataOrCommandStr, i.e. 0.01btc in this case.

        Else if the dataOrCommandStr does contain data only, without a command symbol, the passed
        pattern does not extract any group and the data is returned as is

        :param pattern:
        :param dataOrCommandStr:
        :return: passed data or data part of the passed command + data. In case of syntax error,
                 None is returnedx
        '''
        match = re.match(pattern, dataOrCommandStr)

        if match == None:
            #denotes a syntax error !
            return None

        if match.groups():
            data = match.group(1)
        else:
            data = dataOrCommandStr

        return data

    def _parseAndFillCommandPrice(self, inputStr):
        groupList = self._tryMatchFullPriceCommand(inputStr)

        if groupList == (): #full command pattern not matched --> try match partial command pattern
            groupList = self._tryMatchPartialPriceCommand(inputStr)
            if groupList != (): #here, parms are associated to parrm tag (i.e -c or -d). Means they have been
                                #entered in any order and are all optional
                keys = self.inputParmParmDataDicKeyDic.keys()
                it = iter(groupList)

                for command in it:
                    value = next(it)
                    if value != None:
                        commandUpper = command.upper()
                        if commandUpper in keys:
                            self.commandPrice.parsedParmData[self.inputParmParmDataDicKeyDic[commandUpper]] = value
                        else:
                            self.commandError.rawParmData = inputStr
                            # unknown partial command symbol
                            self.commandError.parsedParmData = [self.commandError.COMMAND_NOT_SUPPORTED_MSG.format(command)]
                            return self.commandError
                            
                if self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] == '0':
                    #-d0 which means RT entered. In this case, the previous
                    #date/time info are no longer relevant !
                    hourMinute, dayMonthYear = self._wipeOutDateTimeInfoFromCommandPrice()
                elif self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] == None and self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] == None:
                    #here, partial command(s) which aren't date/time related were entered: the previous request price type must be considered !
                    if self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_RT:
                        hourMinute, dayMonthYear = self._wipeOutDateTimeInfoFromCommandPrice()
                    else:
                        #here, since previous request was not RT, hourMinute and dayRonthYear must be rebuild
                        #from the date/time values of the previous request. Don't forget that OAY_MONTH_YEAR
                        #and HOUR_MINUTE are set to None once date/time values have been acquired !
                        if self._isDateTimeInfoFromPreviousRequestAvailable():
                            hourMinute = ':'.join([self.commandPrice.parsedParmData[CommandPrice.HOUR], self.commandPrice.parsedParmData[CommandPrice.MINUTE]])
                            dayMonthYear = '/'.join([self.commandPrice.parsedParmData[CommandPrice.DAY], self.commandPrice.parsedParmData[CommandPrice.MONTH], self.commandPrice.parsedParmData[CommandPrice.YEAR]])
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
        else: #full command line entered. Here, parms were entered in an order reflected in the
              # pattern: crypto fiat in this mandatory order, then date time exchange, of which order
              # can be different.
            self.commandPrice.resetData()
            self.commandPrice.parsedParmData[CommandPrice.CRYPTO] = groupList[0] #mandatory crrypto parm, its order is fixed
            self.commandPrice.parsedParmData[CommandPrice.FIAT] = groupList[1] #mandatory fiat parm, its order is fixed
            optionalParsedParmDataDic = self._buildFullCommandPriceOptionalParmsDic(groupList[2:])

            if optionalParsedParmDataDic != None:
                self.commandPrice.parsedParmData.update(optionalParsedParmDataDic)
            else:
                self.commandError.rawParmData = inputStr
                # invalid full command format
                self.commandError.parsedParmData = [self.commandError.FULL_COMMAND_PRICE_FORMAT_INVALID_MSG]

                return self.commandError

            hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
            dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
            
        if hourMinute != None:
            hourMinuteList = hourMinute.split(':')
            if len(hourMinuteList) == 1:
                #supplied time is invalid: does not respect expected format of 0:10 or 12:01 etc
                self.commandError.rawParmData = inputStr
                # invalid time partial command format
                invalidPartialCommand, invalidValue = self._wholeParmAndInvalidValue('-t', inputStr)
                self.commandError.parsedParmData = [self.commandError.PARTIAL_PRICE_COMMAND_TIME_FORMAT_INVALID_MSG.format(invalidPartialCommand, invalidValue)]

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
                if len(dayMonthYearList) == 1: #only day specified
                    day = dayMonthYearList[0]
                    if CommandPrice.DAY in self.commandPrice.parsedParmData:
                        month = self.commandPrice.parsedParmData[CommandPrice.MONTH]
                        year = self.commandPrice.parsedParmData[CommandPrice.YEAR]
                    else:
                        month = None
                        year = None
                    self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_HISTO
                elif len(dayMonthYearList) == 2:
                    day = dayMonthYearList[0]
                    month = dayMonthYearList[1]
                    if CommandPrice.YEAR in self.commandPrice.parsedParmData:
                        year = self.commandPrice.parsedParmData[CommandPrice.YEAR]
                    else:   # year not provided and not obtained from previous full price command input.
                            # Will be set by PriceRequester which knows in which timezone we are
                        year = None
                    self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_HISTO
                elif len(dayMonthYearList) == 3:
                    day = dayMonthYearList[0]
                    month = dayMonthYearList[1]
                    year = dayMonthYearList[2]
                    self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_HISTO
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
                self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] == CommandPrice.PRICE_TYPE_HISTO
            else:
                day = None
                month = None
                year = None

        self._fillDayMonthYearInfo(day, month, year)

        priceValueData = self.commandPrice.parsedParmData[CommandPrice.PRICE_VALUE_DATA]

        if priceValueData != None:
            return self._fillPriceValueInfo(priceValueData, inputStr)
        else:
            #no partial command -v specified here !
            return self.commandPrice


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


    def _fillPriceValueInfo(self, priceValueData, inputStr):
        '''
        Fill parsed parm data price amount and price symbol fields and empty combined price data field
        :param priceValueData: the data following thce -v partial command specification
        :param inputStr: required in case a CommandError must be returned
        :return: self.commandPrice or self.commandError in case -v invalid
        '''

        match = re.match(self.PRICE_VALUE_PARM_DATA_PATTERN, priceValueData)

        if match:
            priceValueAmount = match.group(1)
            priceValueSymbol = match.group(2)
            priceValueErase =  match.group(3)
            if priceValueErase == None:
                self.commandPrice.parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = priceValueAmount
                self.commandPrice.parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = priceValueSymbol
            elif priceValueErase == '0':
                #here, -v0 was entered to stop price value calculation
                self.commandPrice.parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = None
                self.commandPrice.parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = None

            self.commandPrice.parsedParmData[CommandPrice.PRICE_VALUE_DATA] = None

            return self.commandPrice
        else:
            #here, invalid -v command
            self.commandError.rawParmData = inputStr
            self.commandError.parsedParmData = [self.commandError.PARTIAL_PRICE_VALUE_COMMAND_FORMAT_INVALID_MSG.format('-v' + priceValueData, priceValueData)]

            return self.commandError

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


    def _tryMatchFullPriceCommand(self, inputStr):
        '''
        Try matching a full price command like btc usd 0 bittrex
        :param inputStr:
        :return: None or a Match object
        '''
        return self._parseGroups(self.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)


    def _tryMatchPartialPriceCommand(self, inputStr):
        '''
        Try matching a partial price command like -d21/12 or -eccex
        :param inputStr:
        :return: None or a Match object
        '''
        return self._parseGroups(self.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)


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
        self.commandPrice.parsedParmData[CommandPrice.PRICE_TYPE] = CommandPrice.PRICE_TYPE_RT
        self.commandPrice.parsedParmData[CommandPrice.DAY] = '0'
        self.commandPrice.parsedParmData[CommandPrice.MONTH] = '0'
        self.commandPrice.parsedParmData[CommandPrice.YEAR] = '0'
        self.commandPrice.parsedParmData[CommandPrice.HOUR] = '0'
        self.commandPrice.parsedParmData[CommandPrice.MINUTE] = '0'

        return (None, None)


    def _isDateTimeInfoFromPreviousRequestAvailable(self):
        return self.commandPrice.parsedParmData[CommandPrice.DAY] != None and \
               self.commandPrice.parsedParmData[CommandPrice.MONTH] != None and \
               self.commandPrice.parsedParmData[CommandPrice.YEAR] != None and \
               self.commandPrice.parsedParmData[CommandPrice.HOUR] != None and \
               self.commandPrice.parsedParmData[CommandPrice.MINUTE] != None


    def _printHelp(self):
        print('\nCryptoPricer 2.0\n')
        print('Usage:\n')
        print('btc usd 21/11/17 9:08 bittrex  or')
        print('btc usd 21/11 bittrex          or')
        print('btc usd 0 bittrex (real time)  or')
        print('\nany of those options, alone or combined:\n')
        print('   -cbtc')
        print('   -fusd')
        print('   -d21/11')
        print('   -t9:08')
        print('   -ebittrex')
#        print('[btc 5/7 0.0015899 6/7 0.00153] [usd-chf]')
#        print('Beware: IF YOU ENTER MORE THAN ONE FIAT CURRENCY, DO NOT FORGET TO SEPARATE THEM WITH A \'-\' !')
        inp = input('\nm for more or anything else to exit help\n')
        
        if inp.upper() == 'M':
            print("\n-ns or -nosave --> don't save retrieved prices")
            print("-rm [1, 3, 4] --> remove line numbers\n")


    def _parseFiat(self, inputStr):
        # convert "[usd-chf]"
        # into
        # ['usd', 'chf']
        # and return the fiat list

        fiatList = []
        patternFiat = r"((\w+)-)|((\w+)\])|(\[(w+)\])"

        for grp in re.finditer(patternFiat, inputStr):
            for elem in grp.groups():
                if elem != None and len(elem) == 3:
                    fiatList.append(elem)

        return fiatList


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
        # fiatDataList = ['usd', 'chf']
        # flag = '-nosave'
        #
        # in case the user input violates the awaited pattern, a CommandError object is
        # returned instead of the cryptoDataList
        pattern = r"(?:(\w+) (\[.*\]) (\[.*\]))|(-\w+)"

        fiatDataList = []
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
                        else:  # list of fiat currencies
                            fiatDataList = self._parseFiat(elem)
                    else:  # crypto symbol like btc or flag like -nosave
                        if '-' in elem:
                            flag = elem
                        else:  # crypto symbol at first position in input string
                            cryptoDataList.append(elem)

        if (grpNumber == 0) or (grpNumber == 1 and flag != None):
            self.commandError.rawParmData = inputStr
            self.commandError.parsedParmData = [self.commandError.FIAT_LIST_MISSING_MSG]
            return self.commandError, fiatDataList, flag
        else:
            return cryptoDataList, fiatDataList, flag


if __name__ == '__main__':
    from test.testrequester import TestRequester
    
    testR = TestRequester()
    testR.runTests()
    
    '''
    r = Requester()
    
    r.commandPrice = CommandPrice()
    inputStr = "btc usd Kraken 10/9/17 12:45"
#    groupL = r._parseGroups(r.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

#    print(groupL)
#    print(r._validateFullCommandPriceParsedGroupsOrder(groupL))
    print(r._parseAndFillCommandPrice(inputStr))
    '''
