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
        requester.commandQuit = CommandQuit(sys)
        self.commandError = CommandError(None)
        requester.commandError = self.commandError
        self.requester = requester

        
    def test_parseFiatDataFromInputIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, ['USD', 'CHF'])


    def test_parseFiatDataFromInputNoOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd-chf]"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, ['USD', 'CHF'])


    def test_parseFiatDataFromInputEmptyFiatListIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputOneFiatInListIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, ['USD'])


    def test_parseFiatDataFromInputThreeFiatInListIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd-chf-eur] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, ['USD', 'CHF', 'EUR'])


    def test_parseFiatDataFromInputThreeFiatInListNoFiatSepCharIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd chf] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, ['CHF'])


    def test_parseFiatDataFromInputNoFiatListIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputEmptyFiatListNoOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] []"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputNoFiatListNoOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153]"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, [])


    def test_parseCryptoDataFromInputIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputNoOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputNoCryptoSymbolNoOtherCommand(self):
        inputStr = "oo [5/7 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)
        self.assertEqual("Error in input oo [5/7 0.0015899 6/7 0.00153] [usd-chf]: crypto symbol missing !", self.commandError.execute())


    def test_parseCryptoDataFromInputNoCryptoSymbolOtherCommand(self):
        inputStr = "oo [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)


    def test_parseCryptoDataFromInputOnePriceOnlyNoOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyOtherCommand(self):
        inputStr = "oo [btc 5/7 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '5/7', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyNoDateNoOtherCommand(self):
        inputStr = "oo [btc 0.0015899] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, '')


    def test_parseCryptoDataFromInputOnePriceOnlyNoDateOtherCommand(self):
        inputStr = "oo [btc 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, '')


    def test_parseCryptoDataFromInputOneDateMissingIncludeOtherCommand(self):
        inputStr = "oo [btc 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOneDateMissingNoOtherCommand(self):
        inputStr = "oo [btc 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOnePriceMissingIncludeOtherCommand(self):
        inputStr = "oo [btc 5/7 6/7 0.00153] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOnePriceMissingNoOtherCommand(self):
        inputStr = "oo [btc 5/7 6/7 0.00153] [usd-chf]"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '6/7', '0.00153'])


    def test_parseCryptoDataFromInputOnePriceTwoDigitsDateOnlyOtherCommand(self):
        inputStr = "oo [btc 15/12 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '15/12', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceTwoDigitsWithZeroesDateOnlyOtherCommand(self):
        inputStr = "oo [btc 05/02 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, ['BTC', '05/02', '0.0015899'])


    def test_parseCryptoDataFromInputOnePriceOnlyZeroesInDateOtherCommandFiatListFirstPos(self):
        inputStr = "oo [05/07 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)
        self.assertEquals("Error in input oo [05/07 0.0015899] [usd-chf] -nosave: crypto symbol missing !", self.commandError.execute())


    def test_parseCryptoDataFromInputOnePriceOnlyZeroesInDateOtherCommandFiatListFirstPos(self):
        inputStr = "oo [usd-chf] [btc 05/07 0.0015899] -nosave"
        cryptoData = self.requester._parseCryptoDataFromInput(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)
        self.assertEquals("Error in input oo [usd-chf] [btc 05/07 0.0015899] -nosave: crypto symbol missing !", self.commandError.execute())


    def test_getUserCommandCommandMissingOtherCommand(self):
        inputStr = "[btc 05/07 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._getUserCommand(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)
        self.assertEquals("Error in input [btc 05/07 0.0015899] [usd-chf] -nosave: user command missing !", self.commandError.execute())


if __name__ == '__main__':
    unittest.main()