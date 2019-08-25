from abstractcommand import AbstractCommand
from datetimeutil import DateTimeUtil
from resultdata import ResultData

class CommandPrice(AbstractCommand):
    '''
    This command handles RT and historical full and partial price requests. In respect of the
    Command pattern, it calls the getCryptoPrice method on its receiver, a Processor instance
    linked to the Command by the Controller.
    '''
    CRYPTO = "CRYPTO"
    UNIT = "UNIT"
    EXCHANGE = "EXCHANGE"
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
    HOUR = "HOUR"           #store HH user input
    MINUTE = "MINUTE"       #store MM user input
    HOUR_MINUTE = "HM"      #temporary store HH:MM user input
    DAY_MONTH_YEAR = "DMY"  #temporary store DD/MM/YY user input

    PRICE_TYPE = 'PRICE_TYPE'

    PRICE_TYPE_HISTO = 'HISTO'
    PRICE_TYPE_RT = 'REAL_TIME'
    
    OPTION_VALUE_DATA = 'OPTION_VALUE_DATA'     #temporary store the data specified with -v. Ex: 0.0044254btc
    OPTION_VALUE_AMOUNT = 'OPTION_VALUE_AMOUNT' #store the price target specified with -v. Ex: 0.0044354
    OPTION_VALUE_SYMBOL = 'OPTION_VALUE_SYMBOL' #store the price symbol specified with -v. Ex: btc
    OPTION_VALUE_SAVE = 'OPTION_VALUE_SAVE'     #store s or S or None to indicate if the value option is to be stored in history (-vs) or not (-v) --> None
    OPTION_VALUE_MANDATORY_COMPONENTS = [OPTION_VALUE_DATA, OPTION_VALUE_AMOUNT, OPTION_VALUE_SYMBOL]

    UNSUPPORTED_OPTION = "UNSUPPORTED_OPTION"                   #store an unsupported option specification
    UNSUPPORTED_OPTION_MODIFIER = "UNSUPPORTED_OPTION_MODIFIER" #store an unsupported option modifier specification
    UNSUPPORTED_OPTION_DATA = "UNSUPPORTED_OPTION_DATA"         #store any unsupported option specification data

    OPTION_FIAT_DATA = 'OPTION_FIAT_DATA'     #temporary store the data specified with -f. Ex: usd
    OPTION_FIAT_SYMBOL = 'OPTION_FIAT_SYMBOL' #store the price symbol specified with -f. Ex: usd
    OPTION_FIAT_SAVE = 'OPTION_FIAT_SAVE'     #store s or S or None to indicate if the fiat option is to be stored in history (-fs) or not (-f) --> None
    OPTION_FIAT_MANDATORY_COMPONENTS = [OPTION_FIAT_DATA, OPTION_FIAT_SYMBOL]

    OPTION_PRICE_DATA = 'OPTION_PRICE_DATA'     #temporary store the data specified with -p. Ex: 230usd
    OPTION_PRICE_AMOUNT = 'OPTION_PRICE_AMOUNT' #store the price target specified with -p. Ex: 230
    OPTION_PRICE_SYMBOL = 'OPTION_PRICE_SYMBOL' #store the price symbol specified with -p. Ex: usd
    OPTION_PRICE_SAVE = 'OPTION_PRICE_SAVE'     #store s or S or None to indicate if the value option is to be stored in history (-ps) or not (-p) --> None
    OPTION_PRICE_MANDATORY_COMPONENTS = [OPTION_PRICE_DATA, OPTION_PRICE_AMOUNT, OPTION_PRICE_SYMBOL]

    def __init__(self, receiver = None, configManager = None):
        super().__init__(receiver, 'CommandPrice')
        self.configManager = configManager


    def initialiseParsedParmData(self):
        '''
        Prefill the parsedParmData dictionary with empty key/value pair.
        If this is not done, the parsedParmData dictionary will only contain
        key/value pairs added at the first use of the command.

        For example, entering 'btc usd 0 Bittrex' will cause the parsedParmData dic
        to be initialized with only CRYPTO, UNIT, DAY_MONTH_YEAR, DAY, MONTH, YEAR
        and EXCHANGE entries. HOUR_MINUTE, HOUR and MINUTE will be missing. This
        will cause subsequent errors in Requester in case the first usage was
        'btc usd 0 Bittrex'
        :return:
        '''
        self.parsedParmData[self.CRYPTO] = None
        self.parsedParmData[self.UNIT] = None
        self.parsedParmData[self.EXCHANGE] = None
        self.parsedParmData[self.DAY] = None
        self.parsedParmData[self.MONTH] = None
        self.parsedParmData[self.YEAR] = None
        self.parsedParmData[self.HOUR] = None
        self.parsedParmData[self.MINUTE] = None
        self.parsedParmData[self.DAY_MONTH_YEAR] = None
        self.parsedParmData[self.HOUR_MINUTE] = None
        self.parsedParmData[self.PRICE_TYPE] = None
        self.parsedParmData[self.OPTION_VALUE_DATA] = None
        self.parsedParmData[self.OPTION_VALUE_AMOUNT] = None
        self.parsedParmData[self.OPTION_VALUE_SYMBOL] = None
        self.parsedParmData[self.OPTION_VALUE_SAVE] = None
        self.parsedParmData[self.UNSUPPORTED_OPTION_DATA] = None
        self.parsedParmData[self.UNSUPPORTED_OPTION] = None
        self.parsedParmData[self.UNSUPPORTED_OPTION_MODIFIER] = None
        self.parsedParmData[self.OPTION_FIAT_DATA] = None
        self.parsedParmData[self.OPTION_FIAT_SYMBOL] = None
        self.parsedParmData[self.OPTION_FIAT_SAVE] = None
        self.parsedParmData[self.OPTION_PRICE_DATA] = None
        self.parsedParmData[self.OPTION_PRICE_AMOUNT] = None
        self.parsedParmData[self.OPTION_PRICE_SYMBOL] = None
        self.parsedParmData[self.OPTION_PRICE_SAVE] = None
        self.resetTemporaryData()


    def resetTemporaryData(self):
        '''
        This method cleans up any data which are not to be kept between user requests
        :return:
        '''
        self.parsedParmData[self.UNSUPPORTED_OPTION] = None
        self.parsedParmData[self.UNSUPPORTED_OPTION_MODIFIER] = None
        self.parsedParmData[self.UNSUPPORTED_OPTION_DATA] = None


    def execute(self):
        '''

        :seqdiag_return ResultData or False
        :return:
        '''
        resultPriceOrBoolean = self._validateMandatoryData()

        if resultPriceOrBoolean != True:
            return resultPriceOrBoolean

        localTimezone = self.configManager.localTimeZone
        localNow = DateTimeUtil.localNow(localTimezone)

        resultPriceOrBoolean = self._validateDateTimeData(localNow)

        if resultPriceOrBoolean != True:
            return resultPriceOrBoolean

        cryptoUpper = self.parsedParmData[self.CRYPTO].upper()
        unitUpper = self.parsedParmData[self.UNIT].upper()
        exchange = self.parsedParmData[self.EXCHANGE]

        dayStr = self.parsedParmData[self.DAY]

        if dayStr != None:
            day = int(dayStr)
        else:
            day = 0

        monthStr = self.parsedParmData[self.MONTH]

        if monthStr != None:
            month = int(monthStr)
        else:
            month = localNow.month
 
        yearStr = self.parsedParmData[self.YEAR]

        if yearStr != None:
            if len(yearStr) == 2:
                year = 2000 + int(yearStr)
            elif len(yearStr) == 4:
                year = int(yearStr)
            elif yearStr == '0':    # user entered -d0 !
                year = 0
        else:
            year = localNow.year

        hourStr = self.parsedParmData[self.HOUR]

        if hourStr != None:
            hour = int(hourStr)
        else:
            hour = 0

        minuteStr = self.parsedParmData[self.MINUTE]

        if minuteStr != None:
            minute = int(minuteStr)
        else:
            minute = 0

        #storing the parsed parm gata dicèionary before it
        #may be modified in case the user requested a RT
        #price. The initial dictionary wiLl be added to the
        #returned resultData so the client can have access
        #to the full command request, even if only a partial
        #request like -d or -c was entered. This is necessary
        #bcecause if the client is a GUI, it stores the list
        #of requests in order to be able to replay them !
        initialParsedParmDataDic = self.parsedParmData.copy()

        wasDateInFutureSetToLastYear = False
        localRequestDateTime = None

        if day + month + year == 0:
            # asking for RT price here. Current date is stored in parsed parm data for possible
            # use in next request
            self._storeDateTimeDataForNextPartialRequest(localNow)
        else:
            try:
                localRequestDateTime = DateTimeUtil.dateTimeComponentsToArrowLocalDate(day, month, year, hour, minute, 0, localTimezone)
            except ValueError as e:
                # is the when the user specify only the day if he enters 31 and the current month
                # has no 31st or if he enters 30 or 29 and we are on February
                result = ResultData()
                result.setValue(ResultData.RESULT_KEY_ERROR_MSG,
                                     "ERROR - {}: day {}, month {}".format(str(e), day, month))
                return result

            if DateTimeUtil.isAfter(localRequestDateTime, localNow):
                # request date is in the future ---> invalid. This happens for example in case
                # btc usd 31/12 bittrex entered sometime before 31/12. Then the request year is
                # forced to last year and a warning will be displayed.
                year = localNow.year - 1
                wasDateInFutureSetToLastYear = True

        optionValueSymbol = self.parsedParmData[self.OPTION_VALUE_SYMBOL]
        optionValueAmount = self.parsedParmData[self.OPTION_VALUE_AMOUNT]

        if optionValueSymbol:
            optionValueSymbol = optionValueSymbol.upper()

        if optionValueAmount:
            optionValueAmount = float(optionValueAmount)

        optionValueSaveFlag = self.parsedParmData[self.OPTION_VALUE_SAVE]
        result = self.receiver.getCryptoPrice(cryptoUpper,
                                              unitUpper,
                                              exchange,
                                              day,
                                              month,
                                              year,
                                              hour,
                                              minute,
                                              optionValueSymbol,
                                              optionValueAmount,
                                              optionValueSaveFlag,
                                              self.requestInputString)

        #the command components	denoting the user request will be used to recreate
        #a full command request which will be stored in the command history list.
        #The historry list can be replayed, stored on disk, edited ...
        result.setValue(ResultData.RESULT_KEY_INITIAL_COMMAND_PARMS, initialParsedParmDataDic)

        result.setValue(ResultData.RESULT_KEY_OPTION_VALUE_SAVE, optionValueSaveFlag)

        if wasDateInFutureSetToLastYear:
            result.setWarning(ResultData.WARNING_TYPE_FUTURE_DATE,
                              "Warning - request date {} can not be in the future and was shifted back to last year".format(
                                  localRequestDateTime.format(self.configManager.dateTimeFormat)))

        unsupportedOption = self.parsedParmData[self.UNSUPPORTED_OPTION]

        if unsupportedOption:
            result.setWarning(ResultData.WARNING_TYPE_UNSUPPORTED_OPTION,
                              "Warning - unsupported option {}{} in request {}".format(unsupportedOption, self.parsedParmData[self.UNSUPPORTED_OPTION_DATA], self.requestInputString))

        return result


    def isValid(self):
        '''
        Return True if the command contains valid data and can be executed
        '''
        return self.parsedParmData[self.PRICE_TYPE] != None


    def _validateMandatoryData(self):
        resultData = True

        unit = self.parsedParmData[self.UNIT]

        if unit == None or any(char.isdigit() for char in unit):
            resultData = ResultData()
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - unit missing or invalid")

        # debug code useful on phone !
        #        dateTimeList = [dayStr, monthStr, yearStr, hourStr, minuteStr]
        #        with open('/sdcard/compri.txt', 'a') as f:
        #            f.write(str(dateTimeList) + '\n')
                
        return resultData


    def _validateDateTimeData(self, localNow):
        '''
        Ensures that date/time info contained in the parsedParmData dic are valid and in
        a right format. If everything is ok, returns True.

        ['1', '10', '0', '2', '58'] #btc usd 1/10/0 2:58
        [None, None, None, '2', '57'] # btc usd 1 2:57
        ['11', '10', None, None, None] # neo btc 11/10
        :param localNow:
        :return: True if date/time values stored in the parsedParmData dic are valid. If an
                 error was detected, a new ResultData with a meaningfull error msg is
                 returned.
        '''

        dtFormatDic = DateTimeUtil.getDateAndTimeFormatDictionary(self.configManager.dateTimeFormat)

        dateShortFormat = dtFormatDic[DateTimeUtil.SHORT_DATE_FORMAT_KEY]
        dateLongFormat = dtFormatDic[DateTimeUtil.LONG_DATE_FORMAT_KEY]
        timeFormat = dtFormatDic[DateTimeUtil.TIME_FORMAT_KEY]

        resultData = True

        dayStr = self.parsedParmData[self.DAY]
        monthStr = self.parsedParmData[self.MONTH]
        yearStr = self.parsedParmData[self.YEAR]
        hourStr = self.parsedParmData[self.HOUR]
        minuteStr = self.parsedParmData[self.MINUTE]

        if (yearStr == '0' and
            monthStr == '0' and
            dayStr == '0'):
            # RT price asked
            return True
        else:
            # Here, the three date components are not all equal to 0 !
            if (yearStr == None and
                monthStr == None and
                dayStr == None and
                hourStr != None and
                minuteStr != None):
                # Here, only time was specified in the full request, which is now possible.
                # Current day, month and year are fornatted into the parsed parm data
                # and True is returned
                self.parsedParmData[self.DAY] = localNow.format('DD')
                self.parsedParmData[self.MONTH] = localNow.format('MM')
                self.parsedParmData[self.YEAR] = localNow.format('YYYY')
                return True
            elif (yearStr == None and
                  monthStr == None and
                  dayStr != None and
                  hourStr != None and
                  minuteStr != None):
                # Here, only day and time were specified in the full request, which is now possible.
                # Current month and year are fornatted into the parsed parm data
                # and True is returned
                self.parsedParmData[self.MONTH] = localNow.format('MM')
                self.parsedParmData[self.YEAR] = localNow.format('YYYY')
                return True
            elif (yearStr == '0' or
                # yearStr is None when only day/month specified -> valid !
                monthStr == '0' or
                monthStr == None or
                dayStr == '0' or
                dayStr == None):
                # only when user enters -d0 for RT price,
                # is yearStr equal to '0' since 0 is put
                # by Requesèer into day, month and year !
                resultData = ResultData()
                resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - date not valid")
                return resultData
            elif len(monthStr) > 2:
                resultData = ResultData()
                resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG,
                                     "ERROR - {} not conform to accepted month format (MM or M)".format(monthStr))
                return resultData
            elif yearStr != None:
                yearStrLen = len(yearStr)
                if yearStrLen != 2 and yearStrLen != 4:
                    resultData = ResultData()
                    resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG,
                                         "ERROR - {} not conform to accepted year format (YYYY, YY or '')".format(
                                             yearStr))

                    # avoiding that invalid year will pollute next price requests
                    self.parsedParmData[self.YEAR] = None
                    return resultData

            # validating full date. Catch inval day or inval month,
            # like day == 123 or day == 32 or month == 31
            if yearStr == None:
                yearStr = str(localNow.year)

            if hourStr == None:
                hourStr = str(localNow.hour)

            if minuteStr == None:
                minuteStr = str(localNow.minute)

            dateTimeTupleList = [('day', dayStr, dateShortFormat), ('month', monthStr, dateShortFormat), ('year', yearStr, dateLongFormat), ('hour', hourStr, timeFormat), ('minute', minuteStr, timeFormat)]

            try:
                for name, value, format in dateTimeTupleList:
                    int(value)
            except ValueError as e:
                resultData = ResultData()
                resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - invalid value: {} violates format for {} ({})".format(value, name, format))
                return resultData

            try:
                date = DateTimeUtil.dateTimeComponentsToArrowLocalDate(int(dayStr), int(monthStr), int(yearStr),
                                                                int(hourStr), int(minuteStr), 0,
                                                                self.configManager.localTimeZone)
            except ValueError as e:
                resultData = ResultData()
                resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - " + str(e))

        return resultData


    def _storeDateTimeDataForNextPartialRequest(self, localNow):
        self.parsedParmData[self.DAY] = str(localNow.day)
        self.parsedParmData[self.MONTH] = str(localNow.month)
        self.parsedParmData[self.YEAR] = str(localNow.year)
        self.parsedParmData[self.HOUR] = str(localNow.hour)
        self.parsedParmData[self.MINUTE] = str(localNow.minute)


