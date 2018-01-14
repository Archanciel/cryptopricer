import os

from commandprice import CommandPrice
from abstractoutputformater import AbstractOutputFormater
from kivy.core.clipboard import Clipboard


class GuiOutputFormater(AbstractOutputFormater):
    
    
    def __init__(self):
        # commented code below does not run in Pydroid since Pydroid does not support
        # the sl4a lib
        # if os.name == 'posix':
        #     import android
        #     self._clipboard = android.Android()
        # else:
        self._clipboard = Clipboard


    def printDataToConsole(self, resultData):
        '''
        print the result to the console and 
        paste it to the clipboard
        '''
        outputStr = super(GuiOutputFormater, self).getPrintableData(resultData)
                                        	                                  	
        print(outputStr)
        
        
    def getFullCommandString(self, resultData):
        '''
        Recreate the full command string corresponding to a full or partial price request entered by the user.
        The full command string will be stored in the command history list so it can be replayed or save to file.
        An empty string is returned if the command generated an error or a warning msg (empty string will not be
        added to history !

        In case an option to the command with save mode is in effect - for example -vs -, then the full
        command with the save mode option is returned aswell. Othervise, if no command option in save mode
        is in effect (no option or -v for example), then None is returned as second return value.

        :param resultData: result of the last full or partial request
        :return: 1/ full command string with no command option corresponding to a full or partial price request
                    entered by the user or empty string if the command generated an error or a warning msg.
                 2/ full command string with command option in save mode or none if no command option in save mode
                    is in effect.

                 Ex: 1/ eth usd 0 bitfinex
                     2/ eth usd 0 bitfinex -vs0.1eth

                     1/ eth usd 0 bitfinex
                     2/ None (-v0.1eth option in effect)

                     1/ eth usd 0 bitfinex
                     3/ None (no option in effect)
        '''
        if resultData.isError() or resultData.containsWarning():
            return '', None
            
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

        fullCommandStrWithSaveModeOptions = None

        if resultData.getValue(resultData.RESULT_KEY_PRICE_VALUE_SAVE):
            fullCommandStrWithSaveModeOptions = fullCommandStr + ' -vs' + commandDic[CommandPrice.PRICE_VALUE_AMOUNT] + commandDic[CommandPrice.PRICE_VALUE_SYMBOL]

        return fullCommandStr, fullCommandStrWithSaveModeOptions
        

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
