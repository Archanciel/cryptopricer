import json
import sys
import urllib.request
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from datetimeutil import DateTimeUtil

HISTO_DAY_FLAG_VALUE = True
CURRENT_OR_HISTO_MINUTE_FLAG_VALUE = False

IDX_HISTODAY_DATA_ENTRY_TO = 1
IDX_MINUTEDAY_DATA_ENTRY_TO = 1


class PriceRequester:
    IDX_IS_DAY_CLOSE_PRICE = 0
    IDX_TIMESTAMP = 1
    IDX_ERROR_MSG = 1
    IDX_CLOSE_PRICE = 2
    IDX_CURRENT_PRICE = 2

    def __init__(self):
        self._resultList = []


    def getHistoricalPriceAtUTCTimeStamp(self, coin, fiat, timeStampLocalForHistoMinute, timeStampUTCNoHHMMForHistoDay, exchange):
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
        '''
        if DateTimeUtil.isTimeStampOlderThan(timeStampLocalForHistoMinute, dayNumber=7):
            return self._getHistoDayPriceAtUTCTimeStamp(coin, fiat, timeStampUTCNoHHMMForHistoDay, exchange)
        else:
            return self._getHistoMinutePriceAtUTCTimeStamp(coin, fiat, timeStampLocalForHistoMinute, exchange)
        
        
    def _getHistoMinutePriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange):
        timeStampUTCStr = str(timeStampUTC)
        url = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(coin, fiat, timeStampUTCStr, exchange)
        self._resultList = []
        self._resultList.append(CURRENT_OR_HISTO_MINUTE_FLAG_VALUE)

        try:
            webURL = urllib.request.urlopen(url)
        except HTTPError as e:
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(e.reason))
        except URLError as e:
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(e.reason))
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(the_type))
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            if dic['Data'] != []:
                dataDic = dic['Data'][IDX_MINUTEDAY_DATA_ENTRY_TO]
                self._resultList.append(dataDic['time'])
                self._resultList.append(dataDic['close'])
            else:
                self._resultList.append('ERROR - ' + dic['Message'])
        return self._resultList


    def _getHistoDayPriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange):
        timeStampUTCStr = str(timeStampUTC)
        url = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(coin, fiat, timeStampUTCStr, exchange)
        self._resultList = []
        self._resultList.append(HISTO_DAY_FLAG_VALUE)

        try:
            webURL = urllib.request.urlopen(url)
        except HTTPError as e:
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(e.reason))
        except URLError as e:
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(e.reason))
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(the_type))
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            if dic['Data'] != []:
                dataDic = dic['Data'][IDX_HISTODAY_DATA_ENTRY_TO]
                self._resultList.append(dataDic['time'])
                self._resultList.append(dataDic['close'])
            else:
                self._resultList.append('ERROR - ' + dic['Message'])
        return self._resultList


    def getCurrentPrice(self, coin, fiat, exchange):
        url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&e={}".format(coin, fiat, exchange)
        self._resultList = []
        self._resultList.append(CURRENT_OR_HISTO_MINUTE_FLAG_VALUE)

        try:
            webURL = urllib.request.urlopen(url)
        except HTTPError as e:
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(e.reason))
        except URLError as e:
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(e.reason))
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            sys.exit('Could not complete request ' + url + '. Reason: ' + str(the_type))
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            
            if fiat in dic:
                self._resultList.append(DateTimeUtil.utcNowTimeStamp())
                self._resultList.append(dic[fiat]) #current price is indexed by fiat symbol in returned dic
            else:
                self._resultList.append('ERROR - ' + dic['Message'])
        return self._resultList


if __name__ == '__main__':
    pass