if __name__ == '__main__':
    from configurationmanager import ConfigurationManager
    from pricerequester import PriceRequester
    from crypcompexchanges import CrypCompExchanges
    from processor import Processor
    import os

    if os.name == 'posix':
        FILE_PATH = '/sdcard/cryptopricer.ini'
    else:
        FILE_PATH = 'c:\\temp\\cryptopricer.ini'

    cm = ConfigurationManager(FILE_PATH)
    pr = PriceRequester()
    cryp = CrypCompExchanges()
    proc = Processor(cm, pr, cryp)
    
    cpr = CommandPrice(proc, cm)

    print('HISTORICAL')

    cpr.parsedParmData[cpr.CRYPTO] = 'btc'
    cpr.parsedParmData[cpr.UNIT] = 'usd'
    cpr.parsedParmData[cpr.EXCHANGE] = 'bittrex'
    cpr.parsedParmData[cpr.DAY] = '12'
    cpr.parsedParmData[cpr.MONTH] = '9'
    cpr.parsedParmData[cpr.YEAR] = '2017'
    cpr.parsedParmData[cpr.HOUR] = '10'
    cpr.parsedParmData[cpr.MINUTE] = '5'
    print(cpr.execute())

    cpr.parsedParmData[cpr.EXCHANGE] = 'unknown'
    print(cpr.execute())

    print('\nREAL TIME')
    
    cpr.parsedParmData[cpr.EXCHANGE] = 'bittrex'
    cpr.parsedParmData[cpr.DAY] = '0'
    cpr.parsedParmData[cpr.MONTH] = '0'
    cpr.parsedParmData[cpr.YEAR] = '0'
    cpr.parsedParmData[cpr.HOUR] = '0'
    cpr.parsedParmData[cpr.MINUTE] = '0'

    print(cpr.execute())

    cpr.parsedParmData[cpr.EXCHANGE] = 'unknown'
    print(cpr.execute())
