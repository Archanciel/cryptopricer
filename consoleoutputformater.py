import os

from resultdata import ResultData
from abstractoutputformater import AbstractOutputFormater


class ConsoleOutputFormater(AbstractOutputFormater):
    FLOAT_FORMAT = '%.8f'
    
    def __init__(self):
        if os.name == 'posix':
            import android
            self._clipboard = android.Android()
        else:
            from kivy.core.clipboard import Clipboard
            self._clipboard = Clipboard


    def printDataToConsole(self, resultData):
        '''
        print the result to the console and 
        paste it to the clipboard
        '''
        outputStr = super(ConsoleOutputFormater, self).getPrintableData(resultData)

        print(outputStr)

    def toClipboard(self, numericVal):
        if os.name == 'posix':
            self._clipboard.setClipboard(str(numericVal))
        else:
            self._clipboard.copy(str(numericVal))


    def fromClipboard(self):
        if os.name == 'posix':
            return self._clipboard.getClipboard().result
        else:
            return self._clipboard.paste()


if __name__ == '__main__':
    pr = ConsoleOutputFormater()
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
    if os.name == 'posix':
        pr.toClipboard(a)
        print('Clip Android: ' + pr.fromClipboard())

    if os.name != 'posix':
        import clipboard
        clipboard.copy(str(2351.78))
        print('Clip Windows: ' + clipboard.paste())
