import re

class EssPatt:
    def parseFiat(self, inputStr):
        #convert [usd-chf]
        #into
        #[usd, chf]
                
        fiatDataList = []
        patternFiat = r"((\w+)-)|((\w+)\])|(\[(w+)\])"

        for grp in re.finditer(patternFiat, inputStr):
            for elem in grp.groups():
                if elem != None and len(elem) == 3:
                    fiatDataList.append(elem)

        return fiatDataList
        
    def parseDatePrice(self, inputStr):
        #convert [5/7 0.0015899 6/7 0.00153]
        #into
        #[5/7, 0.0015899, 6/7, 0.00153]
        
        cryptoDataList = []             
        patternDatePrice = r"(\d+/\d+) ([0-9\.]+)"

        for grp in re.finditer(patternDatePrice, inputStr):
            for elem in grp.groups():
                cryptoDataList.append(elem)
                
        return cryptoDataList

    def parseOOCommandParms(self, inputStr):        
        pattern = r"(?:(\w+) (\[.*\]) (\[.*\]))|(-\w+)"
        
        fiatDataList = []
        cryptoDataList = []
        flag = ''
        
        for grp in re.finditer(pattern, inputStr):                
            for elem in grp.groups():
                if elem is not None:
                    if '[' in elem:
                        if ' ' in elem: #list of date/price pairs
                            cryptoDataList += self.parseDatePrice(elem)
                        else: #list of fiat currencies
                            fiatDataList = self.parseFiat(elem)
                    else: #crypto symbol like btc or flag like -nosave
                        if '-' in elem:
                            flag = elem
                        else: #crypto symbol at first posieion in input string
                            cryptoDataList.append(elem)

        return cryptoDataList, fiatDataList, flag
    
ep = EssPatt()

inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')

inputStr = "btc [5/7 0.0015899] [usd] -nosave"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')

inputStr = "btc [] [usd-chf-eur] -nosave"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')

inputStr = "btc [5/7 ] [usd-chf] -nosave"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')

inputStr = "btc [0.8888] [usd] -nosave"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')

inputStr = "btc [0.8888] []"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')

inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf]"
cryptoDataList, fiatDataList, flag = ep.parseOOCommandParms(inputStr)
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')