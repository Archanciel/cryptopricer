from abstractcommand import AbstractCommand
from resultdata import ResultData

class CommandError(AbstractCommand):
    USER_COMMAND_MISSING_MSG = 'user command missing'
    CRYPTO_SYMBOL_MISSING_MSG = 'crypto symbol missing' #to delete !
    FIAT_LIST_MISSING_MSG = 'fiat list missing'
    COMMAND_NOT_SUPPORTED_MSG = '{} not supported'
    PARTIAL_PRICE_COMMAND_TIME_FORMAT_INVALID_MSG = 'in {}, {} must respect {} format'
    PARTIAL_PRICE_VALUE_COMMAND_FORMAT_INVALID_MSG = 'in {}, {} must respect 99.99999zzz <price><symbol> format'
    FULL_COMMAND_PRICE_FORMAT_INVALID_MSG = 'full command price format invalid'

    COMMAND_ERROR_TYPE_KEY = 'COMMAND_ERROR_TYPE'

    COMMAND_ERROR_TYPE_FULL_REQUEST = 'FULL_REQUEST_ERROR'
    COMMAND_ERROR_TYPE_PARTIAL_REQUEST = 'PARTIAL_REQUEST_ERROR'
    COMMAND_ERROR_TYPE_INVALID_COMMAND = 'INVALID_COMMAND_ERROR'

    COMMAND_ERROR_MSG_KEY = 'COMMAND_ERROR_MSG'

    def __init__(self, receiver = None):
        super().__init__(receiver, 'CommandError')


    def initialiseParsedParmData(self):
        self.parsedParmData[self.COMMAND_ERROR_TYPE_KEY] = None
        self.parsedParmData[self.COMMAND_ERROR_MSG_KEY] = ''


    def execute(self):
        resultData = ResultData()
        errorDetails = self.parsedParmData[self.COMMAND_ERROR_MSG_KEY]
        errorType = self.parsedParmData[self.COMMAND_ERROR_TYPE_KEY]
        errorTypeLabelStr = ''
        errorMsgTail = ''

        if errorType == self.COMMAND_ERROR_TYPE_FULL_REQUEST:
            errorTypeLabelStr = 'full request'
            errorMsgTail = ' violates format <crypto> <fiat> <date|time> <exchange> <opt commands>'
        elif errorType == self.COMMAND_ERROR_TYPE_PARTIAL_REQUEST:
            errorTypeLabelStr = 'invalid partial request'
        elif errorType == self.COMMAND_ERROR_TYPE_INVALID_COMMAND:
            errorTypeLabelStr = 'invalid request'

        if errorDetails != '':
            errorDetails = ': ' + errorDetails
            
        resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - {} {}{}{}".format(errorTypeLabelStr, self.requestInputString, errorDetails, errorMsgTail))
        
        return resultData


    def isValid(self):
        '''
        Return True if the command contains valid data and can be executed
        '''
        return True
