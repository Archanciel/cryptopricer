import json
import urllib.request
from urllib.error import HTTPError, URLError
import sys

coin = 'BTC'
fiat = 'USD'
urlData = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}'.format(coin, fiat)
try:
    webURL = urllib.request.urlopen(urlData)
except HTTPError as e:
    sys.exit('Could not complete request. Reason: ' + e.reason)
except URLError as e:
    sys.exit('Could not complete request. Reason: ' + e.reason)
else:
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    js = json.loads(data.decode(encoding))
    
    try:
        dataRaw = js['RAW']
        print(coin + '/' + fiat)
        print('CURRENT %.2f' % dataRaw[coin][fiat]['PRICE'])
        print('24HIGH  %.2f' % dataRaw[coin][fiat]['HIGH24HOUR'])
        print('24LOW   %.2f' % dataRaw[coin][fiat]['LOW24HOUR'])

#        return ([(dataRaw[c][fiat]['PRICE'], dataRaw[c][fiat]['HIGH24HOUR'], dataRaw[c][fiat]['LOW24HOUR']) for c in coin.split(',')])
    except:
        sys.exit('Could not parse data')
