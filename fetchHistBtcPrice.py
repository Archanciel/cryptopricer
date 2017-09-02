from datetime import datetime
import time
import json
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm
from pytz import timezone

def timestamp2date(timestamp):
    # function converts a UTC timestamp into Europe/Zurich Gregorian date
    utcTimeStamp = datetime.fromtimestamp(int(timestamp)).replace(tzinfo=timezone('UTC'))

    return utcTimeStamp.astimezone(timezone('Europe/Zurich')).strftime('%Y-%m-%d %H:%M:%S')

def fetchCryptoOHLC(fsym, tsym):
    # function fetches a crypto price-series for fsym/tsym and stores
    # it in pandas DataFrame

    lst = ['time', 'open', 'high', 'low', 'close']

    timestamp_ = time.mktime(datetime.utcnow().timetuple())
    print(timestamp_)
    timestamp = time.mktime(datetime.now(timezone('UTC')).timetuple())
    print(timestamp)

    limit = 3
    url = "https://min-api.cryptocompare.com/data/histominute?fsym=" + fsym + "&tsym=" + tsym + "&toTs=" + str(int(timestamp)) + "&limit=" + str(limit)
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    dic = json.loads(soup.prettify())

    for i in range(0, limit):
        tmp = [fsym + '/' + tsym]
        for e in enumerate(lst):
            x = e[0]
            y = dic['Data'][i][e[1]]
            if(x == 0):
                tmp.append(str(timestamp2date(y)))
            else:
                tmp.append(y)
        print('')
        print(tmp)

def get_multiple_cryptos(symbols):

    # Adding columns with data for all requested cryptocurrencies
    for symbol in tqdm(symbols):
        fsym = symbol
        tsym = "USD"
        fetchCryptoOHLC(fsym, tsym)

if __name__ == '__main__':
    symbols = ['BTC', 'ETH']
    get_multiple_cryptos(symbols)
    #fetchCryptoOHLC('BTC', 'USD')
