import os

class CurrencyPairTester:
    def __init__(self, filename):
        self.filename = filename
        self.currencyPairDic = self._loadCurrencyPairDic()


    def isListed(self, crypto, fiat, exchange):
        '''
        return True if the triplet is known from CurrencyPairTester,
        False if not.
        '''
        cryptoFiatExch = crypto.upper() + fiat.upper() + exchange.upper()
        
        if self.currencyPairDic.get(cryptoFiatExch.upper()) == None:
            return False
        else:
            return True
        

    def addCurrencyPair(self, crypto, fiat, exchange):
        '''
        add the triplet to the internal dic and
        to the file on disk.
        '''
        cryptoU = crypto.upper()
        fiatU = fiat.upper()
        exchangeU = exchange.upper()

        cryptoFiatExch = cryptoU + fiatU + exchangeU
        self.currencyPairDic[cryptoFiatExch] = ''
        
        cryptoFiatExchComma = cryptoU + ',' + fiatU + ',' + exchangeU + '\n'
        
        with open(self.filename, 'a') as currPairFile:
            currPairFile.write(cryptoFiatExchComma)
       
    
    def _loadCurrencyPairDic(self):
        dic = {}
        
        try:
            currPairFile = open(self.filename, 'r') 
        except IOError: 
            currPairFile = open(self.filename, 'w')
            currPairFile.close()
            return dic

        lines = currPairFile.readlines()
        currPairFile.close()
        
        for line in lines:
            line = line[:-1] #removing \n
            cryptoFiatExchList = line.split(',')
            cryptoFiatExch = ''.join(cryptoFiatExchList)
            dic[cryptoFiatExch] = ''
            
        return dic
            

if __name__ == '__main__':
    if os.name == 'posix':
        FILE_PATH = '/sdcard/currencypairs.txt'
    else:
        FILE_PATH = 'c:\\temp\\currencypairs.txt'
        
    cpt = CurrencyPairTester(FILE_PATH)
    print(cpt.currencyPairDic)
    
    if not cpt.isListed('mcap', 'eth', 'ccex'):
        print('adding entry mcap, eth, ccex')
        cpt.addCurrencyPair('mcap', 'eth', 'ccex')
        print(cpt.currencyPairDic)

    if not cpt.isListed('kom', 'eth', 'ccex'):
        print('adding entry kom, eth, ccex')
        cpt.addCurrencyPair('kom', 'eth', 'ccex')
        print(cpt.currencyPairDic)

    if not cpt.isListed('qtum', 'eth', 'ccex'):
        print('adding entry qtum, eth, ccex')
        cpt.addCurrencyPair('qtum', 'eth', 'ccex')
        print(cpt.currencyPairDic)


