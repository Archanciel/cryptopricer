from datetimeutil import DateTimeUtil
from resultdata import ResultData


class Processor:
    '''
    This class is used as Receiver by the Command component in the Command pattern.
    '''
    def __init__(self,
                 configManager,
                 priceRequester,
                 crypCompExchanges):
        self.configManager = configManager
        self.priceRequester = priceRequester
        self.crypCompExchanges = crypCompExchanges


    def getCryptoPrice(self,
                       crypto,
                       unit,
                       exchange,
                       day,
                       month,
                       year,
                       hour,
                       minute,
                       optionValueSymbol = None,
                       optionValueAmount = None,
                       optionValueSaveFlag = None,
                       requestInputString = ''):
        '''
        Ask the PriceRequester either a RT price or a historical price. Then, in case a price value parm (-v)
        was specified, does the conversion and add its result to the returned ResultData
        :param crypto: upper case crypto symbol
        :param unit: upper case counter party symbol
        :param exchange: exchange name
        :param day: int day number
        :param month: int month number
        :param year: int year number
        :param hour: int hour number
        :param minute: int minute number
        :param optionValueSymbol: upper case price value symbol. If == crypto, this means that optionValueAmount provided
                                 is in crypto and must be converted into unit (counter party) at the rate returned by
                                 the PriceRequester.

                                 If the price value symbol == unit, this means that optionValueAmount provided
                                 is in the counter party (unit or an other crypto) and must be converted into crypto at
                                 the rate returned by the PriceRequester.

                                 Ex 1:  -v0.001btc
                                        crypto == BTC
                                        unit == USD
                                        optionValueSymbol == BTC
                                        optionValueAmount == 0.001

                                        if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
                                        converted value will be 20000 USD * 0.001 BTC => 200 USD

                                 Ex 2:  -v500usd
                                        crypto == BTC
                                        unit == USD
                                        optionValueSymbol == USD
                                        optionValueAmount == 500

                                        if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
                                        converted value will be 1 / 20000 USD * 500 USD => 0.025 BTC

        :param optionValueAmount: float price value amount
        :param optionValueSaveFlag: used to refine warning if value command not applicable
        :param requestInputString): used for better error msg !

        :seqdiag_return ResultData
        :return: a ResultData filled with result values
        '''
        if exchange == None:
            resultData = ResultData()
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - exchange could not be parsed due to an error in your request ({})".format(requestInputString))
            return resultData
        else:
            try:
                validExchangeSymbol = self.crypCompExchanges.getExchange(exchange)
            except(KeyError):
                resultData = ResultData()
                resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - {} market does not exist for this coin pair ({}-{})".format(exchange, crypto, unit))
                return resultData

        localTz = self.configManager.localTimeZone
        dateTimeFormat = self.configManager.dateTimeFormat

        if (day + month + year) == 0:
            # when the user specifies 0 for either the date,
            # this means current price is asked and date components
            # are set to zero !
            resultData = self.priceRequester.getCurrentPrice(crypto, unit, validExchangeSymbol)

            if resultData.isEmpty(ResultData.RESULT_KEY_ERROR_MSG):
                #adding date time info if no error returned
                timeStamp = resultData.getValue(ResultData.RESULT_KEY_OPTION_TIME_STAMP)
                requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, localTz)
                requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)
                resultData.setValue(ResultData.RESULT_KEY_OPTION_DATE_TIME_STRING, requestedDateTimeStr)
        else:
            #getting historical price, either histo day or histo minute
            timeStampLocal = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, hour, minute, 0, localTz)
            timeStampUtcNoHHMM = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, 0, 0, 0, 'UTC')
            resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(crypto, unit, timeStampLocal, timeStampUtcNoHHMM, validExchangeSymbol)

            if resultData.isEmpty(ResultData.RESULT_KEY_ERROR_MSG):
                #adding date time info if no error returned
                if resultData.getValue(ResultData.RESULT_KEY_OPTION_TYPE) == ResultData.PRICE_TYPE_HISTO_DAY:
                    #histoday price returned
                    requestedPriceArrowUtcDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampUtcNoHHMM, 'UTC')
                    requestedDateTimeStr = requestedPriceArrowUtcDateTime.format(self.configManager.dateTimeFormat)
                else:
                    requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampLocal, localTz)
                    requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)

                resultData.setValue(ResultData.RESULT_KEY_OPTION_DATE_TIME_STRING, requestedDateTimeStr)
                
        if optionValueSymbol != None and not resultData.isError():
            resultData = self._computePriceValue(resultData, crypto, unit, optionValueSymbol, optionValueAmount, optionValueSaveFlag)
            
        return resultData


    def _computePriceValue(self, resultData, crypto, unit, optionValueSymbol, optionValueAmount, optionValueSaveFlag):
        '''
        Compute the optionValueAmount according to the passed parms and put the result in
        the passed resultData.
        :param optionValueSymbol: upper case price value symbol. If == crypto, this means that optionValueAmount provided
                                 is in crypto and must be converted into unit at the rate returned by the PriceRequester.

                                 If the price value symbol == unit, this means that optionValueAmount provided
                                 is in unit and must be converted into crypto at the rate returned by the PriceRequester.

                                 Ex 1:  crypto == BTC
                                        unit == USD
                                        optionValueSymbol == BTC
                                        optionValueAmount == 0.001

                                        if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
                                        converted value will be 20000 USD * 0.001 BTC => 200 USD

                                 Ex 2:  crypto == BTC
                                        unit == USD
                                        optionValueSymbol == USD
                                        optionValueAmount == 500

                                        if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
                                        converted value will be 1 / 20000 USD * 500 USD => 0.025 BTC

        :param optionValueAmount: float price value amount
        :param optionValueSaveFlag: used to refine warning if value command not applicable
        :return: a ResultData in which price value info has been added.
        '''
        conversionRate = resultData.getValue(resultData.RESULT_KEY_PRICE)
        
        if optionValueSymbol == crypto:
            #converting optionValueAmount in crypto to equivalent value in unit
            convertedValue = optionValueAmount * conversionRate
            resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueAmount)
            resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, convertedValue)
        elif optionValueSymbol == unit:
            #converting optionValueAmount in unit to equivalent value in crypto
            convertedValue = optionValueAmount / conversionRate
            resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, convertedValue)
            resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueAmount)
        else:
            if optionValueSaveFlag:
                valueCommand = '-vs'
            else:
                valueCommand = '-v'

            if optionValueSymbol != '':
                resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE,
                                      "WARNING - currency value symbol {} differs from both crypto ({}) and unit ({}) of last request. {} option ignored".format(
                                          optionValueSymbol, crypto, unit, valueCommand))
            else:
                resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE,
                                      "WARNING - currency value symbol missing. {} option ignored".format(valueCommand))
        return resultData

            
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
    unit = 'USD'
    exchange = 'bittrex'
    day = 12
    month = 9
    year = 2017
    hour = 10
    minute = 5

    print('HISTORICAL')
    print(proc.getCryptoPrice(crypto,
                              unit,
                              exchange,
                              day,
                              month,
                              year,
                              hour,
                              minute))

    print(proc.getCryptoPrice(crypto,
                              unit,
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
                              unit,
                              exchange,
                              day,
                              month,
                              year,
                              hour,
                              minute))

    print(proc.getCryptoPrice(crypto,
                              unit,
                              'unknown_exchange',
                              day,
                              month,
                              year,
                              hour,
                              minute))
