class ResultData:
    RESULT_KEY_CRYPTO = 'CRYPTO'
    RESULT_KEY_UNIT = 'UNIT'
    RESULT_KEY_EXCHANGE = 'EXCHANGE'
    RESULT_KEY_PRICE_TIME_STAMP = 'PRICE_TIMESTAMP'
    RESULT_KEY_PRICE_DATE_TIME_STRING = 'PRICE_DATE_TIME_STR'
    RESULT_KEY_PRICE = 'PRICE'
    RESULT_KEY_PRICE_TYPE = 'PRICE_TYPE'
    RESULT_KEY_ERROR_MSG = 'ERROR_MSG'
    RESULT_KEY_WARNINGS_DIC = 'WARNING_MSG'
    RESULT_KEY_INITIAL_COMMAND_PARMS = 'INIT_COMMAND_PARMS'                 # command parm dic denoting the user requesr

    RESULT_KEY_OPTION_VALUE_CRYPTO = 'OPTION_VALUE_CRYPTO'  # store the crypto price returned for -v option
    RESULT_KEY_OPTION_VALUE_UNIT = 'OPTION_VALUE_UNIT'      # store the unit price returned for -v option
    RESULT_KEY_OPTION_VALUE_FIAT = 'OPTION_VALUE_FIAT'      # store the fiat price returned for -v option
                                                            # provided the -f fiat option is specified
    RESULT_KEY_OPTION_VALUE_SAVE = 'OPTION_VALUE_SAVE'      # store True or False to indicate if the value option is to be stored in history (-vs) or not (-v)

    RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT = 'OPTION_FIAT_COMPUTED_AMOUNT'# store the crypto price in unit converted to fiat returned for the -f option
    RESULT_KEY_OPTION_FIAT_SYMBOL = 'OPTION_FIAT_SYMBOL'                  # store the fiat symbol of the -f option
    RESULT_KEY_OPTION_FIAT_EXCHANGE = 'OPTION_FIAT_EXCHANGE'              # store the fiat exchange of the -f option
    RESULT_KEY_OPTION_FIAT_SAVE = 'OPTION_FIAT_SAVE'                      # store True or False to indicate if the fiat option is to be stored in history (-fs) or not (-f)

    RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT = 'OPTION_PRICE_SPECIFIED_AMOUNT'          # store the crypto or unit user entered value for -v option. Ex: 0.1 if -v0.1btc
    RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT = 'OPTION_PRICE_COMPUTED_UNIT_AMOUNT'  # store the price in unit corresponding to the amount specified in the option synbol specified
                                                                                        # for the -p option. Ex: if crypto is eth and unit is btc and option is -p300usd,
                                                                                        # store the price in btc if 1 eth is 300 usd
    RESULT_KEY_OPTION_PRICE_SYMBOL = 'OPTION_PRICE_SYMBOL'  # store the currency symbol of the -p option, usd if otion is -p300usd
    RESULT_KEY_OPTION_PRICE_SAVE = 'OPTION_PRICE_SAVE'      # store True or False to indicate if the price option is to be stored in history (-ps) or not (-p)

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
        self._resultDataDic[self.RESULT_KEY_PRICE_TIME_STAMP] = None
        self._resultDataDic[self.RESULT_KEY_PRICE_DATE_TIME_STRING] = None
        self._resultDataDic[self.RESULT_KEY_PRICE] = None
        self._resultDataDic[self.RESULT_KEY_PRICE_TYPE] = None
        self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None
        self._resultDataDic[self.RESULT_KEY_WARNINGS_DIC] = {}
        self._resultDataDic[self.RESULT_KEY_INITIAL_COMMAND_PARMS] = None
        self._resultDataDic[self.RESULT_KEY_ERROR_MSG] = None       
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_CRYPTO] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_UNIT] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_FIAT] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_VALUE_SAVE] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_SYMBOL] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_FIAT_SAVE] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_PRICE_SPECIFIED_AMOUNT] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_PRICE_COMPUTED_UNIT_AMOUNT] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_PRICE_SYMBOL] = None
        self._resultDataDic[self.RESULT_KEY_OPTION_PRICE_SAVE] = None

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
