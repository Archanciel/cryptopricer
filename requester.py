import re
from datetime import datetime
from pytz import timezone
from commandprice import CommandPrice

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
PATTERN_FULL_PRICE_REQUEST_DATA = r"(\w+)(?: (\w+)|) ([0-9]+)/([0-9]+)(?:/([0-9]+)|) ([0-9:]+)(?: (\w+)|)"
PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:]+))(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?"


class Requester:
    '''
    Read in commands entered by the
    user, typically
    
    oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave

    and return a command filled with the command parsed parm data
    '''
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
        inputStr = input(ENTER_COMMAND_PROMPT)
        upperInputStr = inputStr.upper()

        while upperInputStr == 'H':
            self._printHelp()
            inputStr = input(ENTER_COMMAND_PROMPT)
            upperInputStr = inputStr.upper()
        
        if upperInputStr == 'Q':
            return self.commandQuit
        else: #here, neither help nor quit command entered. Need to determine which command
              #is entered by the user finding unique pattern match that identify this command
            return self._getCommand(inputStr, upperInputStr)


    def _getCommand(self, inputStr, upperInputStr):
        match = re.match(USER_COMMAND_GRP_PATTERN, upperInputStr)

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

    def _parseAndFillCommandPrice(self, inputStr):
        match = re.match(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        day = ''
        month = ''
        year = ''
        houe = ''
        minute = ''
        hourMinute = ''

        if match == None:
            match = re.match(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)
            if match != None:
                partialArgList = match.groups()
                it = iter(partialArgList)

                for command in it:
                    value = next(it)
                    if value != None:
                        self.commandPrice.parsedParmData[self.inputParmParmDataDicKeyDic[command]] = value

                hourMinute = self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE]
                dayMonthYear = self.commandPrice.parsedParmData[CommandPrice.DAY_MONTH_YEAR]

                dayMonthYearList = dayMonthYear.split('/')
                day = dayMonthYearList[0]
                month = dayMonthYearList[1]

                if len(dayMonthYearList) == 2:  # year not provided. Will be set by PriceRequester
                                                # which knows in which timezone we are
                    year = None
                else:
                    year = dayMonthYearList[2]
            else:
                return None
        else: #regular command line entered
            self.commandPrice.parsedParmData[CommandPrice.CRYPTO] = match.group(1)
            self.commandPrice.parsedParmData[CommandPrice.FIAT] = self._getValue(match.group(2), 'usd')

            day = match.group(3)
            month = match.group(4)
            year = match.group(5)

            self.commandPrice.parsedParmData[CommandPrice.DAY] = day
            self.commandPrice.parsedParmData[CommandPrice.MONTH] = month
            self.commandPrice.parsedParmData[CommandPrice.YEAR] = year

            hourMinute = match.group(6)

            self.commandPrice.parsedParmData[CommandPrice.EXCHANGE] = self._getValue(match.group(7), 'CCCAGG')
        '''
        dayMonthYear is handled differently than hourMinute because Requester does not have the
        responsibility to know about timezone. That is devoted to PriceRequester which will normalize
        the user provided date
        '''
        hourMinuteList = hourMinute.split(':')

        if len(hourMinuteList) == 1:
            minute = '0'
        else:
            hour = hourMinuteList[0]
            minute = hourMinuteList[1]

        self.commandPrice.parsedParmData[CommandPrice.HOUR] = hour
        self.commandPrice.parsedParmData[CommandPrice.MINUTE] = minute
        self.commandPrice.parsedParmData[CommandPrice.HOUR_MINUTE] = None

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
