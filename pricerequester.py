from datetime import datetime
from pytz import timezone
import time
import json
import urllib.request
from urllib.error import HTTPError, URLError
import sys
from bs4 import BeautifulSoup
#from tqdm import tqdm

DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"
DATE_TIME_FORMAT_TZ = DATE_TIME_FORMAT + " %Z%z"


class PriceRequester:
    def __init__(self, localTimeZone):
        self.localTimeZone = localTimeZone

    def _timestamp2date(self, timestamp):
        # function converts a UTC timestamp into Europe/Zurich Gregorian date
        utcTimeStamp = datetime.fromtimestamp(int(timestamp - 3600)).replace(tzinfo=timezone('UTC'))

        return utcTimeStamp.astimezone(timezone(self.localTimeZone)).strftime(DATE_TIME_FORMAT)

    def getPriceAtDatetime(self, coin, fiat, timeStampUTC, exchange):
        timeStamp = str(int(timeStampUTC + 60))
        url = "https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit=1&aggregate=1&toTs={}".format(coin, fiat, timeStamp)
        tmp = []

        try:
            webURL = urllib.request.urlopen(url)
        except HTTPError as e:
            sys.exit('Could not complete request. Reason: ' + e.reason)
        except URLError as e:
            sys.exit('Could not complete request. Reason: ' + e.reason)
        else:
            page = webURL.read()
            soup = BeautifulSoup(page, 'html.parser')
            dic = json.loads(soup.prettify())
#            print(dic)
            lst = ['time', 'open', 'high', 'low', 'close']
            for e in enumerate(lst):
                x = e[0]
                y = dic['Data'][0][e[1]]
                if (x == 0):
                    tmp.append(str(self._timestamp2date(y)))
                else:
                    tmp.append(y)

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

pr = PriceRequester('Europe/Zurich')
#pr.explore()
dateStr = "28-08-2017 12:29:01"
datetimeObj = datetime.strptime(dateStr, DATE_TIME_FORMAT)
datetimeObjUTC = datetimeObj.replace(tzinfo=timezone('UTC'))
print('Date in UTC')
print(datetimeObjUTC.strftime(DATE_TIME_FORMAT_TZ))
timeStampUTC = time.mktime(datetimeObjUTC.timetuple())
print(timeStampUTC)

datetimeObjZH = datetimeObjUTC.astimezone(timezone('Europe/Zurich'))
print('Date in Europe/Zurich')
print(datetimeObjZH.strftime(DATE_TIME_FORMAT_TZ))
timeStampZH = time.mktime(datetimeObjZH.timetuple())
print(timeStampZH)
print(timeStampZH - timeStampUTC)
print(pr.getPriceAtDatetime('BTC', 'USD', timeStampUTC, 'CCEX'))

#timeStampUTC = time.mktime(datetime.utcnow().timetuple())
timeStampUTC = time.mktime(datetime.now(timezone('UTC')).timetuple())
print(pr.getPriceAtDatetime('BTC', 'USD', timeStampUTC, 'CCEX'))