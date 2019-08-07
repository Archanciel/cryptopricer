class CrypCompExchanges:
    '''
    This class translates case insensitive exchange names to the case sensitive
    Cryptocompare data provider exchange name.
    '''
    def __init__(self):
        self._dic = {'ALL': ['CCCAGG', 'BTC', 'USD'],
                     'CCCAGG': ['CCCAGG', 'BTC', 'USD'],
                     'CCEX': ['Ccex', 'MCAP', 'USD'],
                     'BTC38': ['BTC38', 'BTC', 'CNY'],
                     'BTER': ['BTER', 'ETH', 'BTC'],
                     'BINANCE': ['Binance', 'ETH', 'BTC'],
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
                     'ETHEXINDIA': ['EthexIndia', 'ETH', 'INR'],
                     'BTCCHINA': ['BTCChina', 'ETH', 'BTC'],
                     'BTCE': ['BTCE', 'ETH', 'BTC'],
                     'BTCXCHANGE': ['btcXchange', 'ETH', 'BTC'],
                     'ANXBTC': ['ANXBTC', 'ETH', 'BTC'],
                     'EXMO': ['Exmo', 'ETH', 'BTC'],
                     'MERCADOBITCOIN': ['MercadoBitcoin', 'ETH', 'BTC'],
                     'BITFLYERFX': ['bitFlyerFX', 'ETH', 'BTC'],
                     'TUXEXCHANGE': ['TuxExchange', 'ETH', 'BTC'],
                     'CRYPTOX': ['CryptoX', 'ETH', 'BTC'],
                     'MTGOX': ['MtGox', 'ETH', 'BTC'],
                     'BITHUMB': ['Bithumb', 'ETH', 'BTC'],
                     'CHBTC': ['CHBTC', 'ETH', 'BTC'],
                     'VIABTC': ['ViaBTC', 'ETH', 'BTC'],
                     'JUBI': ['Jubi', 'ETH', 'BTC'],
                     'ZAIF': ['Zaif', 'ETH', 'BTC'],
                     'NOVAEXCHANGE': ['Novaexchange', 'ETH', 'BTC'],
                     'WAVESDEX': ['WavesDEX', 'ETH', 'BTC'],
                     'LYKKE': ['Lykke', 'ETH', 'BTC'],
                     'REMITANO': ['Remitano', 'ETH', 'BTC'],
                     'COINROOM': ['Coinroom', 'ETH', 'BTC'],
                     'ABUCOINS': ['Abucoins', 'ETH', 'BTC'],
                     'BXINTH': ['BXinth', 'ETH', 'BTC'],
                     'GATEIO': ['Gateio', 'ETH', 'BTC'],
                     'HUOBIPRO': ['HuobiPro', 'ETH', 'BTC'],
                     'OKEX': ['OKEX', 'ETH', 'BTC']}



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


    def _checkIfHandled(self):
        '''
        Since CryptoCompare constantly adds new exchanges, it is necessary to regularly check
        if CrypCompExchanges supports the new entries. The list of exchange is accessible at
        https://www.cryptocompare.com/api/
        :return:
        '''
        exchangeNameString = "Cryptsy, BTCChina, Bitstamp, BTER, OKCoin, Coinbase, Poloniex, Cexio, BTCE, BitTrex, Kraken, Bitfinex, Yacuna, LocalBitcoins, Yunbi, itBit, HitBTC, btcXchange, BTC38, Coinfloor, Huobi, CCCAGG, LakeBTC, ANXBTC, Bit2C, Coinsetter, CCEX, Coinse, MonetaGo, Gatecoin, Gemini, CCEDK, Cryptopia, Exmo, Yobit, Korbit, BitBay, BTCMarkets, Coincheck, QuadrigaCX, BitSquare, Vaultoro, MercadoBitcoin, Bitso, Unocoin, BTCXIndia, Paymium, TheRockTrading, bitFlyer, Quoine, Luno, EtherDelta, bitFlyerFX, TuxExchange, CryptoX, Liqui, MtGox, BitMarket, LiveCoin, Coinone, Tidex, Bleutrade, EthexIndia, Bithumb, CHBTC, ViaBTC, Jubi, Zaif, Novaexchange, WavesDEX, Binance, Lykke, Remitano, Coinroom, Abucoins, BXinth, Gateio, HuobiPro, OKEX"
        exchangeNameList = exchangeNameString.split(', ')

        for name in exchangeNameList:
            nameU = name.upper()
            if not nameU in self._dic:
                print("'{}': ['{}', 'ETH', 'BTC'],".format(nameU, name))


if __name__ == '__main__':
    from pricerequester import PriceRequester
    from resultdata import ResultData
    import sys

    cc = CrypCompExchanges()

    # cc._checkIfHandled()
    # sys.exit(0)


    pp = PriceRequester()

    ts = 1506729600

    keyList = cc._dic.keys()

    print('\n--- HISTO PRICES ---\n')
    
    for key in keyList:
        exchTestData = cc._getExchangeTestData(key)
        exch = exchTestData[0]
        unit = exchTestData[2]
        crypto = exchTestData[1]
  
        resultData = pp.getHistoricalPriceAtUTCTimeStamp(crypto, unit, ts, ts, exch)

        if resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG) == None:
            print("{} {} {} {}".format(exch, crypto, unit, resultData.getValue(ResultData.RESULT_KEY_PRICE)))
        else:
            print("{} {}".format(exch, resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG)))

    print('\n\n--- CURRENT PRICES ---\n')

    for key in keyList:
        exchTestData = cc._getExchangeTestData(key)
        exch = exchTestData[0]
        unit = exchTestData[2]
        crypto = exchTestData[1]
 
        resultData = pp.getCurrentPrice(crypto, unit, exch)

        if resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG) == None:
            print("{} {} {} {}".format(exch, crypto, unit, resultData.getValue(ResultData.RESULT_KEY_PRICE)))
        else:
            print("{} {}".format(exch, resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG)))

