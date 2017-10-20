class CrypCompExchanges:
    def __init__(self):
        self._dic = {'ALL':'CCCAGG',
                     'BITTREX':'BitTrex',
                     'CCEX':'CCEX',
                     'KRAKEN':'Kraken'}


    def setDic(self, dic):
        self._dic = dic
        
        
    def getExchange(self, exchangeName):
        return self._dic[exchangeName.upper()]


    def getExchangeList(self):
        return self._dic.values()


if __name__ == '__main__':
    from pricerequester import PriceRequester
    
    stre = "BTC38, BTCC, BTCE, BTER, Bit2C, Bitfinex, Bitstamp, Bittrex, CCEDK, Cexio, Coinbase, Coinfloor, Coinse, Coinsetter, Cryptopia, Cryptsy, Gatecoin, Gemini, HitBTC, Huobi, itBit, Kraken, LakeBTC, LocalBitcoins, MonetaGo, OKCoin, Poloniex, Yacuna, Yunbi, Yobit, Korbit, BitBay, BTCMarkets, QuadrigaCX, CoinCheck, BitSquare, Vaultoro, MercadoBitcoin, Unocoin, Bitso, BTCXIndia, Paymium, TheRockTrading, bitFlyer, Quoine, Luno, EtherDelta, Liqui, bitFlyerFX, BitMarket, LiveCoin, Coinone, Tidex, Bleutrade, EthexIndia"
    exchLst = stre.split(", ")
    dic = {}
    for e in exchLst:
        dic[e.upper()] = e
    #print(dic)
    
    cc = CrypCompExchanges()
    cc.setDic(dic)
    pp = PriceRequester()
    crypto = 'BTC'
    
    fiat = 'USD'
    ts = 1506729600
    for exch in cc.getExchangeList():
        res = pp.getHistoricalPriceAtUTCTimeStamp(crypto, fiat, ts, exch)
        if len(res) > 1:
            print("{} {}".format(exch, res[2]))
        else:
            print("{} {}".format(exch, res[0][0:26]))

