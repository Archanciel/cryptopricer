import unittest
import os,sys,inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requester import Requester
from configurationmanager import ConfigurationManager
from commandprice import CommandPrice
from commandcrypto import CommandCrypto
from commandquit import CommandQuit
from commanderror import CommandError
from resultdata import ResultData


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
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)

        requester = Requester(configMgr)
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
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid request [btc 05/07 0.0015899] [usd-chf] -nosave: user command missing", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def testGetCommandInvalidC(self):
        inputStr = "-c"
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -c", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def testGetCommandInvalidF(self):
        inputStr = "-f"
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -f", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def testGetCommandInvalidD(self):
        inputStr = "-d"
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -d", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def testGetCommandInvalidT(self):
        inputStr = "-t"
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -t", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def testGetCommandInvalidE(self):
        inputStr = "-e"
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -e", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


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
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid request : fiat list missing", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def test_parseOOCommandParmsFiatListMissingWithOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] -nosave"
        cryptoDataList, fiatDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid request : fiat list missing", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


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


    def testGetCommand(self):
        inputStr = "oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoCommand = self.requester.getCommand(inputStr)

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
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken', None, None), groupList)


    def test_parseGroupsFullExchangeFirst(self):
        inputStr = "btc usd Kraken 10/9/17 12:45"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', 'Kraken', '10/9/17', '12:45', None, None), groupList)


    def test_parseGroupsFullDayMonthYearHMM(self):
        inputStr = "btc usd 10/9/2017 1:45 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9/2017', '1:45', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDayMonthZeroYearHMM(self):
        inputStr = "btc usd 10/9/0 1:45 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9/0', '1:45', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDH(self):
        inputStr = "btc usd 1 2 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '1', '2', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDDDMH(self):
        inputStr = "btc usd 111/9 2 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '111/9', '2', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDMH(self):
        inputStr = "btc usd 1/9 2 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '1/9', '2', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDayHH(self):
        inputStr = "btc usd 10 12 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10', '12', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDMYearHMM(self):
        inputStr = "btc usd 1/2/17 1:25 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', 'usd', '1/2/17', '1:25', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDHH(self):
        inputStr = "btc usd 1 12 Kraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', 'usd', '1', '12', 'Kraken', None, None), groupList)


    def test_parseGroupsFullDMHHMMNoExchange(self):
        inputStr = "btc usd 1/9 12:05"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', 'usd', '1/9', '12:05', None, None, None), groupList)


    def test_parseGroupsFullNoFiatDMHHMMNoExchange(self):
        inputStr = "btc 1/9 12:05"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', '1/9', '12:05', None, None, None, None), groupList)


    def test_parseGroupsFullNoFiatDMNoTimeNoExchange(self):
        inputStr = "btc 1/9"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', '1/9', None, None, None, None, None), groupList)


    def test_parseGroupsFullNoFiatNoDateNoTimeNoExchange(self):
        inputStr = "btc"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', None, None, None, None, None, None), groupList)

    def test_buildFullCommandPriceOptionalParmsDic(self):
        '''
        ° 0 is legal for date, not for time parms. Zero for either date means now, real time !
        ° Date must be 0 or contain a '/'.
        ° Time must be composed of two numerical groups separated by ':', the second group being a
        ° 2 digits group. Note 00:00 or 0:00 does not mean now, but midnight !
        ° Exchange name must start with a letter. May contain digits.

        Ex:
        Date can be 0, accepted. 1, rejected. 10, rejected. 01, rejected. 01/1, accepted.
                    01/10, accepted. 1/1, accepted. 1/10, accepted. 01/12/16, accepted.
                    01/12/2015, accepted.
        Hour minute can be 0, rejected. 1, rejected. 10, rejected. 01, rejected. 01:1, rejected.
                           01:01, accepted.
                           01:10, accepted. 1:10, accepted. 00:00, accepted. 0:00, accepted. 0:0, rejected.
         '''
        optionalParmList = ['01:10', 'Kraken', '10/9/17']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10/9/17')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '01:10')
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'Kraken')

        optionalParmList = ['1', 'kraken', '10/9/2017']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10/9/2017')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['1', 'kraken', '1']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertNotIn(CommandPrice.DAY_MONTH_YEAR, optionalParmDic)
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['kraken', '0', '10:12']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '10:12')
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['kraken', '0', '1']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = [ '1', 'kraken', '0']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['10', '10:09']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertNotIn(CommandPrice.DAY_MONTH_YEAR, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '10:09')

        optionalParmList = ['01', '1:09']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertNotIn(CommandPrice.DAY_MONTH_YEAR, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '1:09')

        optionalParmList = ['01/1', '00:00']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '01/1')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '00:00')

        optionalParmList = ['1/1', '00:00']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/1')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '00:00')

        optionalParmList = ['1/10', '0:00']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/10')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '0:00')

        optionalParmList = ['1/10', '0:0']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/10')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)

    def test_buildFullCommandPriceOptionalParmsDicExoticExchangeName(self):
        optionalParmList = [ '1', 'BTC38', '0']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'BTC38')

        optionalParmList = ['1', 'Bit2C', '0']
        optionalParmDic = self.requester._buildFullCommandPriceOptionalParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'Bit2C')

    def test_parseGroupsPartialDDZeroMonth(self):
        inputStr = "-ceth -fgbp -d11/0 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)

    def test_parseGroupsPartialDayZeroMonth(self):
        inputStr = "-ceth -fgbp -d1/0 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)

    def test_parseGroupsPartialZeroDayZeroMonth(self):
        inputStr = "-ceth -fgbp -d0/0 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '0/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)

    def test_parseGroupsPartialDayMonthHHMM(self):
        inputStr = "-ceth -fgbp -d11/8 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthYearHMM(self):
        inputStr = "-ceth -fgbp -d11/8/17 -t2:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8/17', '-t', '2:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthYearHHMM(self):
        inputStr = "-ceth -fgbp -d11/8/17 -t12:46 -ebtc38 -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8/17', '-t', '12:46', '-e', 'btc38', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthZeroYearHHMM(self):
        inputStr = "-ceth -fgbp -d11/8/0 -t12:46 -ebtc38 -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8/0', '-t', '12:46', '-e', 'btc38', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDH(self):
        inputStr = "-ceth -fgbp -d1 -t2 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1', '-t', '2', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDHH(self):
        inputStr = "-ceth -fgbp -d1 -t2:5 -ebit2c -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1', '-t', '2:5', '-e', 'bit2c', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayHH(self):
        inputStr = "-ceth -fgbp -d11 -t22 -eKraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11', '-t', '22', '-e', 'Kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDMHH(self):
        inputStr = "-ceth -fgbp -d1/2 -t22 -eKraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '1/2', '-t', '22', '-e', 'Kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDDDMHHValue(self):
        inputStr = "-ceth -fgbp -d110/2 -t22 -eKraken -v0.0044235btc"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-v', '0.0044235btc', None, None, None, None), groupList)


    def test_parseGroupsPartialDDDMHHNoValue(self):
        inputStr = "-ceth -fgbp -d110/2 -t22 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthHHMMNoExchangeNoValue(self):
        inputStr = "-ceth -fgbp -d11/8 -t22:46"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8', '-t', '22:46', None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthNoTimeNoExchangeNoValue(self):
        inputStr = "-ceth -fgbp -d11/8"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', '-d', '11/8', None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoDateNoTimeNoExchangeNoValue(self):
        inputStr = "-ceth -fgbp"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-f', 'gbp', None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoFiatNoDateNoTimeNoExchangeNoValue(self):
        inputStr = "-ceth"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoCryptoNoDateNoTimeNoExchangeNoValue(self):
        inputStr = "-fgbp"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-f', 'gbp', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialValueFloatNoCryptoNoFiatNoDateNoTimeNoExchange(self):
        inputStr = "-v700.05usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-v', '700.05usd', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialValueIntNoCryptoNoFiatNoDateNoTimeNoExchange(self):
        inputStr = "-v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-v', '700usd', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoCryptoNoDateNoExchangeNoValue(self):
        inputStr = "-fgbp -t3:45"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-f', 'gbp', '-t', '3:45', None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseAndFillFullCommandPrice(self):
        inputStr = "btc usd 10/9/2017 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceInvalDate1(self):
        inputStr = "btc usd 1 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceInvalDate2(self):
        inputStr = "btc usd 10 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceInvalDate3(self):
        inputStr = "btc usd 01 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceInvalMonthAccepted(self):
        inputStr = "btc usd 01/0 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceInvalDayAccepted(self):
        inputStr = "btc usd 0/0 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceValidDate1(self):
        inputStr = "btc usd 01/1 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '1')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceValidDate2(self):
        inputStr = "btc usd 1/01 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '01')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceValidDate3(self):
        inputStr = "btc usd 1/1 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '1')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceValidDate4(self):
        inputStr = "btc usd 1/10 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '10')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceValidDate5(self):
        inputStr = "btc usd 01/10 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '10')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDate(self):
        #means current date !
        inputStr = "btc usd 0 2:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '2')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime1(self):
        #means current date !
        inputStr = "btc usd 0 2:4 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime2(self):
        #means current date !
        inputStr = "btc usd 0 2: Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime3(self):
        #means current date !
        inputStr = "btc usd 0 20 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime4(self):
        #means current date !
        inputStr = "btc usd 0 2 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime5(self):
        #means current date !
        inputStr = "btc usd 0 01 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime6(self):
        #means current date !
        inputStr = "btc usd 0 10 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime7(self):
        inputStr = "btc usd 10/9/2017 01:1 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateInvalidTime8(self):
        inputStr = "btc usd 10/9/2017 0:0 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateValidTime1(self):
        inputStr = "btc usd 10/9/2017 00:00 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '00')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '00')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateValidTime2(self):
        inputStr = "btc usd 10/9/2017 0:00 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '00')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceDateBeforeZeroTime(self):
        inputStr = "btc usd 10/9/17 0 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroTimeBeforeDate(self):
        #zero time is rejected. Instead, it is interrpreted as date == 0
        #means current date !
        inputStr = "btc usd 0 10/9/17 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceZeroDateZeroTime(self):
        #first zero means current date. Second zero for 0 time is not acceptable for time !
        inputStr = "btc usd 0 0 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceExchangeBeforeDateTime(self):
        inputStr = "btc usd Kraken 10/9/17 12:45"
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


    def test_parseAndFillFullCommandPriceNoYearTimeBeforeDate(self):
        inputStr = "btc usd Kraken 12:45 10/9"
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


    def test_parseAndFillPartialCommandPriceNoInitYearThenPriceValue(self):
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

        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken -v0.0044256btc"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercasePriceValue(self):
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

        inputStr = "-V0.0044256btc -Ceth -Fgbp -D11/8 -T22:46 -EKraken"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearPriceValue(self):
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

        inputStr = "-ceth -v500gbp -fgbp -d11/8/15 -t22:46 -eKraken"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'gbp')
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPricePriceValuePreviouslySet(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'

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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'gbp')
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceErasePriceValue(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'

        inputStr = "-ceth -v0 -fgbp -d11/8/15 -t22:46 -eKraken"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceIneffectivePriceValueSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.PRICE_VALUE_SAVE] = False

        inputStr = "-ceth -v -fgbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SAVE], False)


    def test_parseAndFillPartialCommandPriceInvalidPriceValueSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])

        inputStr = "-ceth -vooo -fgbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : in -vooo, ooo must respect 99.99999zzz <price><symbol> format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def test_parseAndFillPartialCommandPriceNoInitYearThenPriceValueSave(self):
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

        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken -vs0.0044256btc"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SAVE], True)


    def test_parseAndFillPartialCommandPriceNoInitYearThenPriceValueSaveAndUnsupportedCommand(self):
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

        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken -vs0.0044256btc -zunsupported"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND], '-z')
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA], 'unsupported')


    def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercasePriceValueSave(self):
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

        inputStr = "-VS0.0044256btc -Ceth -Fgbp -D11/8 -T22:46 -EKraken"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SAVE], True)


    def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearPriceValueSave(self):
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

        inputStr = "-ceth -vs500gbp -fgbp -d11/8/15 -t22:46 -eKraken"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SAVE], True)


    def test_parseAndFillPartialCommandPricePriceValueSavePreviouslySet(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.PRICE_VALUE_SAVE] = True

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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SAVE], True)


    def test_parseAndFillPartialCommandPriceErasePriceValueSave(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.PRICE_VALUE_SAVE] = True

        inputStr = "-ceth -v0 -fgbp -d11/8/15 -t22:46 -eKraken"
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceIneffectivePriceValueSaveSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.PRICE_VALUE_SAVE] = False

        inputStr = "-ceth -vs -fgbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : in -vs, s must respect 99.99999zzz <price><symbol> format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def test_parseAndFillPartialCommandPriceInvalidPriceValueSaveSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
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
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.PRICE_VALUE_SAVE] = True

        inputStr = "-ceth -vsooo -fgbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : in -vsooo, sooo must respect 99.99999zzz <price><symbol> format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceWithInitYearNoPartialYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.FIAT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '15'
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
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceWithInitYearWithPartialDateDayOnly(self):
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

        inputStr = "-ceth -fgbp -d11 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


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
        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : in -t5, 5 must respect HH:mm format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def test_parseAndFillPartialCommandPriceNoInitYearNoMinuteInvalidTime(self):
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

        inputStr = "-ceth -ebittrex -t6.45 -d21/12"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : in -t6.45, 6.45 must respect HH:mm format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


    def test_parseAndFillPartialCommandPriceWrongCommand(self):
        commandError = self.requester.commandPrice

        parsedParmData = commandError.parsedParmData

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

        inputStr = "-ceth -fgbp -d11/8 -h22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND], '-h')
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA], '22:46')

        # formatting of request input string has been moved to end of Requester.getCommand !


    def test_parseAndFillPartialCommandPriceCommandNoHiphen(self):
        commandError = self.requester.commandPrice

        parsedParmData = commandError.parsedParmData

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
        parsedParmData[CommandPrice.PRICE_VALUE_DATA] = None
        parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT] = None
        parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL] = None

        inputStr = "-ceth fgbp -d11/8 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])


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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])

        sys.stdin = stdin


    def testRequestPriceCommandFullEndingWithPriceValueCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0.01btc")
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.01')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])

        sys.stdin = stdin


    def testRequestPriceCommandFullEndingWithPriceValueSaveCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01btc")
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.01')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertIsNotNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])

        sys.stdin = stdin


    def testRequestPriceCommandFullEndingWithPriceValueSaveCommandAndUnsupportedCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01btc -zunsupported")
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.01')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertIsNotNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND], '-z')
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA], 'unsupported')

        sys.stdin = stdin


    def testRequestPriceCommandFullEndingWithPriceUnsupportedCommandAndValueSaveCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -zunsupported -vs0.01btc")
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
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], '0.01')
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], 'btc')
        self.assertIsNotNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND], '-z')
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA], 'unsupported')

        sys.stdin = stdin


    def testRequestPriceCommandFullWithPriceValueCommandInInvalidPosThree(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -v0.01btc 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd -v0.01btc 10/9/17 12:45 Kraken violates format <crypto> <fiat> <date|time> <exchange> <opt commands>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def testRequestPriceCommandFullWithPriceValueCommandInInvalidPosFour(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 -v0.01btc 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd 10/9/17 -v0.01btc 12:45 Kraken violates format <crypto> <fiat> <date|time> <exchange> <opt commands>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def testRequestPriceCommandFullWithPriceValueCommandInInvalidPosFive(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 -v0.01btc Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd 10/9/17 12:45 -v0.01btc Kraken violates format <crypto> <fiat> <date|time> <exchange> <opt commands>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def testRequestPriceCommandFullWithPriceValueSaveCommandInInvalidPosThree(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -vs0.01btc 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd -vs0.01btc 10/9/17 12:45 Kraken violates format <crypto> <fiat> <date|time> <exchange> <opt commands>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def testRequestPriceCommandFullWithPriceValueSaveCommandInInvalidPosThreeAndUnsupportedCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -vs0.01btc 10/9/17 12:45 Kraken -zunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd -vs0.01btc 10/9/17 12:45 Kraken -zunsupported violates format <crypto> <fiat> <date|time> <exchange> <opt commands>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def testRequestPriceCommandFullWithPriceValueSaveCommandInInvalidPosFour(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 -vs0.01btc 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd 10/9/17 -vs0.01btc 12:45 Kraken violates format <crypto> <fiat> <date|time> <exchange> <opt commands>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithPriceValueSaveCommandInInvalidPosFive(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 -vs0.01btc Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd 10/9/17 12:45 -vs0.01btc Kraken violates format <crypto> <fiat> <date|time> <exchange> <opt commands>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def testRequestPriceCommandFullDateZero(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])

        sys.stdin = stdin


    def testRequestPriceCommandFullDateBeforeTimeZero(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/2017 0 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])

        sys.stdin = stdin


    def testRequestPriceCommandFullTimeZeroBeforeDate(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 10/9/2017 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.PRICE_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.PRICE_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_COMMAND_DATA])

        sys.stdin = stdin


    def testRequestPriceCommandFullDateZeroTimeZero(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 0 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        sys.stdin = stdin


    def testRequestPriceCommandFullDateZeroNoTime(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
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


    def testRequestPriceCommandPartialDateZeroMeansCurent(self):
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
        sys.stdin = StringIO("-d0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.FIAT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
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
        sys.stdin = StringIO("-fusd -t0:15")
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
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '15')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        sys.stdin = stdin


    def testRequestPriceCommandPartialFiatTimeZeroRejected(self):
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

        # then, enter partial command price. -t0 means we want current price
        sys.stdin = StringIO("-fusd -t0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -fusd -t0: in -t0, 0 must respect HH:mm format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin


    def runTests(self):
        unittest.main()
        

if __name__ == '__main__':
    unittest.main()