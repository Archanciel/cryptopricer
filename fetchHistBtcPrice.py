from datetime import datetime
import time
import json
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm

def timestamp2date(timestamp):
    # function converts a Uniloc timestamp into Gregorian date
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')

def date2timestamp(date):
    # function coverts Gregorian date in a given format to timestamp
    return datetime.strptime(date, '%Y-%m-%d').timestamp()

def fetchCryptoOHLC(fsym, tsym):
    # function fetches a crypto price-series for fsym/tsym and stores
    # it in pandas DataFrame

    cols = ['date', 'timestamp', 'open', 'high', 'low', 'close']
    lst = ['time', 'open', 'high', 'low', 'close']

    #timestamp = time.mktime(today().timetuple())
    timestamp = time.mktime(datetime(2016, 8, 7).timetuple())


    # (limit-1) * 2 = days
    # One year is around 184
    limit = 100 
    url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + fsym + "&tsym=" + tsym + "&toTs=" + str(int(timestamp)) + "&limit=" + str(limit)
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')
    dic = json.loads(soup.prettify())
    for i in range(0, limit):
        tmp = []
        for e in enumerate(lst):
            x = e[0]
            y = dic['Data'][i][e[1]]
            if(x == 0):
                tmp.append(str(timestamp2date(y)))
            tmp.append(y)
        print(tmp)
        print('/n')

def get_multiple_cryptos(symbols):

    # Adding columns with data for all requested cryptocurrencies
    for symbol in tqdm(symbols):
        fsym = symbol
        tsym = "BTC"
        data_symbol = fetchCryptoOHLC(fsym, tsym)

        print(data_symbol )


if __name__ == '__main__':

    symbols = ['ETH', 'LTC', 'ETC', 'DOGE', 'DGB', 'SC']
    get_multiple_cryptos(symbols)
    #fetchCryptoOHLC('BTC', 'USD')
