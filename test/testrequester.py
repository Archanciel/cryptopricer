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


    def test_parseFiatTwoFiatsNoFiatSep(self):
        inputStr = "[usd chf]"
        fiatList = self.requester._parseFiat(inputStr.upper())
        self.assertEqual(fiatList, ['CHF'])


    def test_parseFiatTwoFiats(self):
        inputStr = "[usd-chf]"
        fiatList = self.requester._parseFiat(inputStr.upper())
        self.assertEqual(fiatList, ['USD', 'CHF'])


    def test_parseFiatEmptyFiatList(self):
        inputStr = "[]"
        fiatList = self.requester._parseFiat(inputStr.upper())
        self.assertEqual(fiatList, [])


    def test_parseFiatOneFiat(self):
        inputStr = "[usd]"
        fiatList = self.requester._parseFiat(inputStr.upper())
        self.assertEqual(fiatList, ['USD'])


    def test_parseFiatThreeFiats(self):
        inputStr = "[usd-chf-eur]"
        fiatList = self.requester._parseFiat(inputStr.upper())
        self.assertEqual(fiatList, ['USD', 'CHF', 'EUR'])


    def test_parseFiatNoFiatList(self):
        inputStr = ""
        fiatList = self.requester._parseFiat(inputStr.upper())
        self.assertEqual(fiatList, [])


    def test_getUserCommandCommandMissingOtherCommand(self):
        inputStr = "[btc 05/07 0.0015899] [usd-chf] -nosave"
        cryptoData = self.requester._getUserCommand(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)
        self.assertEquals("Error in input [btc 05/07 0.0015899] [usd-chf] -nosave: user command missing !", self.commandError.execute())


    def test_parseDatePriceTwoPairs(self):
        inputStr = "[5/7 0.0015899 6/7 0.00153]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, ['5/7', '0.0015899', '6/7', '0.00153'])


    def test_parseDatePriceOnePair(self):
        inputStr = "[5/7 0.0015899]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, ['5/7', '0.0015899'])


    def test_parseDatePriceOnePriceOnlyNoDateNoOtherCommand(self):
        inputStr = "[btc 0.0015899] [usd-chf]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, [])


    def test_parseDatePriceOnePriceNoDateOtherCommand(self):
        inputStr = "[0.0015899]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, [])


    def test_parseDatePriceOneDateMissing(self):
        inputStr = "[0.0015899 6/7 0.00153]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, ['6/7', '0.00153'])


    def test_parseDatePriceOnePriceMissing(self):
        inputStr = "[5/7 6/7 0.00153]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, ['6/7', '0.00153'])


    def test_parseDatePriceOnePriceTwoDigitsDateOnlyOtherCommand(self):
        inputStr = "[15/12 0.0015899]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, ['15/12', '0.0015899'])


    def test_parseDatePriceOnePriceTwoDigitsWithZeroeDate(self):
        inputStr = "[05/02 0.0015899]"
        datePriceList = self.requester._parseDatePrice(inputStr.upper())
        self.assertEqual(datePriceList, ['05/02', '0.0015899'])






    def test_parseFiatDataFromInputNoFiatListIncludeOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] -nosave"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, [])


    def test_parseFiatDataFromInputEmptyFiatListNoOtherCommand(self):
        inputStr = "[btc 5/7 0.0015899 6/7 0.00153] []"
        fiatData = self.requester._parseFiatDataFromInput(inputStr.upper())
        self.assertEqual(fiatData, [])


    def test_parseOOCommandParmsFiatListMissingNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153]"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        self.assertEquals("Error in input btc [5/7 0.0015899 6/7 0.00153]: invalid command parm data format !", self.commandError.execute())


    def test_parseOOCommandParmsFiatListMissingWithOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] -nosave"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        self.assertEquals("Error in input btc [5/7 0.0015899 6/7 0.00153] -nosave: invalid command parm data format !", self.commandError.execute())


    def test_parseOOCommandParms(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(fiatDataList, ['USD', 'CHF'])
        self.assertEqual(flag, '-NOSAVE')


    def test_parseOOCommandParmsNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(fiatDataList, ['USD', 'CHF'])
        self.assertEqual(flag, None)


    def test_parseOOCommandParmsEmptyFiatListNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] []"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(fiatDataList, [])
        self.assertEqual(flag, None)













if __name__ == '__main__':
    unittest.main()