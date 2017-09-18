import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requester import Requester
from commandprice import CommandPrice
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
        self.commandPrice = CommandPrice(None)
        requester.commandPrice = self.commandPrice
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
        cryptoData = self.requester._getCommand(inputStr, inputStr.upper())
        self.assertEqual(cryptoData, self.commandError)
        self.assertEqual("Error in input [btc 05/07 0.0015899] [usd-chf] -nosave: user command missing !", self.commandError.execute())


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


    def test_parseOOCommandParmsFiatListMissingNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153]"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        self.assertEqual("Error in input btc [5/7 0.0015899 6/7 0.00153]: fiat list missing !", self.commandError.execute())


    def test_parseOOCommandParmsFiatListMissingWithOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] -nosave"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        self.assertEqual("Error in input btc [5/7 0.0015899 6/7 0.00153] -nosave: fiat list missing !", self.commandError.execute())


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


    def test_getCommand(self):
        inputStr = "oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoCommand = self.requester._getCommand(inputStr, inputStr.upper())

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.FIAT_LIST], ['USD', 'CHF'])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')


    def testRequestOOCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave")
        cryptoCommand = self.requester.request()

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.FIAT_LIST], ['USD', 'CHF'])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')


        sys.stdin = stdin


    def testRequestOOCommandNoFlag(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf]")
        cryptoCommand = self.requester.request()

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.FIAT_LIST], ['USD', 'CHF'])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], None)

        sys.stdin = stdin


    def testRequestOOCommandEmptyFiat(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [] -nosave")
        cryptoCommand = self.requester.request()

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.FIAT_LIST], [])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')

        sys.stdin = stdin


    def testRequestOOCommandNoFiat(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] -nosave")
        command = self.requester.request()

        self.assertIsInstance(command, CommandError)

        sys.stdin = stdin


    def testRequestUserCommandNoCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc [5/7 0.0015899 6/7 0.00153] -nosave")
        command = self.requester.request()

        #now that you changed command price full pattern to render all parms except the first one optional,
        #this input is interpreted as a CommandPrice
        self.assertIsInstance(command, CommandPrice)

        sys.stdin = stdin


    def test_parseGroupsFullDayMonthHHMM(self):
        inputStr = "btc usd 10/9 12:45 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken'), groupList)


    def test_parseGroupsFullDayMonthYearHMM(self):
        inputStr = "btc usd 10/9/17 1:45 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9/17', '1:45', 'Kraken'), groupList)


    def test_parseGroupsFullDH(self):
        inputStr = "btc usd 1 2 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '1', '2', 'Kraken'), groupList)


    def test_parseGroupsFullDDDMH(self):
        inputStr = "btc usd 111/9 2 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '111/9', '2', 'Kraken'), groupList)


    def test_parseGroupsFullDMH(self):
        inputStr = "btc usd 1/9 2 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '1/9', '2', 'Kraken'), groupList)


    def test_parseGroupsFullDayHH(self):
        inputStr = "btc usd 10 12 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10', '12', 'Kraken'), groupList)


    def test_parseGroupsFullDMYearHMM(self):
        inputStr = "btc usd 1/2/17 1:25 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', 'usd', '1/2/17', '1:25', 'Kraken'), groupList)


    def test_parseGroupsFullDHH(self):
        inputStr = "btc usd 1 12 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', 'usd', '1', '12', 'Kraken'), groupList)


    def test_parseGroupsFullDMHHMMNoExchange(self):
        inputStr = "btc usd 1/9 12:05"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', 'usd', '1/9', '12:05', None), groupList)


    def test_parseGroupsFullNoFiatDMHHMMNoExchange(self):
        inputStr = "btc 1/9 12:05"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', '1/9', '12:05', None, None), groupList)


    def test_parseGroupsFullNoFiatDMNoTimeNoExchange(self):
        inputStr = "btc 1/9"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', '1/9', None, None, None), groupList)


    def test_parseGroupsFullNoFiatNoDateNoTimeNoExchange(self):
        inputStr = "btc"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthHHMM(self):
        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8', '-t', '22:46', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDayMonthYearHMM(self):
        inputStr = "-ceth -fgbp -d11/8/17 -t2:46 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8/17', '-t', '2:46', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDayMonthYearHHMM(self):
        inputStr = "-ceth -fgbp -d11/8/17 -t12:46 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8/17', '-t', '12:46', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDH(self):
        inputStr = "-ceth -fgbp -d1 -t2 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1', '-t', '2', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDHH(self):
        inputStr = "-ceth -fgbp -d1 -t2:5 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1', '-t', '2:5', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDayHH(self):
        inputStr = "-ceth -fgbp -d11 -t22 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11', '-t', '22', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDMHH(self):
        inputStr = "-ceth -fgbp -d1/2 -t22 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1/2', '-t', '22', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDDDMHH(self):
        inputStr = "-ceth -fgbp -d110/2 -t22 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken'), groupList)


    def test_parseGroupsPartialDayMonthHHMMNoExchange(self):
        inputStr = "-ceth -fgbp -d11/8 -t22:46"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8', '-t', '22:46', None, None), groupList)


    def test_parseGroupsPartialDayMonthNoTimeNoExchange(self):
        inputStr = "-ceth -fgbp -d11/8"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8', None, None, None, None), groupList)


    def test_parseGroupsPartialNoDateNoTimeNoExchange(self):
        inputStr = "-ceth -fgbp"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoFiatNoDateNoTimeNoExchange(self):
        inputStr = "-ceth"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoCryptoNoDateNoTimeNoExchange(self):
        inputStr = "-fgbp"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-f', 'gbp', None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoCryptoNoDateNoExchange(self):
        inputStr = "-fgbp -t3:45"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-f', 'gbp', '-t', '3:45', None, None, None, None, None, None), groupList)


    def test_parseAndFillFullCommandPrice(self):
        inputStr = "btc usd 10/9/17 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceNoYear(self):
        inputStr = "btc usd 10/9 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceNoYearNoExchange(self):
        inputStr = "btc usd 10/9 12:45"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceNoTimeNoYearNoExchange(self):
        inputStr = "btc usd 10/9"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceNoDateNoTimeNoExchange(self):
        inputStr = "btc usd"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceNoFiatNoDateNoTimeNoExchange(self):
        inputStr = "btc"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceNoInitYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercase(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-Ceth -Fgbp -D11/8 -T22:46 -EKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceWithInitYearWithPartialYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '17'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8/16 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceNoInitYearNoExchange(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8 -t22:46"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceNoInitYearNoExchangeNoTime(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceNoInitYearNoExchangeNoMinute(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8 -t5"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '5')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillPartialCommandPriceWithInitYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def testRequestPriceCommandFull(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        sys.stdin = stdin


    def testRequestPriceCommandPartialCryptoExchange(self):
        #first, enter full command price
        stdin = sys.stdin
        sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        #then, enter partial command price
        sys.stdin = StringIO("-cbtc -eKraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        sys.stdin = stdin


    def testRequestPriceCommandPartialDate(self):
        # first, enter full command price
        stdin = sys.stdin
        sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        # then, enter partial command price
        sys.stdin = StringIO("-d10/9")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        sys.stdin = stdin


    def testRequestPriceCommandPartialFiatTime(self):
        # first, enter full command price
        stdin = sys.stdin
        sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        # then, enter partial command price
        sys.stdin = StringIO("-fusd -t0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        sys.stdin = stdin


if __name__ == '__main__':
    unittest.main()