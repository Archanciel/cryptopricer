import json
import json
import sys
import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from datetimeutil import DateTimeUtil



#from tqdm import tqdm

class PriceRequester:
    def getHistoricalPriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange):
        if DateTimeUtil.isTimeStampOlderThan(timeStampUTC, dayNumber=7):
            return self._getHistoDayPriceAtUTCTimeStamp(coin, fiat, DateTimeUtil.shiftTimeStampToEndOfDay(timeStampUTC), exchange)
        else:
            return self._getHistoMinutePriceAtUTCTimeStamp(coin, fiat, timeStampUTC, exchange)


    def _getHistoMinutePriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange):
        timeStampUTCStr = str(timeStampUTC)
        url = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(coin, fiat, timeStampUTCStr, exchange)
        resultList = []

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
                dataDic = dic['Data'][0]
                resultList.append(dataDic['time'])
                resultList.append(dataDic['close'])
            else:
                resultList = ['ERROR-' + dic['Message']]
        return resultList


    def _getHistoDayPriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange):
        timeStampUTCStr = str(timeStampUTC)
        url = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(coin, fiat, timeStampUTCStr, exchange)
        resultList = []

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
                dataDic = dic['Data'][0]
                resultList.append(dataDic['time'])
                resultList.append(dataDic['close'])
            else:
                resultList = ['ERROR-' + dic['Message']]
        return resultList


    def getCurrentPrice(self, coin, fiat, exchange):
        url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}&e={}".format(coin, fiat, exchange)
        resultList = []

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
            if len(dic) > 0:
                resultList.append(dic[fiat])
            else:
                resultList = ['ERROR-' + dic['Message']]
        return resultList


if __name__ == '__main__':
    import re
    import os
    from configurationmanager import ConfigurationManager
    from datetimeutil import DateTimeUtil

    PATTERN_FULL_PRICE_REQUEST_DATA = r"(\w+)(?: (\w+)|) ([0-9]+)/([0-9]+)(?:/([0-9]+)|) ([0-9:]+)(?: (\w+)|)"
    PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:]+))(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?"

    if os.name == 'posix':
        FILE_PATH = '/sdcard/cryptopricer.ini'
    else:
        FILE_PATH = 'c:\\temp\\cryptopricer.ini'

    configMgr = ConfigurationManager(FILE_PATH)
    pr = PriceRequester()
    prompt = "crypto fiat d/m[/y] h:m exch (q/quit):\n"
    inputStr = input(prompt)
    #([0-9]+)-([0-9]+)(?:-([0-9]+)|) matches either 1-9 or 1-9-17
    crypto = ''
    fiat = ''
    exchange = ''
    day = ''
    month = ''
    year = ''
    hourMin = ''
    localDateTimeStr = ''
    commandVarDic = {'-c' : 'crypto',
                 '-f' : 'fiat',
                 '-t' : 'hourMin',
                 '-e' : 'exchange'}

    while inputStr.upper() != 'Q':
        match = re.match(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        if match == None:
            match = re.match(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)
            if match != None:
                partialArgList = match.groups()
                it = iter(partialArgList)

                for command in it:
                    value = next(it)
                    if value != None:
                        if command != '-e': #all values except exchange name !
                            value = value.upper()
                        exec(commandVarDic[command] + " = value")
            else:
                inputStr = input(prompt)
                continue
        else: #regular command line entered
            crypto = match.group(1).upper()
            fiat = match.group(2).upper()
            day = match.group(3)
            if len(day) == 1:
                day = '0' + day
            month = match.group(4)
            if len(month) == 1:
                month = '0' + month
            year = match.group(5)

            hourMin = match.group(6)

            if year == None:
                year = '17'
            elif len(year) > 2:
                year = year[-2:]

            exchange = match.group(7)

        if ':' not in hourMin:
            hourMin = hourMin + ':00'

        localDateTimeStr = day + '/' + month + '/' + year + ' ' + hourMin
        localTz = configMgr.localTimeZone
        daTmFormat = configMgr.dateTimeFormat
        arrowLocalDateTime = DateTimeUtil.dateTimeStringToArrowLocalDate(localDateTimeStr, localTz, daTmFormat)

        #histo price
        priceInfoList = pr.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, arrowLocalDateTime.timestamp, exchange)

        if len(priceInfoList) > 1:
            priceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[0], localTz)
            dateTimeStr = priceArrowLocalDateTime.format(configMgr.dateTimeFormat)
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[1]))
        else:
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[0])

        #current orice
        priceInfoList = pr.getCurrentPrice(crypto, fiat, exchange)
        priceArrowLocalDateTime = DateTimeUtil.localNow(localTz)
        dateTimeStr = priceArrowLocalDateTime.format(configMgr.dateTimeFormat)
        print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[0]))

        #histo day price
        priceInfoList = pr._getHistoDayPriceAtUTCTimeStamp(crypto, fiat, arrowLocalDateTime.timestamp, exchange)

        if len(priceInfoList) > 1:
            priceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[0], localTz)
            dateTimeStr = priceArrowLocalDateTime.format(configMgr.dateTimeFormat)
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[1]))
        else:
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[0])

        inputStr = input(prompt)
