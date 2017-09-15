import re
from datetime import datetime
from pytz import timezone
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
    Full price command parms pattern. Crypto symbol, fiat symbol, date, time,and exchange.
    Must be provided in this order. Second parm, fiat symbol, and last parm, exchange name, 
    are optional.
    
    Ex; btc usd 13/9 12:15 Kraken
    '''
    PATTERN_FULL_PRICE_REQUEST_DATA = r"(\w+)(?: (\w+)|) ([\d/]+) ([\d:]+)(?: (\w+)|)"

    '''
    Grabs one group of kind -cbtc or -t12:54 or -d15/09 followed
    by several OPTIONAL groups sticking to the same format
    -<command letter> followed by 1 or more \w or \d or / or :
    characters.

    Unlike with pattern 'full', the groups can occur in
    any order, reason for which all groups have the same
    structure
    
    Ex: -ceth -fgbp -d13/9 -t23:09 -eKraken
    '''
    PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:]+))(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?"

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
        self.inputParmParmDataDicKeyDic = {'-c': CommandPrice.CRYPTO,
                                           '-f': CommandPrice.FIAT,
                                           '-d': CommandPrice.DAY_MONTH_YEAR,
                                           '-t': CommandPrice.HOUR_MINUTE,
                                           '-e': CommandPrice.EXCHANGE}


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
            return self._getCommand(inputStr, upperInputStr)


    def _getCommand(self, inputStr, upperInputStr):
        match = re.match(Requester.USER_COMMAND_GRP_PATTERN, upperInputStr)

        if match == None:
            #here, either historical/RT price request which has no command symbol or user input error
            if self.commandPrice == self._parseAndFillCommandPrice(inputStr):
                return self.commandPrice
            else:
                self.commandError.rawParmData = inputStr
                self.commandError.parsedParmData = [self.commandError.USER_COMMAND_MISSING_MSG]
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


    def _getValue(self, value, default):
        if value == None:
            return default
        else:
            return value


    def _parseGroups(self, pattern, inputStr):
        '''
        Embeding this trjvial code in a method enable to
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


    def _parseAndFillCommandPrice(self, inputStr):
        groupList = self._parseGroups(self.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        if groupList == (): #full pattern not matched --> try match partial pattern
            groupList = self._parseGroups(self.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)
            if groupList != (): #here, parms are associated to parrm tag (i.e -c or -d). Means they have been
                                #entered in any order and are all optional
                it = iter(groupList)

                for command in it:
                    value = next(it)
                    if value != None:
                        self.commandPrice.parsedParmData[self.inputParmParmDataDicKeyDic[command]] = value

                hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
                dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]
            else: #neither full nor parrial pattern matched
                return None
        else: #regular command line entered. Here, parms were entered in a fixed order reflected in the pattern.
            self.commandPrice.parsedParmData[CommandPrice.CRYPTO] = groupList[0]
            self.commandPrice.parsedParmData[CommandPrice.FIAT] = self._getValue(groupList[1], 'usd')

            dayMonthYear = groupList[2]
            hourMinute = groupList[3]

            self.commandPrice.parsedParmData[CommandPrice.EXCHANGE] = self._getValue(groupList[4], 'CCCAGG')

        hourMinuteList = hourMinute.split(':')

        if len(hourMinuteList) == 1:
            minute = '0'
        else:
            hour = hourMinuteList[0]
            minute = hourMinuteList[1]

        self.commandPrice.parsedParmData[CommandPrice.HOUR] = hour
        self.commandPrice.parsedParmData[CommandPrice.MINUTE] = minute
        self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] = None

        dayMonthYearList = dayMonthYear.split('/')
        day = dayMonthYearList[0]
        month = dayMonthYearList[1]

        if len(dayMonthYearList) == 2:  # year not provided. Will be set by PriceRequester
            # which knows in which timezone we are
            year = None
        else:
            year = dayMonthYearList[2]

        self.commandPrice.parsedParmData[CommandPrice.DAY] = day
        self.commandPrice.parsedParmData[CommandPrice.MONTH] = month
        self.commandPrice.parsedParmData[CommandPrice.YEAR] = year
        self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

#        print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' '.join(map(str, pr.getPriceAtLocalDateTimeStr(crypto, fiat, localDateTimeStr, exchange))))
        return self.commandPrice


    def _printHelp(self):
        print('Usage:\n')
        print('[btc 5/7 0.0015899 6/7 0.00153] [usd-chf]')
        print('Beware: IF YOU ENTER MORE THAN ONE FIAT CURRENCY, DO NOT FORGET TO SEPARATE THEM WITH A \'-\' !')
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
    r = Requester()
    print(r._parseCryptoDataFromInput('[btc 5/7 0.0015899 6/7 0.00153] [usd-chf-eur] -nosave'))
