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
             
        patternDatePrice = r"(\d+/\d+) (\d+\.\d+)"

        for grp in re.finditer(patternDatePrice, inputStr):
            for elem in grp.groups():
                cryptoDataList.append(elem)
                
        return cryptoDataList

    def parseDown(self, inputStr):
        pattern = r"(?:(\w+) (\[.*\]) (\[.*\]))|(-\w+)"
        print(inputStr)
        for grp in re.finditer(pattern, inputStr):                
            for elem in grp.groups():
                if elem is not None:
                    if '[' in elem:
                        if ' ' in elem: #list of date/price pairs
                            for e in self.parseDatePrice(elem):
                                print(e)
                        else: #list of fiat currencies
                            for e in self.parseFiat(elem):
                                print(e)
                    else:
                        print(elem)

    
ep = EssPatt()

ep.parseDown("btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave")
ep.parseDown("btc [5/7 0.0015899] [usd] -nosave")
ep.parseDown("btc [] [usd-chf-eur] -nosave")
ep.parseDown("btc [5/7 ] [usd-chf] -nosave")
ep.parseDown("btc [0.8888] [usd] -nosave")
ep.parseDown("btc [0.8888] []")
ep.parseDown("btc [5/7 0.0015899 6/7 0.00153] [usd-chf]")
