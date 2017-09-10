from datetime import datetime
from pytz import timezone
import time
import json
import urllib.request
from urllib.error import HTTPError, URLError
import sys
from bs4 import BeautifulSoup
#from tqdm import tqdm

DATE_TIME_FORMAT = "%d-%m-%y %H:%M"
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
        #timeStamp = str(int(timeStampUTC + 45))
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
    #            print(dataDic)
                lst = ['time', 'open', 'high', 'low', 'close']
                tmp.append(str(self._UTCTimestamp2LocalizedDate(dataDic['time'])))
                tmp.append(dataDic['close'])
                """
                for e in enumerate(lst):
                    x = e[0]
                    y = dataDic[e[1]]
                    if (x == 0):
                        tmp.append(str(self._UTCTimestamp2LocalizedDate(y)))
                    else:
                        tmp.append(y)
                """
            else:
                #tmp = ["No minute data available for " + self._UTCTimestamp2LocalizedDate(timeStampUTC)]
                #print(dic)
                tmp = str(dic['Message'])
        return tmp

    def explore(self):
        print('\nConverting now ...')
        fmt = "%Y-%m-%d %H:%M:%S %Z%z"

        print('Current time in UTC')
        now_utc = datetime.now(timezone('UTC'))
#        now_utc = datetime.utcnow()
        print(now_utc.strftime(fmt))

        print('Convert to US/Pacific time zone')
        now_pacific = now_utc.astimezone(timezone('US/Pacific'))
        print(now_pacific.strftime(fmt))

        print('Convert to Europe/Zurich time zone')
        now_berlin = now_pacific.astimezone(timezone('Europe/Zurich'))
        print(now_berlin.strftime(fmt))


        print('\nLocalizing a date/time')
        dateStr = "2014-05-28 22:28:15"
        datetimeObj_naive = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")

        # Wrong way!
        datetimeObj_pacific = datetimeObj_naive.replace(tzinfo=timezone('US/Pacific'))
        print('WRONG')
        print(datetimeObj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        # Right way!
        datetimeObj_pacific = timezone('US/Pacific').localize(datetimeObj_naive)
        print('RIGHT')
        print(datetimeObj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        datetimeObj = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
        localDatetimeObj = timezone("Europe/Zurich").localize(datetimeObj)
        print("local time:               " + localDatetimeObj.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        datetimeObjUTC = localDatetimeObj.astimezone(timezone('UTC'))
        timeStampUTC = time.mktime(datetimeObjUTC.timetuple())
        print("local time to UTC time:   " + datetimeObjUTC.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        swissDateTimeObj = datetimeObjUTC.astimezone(timezone("Europe/Zurich"))
        print("local time from UTC time: " + swissDateTimeObj.strftime("%Y-%m-%d %H:%M:%S %Z%z"))


        print('\nConverting UTC date to other time zone')
        dateStr = "2014-05-28 22:28:15"
        datetimeObj = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
        datetimeObjUTC = datetimeObj.replace(tzinfo=timezone('UTC'))
        print('Date in UTC')
        print(datetimeObjUTC.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        print('Convert to US/Pacific time zone')
        pacificTime = datetimeObjUTC.astimezone(timezone('US/Pacific'))
        print(pacificTime.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
        print('Convert Europe/Zurich time zone')
        zurichTime = datetimeObjUTC.astimezone(timezone('Europe/Zurich'))
        print(zurichTime.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

def play():
    pr = PriceRequester('Europe/Zurich')
    #pr.explore()

    """
    localDateTimeStr = "28-08-17 12:29"
    datetimeObj = datetime.strptime(localDateTimeStr, DATE_TIME_FORMAT)
    datetimeObjUTC = datetimeObj.replace(tzinfo=timezone('UTC'))
    print('Date in UTC wrong')
    print(datetimeObjUTC.strftime(DATE_TIME_FORMAT_TZ))
    timeStampUTC = time.mktime(datetimeObjUTC.timetuple())
    print(timeStampUTC)


    datetimeObjUTC = timezone('UTC').localize(datetimeObj)
    print('Date in UTC right')
    print(datetimeObjUTC.strftime(DATE_TIME_FORMAT_TZ))
    timeStampUTC = time.mktime(datetimeObjUTC.timetuple())
    print(timeStampUTC)


    datetimeObjZH = datetimeObjUTC.astimezone(timezone('Europe/Zurich'))
    print('Date in Europe/Zurich')
    print(datetimeObjZH.strftime(DATE_TIME_FORMAT_TZ))
    timeStampZH = time.mktime(datetimeObjZH.timetuple())
    print(timeStampZH)
    print(timeStampZH - timeStampUTC)
    crypto = 'BTC'
    fiat = 'USD'
    print(crypto + ' ' + str(pr.getPriceAtTimeStampUTC(crypto, fiat, timeStampUTC, 'CCEX')))

    #timeStampUTC = time.mktime(datetime.utcnow().timetuple())
    """
    timeStampUTC = time.mktime(datetime.now(timezone('UTC')).timetuple())
    crypto = 'BTC'
    fiat = 'USD'
    # print(crypto + ' ' + str(pr.getPriceAtTimeStampUTC(crypto, fiat, timeStampUTC, 'CCEX')))
    crypto = 'MCAP'
    print(crypto + ' (now tstamp UTC: ' + str(pr.getPriceAtUTCTimeStamp(crypto, fiat, timeStampUTC, 'CCEX')))

    localDateTimeStampNow = time.mktime(datetime.now(timezone('Europe/Zurich')).timetuple())
    print(crypto + ' (now tstamp Europe/Zurich:NONSENSE ' + str(pr.getPriceAtUTCTimeStamp(crypto, fiat, localDateTimeStampNow, 'CCEX')))
    localDateTimeStr = datetime.fromtimestamp(localDateTimeStampNow).strftime(DATE_TIME_FORMAT)
    print(crypto + ' (now date str Europe/Zurich: ' + str(pr.getPriceAtLocalDateTimeStr(crypto, fiat, localDateTimeStr, 'CCEX')))

    localDateTimeStr = "1-9-17 11:00"
    print(crypto + ' ' + str(pr.getPriceAtLocalDateTimeStr(crypto, fiat, localDateTimeStr, 'CCEX')))
        
if __name__ == '__main__':
    #play()
    import re
    pr = PriceRequester('Europe/Zurich')
    prompt = "crypto fiat d-m[-y] h:m exch (q/quit): "
    inputStr = input(prompt)

    while inputStr.upper() != 'Q':
        #([0-9]+)-([0-9]+)(?:-([0-9]+)|) matches either 1-9 or 1-9-17
        pattern = r"(\w+) (\w+) ([0-9]+)-([0-9]+)(?:-([0-9]+)|) ([0-9:]+)(?: (\w+)|)"
        data = re.match(pattern, inputStr)
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
            
        localDateTimeStr = day + '-' + month + '-' + year + ' ' + hourMin
        print("{}/{} on {}: ".format(crypto, fiat, exchange) + ' '.join(map(str, pr.getPriceAtLocalDateTimeStr(crypto, fiat, localDateTimeStr, exchange))))
        inputStr = input(prompt)
