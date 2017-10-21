from abstractcommand import AbstractCommand
from datetimeutil import DateTimeUtil


class Processor:
    def __init__(self, \
                 configManager, \
                 priceRequester, \
                 crypCompExchanges):
        self.configManager = configManager
        self.priceRequester = priceRequester
        self.crypCompExchanges = crypCompExchanges


    def getCryptoPrice(self, \
                       crypto, \
                       fiat, \
                       exchange, \
                       day, \
                       month, \
                       year, \
                       hour, \
                       minute):
        try:
            validExchangeSymbol = self.crypCompExchanges.getExchange(exchange)
        except(KeyError):
            return "ERROR - invalid exchange '{}'".format(exchange)

        localTz = self.configManager.localTimeZone
        dateTimeFormat = self.configManager.dateTimeFormat

        if (day + month + year + hour + minute) == 0:
            # when the user specifies 0 for either the date or the time,
            # this means current price is asked and all date/time components
            # are set to zero !
            priceInfoList = self.priceRequester.getCurrentPrice(crypto, fiat, validExchangeSymbol)

            if len(priceInfoList) > 1:
                timeStamp_ = priceInfoList[self.priceRequester.IDX_TIMESTAMP]
                requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStamp_, localTz)
                requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)
                return "{}/{} on {}: ".format(crypto, fiat, validExchangeSymbol) + ' ' + requestedDateTimeStr + ' ' + str(priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])
            else:
                return "{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[self.priceRequester.IDX_ERROR_MSG]
        else:
            timeStampUtc = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, hour, minute, 0, 'Europe/Zurich')
            priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, timeStampUtc, validExchangeSymbol)

            if len(priceInfoList) > 1:
                requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampUtc, localTz)
                requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)
                return "{}/{} on {}: ".format(crypto, fiat, validExchangeSymbol) + ' ' + requestedDateTimeStr + ' ' + \
                        str(priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])
            else:
                return "{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[self.priceRequester.IDX_ERROR_MSG]


if __name__ == '__main__':
    from configurationmanager import ConfigurationManager
    from pricerequester import PriceRequester
    from crypcompexchanges import CrypCompExchanges
    import os

    if os.name == 'posix':
        FILE_PATH = '/sdcard/cryptopricer.ini'
    else:
        FILE_PATH = 'c:\\temp\\cryptopricer.ini'

    cm = ConfigurationManager(FILE_PATH)
    pr = PriceRequester()
    cryp = CrypCompExchanges()
    proc = Processor(cm, pr, cryp)

    crypto = 'BTC'
    fiat = 'USD'
    exchange = 'bittrex'
    day = 12
    month = 9
    year = 2017
    hour = 10
    minute = 5

    print('HISTORICAL')
    print(proc.getCryptoPrice(crypto, \
                              fiat, \
                              exchange, \
                              day, \
                              month, \
                              year, \
                              hour, \
                              minute))

    print(proc.getCryptoPrice(crypto, \
                              fiat, \
                              'unknown_exchange', \
                              day, \
                              month, \
                              year, \
                              hour, \
                              minute))

    day = 0
    month = 0
    year = 0
    hour = 0
    minute = 0

    print('\nREAL TIME')
    print(proc.getCryptoPrice(crypto, \
                              fiat, \
                              exchange, \
                              day, \
                              month, \
                              year, \
                              hour, \
                              minute))

    print(proc.getCryptoPrice(crypto, \
                              fiat, \
                              'unknown_exchange', \
                              day, \
                              month, \
                              year, \
                              hour, \
                              minute))
