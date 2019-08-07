import os

class CurrencyPairTester:
    def __init__(self, filename):
        self.filename = filename
        self.currencyPairDic = self._loadCurrencyPairDic()


    def isListed(self, crypto, unit, exchange):
        '''
        return True if the triplet is known from CurrencyPairTester,
        False if not.
        '''
        cryptoUnitExch = crypto.upper() + unit.upper() + exchange.upper()
        
        if self.currencyPairDic.get(cryptoUnitExch.upper()) == None:
            return False
        else:
            return True
        

    def addCurrencyPair(self, crypto, unit, exchange):
        '''
        add the triplet to the internal dic and
        to the file on disk.
        '''
        if self.isListed(crypto, unit, exchange):
            return #do not add same entry twice !
            
        cryptoU = crypto.upper()
        unitU = unit.upper()
        exchangeU = exchange.upper()

        cryptoUnitExch = cryptoU + unitU + exchangeU
        self.currencyPairDic[cryptoUnitExch] = ''
        
        cryptoUnitExchComma = cryptoU + ',' + unitU + ',' + exchangeU + '\n'
        
        with open(self.filename, 'a') as currPairFile:
            currPairFile.write(cryptoUnitExchComma)
       
    
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
            cryptoUnitExchList = line.split(',')
            cryptoUnitExch = ''.join(cryptoUnitExchList)
            dic[cryptoUnitExch] = ''
            
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


