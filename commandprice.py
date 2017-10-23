from abstractcommand import AbstractCommand

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

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        super().__init__(receiver, 'CommandPrice', rawParmData, parsedParmData)

    def execute(self):
        dayStr = self.parsedParmData[self.DAY]
        if dayStr != None:
            day = int(dayStr)
        else:
            day = 0

        monthStr = self.parsedParmData[self.MONTH]
        if monthStr != None:
            month = int(monthStr)
        else:
            month = 0
 
        yearStr = self.parsedParmData[self.YEAR]
        if yearStr != None:
            year = int(yearStr)
        else:
            year = 0
            
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
    
        result = self.receiver.getCryptoPrice(self.parsedParmData[self.CRYPTO], \
        	                            self.parsedParmData[self.FIAT], \
        	                            self.parsedParmData[self.EXCHANGE], \
        	                            day, \
        	                            month, \
        	                            year, \
        	                            hour, \
        	                            minute)
        	                            
        return result


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
    
    cpr = CommandPrice(proc)

    print('HISTORICAL')

    cpr.parsedParmData[cpr.CRYPTO] = 'BTC'
    cpr.parsedParmData[cpr.FIAT] = 'USD'
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

    print(cpr.execute())

    cpr.parsedParmData[cpr.EXCHANGE] = 'unknown'
    print(cpr.execute())
