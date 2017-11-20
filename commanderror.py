from abstractcommand import AbstractCommand
from resultdata import ResultData

class CommandError(AbstractCommand):
    USER_COMMAND_MISSING_MSG = 'user command missing'
    CRYPTO_SYMBOL_MISSING_MSG = 'crypto symbol missing' #to delete !
    FIAT_LIST_MISSING_MSG = 'fiat list missing'
    COMMAND_NOT_SUPPORTED_MSG = '{} not supported'

    def __init__(self, receiver=None, rawParmData='', parsedParmData=''):
        super().__init__(receiver, 'CommandError', rawParmData, parsedParmData)


    def _initialiseParsedParmData(self):
        pass


    def execute(self):
        priceResult = ResultData()
        errorDetails = self.parsedParmData[0]
        
        if errorDetails != '':
            errorDetails = ': ' + errorDetails
            
        priceResult.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - invalid command " + self.rawParmData + errorDetails)
        
        return priceResult