import os

from resultdata import ResultData
from kivy.core.clipboard import Clipboard


class Printer:
    FLOAT_FORMAT = '%.8f'
    
    def __init__(self):
        self._clipboard = Clipboard
#        if os.name == 'posix':
#            import android
#            self._clipboard = android.Android()
#        else:
#            import clipboard
#            self._clipboard = Clipboard

    def print(self, resultData):
        '''
        print the result to the console and 
        paste it to the clipboard
        '''
        errorMsg = resultData.getValue(resultData.RESULT_KEY_ERROR_MSG)

        if errorMsg == None:
            price = resultData.getValue(resultData. RESULT_KEY_PRICE)
            formattedPriceStr = self.formatFloatToStr(price)
            self.toClipboard(formattedPriceStr)
            dateTimeStr = resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING)
            priceType = resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE)
            
            if  priceType == resultData.PRICE_TYPE_HISTO_DAY:
                dateTimeStr += 'C' #adding close symbol
            elif priceType == resultData.PRICE_TYPE_HISTO_MINUTE:
                dateTimeStr += 'M' #adding histo MINUTE symbol
            else:
                dateTimeStr += 'R' #adding RT symbol
            
            outputStr = '{}/{} on {}: {} {}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
        	                                           resultData.getValue(resultData.RESULT_KEY_FIAT),
        	                                           resultData.getValue(resultData.RESULT_KEY_EXCHANGE),
        	                                           dateTimeStr,
        	                                           formattedPriceStr)    
        else:
        	   outputStr = '{}'.format(errorMsg)
                                        	                                  	
        print(outputStr)
        
        
    def toClipboard(self, numericVal):
        # if os.name == 'posix':
        #     self._clipboard.setClipboard(str(numericVal))
        # else:
        self._clipboard.copy(str(numericVal))


    def fromClipboard(self):
        # if os.name == 'posix':
        #     return self._clipboard.getClipboard().result
        # else:
        return self._clipboard.paste()


    def formatFloatToStr(self, floatNb):
        try:
            floatNbFormatted = self.FLOAT_FORMAT % floatNb
        except TypeError:
            return ''
            
        floatNbFormattedStripZero = floatNbFormatted.rstrip('0')
        return floatNbFormattedStripZero.rstrip('.')
        
if __name__ == '__main__':
    pr = Printer()
    y = round(5.59, 1)
    y = 0.999999999
    y = 0.9084
    y = 40
    yFormatted = '%.8f' % y
    print()
    print('No formatting:                 ' + str(y))
    print('With formatting:               ' + yFormatted)
    print('With formatting no trailing 0: ' + pr.formatFloatToStr(y))
    print()

    a = 12.56
#    if os.name == 'posix':
    pr.toClipboard(a)
    print('Clip Android: ' + pr.fromClipboard())

#    if os.name != 'posix':
#        import clipboard
#        clipboard.copy(str(2351.78))
#        print('Clip Windows: ' + clipboard.paste())


