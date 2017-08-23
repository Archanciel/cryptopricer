import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requester import Requester
from commandcrypto import CommandCrypto
from commandquit import CommandQuit
from commanderror import CommandError


class TestRequester(unittest.TestCase):
    '''
    -teste input crypto + fiat avec ou sans
    nosave ou ns
    
    -teste input crypto avec 0 price/oate,
    1 price/date, n price/date
    
    -idem 0, 1, n fiats
    
    -varie order crypto list/fiat list/
    nosave command
    '''
    def setUp(self):
        requester = Requester()
        requester.commandCrypto = CommandCrypto(None)
        requester.commandQuit = CommandQuit(None)
        self.commandError = CommandError(None)
        requester.commandError = self.commandError
        self.requester = requester

        
    def test_parseFiatDataFromInputIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['usd', 'chf'])


    def test_parseFiatDataFromInputNoOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd-chf]"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['usd', 'chf'])


    def test_parseFiatDataFromInputEmptyFiatListIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputOneFiatInListIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['usd'])


    def test_parseFiatDataFromInputThreeFiatInListIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd-chf-eur] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['usd', 'chf', 'eur'])


    def test_parseFiatDataFromInputThreeFiatInListNoFiatSepCharIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd chf] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['chf'])


    def test_parseFiatDataFromInputNoFiatListIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputEmptyFiatListNoOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] []"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputNoFiatListNoOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153]"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputIncludeOtherCommandFiatListFirstPos(self):
        inputStr = "[usd-chf] [btc 5/7 0.0015899 6/7 0.00153] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['usd', 'chf'])


    def test_parseFiatDataFromInputNoOtherCommandFiatListFirstPos(self):
        inputStr = "[usd-chf] [btc 5/7 0.0015899 6/7 0.00153]"
        fiatData = self.requester._parseFiatDataFromInput(inputStr)
        self.assertEqual(fiatData, ['usd', 'chf'])


    def test_parseCryptoDataFromInputIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputNoOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputNoCryptoSymbolNoOtherCommand(self):
        inputStr = "[5/7 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, self.commandError)


    def test_parseCryptoDataFromInputNoCryptoSymbolOtherCommand(self):
        inputStr = "[5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, self.commandError)


    def test_parseCryptoDataFromInputOnePriceOnlyNoOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyNoDateNoOtherCommand(self):
        inputStr = "[btc 0.0015899] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, '')


    def test_parseCryptoDataFromInputOnePriceOnlyNoDateOtherCommand(self):
        inputStr = "[btc 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, '')


    def test_parseCryptoDataFromInputOneDateMissingIncludeOtherCommand(self):
        inputStr = "[btc 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOneDateMissingNoOtherCommand(self):
        inputStr = "[btc 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOnePriceMissingIncludeOtherCommand(self):
        inputStr = "[btc 5/7 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOnePriceMissingNoOtherCommand(self):
        inputStr = "[btc 5/7 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOnePriceTwoDigitaDateOnlyOtherCommand(self):
        inputStr = "[btc 15/12 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, ['BTC', '15/12', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyZeroesInDateOtherCommandFiatListFirstPos(self):
        inputStr = "[usd-chf] [btc 05/07 0.0015899] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr)
        self.assertEqual(cryptoData, self.commandError)


if __name__ == '__main__':
    unittest.main()