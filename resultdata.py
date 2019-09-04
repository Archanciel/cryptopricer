class ResultData:
    RESULT_KEY_CRYPTO = 'CRYPTO'
    RESULT_KEY_UNIT = 'UNIT'
    RESULT_KEY_EXCHANGE = 'EXCHANGE'
    RESULT_KEY_OPTION_TIME_STAMP = 'PRICE_TIMESTAMP'
    RESULT_KEY_OPTION_DATE_TIME_STRING = 'PRICE_DATE_TIME_STR'
    RESULT_KEY_PRICE = 'PRICE'
    RESULT_KEY_OPTION_TYPE = 'PRICE_TYPE'
    RESULT_KEY_ERROR_MSG = 'ERROR_MSG'
    RESULT_KEY_WARNINGS_DIC = 'WARNING_MSG'
    RESULT_KEY_INITIAL_COMMAND_PARMS = 'INIT_COMMAND_PARMS'                 # command parm dic denoting the user requesr
    RESULT_KEY_OPTION_VALUE_COMPUTED_AMOUNT = 'OPTION_VALUE_COMPUTED_AMOUNT'# store the crypto or unit computed value returned for -v option
    RESULT_KEY_OPTION_VALUE_SYMBOL = 'OPTION_VALUE_SYMBOL'                  # store the currency or unit symbol returned for -v option
    RESULT_KEY_OPTION_VALUE_SAVE = 'OPTION_VALUE_SAVE'                      # store True or False to indicate if the price value option is to be stored in history (-vs) or not (-v)

    WARNING_TYPE_FUTURE_DATE = 'FUTURE_DATE'
    WARNING_TYPE_COMMAND_VALUE = 'VALUE_COMMAND'
    WARNING_TYPE_UNSUPPORTED_OPTION = 'UNSUPPORTED_OPTION'

    PRICE_TYPE_HISTO_DAY = 'HISTO_DAY'
    PRICE_TYPE_HISTO_MINUTE = 'HISTO_MINUTE'
    PRICE_TYPE_RT = 'REAL_TIME'

    
    def __init__(self):
        self._resultDataDic = {}
        self._resultDataDic[self.RESULT_KEY_CRYPTO] = None
        self._resultDataDic[self.RESULT_KEY_UNIT] = None
        self._resultDataDic[self.RESULT_KEY_EXCHANGE] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_TIME_STAMP] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_DATE_TIME_STRING] = None
        self._resultDataDic[self.RESULT_KEY_PRICE] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_TYPE] = None
        self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None
        self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] = {}
        self._resultDataDic[self.RESULT_KEY_INITIAL_COMMAND_PARMS] = None
        self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None       
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_COMPUTED_AMOUNT] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_SYMBOL] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_SAVE] = None

        self.requestInputString = ''


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


    def containsWarning(self, warningType):
        '''
        Return True if the ResultData contains a warning msg
        '''
        warningDic = self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC]

        if warningDic == {}:
            return False
        else:
            return warningType in warningDic.keys()


    def containsWarnings(self):
        '''
        Return True if the ResultData contains a warning msg
        '''
        return self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] != {}


    def getWarningMessage(self, warningType):
        '''
        Return the warning msg contained in the ResultData
        :param warningType:
        '''
        return self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC][warningType]


    def setWarning(self, warningType, warningMessage):
        '''
        Set the warning msg entry in the ResultData
        :param warningType:
        '''
        warningsDic = self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC]
        warningsDic[warningType] = warningMessage


    def getAllWarningMessages(self):
        '''
        Return a list of warning messages.
        :return: list containing the warning msg strings
        '''

        return list(self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC].values())


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
