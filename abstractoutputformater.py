from abc import ABCMeta
from abc import abstractmethod

class AbstractOutputFormater(metaclass=ABCMeta):
    '''
    '''
    FLOAT_FORMAT = '%.8f'
    

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        pass


    @abstractmethod
    def printDataToConsole(self):
        '''
        Output formated data in the console
        :return: nothing
        '''
        pass


    @abstractmethod
    def toClipboard(self, numericVal):
        pass


    @abstractmethod
    def fromClipboard(self):
        pass


    def getPrintableData(self, resultData):
        errorMsg = resultData.getValue(resultData.RESULT_KEY_ERROR_MSG)

        if errorMsg == None:
            price = resultData.getValue(resultData.RESULT_KEY_PRICE)
            formattedPriceStr = self.formatFloatToStr(price)
            self.toClipboard(formattedPriceStr)
            dateTimeStr = resultData.getValue(resultData.RESULT_KEY_OPTION_DATE_TIME_STRING)
            priceType = resultData.getValue(resultData.RESULT_KEY_OPTION_TYPE)

            if priceType == resultData.PRICE_TYPE_HISTO_DAY:
                dateTimeStr += 'C'  # adding close symbol
            elif priceType == resultData.PRICE_TYPE_HISTO_MINUTE:
                dateTimeStr += 'M'  # adding histo MINUTE symbol
            else:
                dateTimeStr += 'R'  # adding RT symbol

            cryptoUnitPart = self._formatCryptoUnitPart(resultData)
            outputStr = cryptoUnitPart + ' on {}: {} {}'.format(resultData.getValue(resultData.RESULT_KEY_EXCHANGE),
                                                                dateTimeStr,
                                                                formattedPriceStr)
        else:
            outputStr = '{}'.format(errorMsg)

        if resultData.containsWarnings():
            outputStr = outputStr + '\n' + '\n'.join(resultData.getAllWarningMessages())
            
        return outputStr


    def _formatCryptoUnitPart(self, resultData):
        if resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO) == None:
            return '{}/{}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO), 
                                  resultData.getValue(resultData.RESULT_KEY_UNIT))
        else:
            formattedPriceCryptoStr = self.formatFloatToStr(float(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO)))
            formattedPriceUnitStr = self.formatFloatToStr(float(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT)))
            
            return '{} {}/{} {}'.format(formattedPriceCryptoStr, 
                                        resultData.getValue(resultData.RESULT_KEY_CRYPTO),
                                        formattedPriceUnitStr, 
                                        resultData.getValue(resultData.RESULT_KEY_UNIT))
                                                       
        
        
    def formatFloatToStr(self, floatNb):
        try:
            floatNbFormatted = self.FLOAT_FORMAT % floatNb
        except TypeError:
            return ''

        floatNbFormattedStripZero = floatNbFormatted.rstrip('0')
        return floatNbFormattedStripZero.rstrip('.')
