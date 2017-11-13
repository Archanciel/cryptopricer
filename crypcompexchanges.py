class CrypCompExchanges:
    def __init__(self):
        self._dic = {'ALL': ['CCCAGG', 'BTC', 'USD'],
                     'CCCAGG': ['CCCAGG', 'BTC', 'USD'],
                     'CCEX': ['Ccex', 'MCAP', 'USD'],
                     'BTC38': ['BTC38', 'BTC', 'CNY'],
                     'BTER': ['BTER', 'ETH', 'BTC'],
                     'BIT2C': ['Bit2C', 'LTC', 'ILS'],
                     'BITFINEX': ['Bitfinex', 'BTC', 'USD'],
                     'BITSTAMP': ['Bitstamp', 'BTC', 'USD'],
                     'BITTREX': ['BitTrex', 'BTC', 'USD'],
                     'CCEDK': ['CCEDK', 'BTC', 'USD'],
                     'CEXIO': ['Cexio', 'BTC', 'USD'],
                     'COINBASE': ['Coinbase', 'BTC', 'USD'],
                     'COINFLOOR': ['Coinfloor', 'BTC', 'USD'],
                     'COINSE': ['Coinse', 'LTC', 'BTC'],
                     'COINSETTER': ['Coinsetter', 'BTC', 'USD'],
                     'CRYPTOPIA': ['Cryptopia', 'AUR', 'BTC'],
                     'CRYPTSY': ['Cryptsy', 'BTC', 'USD'],
                     'GATECOIN': ['Gatecoin', 'BTC', 'USD'],
                     'GEMINI': ['Gemini', 'BTC', 'USD'],
                     'HITBTC': ['HitBTC', 'BTC', 'USD'],
                     'HUOBI': ['Huobi', 'BTC', 'USD'],
                     'ITBIT': ['itBit', 'BTC', 'USD'],
                     'KRAKEN': ['Kraken', 'BTC', 'USD'],
                     'LAKEBTC': ['LakeBTC', 'BTC', 'USD'],
                     'LOCALBITCOINS': ['LocalBitcoins', 'BTC', 'USD'],
                     'MONETAGO': ['MonetaGo', 'BTC', 'USD'],
                     'OKCOIN': ['OKCoin', 'BTC', 'USD'],
                     'POLONIEX': ['Poloniex', 'BTC', 'USD'],
                     'YACUNA': ['Yacuna', 'DOGE', 'BTC'],
                     'YUNBI': ['Yunbi', 'ETC', 'CNY'],
                     'YOBIT': ['Yobit', 'BTC', 'USD'],
                     'KORBIT': ['Korbit', 'BTC', 'KRW'],
                     'BITBAY': ['BitBay', 'BTC', 'USD'],
                     'BTCMARKETS': ['BTCMarkets', 'BTC', 'AUD'],
                     'QUADRIGACX': ['QuadrigaCX', 'BTC', 'USD'],
                     'COINCHECK': ['CoinCheck', 'BTC', 'JPY'],
                     'BITSQUARE': ['BitSquare', 'BTC', 'USD'],
                     'VAULTORO': ['Vaultoro', 'BTC', 'GOLD'],
                     'UNOCOIN': ['Unocoin', 'BTC', 'INR'],
                     'BITSO': ['Bitso', 'BTC', 'MXN'],
                     'BTCXINDIA': ['BTCXIndia', 'XRP', 'INR'],
                     'PAYMIUM': ['Paymium', 'BTC', 'EUR'],
                     'THEROCKTRADING': ['TheRockTrading', 'BTC', 'USD'],
                     'BITFLYER': ['bitFlyer', 'ETH', 'BTC'],
                     'QUOINE': ['Quoine', 'BTC', 'USD'],
                     'LUNO': ['Luno', 'BTC', 'SGD'],
                     'ETHERDELTA': ['EtherDelta', 'REQ', 'ETH'],
                     'LIQUI': ['Liqui', 'ETH', 'BTC'],
                     'BITMARKET': ['BitMarket', 'BTC', 'PLN'],
                     'LIVECOIN': ['LiveCoin', 'BTC', 'USD'],
                     'COINONE': ['Coinone', 'BTC', 'KRW'],
                     'TIDEX': ['Tidex', 'WAVES', 'BTC'],
                     'BLEUTRADE': ['Bleutrade', 'ETH', 'BTC'],
                     'ETHEXINDIA': ['EthexIndia', 'ETH', 'INR']}



    def getExchange(self, exchangeName):
        '''
        Avoid price request failure due to incorrect exchange name case. For example,
        returns 'BitTrex' for 'bitrex' or ' Bittrex' !

        :param exchangeName: exchange name without paying attention to case
        :return: exchange name with right case
        :raise KeyException if passed exchangeName not found.
        '''
        return self._dic[exchangeName.upper()][0]


    def _getExchangeTestData(self, exchangeName):
        '''
        Used for testing purpose
        :param exchangeName:
        :return: list containing exchange test data. Ex: ['BitTrex', 'BTC', 'USD']
        '''
        return self._dic[exchangeName.upper()]


if __name__ == '__main__':
    from pricerequester import PriceRequester
    from priceresult import PriceResult

    cc = CrypCompExchanges()
    pp = PriceRequester()

    ts = 1506729600

    keyList = cc._dic.keys()

    print('\n--- HISTO PRICES ---\n')
    
    for key in keyList:
        exchTestData = cc._getExchangeTestData(key)
        exch = exchTestData[0]
        fiat = exchTestData[2]
        crypto = exchTestData[1]
  
        priceResult = pp.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, ts, ts, exch)

        if priceResult.getValue(PriceResult.RESULT_KEY_ERROR_MSG) == None:
            print("{} {} {} {}".format(exch, crypto, fiat, priceResult.getValue(PriceResult.RESULT_KEY_PRICE)))
        else:
            print("{} {}".format(exch, priceResult.getValue(PriceResult.RESULT_KEY_ERROR_MSG)[0:26]))

    print('\n\n--- CURRENT PRICES ---\n')

    for key in keyList:
        exchTestData = cc._getExchangeTestData(key)
        exch = exchTestData[0]
        fiat = exchTestData[2]
        crypto = exchTestData[1]
 
        priceResult = pp.getCurrentPrice(crypto, fiat, exch)

        if priceResult.getValue(PriceResult.RESULT_KEY_ERROR_MSG) == None:
            print("{} {} {} {}".format(exch, crypto, fiat, priceResult.getValue(PriceResult.RESULT_KEY_PRICE)))
        else:
            print("{} {}".format(exch, priceResult.getValue(PriceResult.RESULT_KEY_ERROR_MSG)[0:26]))

