import re

class EssPattXO:
    def _parseFiat(self, inputStr):
        # convert "[usd-chf]"
        # into
        # ['usd', 'chf']
        # and return the fiat list

        fiatList = []
        patternFiat = r"((\w+)-)|((\w+)\])|(\[(w+)\])"

        for grp in re.finditer(patternFiat, inputStr):
            for elem in grp.groups():
                if elem != None and len(elem) == 3:
                    fiatList.append(elem)

        return fiatList

    def _parseDateTimePriceExchange(self, inputStr):
        # convert "[22/08 23:54 0.00046306 ccex]"
        # into
        # ['22/07', '23:54', '0.00046306', 'ccex']]
        # and return the date price pair list
        priceDateList = []
        patternDatePrice = r"\[(\d+/\d+) (\d+\:\d+) (\d+\.\d+) (\w+)\]"     

        match = re.match(patternDatePrice, inputStr)
        
        if match:
            priceDateList = match.groups()

        return priceDateList

    def _parseXOCommandParms(self, inputStr, upperInputStr):
        # convert "btc [22/08 23:54 0.00046306 ccex] [usd-chf] -save"
        # into
        # cryptoDataList = ['btc', '22/07', '23:54', '0.00046306', 'ccex']
        # fiatDataList = ['usd', 'chf']
        # flag = '-save'
        #
        # in case the user input violates the awaited pattern, a CommandError object is
        # returned instead of the cryptoDataList
        pattern = r"(?:(\w+) (\[.*\]) (\[.*\]))|(-\w+)"

        fiatDataList = []
        cryptoDataList = []
        flag = None
        grpNumber = 0

        for grp in re.finditer(pattern, upperInputStr):
            grpNumber += 1
            for elem in grp.groups():
                if elem is not None:
                    if '[' in elem:
                        if ' ' in elem:  # list of date/price pairs
                            cryptoDataList += self._parseDateTimePriceExchange(elem)
                        else:  # list of fiat currencies
                            fiatDataList = self._parseFiat(elem)
                    else:  # crypto symbol like btc or flag like -nosave
                        if '-' in elem:
                            flag = elem
                        else:  # crypto symbol at first position in input string
                            cryptoDataList.append(elem)

        if (grpNumber == 0) or (grpNumber == 1 and flag != None):
            #self.commandError.rawParmData = inputStr
            #self.commandError.parsedParmData = [self.commandError.FIAT_LIST_MISSING_MSG]
            #return self.commandError, fiatDataList, flag
            pass
        else:
            return cryptoDataList, fiatDataList, flag

    
ep = EssPattXO()

inputStr = "btc [22/08 23:54 0.00046306 ccex] [usd-chf] -save"
cryptoDataList, fiatDataList, flag = ep._parseXOCommandParms(inputStr, inputStr.upper())
print(inputStr)
print(cryptoDataList)
print(fiatDataList)
print(flag)
print('')
