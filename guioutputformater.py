import os

from resultdata import ResultData
from commandprice import CommandPrice
from abstractoutputformater import AbstractOutputFormater
from kivy.core.clipboard import Clipboard


class GuiOutputFormater(AbstractOutputFormater):
    FLOAT_FORMAT = '%.8f'
    
    
    def __init__(self):
        self._clipboard = Clipboard


    def printDataToConsole(self, resultData):
        '''
        print the result to the console and 
        paste it to the clipboard
        '''
        outputStr = super(GuiOutputFormater, self).getPrintableData(resultData)
                                        	                                  	
        print(outputStr)
        
    def getFullCommandString(self, resultData):
        commandDic = resultData.getValue(resultData.RESULT_KEY_COMMAND)
        priceType = resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE)
        
        if priceType == resultData.PRICE_TYPE_RT:      
            fullCommandStr = commandDic[CommandPrice.CRYPTO] + ' ' + \
                             commandDic[CommandPrice.FIAT] + ' 0 ' + \
                             commandDic[CommandPrice.EXCHANGE]
        else:
            year = commandDic[CommandPrice.YEAR]
            if year == None:
                monthYear = commandDic[CommandPrice.MONTH] + ' '
            else:
                monthYear = commandDic[CommandPrice.MONTH] + '/' + commandDic[CommandPrice.YEAR] + ' '

            fullCommandStr = commandDic[CommandPrice.CRYPTO] + ' ' + \
                             commandDic[CommandPrice.FIAT] + ' ' + \
                             commandDic[CommandPrice.DAY] + '/' + \
                             monthYear + \
                             commandDic[CommandPrice.HOUR] + ':' + \
                             commandDic[CommandPrice.MINUTE] + ' ' + \
                             commandDic[CommandPrice.EXCHANGE]

        return fullCommandStr
        

    def toClipboard(self, numericVal):
        self._clipboard.copy(str(numericVal))


    def fromClipboard(self):
        return self._clipboard.paste()


if __name__ == '__main__':
    pr = GuiOutputFormater()
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
    pr.toClipboard(a)
    print('Clipboard: ' + pr.fromClipboard())
