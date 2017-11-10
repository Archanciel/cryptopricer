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
        cryptoUpper = self.parsedParmData[self.CRYPTO].upper()
        fiatUpper = self.parsedParmData[self.FIAT].upper()
        exchange = self.parsedParmData[self.EXCHANGE]

        dayStr = self.parsedParmData[self.DAY]

        if dayStr != None:
            day = int(dayStr)
        else:
            day = 0

        localNow = DateTimeUtil.localNow(self.configManager.localTimeZone)

        monthStr = self.parsedParmData[self.MONTH]

        if monthStr != None:
            if len(monthStr) <= 2:
                month = int(monthStr)
            else:
                priceResult = PriceResult()
                priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - {} not conform to accepted month format (MM, M, or '')".format(monthStr))
                return priceResult
        else:
            month = localNow.month
 
        yearStr = self.parsedParmData[self.YEAR]

        if yearStr != None:
            if len(yearStr) == 2:
                year = 2000 + int(yearStr)
            elif len(yearStr) == 4:
                year = int(yearStr)
            elif dayStr != '0' and monthStr != '0' and yearStr == '0': # only when user enters -d0 for RT price,
                                                                       # yearStr is '0' since 0 is put into day,
                                                                       # month and year. Otherwise, yearStr is
                                                                       # illegal and must generate an error msg !
                priceResult = PriceResult()
                priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - {} not conform to accepted year format (YYYY, YY or '')".format(yearStr))
                return priceResult
            elif yearStr == '0':    # user entered -d0 !
                year = 0
            else:
                priceResult = PriceResult()
                priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - {} not conform to accepted year format (YYYY, YY or '')".format(yearStr))
                return priceResult
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
        elif day == 0 or month == 0 or year == 0:
            priceResult = PriceResult()
            priceResult.setValue(PriceResult.RESULT_KEY_ERROR_MSG, "ERROR - {}/{}/{} is not a valid date".format(day, month, year))
            return priceResult

        result = self.receiver.getCryptoPrice(cryptoUpper,
                                              fiatUpper,
                                              exchange,
                                              day,
                                              month,
                                              year,
                                              hour,
                                              minute)
        	                            
        return result


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
