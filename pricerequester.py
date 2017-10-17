import json
import json
import sys
import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from datetimeutil import DateTimeUtil

IDX_HISTODAY_DATA_ENTRY_TO = 1
IDX_MINUTEDAY_DATA_ENTRY_TO = 1


class PriceRequester:
    IDX_TIMESTAMP = 0
    IDX_ERROR_MSG = 0
    IDX_CLOSE_PRICE = 1
    IDX_CURRENT_PRICE = 1    
    
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
                dataDic = dic['Data'][IDX_MINUTEDAY_DATA_ENTRY_TO]
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
                dataDic = dic['Data'][IDX_HISTODAY_DATA_ENTRY_TO]
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
            
            if fiat in dic:
                resultList.append(DateTimeUtil.utcNowTimeStamp())
                resultList.append(dic[fiat]) #current price is indexed by fiat symbol in returned dic
            else:
                resultList = ['ERROR-' + dic['Message']]
        return resultList


if __name__ == '__main__':
    import re
    import os
    from io import StringIO
    from configurationmanager import ConfigurationManager
    from datetimeutil import DateTimeUtil

    FR_DATE_TIME_FORMAT_ARROW = 'DD/MM/YYYY HH:mm:ss'
    FR_YY_DATE_TIME_FORMAT_ARROW = 'DD/MM/YY HH:mm:ss'
    FR_DATE_TIME_FORMAT_TZ_ARROW = FR_DATE_TIME_FORMAT_ARROW + ' ZZ'
    FR_YY_DATE_TIME_FORMAT_TZ_ARROW = FR_YY_DATE_TIME_FORMAT_ARROW + ' ZZ'
    PATTERN_FULL_PRICE_REQUEST_DATA = r"(\w+)(?: (\w+)|) ([0-9]+)/([0-9]+)(?:/([0-9]+)|) ([0-9:]+)(?: (\w+)|)"
    PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:]+))(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?"

    stdin = sys.stdin
    sys.stdin = StringIO('btc usd 12/10 12:00 BitTrex')

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
            requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], localTz)
            requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(configMgr.dateTimeFormat)
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + requestedDateTimeStr + ' ' + str(priceInfoList[pr.IDX_CLOSE_PRICE]))
        else:
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[pr.IDX_ERROR_MSG])

        #current orice
        priceInfoList = pr.getCurrentPrice(crypto, fiat, exchange)

        if len(priceInfoList) > 1:
            requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], localTz)
            requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(configMgr.dateTimeFormat)
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + requestedDateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))
        else:
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[pr.IDX_ERROR_MSG])

        #histo day price
        timeStamp = 1506787315 #30/09/2017 16:01:55 +00:00 or 30/09/2017 18:01:55 +02:00
        arrowObjTimeStampUTC = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'UTC')
        print('arrowObjTimeStampUTC: ' + arrowObjTimeStampUTC.format(FR_DATE_TIME_FORMAT_TZ_ARROW))
        arrowObjTimeStampZH = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, 'Europe/Zurich')
        print('arrowObjTimeStampZH: ' + arrowObjTimeStampZH.format(FR_DATE_TIME_FORMAT_TZ_ARROW))

        priceInfoList = pr.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, arrowObjTimeStampZH.timestamp, exchange)

        if len(priceInfoList) > 1:
            priceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], localTz)
            dateTimeStr = priceArrowLocalDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
            print("arrowObjTimeStampZH.timestamp: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))
        else:
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[pr.IDX_ERROR_MSG])

        priceInfoList = pr.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, timeStamp, exchange)

        if len(priceInfoList) > 1:
            priceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], localTz)
            dateTimeStr = priceArrowLocalDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
            print("timeStamp: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))
            priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], 'UTC')
            dateTimeStr = priceArrowUTCDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
            print("priceArrowUTCDateTime: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))
        else:
            print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + priceInfoList[pr.IDX_ERROR_MSG])

        utcArrowDateTimeObj_endOfDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/09/30 23:59:59", 'UTC', "YYYY/MM/DD HH:mm:ss")
        print('\n\n' + utcArrowDateTimeObj_endOfDay.format(FR_DATE_TIME_FORMAT_TZ_ARROW))
        priceInfoList = pr._getHistoDayPriceAtUTCTimeStamp(crypto, fiat, utcArrowDateTimeObj_endOfDay.timestamp, exchange)
        print('passed eod ts: ' + str(utcArrowDateTimeObj_endOfDay.timestamp))
        print('returned eod ts: ' + str(priceInfoList[pr.IDX_TIMESTAMP]))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], 'UTC')
        dateTimeStr = priceArrowUTCDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
        print("utcArrowDateTimeObj _getHistoDayPrice...: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))

        priceInfoList = pr.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, utcArrowDateTimeObj_endOfDay.timestamp, exchange)
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], 'UTC')
        dateTimeStr = priceArrowUTCDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
        print("utcArrowDateTimeObj_endOfDay getHistorical...: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))

        utcArrowDateTimeObj_begNextDay = DateTimeUtil.dateTimeStringToArrowLocalDate("2017/10/01 00:00:00",'UTC',"YYYY/MM/DD HH:mm:ss")
        print('\n\n' + utcArrowDateTimeObj_begNextDay.format(FR_DATE_TIME_FORMAT_TZ_ARROW))
        priceInfoList = pr._getHistoDayPriceAtUTCTimeStamp(crypto, fiat, utcArrowDateTimeObj_begNextDay.timestamp, exchange)
        print('passed beg nxt day ts: ' + str(utcArrowDateTimeObj_begNextDay.timestamp))
        print('returned beg nxt day ts: ' + str(priceInfoList[pr.IDX_TIMESTAMP]))
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], 'UTC')
        dateTimeStr = priceArrowUTCDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
        print("utcArrowDateTimeObj_begNextDay _getHistoDayPrice...: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))

        priceInfoList = pr.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, utcArrowDateTimeObj_begNextDay.timestamp, exchange)
        priceArrowUTCDateTime = DateTimeUtil.timeStampToArrowLocalDate(priceInfoList[pr.IDX_TIMESTAMP], 'UTC')
        dateTimeStr = priceArrowUTCDateTime.format(FR_DATE_TIME_FORMAT_TZ_ARROW)
        print("utcArrowDateTimeObj_begNextDay getHistorical...: {}/{} on {}: ".format(crypto, fiat, exchange) + ' ' + dateTimeStr + ' ' + str(priceInfoList[pr.IDX_CURRENT_PRICE]))

        print('Conclusion: you need to pass beg of next day to histoday and shift back returned ts to end of current day !')

        sys.stdin = stdin

        inputStr = input(prompt)
