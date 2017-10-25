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
            return "{}/{} on {}:".format(crypto, fiat, exchange) + ' ' + "ERROR - {} market does not exist for this coin pair ({}-{})".format(exchange, crypto, fiat)
        except Exception as e:
            #occurs if exchange name does not start with an upper case. Parsing it returns None !
            return "{}/{} on {}:".format(crypto, fiat, exchange) + ' ' + "ERROR - {}".format(str(e))

        localTz = self.configManager.localTimeZone
        dateTimeFormat = self.configManager.dateTimeFormat

        if (day + month + year) == 0:
            # when the user specifies 0 for either the date,
            # this means current price is asked and date components
            # are set to zero !
            priceInfoList = self.priceRequester.getCurrentPrice(crypto, fiat, validExchangeSymbol)

            if len(priceInfoList) > 2:
                timeStamp_ = priceInfoList[self.priceRequester.IDX_TIMESTAMP]
                requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStamp_, localTz)
                requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)
                return "{}/{} on {}:".format(crypto, fiat, validExchangeSymbol) + ' ' + requestedDateTimeStr + ' ' + str(priceInfoList[self.priceRequester.IDX_CURRENT_PRICE])
            else:
                return "{}/{} on {}:".format(crypto, fiat, exchange) + ' ' + priceInfoList[self.priceRequester.IDX_ERROR_MSG]
        else:
            timeStampUtc = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, hour, minute, 0, 'Europe/Zurich')
            priceInfoList = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, timeStampUtc, validExchangeSymbol)

            if len(priceInfoList) > 2:
                requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampUtc, localTz)
                if priceInfoList[self.priceRequester.IDX_IS_DAY_CLOSE_PRICE]:
                    #histoday price returned
                    requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(self.configManager.dateOnlyFormat)
                else:
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
