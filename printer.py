import os

from priceresult import PriceResult

class Printer:
    def __init__(self):
        if os.name == 'posix':
            import android
            self._clipboard = android.Android()
        else:
            pass
           
    
    def print(self, priceResult):
        '''
        print the result to the console and 
        paste it to the clipboard
        '''
        errorMsg = priceResult.getValue(priceResult.RESULT_KEY_ERROR_MSG)

        if errorMsg == None:
            price = priceResult.getValue(priceResult. RESULT_KEY_PRICE)
            self.toClipboard(str(price))
            dateTimeStr = priceResult.getValue(priceResult.RESULT_KEY_PRICE_DATE_TIME_STRING)
            priceType = priceResult.getValue(priceResult.RESULT_KEY_PRICE_TYPE)
            
            if  priceType == priceResult.PRICE_TYPE_HISTO_DAY:
                dateTimeStr += 'C' #adding close symbol
            elif priceType == priceResult.PRICE_TYPE_HISTO_MINUTE:
                dateTimeStr += 'M' #adding histo MINUTE symbol
            else:
                dateTimeStr += 'R' #adding RT symbol
            
            outputStr = '{}/{} on {}: {} {}'.format(priceResult.getValue(priceResult.RESULT_KEY_CRYPTO),
        	                                           priceResult.getValue(priceResult.RESULT_KEY_FIAT),
        	                                           priceResult.getValue(priceResult.RESULT_KEY_EXCHANGE),
        	                                           dateTimeStr,
        	                                           price)
        else:
        	   outputStr = '{}'.format(errorMsg)
                                        	                                  	
        print(outputStr)
        
        
    def toClipboard(self, value):
        if os.name == 'posix':
            self._clipboard.setClipboard(str(value))
        else:
            pass


    def fromClipboard(self):
        if os.name == 'posix':
            return self._clipboard.getClipboard().result
        else:
            pass


if __name__ == '__main__':
    pr = Printer()

    a = 12.56
    pr.toClipboard(a)
    print('Clip: ' + pr.fromClipboard())

