import json
import sys
import ssl
import urllib.request
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup

from datetimeutil import DateTimeUtil
from resultdata import ResultData

IDX_DATA_ENTRY_TO = 1


class PriceRequester:
    def __init__(self):
        try:
            #since ssl prevents requesting the data from CryptoCompare
            #when run from Kivy GUI, it must be be disabled
            self.ctx = ssl.create_default_context()
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE
        except AttributeError:
            #occurs when run in QPython under Python 3.2
            self.ctx = None
      
    def getHistoricalPriceAtUTCTimeStamp(self, crypto, fiat, timeStampLocalForHistoMinute, timeStampUTCNoHHMMForHistoDay, exchange):
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
        resultData = ResultData()

        resultData.setValue(ResultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(ResultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(ResultData.RESULT_KEY_EXCHANGE, exchange)

        if DateTimeUtil.isTimeStampOlderThan(timeStampLocalForHistoMinute, dayNumberInt=7):
            return self._getHistoDayPriceAtUTCTimeStamp(crypto, fiat, timeStampUTCNoHHMMForHistoDay, exchange, resultData)
        else:
            return self._getHistoMinutePriceAtUTCTimeStamp(crypto, fiat, timeStampLocalForHistoMinute, exchange, resultData)
        
        
    def _getHistoMinutePriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange, resultData):
        timeStampUTCStr = str(timeStampUTC)
        url = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(coin, fiat, timeStampUTCStr, exchange)
        resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)

        try:
            if self.ctx == None:
                #here, run in QPython under Python 3.2
                webURL = urllib.request.urlopen(url)
            else:
                webURL = urllib.request.urlopen(url, context=self.ctx)
        except HTTPError as e:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Check your internet connection. Details: ' + str(e.reason))
        except URLError as e:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Check your internet connection. Details: ' + str(e.reason))
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(the_type))
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            if dic['Data'] != []:
                dataDic = dic['Data'][IDX_DATA_ENTRY_TO]
                resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, dataDic['time'])
                resultData.setValue(ResultData.RESULT_KEY_PRICE, dataDic['close'])
            else:
                resultData = self._handleError(dic, resultData, url)

        return resultData


    def _getHistoDayPriceAtUTCTimeStamp(self, crypto, fiat, timeStampUTC, exchange, resultData):
        timeStampUTCStr = str(timeStampUTC)
        url = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(crypto, fiat, timeStampUTCStr, exchange)
        resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)

        try:
            if self.ctx == None:
                #here, run in QPython under Python 3.2
                webURL = urllib.request.urlopen(url)
            else:
                webURL = urllib.request.urlopen(url, context=self.ctx)
        except HTTPError as e:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(e.reason))
        except URLError as e:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(e.reason))
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(the_type))
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            if dic['Data'] != []:
                dataDic = dic['Data'][IDX_DATA_ENTRY_TO]
                resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, dataDic['time'])
                resultData.setValue(ResultData.RESULT_KEY_PRICE, dataDic['close'])
            else:
                resultData = self._handleError(dic, resultData, url)

        return resultData


    def getCurrentPrice(self, crypto, fiat, exchange):
        url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&e={}".format(crypto, fiat, exchange)
        resultData = ResultData()

        resultData.setValue(ResultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(ResultData.RESULT_KEY_FIAT, fiat)
        resultData.setValue(ResultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)

        try:
            if self.ctx == None:
                #here, run in QPython under Python 3.2
                webURL = urllib.request.urlopen(url)
            else:
                webURL = urllib.request.urlopen(url, context=self.ctx)
        except HTTPError as e:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(e.reason))
        except URLError as e:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(e.reason))
        except: 
            the_type, the_value, the_traceback = sys.exc_info()
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - could not complete request ' + url + '. Reason: ' + str(the_type))
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
            
            if fiat in dic:
                resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, DateTimeUtil.utcNowTimeStamp())
                resultData.setValue(ResultData.RESULT_KEY_PRICE, dic[fiat]) #current price is indexed by fiat symbol in returned dic
            else:
                resultData = self._handleError(dic, resultData, url)

        return resultData

    def _handleError(self, dic, resultData, url):
        if 'Message' in dic.keys():
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, 'ERROR - ' + dic['Message'])
        else:
            resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG,
                                'ERROR - ' + 'Request ' + url + 'did not return any data !')

        return resultData


if __name__ == '__main__':
    pr = PriceRequester()

