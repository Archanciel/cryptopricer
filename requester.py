from command import Command
import re

class Requester:
    '''
    Read in commands entered by the
    user, typically
    
    [btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave

    and return a dictionnary of commands
      
    {CRYPTO:[btc, 5/7, 0.0015899, 6/7, 0.00153], FIAT:[usd, chf], NOSAVE:[]}
    '''
    def request(self):
        inp = input('Enter command (h for help)\n').upper()

        while inp == 'H':
            self._printHelp()
            inp = input('Enter command (h for help)\n').upper()
        
        if inp == 'Q':   
            return {Command.QUIT : ''}
        else:
            parsedInput = self._parseInput(inp)

            if Command.ERROR in parsedInput:
                return parsedInput
            else:
                return {Command.CRYPTO : [parsedInput]}

    def _printHelp(self):
        print('Usage:\n')
        print('[btc 5/7 0.0015899 6/7 0.00153] [usd-chf]')
        inp = input('\nm for more or anything else to exit help\n')
        
        if inp.upper() == 'M':
            print("\nns - don't save retrieved prices")
            print("rm [1, 3, 4] - remove line numbers\n")

    def _parseInput(self, inputStr):
        #convert [btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave
        #into
        #[CRYPTO:[btc, 5/7, 0.0015899, 6/7, 0.00153], FIAT:[usd, chf], NOSAVE:[]}
        cryptoDataList = self._parseCryptoDataFromInput(inputStr)

        if cryptoDataList == "":
            return {Command.ERROR : inputStr}
        
        cryptoDataDic = {cryptoDataList[0]:cryptoDataList[1:]}
        
        fiatDataList = self._parseFiatDataFromInput(inputStr)
        fiatDataDic = {Command.FIAT:fiatDataList}

        cryptoDic = {Command.CRYPTO:cryptoDataList,'FIAT':fiatDataList}


    def _parseFiatDataFromInput(self, inputStr):
        #convert [btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave
        #into
        #[usd, chf]
        
        fiatDataList = []
        patternFiat = r"(([a-zA-Z]+)-)|(([a-zA-Z]+)\])|(\[([a-zA-Z]+)\])"

        for grp in re.finditer(patternFiat, inputStr):
            for elem in grp.groups():
                if elem != None and len(elem) == 3:
                    fiatDataList.append(elem)

        print(fiatDataList)

        return fiatDataList
        
    def _parseCryptoDataFromInput(self, inputStr):
        #convert [btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave
        #into
        #[btc, 5/7, 0.0015899, 6/7, 0.00153]
        
        cryptoDataList = []
        
        patternCryptoSymbol = r"\[(\w+) "
        
        match = re.match(patternCryptoSymbol, inputStr)

        if match == None:
            return ""

        cryptoSymbol = match.group(1)
        cryptoDataList.append(cryptoSymbol)
        
        patternDatePrice = r"(\d+/\d+) ([0-9\.]+)"

        for grp in re.finditer(patternDatePrice, inputStr):
            for elem in grp.groups():
                cryptoDataList.append(elem)
                
        return cryptoDataList
                

if __name__ == '__main__':
    r = Requester()
    r._parseInput('[btc 5/7 0.0015899 6/7 0.00153] [usd-chf-eur] -nosave')
    r._parseInput('[btc 5/7 0.0015899 6/7 0.00153] [usd] -nosave')
    r._parseInput('[btc 5/7 0.0015899 6/7 0.00153] [] -nosave')