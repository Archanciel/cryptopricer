import json
import sys
import ssl
import urllib.request
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from datetimeutil import DateTimeUtil
from resultdata import ResultData
from pricerequester import PriceRequester

MINUTE_PRICE_DAY_NUMBER_LIMIT = 7   # if the request date is older than current time - this value,
                                    # the price returned is a day close price, not a minute price !

IDX_DATA_ENTRY_TO = 1

class PriceRequesterTestStub(PriceRequester):
    '''
    This class is used for testing purposes only to solve the fact that sometimes requesting
    a fiat/fiat (USD/CHF for example) historical price does not return a correct price.
    '''

    def getHistoricalPriceAtUTCTimeStamp(self,
                                         crypto,
                                         unit,
                                         timeStampLocalForHistoMinute,
                                         timeStampUTCNoHHMMForHistoDay,
                                         exchange):
        '''
        Why do we pass two different time stamp to the method ?
        
        When requesting a minute price the time stamp obtained
        from a local arrow datetime object is used. If we
        request a minute price for 15:18 Zurich time (+00.02)
        time, the minute price returned is the one at UTC 13:18.
        Asking the same price from Mumbay would require to
        ask the price for 20:18 (+00.05).
        
        Now, when asking an histo day price, the returned price
        is a close price. But crypto trade 24 H a day. The "close"
        price time stamp must not be dependant from the location 
        from which the request is sent. Instead, the "close" price
        is the one at the passed date with hour and minute set to 0.
        This date is not a loculiszd date, but a UTC localization
        independant date.
        When you go on the Cryptocompare site and you search for 
        historical prices, the close price for a given date is
        the same whatever the location of the user is !

        :seqdiag_note Obtainins a minute price if request date < 7 days from now, else a day close price.
        :seqdiag_return ResultData
        '''
        resultData = super().getHistoricalPriceAtUTCTimeStamp(crypto,
                                                              unit,
                                                              timeStampLocalForHistoMinute,
                                                              timeStampUTCNoHHMMForHistoDay,
                                                              exchange)

        # fed up with this fucking provider which regurlarly return an invalid value of 1.06
        # for USD/CHF on CCCAGG on 12/9/17 !
        if crypto == 'USD' and unit == 'CHF' and exchange == 'CCCAGG' and timeStampUTCNoHHMMForHistoDay == 1536710400:
            resultData.setValue(resultData.RESULT_KEY_PRICE, 0.9728)
        elif crypto == 'USD' and unit == 'CHF' and exchange == 'CCCAGG' and timeStampUTCNoHHMMForHistoDay == 1505174400:
            resultData.setValue(resultData.RESULT_KEY_PRICE, 1.001)
        elif crypto == 'USD' and unit == 'EUR' and exchange == 'CCCAGG' and timeStampUTCNoHHMMForHistoDay == 1505174400:
            resultData.setValue(resultData.RESULT_KEY_PRICE, 0.8346)

        return resultData

    def getCurrentPrice(self,
                        crypto,
                        unit,
                        exchange):
        resultData = super().getCurrentPrice(crypto,
                                             unit,
                                             exchange)

        return resultData

if __name__ == '__main__':
    pr = PriceRequesterTestStub()

