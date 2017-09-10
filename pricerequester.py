from datetime import datetime
from pytz import timezone
import time
import json
import urllib.request
from urllib.error import HTTPError, URLError
import sys
from bs4 import BeautifulSoup
#from tqdm import tqdm

DATE_TIME_FORMAT = "%d/%m/%y %H:%M"
DATE_TIME_FORMAT_TZ = DATE_TIME_FORMAT + " %Z%z"


class PriceRequester:
    def __init__(self, localTimeZone):
        self.localTimeZone = localTimeZone

    def _UTCTimestamp2LocalizedDate(self, utcTimestamp):
        """Return localized string repr of a UTC timestamp"""
        utcDateTimeObj = datetime.fromtimestamp(int(utcTimestamp - 3600)).replace(tzinfo=timezone('UTC'))
        #print(utcDateTimeObj.timetuple()[8])

        localizedDateTimeObj = utcDateTimeObj.astimezone(timezone(self.localTimeZone))
        #print(localizedDateTimeObj.timetuple()[8])
        return localizedDateTimeObj.strftime(DATE_TIME_FORMAT_TZ)

    def getPriceAtLocalDateTimeStr(self, coin, fiat, localDateTimeStr, exchange):
        datetimeObj = datetime.strptime(localDateTimeStr, DATE_TIME_FORMAT)
        localDatetimeObj = timezone(self.localTimeZone).localize(datetimeObj)
        datetimeObjUTC = localDatetimeObj.astimezone(timezone('UTC'))
        timeStampUTC = time.mktime(datetimeObjUTC.timetuple())

        return self.getPriceAtUTCTimeStamp(coin, fiat, timeStampUTC, exchange)

    def getPriceAtUTCTimeStamp(self, coin, fiat, timeStampUTC, exchange):
        timeStamp = str(int(timeStampUTC + 60))
        url = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}&e={}".format(coin, fiat, timeStamp, exchange)
        tmp = []

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
                lst = ['time', 'open', 'high', 'low', 'close']
                tmp.append(str(self._UTCTimestamp2LocalizedDate(dataDic['time'])))
                tmp.append(dataDic['close'])
            else:
                tmp = str(dic['Message'])
        return tmp

if __name__ == '__main__':
    import re
    pr = PriceRequester('Europe/Zurich')
    prompt = "crypto fiat d/m[/y] h:m exch (q/quit):\n"
    inputStr = input(prompt)
    #([0-9]+)-([0-9]+)(?:-([0-9]+)|) matches either 1-9 or 1-9-17
    patternFullData = r"(\w+) (\w+) ([0-9]+)/([0-9]+)(?:/([0-9]+)|) ([0-9:]+)(?: (\w+)|)"
    patternPartialData = r"(?:(-\w)([\w\d/:]+))(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?"
    crypto = ''
    fiat = ''
    exchange = ''
    day = ''
    month = ''
    year = ''
    hourMin = ''
    localDateTimeStr = ''
    
    while inputStr.upper() != 'Q':
        data = re.match(patternFullData, inputStr)
        
        if data == None:
            data = re.match(patternPartialData, inputStr)
            if data != None:
                partialArgList = data.groups()
                i = 0
                while i < len(partialArgList):
                    arg = partialArgList[i]
                    if arg != None:
                        val = partialArgList[i + 1]
                        if val != None:
                            valLower = val #for exchange !
                            val = val.upper()
                            arg = arg.upper()
                            if '-C' == arg:
                                crypto = val
                            elif '-F' == arg:
                                fiat = val
                            elif '-D' == arg:
                                date = val
                            elif '-T' == arg:
                                hourMin = val
                            elif '-E' == arg:
                                exchange = valLower
                    i += 2
            else:
                inputStr = input(prompt)
                continue
        else: #regular command line entered         
            crypto = data.group(1).upper()
            fiat = data.group(2).upper()
            day = data.group(3)
            month = data.group(4)
            year = data.group(5)
            
            hourMin = data.group(6)
        
            if year == None:
                year = '17'
            elif len(year) > 2:
                year = year[-2:]
            
            exchange = data.group(7)
        
            if exchange == None:
                exchange = 'CCCAGG'
                    
        if ':' not in hourMin:
            hourMin = hourMin + ':00'
    
        localDateTimeStr = day + '/' + month + '/' + year + ' ' + hourMin
        print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' '.join(map(str, pr.getPriceAtLocalDateTimeStr(crypto, fiat, localDateTimeStr, exchange))))
        inputStr = input(prompt)
