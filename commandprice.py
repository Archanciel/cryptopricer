from abstractcommand import AbstractCommand
from datetimeutil import DateTimeUtil
from priceresult import PriceResult

class CommandPrice(AbstractCommand):
    CRYPTO = "CRYPTO"
    FIAT = "FIAT"
    EXCHANGE = "EXCHANGE"
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
    HOUR = "HOUR"           #store HH user input
    MINUTE = "MINUTE"       #store MM user input
    HOUR_MINUTE = "HM"      #temporary store HH:MM user input
    DAY_MONTH_YEAR = "DMY"  #temporary store DD/MM/YY user input

    def __init__(self, receiver=None, configManager=None, rawParmData='', parsedParmData={}):
        super().__init__(receiver, 'CommandPrice', rawParmData, parsedParmData)
        self.configManager = configManager
        self._initialiseParsedParmData()


    def _initialiseParsedParmData(self):
        '''
        Prefill the parsedParmData dictionary with empty key/value pair.
        If this is not done, the parsedParmData dictionary will only contain
        key/value pairs added at the first use of the command.

        For example, entering 'btc usd 0 Bittrex' will cause the parsedParmData dic
        to be initialized with only CRYPTO, FIAT, DAY_MONTH_YEAR, DAY, MONTH, YEAR
        and EXCHANGE entries. HOUR_MINUTE, HOUR and MINUTE will be missing. This
        will cause subsequent errors in Requester in case the firs usage was
        'btc usd 0 Bittrex'
        :return:
        '''
        self.parsedParmData[self.CRYPTO] = None
        self.parsedParmData[self.FIAT] = None
        self.parsedParmData[self.EXCHANGE] = None
        self.parsedParmData[self.DAY] = None
        self.parsedParmData[self.MONTH] = None
        self.parsedParmData[self.YEAR] = None
        self.parsedParmData[self.HOUR] = None
        self.parsedParmData[self.MINUTE] = None
        self.parsedParmData[self.DAY_MONTH_YEAR] = None
        self.parsedParmData[self.HOUR_MINUTE] = None


    def execute(self):
        localNow = DateTimeUtil.localNow(self.configManager.localTimeZone)

        resultPriceOrBoolean = self._validateDateTimeData(localNow)
        
        if resultPriceOrBoolean != True:
            return resultPriceOrBoolean
            
        cryptoUpper = self.parsedParmData[self.CRYPTO].upper()
        fiatUpper = self.parsedParmData[self.FIAT].upper()
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

        if day + month + year == 0:
            # asking for RT price here. Current date is stored in parsed parm data for possible
            # use in next request
            self._storeDateTimeDataForNextPartialRequest(localNow)

        result = self.receiver.getCryptoPrice(cryptoUpper,
                                              fiatUpper,
                                              exchange,
                                              day,
                                              month,
                                              year,
                                              hour,
                                              minute)
        	                            
        return result


    def _validateDateTimeData(self, localNow):
        '''
        ['1', '10', '0', '2', '58'] #btc usd 1/10/0 2:58
        [None, None, None, '2', '57'] # btc usd 1 2:57
        ['11', '10', None, None, None] # neo btc 11/10
        '''
        
        dayStr = self.parsedParmData[self.DAY]
        monthStr = self.parsedParmData[self.MONTH]
        yearStr = self.parsedParmData[self.YEAR]
        hourStr = self.parsedParmData[self.HOUR]
        minuteStr = self.parsedParmData[self.MINUTE]
        
        priceResult = True
        
        if (yearStr == '0' and
                    monthStr == '0' and
                    dayStr == '0'):
            # RT price asked
            return priceResult
        else:
            if (yearStr == '0' or
                #yearStr is None when only day/month specified -> valid !
                monthStr == '0' or
                        monthStr == None or
                        dayStr == '0' or
                        dayStr == None):
                # only when user enters -d0 for RT price,
                # is yearStr equal to '0' since 0 is put 
                # by Requesèer into day, month and year !                                                                       
                priceResult = PriceResult()
                priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - date not valid")
                return priceResult
            elif len(monthStr) > 2:
                priceResult = PriceResult()
                priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - {} not conform to accepted month format (MM or M)".format(monthStr))
                return priceResult
            elif yearStr != None:
                yearStrLen = len(yearStr)
                if yearStrLen != 2 and yearStrLen != 4:
                    priceResult = PriceResult()
                    priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - {} not conform to accepted year format (YYYY, YY or '')".format(yearStr))
                    
                    # avoiding that invalid year will pollute next price requests
                    self.parsedParmData[self.YEAR] = None
                    return priceResult
                    
            # validating full date. Catch inval day or inval month,
            # like day == 123 or day == 32 or month == 31
            if yearStr == None:
                yearStr = str(localNow.year)
                
            if hourStr == None:
                hourStr = str(localNow.hour)
                
            if minuteStr == None:
                minuteStr = str(localNow.minute)
                
            try:
                DateTimeUtil.dateTimeComponentsToArrowLocalDate(int(dayStr), int(monthStr), int(yearStr), int(hourStr), int(minuteStr), 0, self.configManager.localTimeZone)
            except ValueError as e:
                priceResult = PriceResult()
                priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - " + str(e))

# debug code useful on phone !
#        dateTimeList = [dayStr, monthStr, yearStr, hourStr, minuteStr]
#        with open('/sdcard/compri.txt', 'a') as f:
#            f.write(str(dateTimeList) + '\n')
                
        return priceResult
        
        
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
    cpr.parsedParmData[cpr.FIAT] = 'usd'
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
