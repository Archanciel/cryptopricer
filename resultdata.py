

class ResultData:
    RESULT_KEY_CRYPTO = 'CRYPTO'
    RESULT_KEY_FIAT = 'FIAT'
    RESULT_KEY_EXCHANGE = 'EXCHANGE'
    RESULT_KEY_PRICE_TIME_STAMP = 'PRICE_TIMESTAMP'
    RESULT_KEY_PRICE_DATE_TIME_STRING = 'PRICE_DATE_TIME_STR'
    RESULT_KEY_PRICE = 'PRICE'
    RESULT_KEY_PRICE_TYPE = 'PRICE_TYPE'
    RESULT_KEY_ERROR_MSG = 'ERROR_MSG'
    RESULT_KEY_WARNING_MSG = 'WARNING_MSG'
    RESULT_KEY_COMMAND = 'COMMAND' #full command which generated the result
    RESULT_KEY_PRICE_VALUE_CRYPTO = 'PRICE_VAL_CRYPTO' #store the crypto price returned for -v command
    RESULT_KEY_PRICE_VALUE_FIAT = 'PRICE_VAL_FIAT'     #store the fiat price returned for -v command

    PRICE_TYPE_HISTO_DAY = 'HISTO_DAY'
    PRICE_TYPE_HISTO_MINUTE = 'HISTO_MINUTE'
    PRICE_TYPE_RT = 'REAL_TIME'

    
    def __init__(self):
        self._resultDataDic = {}
        self._resultDataDic[self.RESULT_KEY_CRYPTO] = None
        self._resultDataDic[self.RESULT_KEY_FIAT] = None
        self._resultDataDic[self.RESULT_KEY_EXCHANGE] = None
        self._resultDataDic[self.RESULT_KEY_PRICE_TIME_STAMP] = None
        self._resultDataDic[self.RESULT_KEY_PRICE_DATE_TIME_STRING] = None
        self._resultDataDic[self.RESULT_KEY_PRICE] = None
        self._resultDataDic[self.RESULT_KEY_PRICE_TYPE] = None
        self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None
        self._resultDataDic[self.RESULT_KEY_WARNING_MSG] = None
        self._resultDataDic[self.RESULT_KEY_COMMAND] = None
        self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None       
        self._resultDataDic[self.RESULT_KEY_PRICE_VALUE_CRYPTO] = None
        self._resultDataDic[self.RESULT_KEY_PRICE_VALUE_FIAT] = None

 

    def setValue(self, key, value):
        self._resultDataDic[key] = value


    def getValue(self, key):
        return self._resultDataDic[key]


    def isEmpty(self, key):
        return self._resultDataDic[key] == None


    def isError(self):
        '''
        Return True if the ResultData contains an error msg
        '''
        return self._resultDataDic[self.RESULT_KEY_ERROR_MSG] != None


    def __str__(self):
        strRepr = ''

        for key in self._resultDataDic.keys():
            val = self._resultDataDic.get(key)
            if val != None:
                strRepr += key + ': ' + str(val) + ' '
            else:
                strRepr += key + ': None '

        return strRepr


if __name__ == '__main__':
    pass
