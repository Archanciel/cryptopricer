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
            dateTimeStr = resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING)
            priceType = resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE)

            if priceType == resultData.PRICE_TYPE_HISTO_DAY:
                dateTimeStr += 'C'  # adding close symbol
            elif priceType == resultData.PRICE_TYPE_HISTO_MINUTE:
                dateTimeStr += 'M'  # adding histo MINUTE symbol
            else:
                dateTimeStr += 'R'  # adding RT symbol

            outputStr = '{}/{} on {}: {} {}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
                                                    resultData.getValue(resultData.RESULT_KEY_FIAT),
                                                    resultData.getValue(resultData.RESULT_KEY_EXCHANGE),
                                                    dateTimeStr,
                                                    formattedPriceStr)
        else:
            outputStr = '{}'.format(errorMsg)
        return outputStr


    def formatFloatToStr(self, floatNb):
        try:
            floatNbFormatted = self.FLOAT_FORMAT % floatNb
        except TypeError:
            return ''

        floatNbFormattedStripZero = floatNbFormatted.rstrip('0')
        return floatNbFormattedStripZero.rstrip('.')
