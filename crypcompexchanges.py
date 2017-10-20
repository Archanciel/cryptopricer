class CrypCompExchanges:
    def __init__(self):
        self._dic = {'BTC38': 'BTC38', #test pair btc/cny
                     'BTER': 'BTER', #test pair eth/btc
                     'BIT2C': 'Bit2C', #test pair ltc/ils
                     'BITFINEX': 'Bitfinex',
                     'BITSTAMP': 'Bitstamp',
                     'BITTREX': 'BitTrex',
                     'CCEDK': 'CCEDK',
                     'CEXIO': 'Cexio',
                     'COINBASE': 'Coinbase',
                     'COINFLOOR': 'Coinfloor',
                     'COINSE': 'Coinse', #test pair ltc/btc
                     'COINSETTER': 'Coinsetter',
                     'CRYPTOPIA': 'Cryptopia', #test pair aur/btc
                     'CRYPTSY': 'Cryptsy',
                     'GATECOIN': 'Gatecoin',
                     'GEMINI': 'Gemini',
                     'HITBTC': 'HitBTC',
                     'HUOBI': 'Huobi',
                     'ITBIT': 'itBit',
                     'KRAKEN': 'Kraken',
                     'LAKEBTC': 'LakeBTC',
                     'LOCALBITCOINS': 'LocalBitcoins',
                     'MONETAGO': 'MonetaGo',
                     'OKCOIN': 'OKCoin',
                     'POLONIEX': 'Poloniex',
                     'YACUNA': 'Yacuna', #test pair doge/btc
                     'YUNBI': 'Yunbi', #test pair etc/cny
                     'YOBIT': 'Yobit',
                     'KORBIT': 'Korbit', #test pair btc/krw
                     'BITBAY': 'BitBay',
                     'BTCMARKETS': 'BTCMarkets', #test pair btc/aud
                     'QUADRIGACX': 'QuadrigaCX',
                     'COINCHECK': 'CoinCheck', #test pair btc/jpy
                     'BITSQUARE': 'BitSquare',
                     'VAULTORO': 'Vaultoro', #test pair btc/gold
                     'UNOCOIN': 'Unocoin', #test pair btc/inr
                     'BITSO': 'Bitso', #test pair btc/mxn
                     'BTCXINDIA': 'BTCXIndia', #test pair xrp/inr
                     'PAYMIUM': 'Paymium', #test pair btc/eur
                     'THEROCKTRADING': 'TheRockTrading',
                     'BITFLYER': 'bitFlyer', #test pair eth/btc
                     'QUOINE': 'Quoine',
                     'LUNO': 'Luno', #test pair btc/sgd
                     'ETHERDELTA': 'EtherDelta', #test pair req/eth
                     'LIQUI': 'Liqui', #test pair eth/btc
                     'BITMARKET': 'BitMarket', #test pair btc/pln
                     'LIVECOIN': 'LiveCoin',
                     'COINONE': 'Coinone', #test pair btc/krw
                     'TIDEX': 'Tidex', #test pair waves/btc
                     'BLEUTRADE': 'Bleutrade', #test pair eth/btc
                     'ETHEXINDIA': 'EthexIndia'} #test pair eth/inr



    def getExchange(self, exchangeName):
        return self._dic[exchangeName.upper()]


    def _setDic(self, dic):
        self._dic = dic


    def _getExchangeKeyList(self):
        return self._dic.keys()


    def _removeKeys(self, keyList):
        for key in keyList:
            del self._dic[key]


    def _printExchangeDic(self):
        print(self._dic)


if __name__ == '__main__':
    from pricerequester import PriceRequester
    import sys

    #exchangeListFromCryptoCompare URL: https://www.cryptocompare.com/api/#introduction
    exchangeListFromCryptoCompareOri = "BTC38, BTCC, BTER, Bit2C, Bitfinex, Bitstamp, BitTrex, CCEDK, Cexio, Coinbase, Coinfloor, Coinse, Coinsetter, Cryptopia, Cryptsy, Gatecoin, Gemini, HitBTC, Huobi, itBit, Kraken, LakeBTC, LocalBitcoins, MonetaGo, OKCoin, Poloniex, Yacuna, Yunbi, Yobit, Korbit, BitBay, BTCMarkets, QuadrigaCX, CoinCheck, BitSquare, Vaultoro, MercadoBitcoin, Unocoin, Bitso, BTCXIndia, Paymium, TheRockTrading, bitFlyer, Quoine, Luno, EtherDelta, Liqui, bitFlyerFX, BitMarket, LiveCoin, Coinone, Tidex, Bleutrade, EthexIndia"
    exchangeListFromCryptoComparePurged = "BTC38, BTER, Bit2C, Bitfinex, Bitstamp, BitTrex, CCEDK, Cexio, Coinbase, Coinfloor, Coinse, Coinsetter, Cryptopia, Cryptsy, Gatecoin, Gemini, HitBTC, Huobi, itBit, Kraken, LakeBTC, LocalBitcoins, MonetaGo, OKCoin, Poloniex, Yacuna, Yunbi, Yobit, Korbit, BitBay, BTCMarkets, QuadrigaCX, CoinCheck, BitSquare, Vaultoro, Mercado Bitcoin, Unocoin, Bitso, BTCXIndia, Paymium, TheRockTrading, bitFlyer, Quoine, Luno, EtherDelta, Liqui, BitMarket, LiveCoin, Coinone, Tidex, Bleutrade, EthexIndia"
    exchangeList = exchangeListFromCryptoComparePurged.split(", ")
    dic = {}
    # for e in exchangeList:
    #     dic[e.upper()] = e
    # print(dic)

    cc = CrypCompExchanges()
    #cc._setDic(dic)
    pp = PriceRequester()
    crypto = 'BTC'
    fiat = 'USD'
    ts = 1506729600
    keyList = cc._getExchangeKeyList()
    removeKeyList = []
    for key in keyList:
        exch = cc.getExchange(key)
        res = pp.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, ts, exch)
        if len(res) > 1:
            print("{} {}".format(exch, res[2]))
        else:
            print("{} {}".format(exch, res[0][0:26]))
#            removeKeyList.append(key)

    # cc._removeKeys(removeKeyList)
    # print('removeKeyList^size: {}'.format(len(removeKeyList)))
    # print(removeKeyList)
    # cc._printExchangeDic()

