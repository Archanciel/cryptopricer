import os

from abstractoutputformater import AbstractOutputFormater


class ConsoleOutputFormater(AbstractOutputFormater):
    PRICE_FLOAT_FORMAT = '%.8f'
    
    def __init__(self, activateClipboard = False):
        '''
        Ctor. The parm activateClipboard with default value set to False was added to prevent SeqDiagBuilder
        unit tests in TestSeqDiagBuilder where the CryptoPricer Condtroller class were implied to crash the Pycharm
        unit test environment. This crask was due to an obscure problem in the Pycharm unit test framework. This
        failure only happened if the kivy clipboard class was imported.

        :param activateClipboard:
        '''
        self.activateClipboard = activateClipboard

        if os.name == 'posix':
            import android
            self._clipboard = android.Android()
        else:
            if self.activateClipboard:
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
            if not self.activateClipboard:
                pass
            else:
                self._clipboard.copy(str(numericVal))


    def fromClipboard(self):
        if os.name == 'posix':
            return self._clipboard.getClipboard().result
        else:
            if self.activateClipboard:
                return self._clipboard.paste()
            else:
                return 'Clipboard not available since not activated at ConsoleOutputFormater initialisation'


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
    print('With formatting no trailing 0: ' + pr._formatPriceFloatToStr(y))
    print()

    a = 12.56
    if os.name == 'posix':
        pr.toClipboard(a)
        print('Clip Android: ' + pr.fromClipboard())

    if os.name != 'posix':
        import clipboard
        clipboard.copy(str(2351.78))
        print('Clip Windows: ' + clipboard.paste())
