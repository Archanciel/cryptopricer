from datetimeutil import DateTimeUtil
from priceresult import PriceResult


class Processor:
    def __init__(self,
                 configManager,
                 priceRequester,
                 crypCompExchanges):
        self.configManager = configManager
        self.priceRequester = priceRequester
        self.crypCompExchanges = crypCompExchanges


    def getCryptoPrice(self,
                       crypto,
                       fiat,
                       exchange,
                       day,
                       month,
                       year,
                       hour,
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
            priceResult = self.priceRequester.getCurrentPrice(crypto, fiat, validExchangeSymbol)

            if priceResult.isEmpty(PriceResult.RESULT_KEY_ERROR_MSG):
                timeStamp = priceResult.getValue(PriceResult.RESULT_KEY_PRICE_TIME_STAMP)
                requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, localTz)
                requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)
                priceResult.setValue(PriceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, requestedDateTimeStr)
                return "{}/{} on {}:".format(priceResult.getValue(PriceResult.RESULT_KEY_CRYPTO), priceResult.getValue(PriceResult.RESULT_KEY_FIAT), priceResult.getValue(PriceResult.RESULT_KEY_EXCHANGE)) + ' ' + priceResult.getValue(PriceResult.RESULT_KEY_PRICE_DATE_TIME_STRING) + ' ' + str(priceResult.getValue(PriceResult.RESULT_KEY_PRICE))
            else:
                return "{}/{} on {}:".format(priceResult.getValue(PriceResult.RESULT_KEY_CRYPTO), priceResult.getValue(PriceResult.RESULT_KEY_FIAT), priceResult.getValue(PriceResult.RESULT_KEY_EXCHANGE)) + ' ' + priceResult.getValue(PriceResult.RESULT_KEY_ERROR_MSG)
        else:
            timeStampLocal = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, hour, minute, 0, localTz)
            timeStampUtcNoHHMM = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, 0, 0, 0, 'UTC')
            priceResult = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, timeStampLocal, timeStampUtcNoHHMM, validExchangeSymbol)

            if priceResult.isEmpty(PriceResult.RESULT_KEY_ERROR_MSG):
                if priceResult.getValue(PriceResult.RESULT_KEY_PRICE_TYPE) == PriceResult.PRICE_TYPE_HISTO_DAY:
                    #histoday price returned
                    requestedPriceArrowUtcDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampUtcNoHHMM, 'UTC')
                    requestedDateTimeStr = requestedPriceArrowUtcDateTime.format(self.configManager.dateTimeFormat)
                else:
                    requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampLocal, localTz)
                    requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)

                priceResult.setValue(PriceResult.RESULT_KEY_PRICE_DATE_TIME_STRING, requestedDateTimeStr)

                return "{}/{} on {}:".format(priceResult.getValue(PriceResult.RESULT_KEY_CRYPTO), priceResult.getValue(PriceResult.RESULT_KEY_FIAT), priceResult.getValue(PriceResult.RESULT_KEY_EXCHANGE)) + ' ' + priceResult.getValue(PriceResult.RESULT_KEY_PRICE_DATE_TIME_STRING) + ' ' + str(priceResult.getValue(PriceResult.RESULT_KEY_PRICE))
                # return "{}/{} on {}:".format(priceResult.getValue(PriceResult.RESULT_KEY_CRYPTO], priceResult.getValue(PriceResult.RESULT_KEY_FIAT], priceResult.getValue(PriceResult.RESULT_KEY_EXCHANGE]) + ' ' + requestedDateTimeStr + ' ' + \
                #         str(priceResult.getValue(self.priceRequester.IDX_CURRENT_PRICE])
            else:
                return "{}/{} on {}:".format(priceResult.getValue(PriceResult.RESULT_KEY_CRYPTO), priceResult.getValue(PriceResult.RESULT_KEY_FIAT), priceResult.getValue(PriceResult.RESULT_KEY_EXCHANGE) + ' ' + priceResult.getValue(PriceResult.RESULT_KEY_ERROR_MSG))
#                return "{}/{} on {}:".format(crypto, fiat, exchange) + ' ' + priceResult.getValue(self.priceRequester.IDX_ERROR_MSG]


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
    print(proc.getCryptoPrice(crypto,
                              fiat,
                              exchange,
                              day,
                              month,
                              year,
                              hour,
                              minute))

    print(proc.getCryptoPrice(crypto,
                              fiat,
                              'unknown_exchange',
                              day,
                              month,
                              year,
                              hour,
                              minute))

    day = 0
    month = 0
    year = 0
    hour = 0
    minute = 0

    print('\nREAL TIME')
    print(proc.getCryptoPrice(crypto,
                              fiat,
                              exchange,
                              day,
                              month,
                              year,
                              hour,
                              minute))

    print(proc.getCryptoPrice(crypto,
                              fiat,
                              'unknown_exchange',
                              day,
                              month,
                              year,
                              hour,
                              minute))
