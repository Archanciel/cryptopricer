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
    -teste input crypto + unit avec ou sans
    nosave ou ns
    
    -teste input crypto avec 0 price/oate,
    1 price/date, n price/date
    
    -idem 0, 1, n units
    
    -varie order crypto list/unit list/
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


    def test_parseUnitTwoUnitsNoUnitSep(self):
        inputStr = "[usd chf]"
        unitList = self.requester._parseUnit(inputStr.upper())
        self.assertEqual(unitList, ['CHF'])


    def test_parseUnitTwoUnits(self):
        inputStr = "[usd-chf]"
        unitList = self.requester._parseUnit(inputStr.upper())
        self.assertEqual(unitList, ['USD', 'CHF'])


    def test_parseUnitEmptyUnitList(self):
        inputStr = "[]"
        unitList = self.requester._parseUnit(inputStr.upper())
        self.assertEqual(unitList, [])


    def test_parseUnitOneUnit(self):
        inputStr = "[usd]"
        unitList = self.requester._parseUnit(inputStr.upper())
        self.assertEqual(unitList, ['USD'])


    def test_parseUnitThreeUnits(self):
        inputStr = "[usd-chf-eur]"
        unitList = self.requester._parseUnit(inputStr.upper())
        self.assertEqual(unitList, ['USD', 'CHF', 'EUR'])


    def test_parseUnitNoUnitList(self):
        inputStr = ""
        unitList = self.requester._parseUnit(inputStr.upper())
        self.assertEqual(unitList, [])


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
        inputStr = "-u"
        cryptoData = self.requester.getCommand(inputStr)
        self.assertEqual(cryptoData, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -u", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


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


    def test_parseOOCommandParmsUnitListMissingNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153]"
        cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid request : unit list missing", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def test_parseOOCommandParmsUnitListMissingWithOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] -nosave"
        cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid request : unit list missing", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))


    def test_parseOOCommandParms(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(unitDataList, ['USD', 'CHF'])
        self.assertEqual(flag, '-NOSAVE')


    def test_parseOOCommandParmsNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] [usd-chf]"
        cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(unitDataList, ['USD', 'CHF'])
        self.assertEqual(flag, None)


    def test_parseOOCommandParmsEmptyUnitListNoOtherCommand(self):
        inputStr = "btc [5/7 0.0015899 6/7 0.00153] []"
        cryptoDataList, unitDataList, flag = self.requester._parseOOCommandParms(inputStr, inputStr.upper())
        self.assertEqual(cryptoDataList, ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(unitDataList, [])
        self.assertEqual(flag, None)


    def testGetCommand(self):
        inputStr = "oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave"
        cryptoCommand = self.requester.getCommand(inputStr)

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], ['USD', 'CHF'])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')


    def testRequestOOCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf] -nosave")
        cryptoCommand = self.requester.request()

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], ['USD', 'CHF'])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')

        sys.stdin = stdin


    def testRequestOOCommandNoFlag(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [usd-chf]")
        cryptoCommand = self.requester.request()

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], ['USD', 'CHF'])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], None)

        sys.stdin = stdin


    def testRequestOOCommandEmptyUnit(self):
        stdin = sys.stdin
        sys.stdin = StringIO("oo btc [5/7 0.0015899 6/7 0.00153] [] -nosave")
        cryptoCommand = self.requester.request()

        self.assertIsInstance(cryptoCommand, CommandCrypto)
        parsedParmData = cryptoCommand.parsedParmData
        self.assertEqual(parsedParmData[cryptoCommand.CRYPTO_LIST], ['BTC', '5/7', '0.0015899', '6/7', '0.00153'])
        self.assertEqual(parsedParmData[cryptoCommand.UNIT_LIST], [])
        self.assertEqual(parsedParmData[cryptoCommand.FLAG], '-NOSAVE')

        sys.stdin = stdin


    def testRequestOOCommandNoUnit(self):
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

    def test_parseGroupsFullDayMonthHHMMValueOption(self):
        inputStr = "btc usd 10/9 12:45 Kraken -v100usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken', '-v100usd', None), groupList)

    def test_parseGroupsFullDayMonthHHMMValueOptionIncomplete(self):
        inputStr = "btc usd 10/9 12:45 Kraken -v100"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'usd', '10/9', '12:45', 'Kraken', '-v100', None), groupList)

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


    def test_parseGroupsFullNoUnitDMHHMMNoExchange(self):
        inputStr = "btc 1/9 12:05"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', '1/9', '12:05', None, None, None, None), groupList)


    def test_parseGroupsFullNoUnitDMNoTimeNoExchange(self):
        inputStr = "btc 1/9"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)
        self.assertEqual(('btc', '1/9', None, None, None, None, None), groupList)


    def test_parseGroupsFullNoUnitNoDateNoTimeNoExchange(self):
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
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10/9/17')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '01:10')
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'Kraken')

        optionalParmList = ['1', 'kraken', '10/9/2017']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
#        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10/9/2017')
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['1', 'kraken', '1']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['kraken', '0', '10:12']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '10:12')
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['kraken', '0', '1']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = [ '1', 'kraken', '0']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'kraken')

        optionalParmList = ['10', '10:09']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '10')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '10:09')

        optionalParmList = ['01', '1:09']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '01')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '1:09')

        optionalParmList = ['01/1', '00:00']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '01/1')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '00:00')

        optionalParmList = ['1/1', '00:00']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/1')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '00:00')

        optionalParmList = ['1/10', '0:00']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/10')
        self.assertEqual(optionalParmDic[CommandPrice.HOUR_MINUTE], '0:00')

        optionalParmList = ['1/10', '0:0']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1/10')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)

    def test_buildFullCommandPriceOptionalParmsDicExoticExchangeName(self):
        optionalParmList = [ '1', 'BTC38', '0']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
#        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '0')
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'BTC38')

        optionalParmList = ['1', 'Bit2C', '0']
        optionalParmDic = self.requester._buildFullCommandPriceOrderFreeParmsDic(optionalParmList)
        self.assertEqual(optionalParmDic[CommandPrice.DAY_MONTH_YEAR], '1')
        self.assertNotIn(CommandPrice.HOUR_MINUTE, optionalParmDic)
        self.assertEqual(optionalParmDic[CommandPrice.EXCHANGE], 'Bit2C')

    def test_parseGroupsPartialDDZeroMonth(self):
        inputStr = "-ceth -ugbp -d11/0 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)

    def test_parseGroupsPartialDayZeroMonth(self):
        inputStr = "-ceth -ugbp -d1/0 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)

    def test_parseGroupsPartialZeroDayZeroMonth(self):
        inputStr = "-ceth -ugbp -d0/0 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '0/0', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)

    def test_parseGroupsPartialDayMonthHHMM(self):
        inputStr = "-ceth -ugbp -d11/8 -t22:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8', '-t', '22:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthYearHMM(self):
        inputStr = "-ceth -ugbp -d11/8/17 -t2:46 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8/17', '-t', '2:46', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthYearHHMM(self):
        inputStr = "-ceth -ugbp -d11/8/17 -t12:46 -ebtc38 -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8/17', '-t', '12:46', '-e', 'btc38', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthZeroYearHHMM(self):
        inputStr = "-ceth -ugbp -d11/8/0 -t12:46 -ebtc38 -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8/0', '-t', '12:46', '-e', 'btc38', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDH(self):
        inputStr = "-ceth -ugbp -d1 -t2 -ekraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1', '-t', '2', '-e', 'kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDHH(self):
        inputStr = "-ceth -ugbp -d1 -t2:5 -ebit2c -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1', '-t', '2:5', '-e', 'bit2c', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDayHH(self):
        inputStr = "-ceth -ugbp -d11 -t22 -eKraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11', '-t', '22', '-e', 'Kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDMHH(self):
        inputStr = "-ceth -ugbp -d1/2 -t22 -eKraken -v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '1/2', '-t', '22', '-e', 'Kraken', '-v', '700usd', None, None, None, None), groupList)


    def test_parseGroupsPartialDDDMHHValue(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -v0.0044235btc"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-v', '0.0044235btc', None, None, None, None), groupList)


    def test_parseGroupsPartialDDDMHHNoValue(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthHHMMNoExchangeNoValue(self):
        inputStr = "-ceth -ugbp -d11/8 -t22:46"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8', '-t', '22:46', None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialDayMonthNoTimeNoExchangeNoValue(self):
        inputStr = "-ceth -ugbp -d11/8"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '11/8', None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoDateNoTimeNoExchangeNoValue(self):
        inputStr = "-ceth -ugbp"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoUnitNoDateNoTimeNoExchangeNoValue(self):
        inputStr = "-ceth"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoCryptoNoDateNoTimeNoExchangeNoValue(self):
        inputStr = "-ugbp"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-u', 'gbp', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialValueFloatNoCryptoNoUnitNoDateNoTimeNoExchange(self):
        inputStr = "-v700.05usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-v', '700.05usd', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialValueIntNoCryptoNoUnitNoDateNoTimeNoExchange(self):
        inputStr = "-v700usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-v', '700usd', None, None, None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseGroupsPartialNoCryptoNoDateNoExchangeNoValue(self):
        inputStr = "-ugbp -t3:45"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-u', 'gbp', '-t', '3:45', None, None, None, None, None, None, None, None, None, None, None, None), groupList)


    def test_parseAndFillFullCommandPrice(self):
        inputStr = "btc usd 10/9/2017 12:45 Kraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '01')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)


    def test_parseAndFillFullCommandPriceNoUnitNoDateNoTimeNoExchange(self):
        inputStr = "btc"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY], None)
        self.assertEqual(parsedParmData[CommandPrice.MONTH], None)
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

    def test_parseAndFillPartialCommandPriceWithInitYearWithPartialYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '17'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8/16 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceWithInitYearNoPartialYear(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '15'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceWithInitYearWithPartialDateDayOnly(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '17'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceNoInitYearNoExchange(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceNoInitYearNoExchangeNoTime(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceNoInitYearNoExchangeNoMinute(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t5"
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
        parsedParmData[CommandPrice.UNIT] = 'usd'
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
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceWrongCommand(self):
        commandError = self.requester.commandPrice

        parsedParmData = commandError.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -h22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_OPTION], '-h')
        self.assertEqual(parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA], '22:46')
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceCommandNoHiphen(self):
        commandError = self.requester.commandPrice

        parsedParmData = commandError.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_DATA] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = None
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = None

        inputStr = "-ceth fgbp -d11/8 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def testRequestPriceCommandFull(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullDateZero(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin


    def testRequestPriceCommandFullDateBeforeTimeZero(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/2017 0 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '2017')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin


    def testRequestPriceCommandFullTimeZeroBeforeDate(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 10/9/2017 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin


    def testRequestPriceCommandFullDateZeroTimeZero(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 0 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullDateZeroNoTime(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 0 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], None)
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

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
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        # then, enter partial command price
        sys.stdin = StringIO("-d0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '0')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '0')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '0')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '0')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandPartialUnitTime(self):
        # first, enter full command price
        stdin = sys.stdin
        sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        # then, enter partial command price
        sys.stdin = StringIO("-uusd -t0:15")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '0')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '15')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandPartialUnitTimeZeroRejected(self):
        # first, enter full command price
        stdin = sys.stdin
        sys.stdin = StringIO("eth gbp 1/8/16 13:46 CCEX")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '1')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '13')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)

        # then, enter partial command price. -t0 means we want current price
        sys.stdin = StringIO("-uusd -t0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - invalid partial request -uusd -t0: in -t0, 0 must respect HH:mm format", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def test_fillOptionValueInfoRequestTypeFullAmountIntegerCurrencySymbolOk(self):
        optionType = 'VALUE'
        tstOptionValueData = '100usd'
        requestType = Requester.REQUEST_TYPE_FULL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypePartialAmountIntegerCurrencySymbolOk(self):
        optionType = 'VALUE'
        tstOptionValueData = '100usd'
        requestType = Requester.REQUEST_TYPE_PARTIAL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypeFullAmountFloatCurrencySymbolOk(self):
        optionType = 'VALUE'
        tstOptionValueData = '10.55usd'
        requestType = Requester.REQUEST_TYPE_FULL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('10.55', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypePartialAmountFloatCurrencySymbolOk(self):
        optionType = 'VALUE'
        tstOptionValueData = '10.55usd'
        requestType = Requester.REQUEST_TYPE_PARTIAL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('usd', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('10.55', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypeFullCancelValueOption(self):
        optionType = 'VALUE'
        tstOptionValueData = '0'
        requestType = Requester.REQUEST_TYPE_FULL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypePartialCancelValueOption(self):
        optionType = 'VALUE'
        tstOptionValueData = '0'
        requestType = Requester.REQUEST_TYPE_PARTIAL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypeFullAmountIntegerCurrencySymbolMissing(self):
        optionType = 'VALUE'
        tstOptionValueData = '100'
        requestType = Requester.REQUEST_TYPE_FULL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypePartialAmountIntegerCurrencySymbolMissing(self):
        optionType = 'VALUE'
        tstOptionValueData = '100'
        requestType = Requester.REQUEST_TYPE_PARTIAL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('100', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypeFullAmountFloatIncompleteCurrencySymbolMissing(self):
        optionType = 'VALUE'
        tstOptionValueData = '12.'
        requestType = Requester.REQUEST_TYPE_FULL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('12', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypePartialAmountFloatIncompleteCurrencySymbolMissing(self):
        optionType = 'VALUE'
        tstOptionValueData = '12.'
        requestType = Requester.REQUEST_TYPE_PARTIAL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('12', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypeFullAmountFloatCurrencySymbolMissing(self):
        optionType = 'VALUE'
        tstOptionValueData = '12.5'
        requestType = Requester.REQUEST_TYPE_FULL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('12.5', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

    def test_fillOptionValueInfoRequestTypePartialAmountFloatCurrencySymbolMissing(self):
        optionType = 'VALUE'
        tstOptionValueData = '12.5'
        requestType = Requester.REQUEST_TYPE_PARTIAL
        commandPrice = self.requester._fillOptionValueInfo(optionType, tstOptionValueData, requestType)

        self.assertEqual('', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual('12.5', commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, commandPrice.parsedParmData[CommandPrice.OPTION_VALUE_SAVE])

# test new FIAT -f and PRICE -p options

    def test_parseGroupsFullDayMonthHHMMFiatValueOption(self):
        inputStr = "btc eth 10/9 12:45 Kraken -fusd -v100usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-fusd', '-v100usd'), groupList)

    def test_parseGroupsFullDayMonthHHMMFiatValueOptionIncomplete(self):
        inputStr = "btc eth 10/9 12:45 Kraken -fusd -v100"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-fusd', '-v100'), groupList)

    def test_parseGroupsFullDayMonthHHMMPriceOption(self):
        inputStr = "btc eth 10/9 12:45 Kraken -p200.453usd "
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200.453usd', None), groupList)

    def test_parseGroupsFullDayMonthHHMMPriceOptionIncomplete(self):
        inputStr = "btc eth 10/9 12:45 Kraken -p200"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200', None), groupList)

    def test_parseGroupsFullDayMonthHHMMOptionPrice(self):
        inputStr = "btc eth 10/9 12:45 Kraken -p200.453usd -v100.675usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200.453usd', '-v100.675usd'), groupList)

    def test_parseGroupsFullDayMonthHHMMOptionPriceIncomplete(self):
        inputStr = "btc eth 10/9 12:45 Kraken -p200usd -v100"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200usd', '-v100'), groupList)

    def test_parseGroupsFullDayMonthHHMMPriceIncompleteValueOption(self):
        inputStr = "btc eth 10/9 12:45 Kraken -p200 -v100usd"
        groupList = self.requester._parseGroups(Requester.PATTERN_FULL_PRICE_REQUEST_WITH_OPTIONAL_COMMAND_DATA, inputStr)

        self.assertEqual(('btc', 'eth', '10/9', '12:45', 'Kraken', '-p200', '-v100usd'), groupList)

    def test_parseGroupsPartialDDDMHHFiatValueOptions(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -fusd -v0.0044235btc"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-f', 'usd', '-v', '0.0044235btc', None, None), groupList)

    def test_parseGroupsPartialDDDMHHFiatValueIncompleteOptions(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -fusd -v0.0044235"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-f', 'usd', '-v', '0.0044235', None, None), groupList)

    def test_parseGroupsPartialDDDMHHPriceValueOptions(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -p300.567usd -v0.0044235btc"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-p', '300.567usd', '-v', '0.0044235btc', None, None), groupList)

    def test_parseGroupsPartialDDDMHHPriceValueIncompleteOptions(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -p500usd -v0.0044235"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-p', '500usd', '-v', '0.0044235', None, None), groupList)

    def test_parseGroupsPartialDDDMHHPriceIncompleteValueIncompleteOptions(self):
        inputStr = "-ceth -ugbp -d110/2 -t22 -eKraken -p500 -v0.0044235"
        groupList = self.requester._parseGroups(Requester.PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c', 'eth', '-u', 'gbp', '-d', '110/2', '-t', '22', '-e', 'Kraken', '-p', '500', '-v', '0.0044235', None, None), groupList)

# test fiat option

    def testRequestPriceCommandFullEndingWithFiatOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -fusd")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithFiatOptionSave(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -fsusd")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual('usd', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithOptionFiatErase(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -f0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertIsNone(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionFiatWithAmount(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -f0.01")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -f0.01: -f0.01 option violates the -f option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionFiatSaveWithAmount(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fs0.01")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -fs0.01: -fs0.01 option violates the -f option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

# test full request options

# value

    def testRequestPriceCommandFullWithOptionValueSaveCommandInInvalidPosThree(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -vs0.01btc 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd -vs0.01btc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithOptionValueSaveCommandInInvalidPosThreeAndUnsupportedOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -vs0.01btc 10/9/17 12:45 Kraken -zunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd -vs0.01btc 10/9/17 12:45 Kraken -zunsupported violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithOptionValueSaveCommandInInvalidPosFour(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 -vs0.01btc 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd 10/9/17 -vs0.01btc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithOptionValueSaveCommandInInvalidPosFive(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 -vs0.01btc Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd 10/9/17 12:45 -vs0.01btc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithUnsupportedOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -zunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithUnsupportedOptionWithSaveModifier(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc eth 10/9/17 12:45 Kraken -zsunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], None)
        self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithValueOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0.01btc")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithOptionValueSaveCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01btc")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithOptionValueSaveCommandAndUnsupportedOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01btc -zunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithPriceUnsupportedOptionAndValueSaveCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -zunsupported -vs0.01btc")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.01', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullWithValueOptionInInvalidPosThree(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -v0.01btc 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd -v0.01btc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithValueOptionInInvalidPosFour(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 -v0.01btc 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd 10/9/17 -v0.01btc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithValueOptionInInvalidPosFive(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 -v0.01btc Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd 10/9/17 12:45 -v0.01btc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionValueSaveCommand(self):
        stdin = sys.stdin
        #        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01")
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vsooo")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -vsooo: -vsooo option violates the -vs option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionValueCommand(self):
        stdin = sys.stdin
        #        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01")
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vooo")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -vooo: -vooo option violates the -v option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionValueSaveSpec(self):
        stdin = sys.stdin
        #        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01")
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -vs: -vs option violates the -v option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionValueSaveNoFiatWithAmount(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -vs0.01: -vs0.01 option violates the -vs option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionValueNoFiatWithAmount(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0.01")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -v0.01: -v0.01 option violates the -v option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithOptionValueEraseCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v0")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin


    def testRequestPriceCommandFullEndingWithInvalidOptionValueNoAmountNoFiat(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -v")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

# fiat

    def testRequestPriceCommandFullWithOptionFiatSaveCommandInInvalidPosThree(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -fsbtc 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd -fsbtc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithOptionFiatSaveCommandInInvalidPosThreeAndUnsupportedOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -fsbtc 10/9/17 12:45 Kraken -zunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd -fsbtc 10/9/17 12:45 Kraken -zunsupported violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithOptionFiatSaveCommandInInvalidPosFour(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 -fsbtc 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd 10/9/17 -fsbtc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithOptionFiatSaveCommandInInvalidPosFive(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 -fsbtc Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual(
            "ERROR - full request btc usd 10/9/17 12:45 -fsbtc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>",
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithFiatOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fbtc")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithOptionFiatSaveCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fsbtc")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithOptionFiatSaveCommandAndUnsupportedOption(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fsbtc -zunsupported")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithPriceUnsupportedOptionAndFiatSaveCommand(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -zunsupported -fsbtc")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

    def testRequestPriceCommandFullWithFiatOptionInInvalidPosThree(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd -fbtc 10/9/17 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd -fbtc 10/9/17 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithFiatOptionInInvalidPosFour(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 -fbtc 12:45 Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd 10/9/17 -fbtc 12:45 Kraken violates format <crypto> <unit> <date|time> <exchange> <options>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullWithFiatOptionInInvalidPosFive(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 -fbtc Kraken")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandError)
        self.assertEqual(commandPrice, self.commandError)
        resultData = self.commandError.execute()
        self.assertEqual("ERROR - full request btc usd 10/9/17 12:45 -fbtc Kraken violates format <crypto> <unit> <date|time> <exchange> <options>", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionFiatSaveSpec(self):
        stdin = sys.stdin
        #        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -vs0.01")
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -fs")
        commandError = self.requester.request()

        self.assertEqual(self.commandError, commandError)
        resultData = self.commandError.execute()

        # formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual(
            'ERROR - full request btc usd 10/9/17 12:45 Kraken -fs: -fs option violates the -f option format. See help for more information.',
            resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))
        sys.stdin = stdin

    def testRequestPriceCommandFullEndingWithInvalidOptionFiatNoFiat(self):
        stdin = sys.stdin
        sys.stdin = StringIO("btc usd 10/9/17 12:45 Kraken -f")
        commandPrice = self.requester.request()

        self.assertIsInstance(commandPrice, CommandPrice)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '17')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

        sys.stdin = stdin

# test partial request options

# value

    def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValue(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -v0.0044256btc"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], 'btc')
        self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

    def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionValue(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-V0.0044256btc -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], 'btc')
        self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

    def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionValue(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -v500gbp -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], 'gbp')
        self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

    def test_parseAndFillPartialCommandPriceOptionValuePreviouslySet(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'

        inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], 'gbp')
        self.assertIsNone(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertIsNone(parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])

    def test_parseAndFillPartialCommandPriceIneffectiveOptionValueSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

        inputStr = "-ceth -v -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'usd')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '10')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '9')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '16')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '12')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '45')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'CCEX')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], '500')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SAVE], False)

    def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValueSave(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -vs0.0044256btc"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_DATA], None)
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT], '0.0044256')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL], 'btc')
        self.assertEqual(parsedParmData[CommandPrice.OPTION_VALUE_SAVE], True)

    def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValueSaveAndUnsupportedOptionWithSaveOptionModifier(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -vs0.0044256btc -zsunsupported"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('unsupported', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual('s', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceNoInitYearThenOptionValueSaveAndUnsupportedOption(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -ugbp -d11/8 -t22:46 -eKraken -vs0.0044256btc -zunsupported100"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual('-z', parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual('unsupported100', parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceNoInitYearCommandUppercaseOptionValueSave(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-VS0.0044256btc -Ceth -Ugbp -D11/8 -T22:46 -EKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], None)
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('0.0044256', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('btc', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceNoInitYearWithPartialYearOptionValueSave(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        #prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None

        inputStr = "-ceth -vs500gbp -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceOptionValueSavePreviouslySet(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

        inputStr = "-ceth -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual('500', parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual('gbp', parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertTrue(parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceEraseOptionValueSave(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

        inputStr = "-ceth -v0 -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceInvalidOptionValueSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'

        inputStr = "-ceth -vooo -ugbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : -vooo option violates the -v option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

    def test_parseAndFillPartialCommandPriceInvalidOptionValueSaveSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

        inputStr = "-ceth -vsooo -ugbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : -vsooo option violates the -vs option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

    def test_parseAndFillPartialCommandPriceInvalidOptionValueSaveSpecNoFiatWithAmount(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

        inputStr = "-ceth -vs0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : -vs0.01 option violates the -vs option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

    def test_parseAndFillPartialCommandPriceInvalidOptionValueNoFiatWithAmount(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = True

        inputStr = "-ceth -v0.01 -ugbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : -v0.01 option violates the -v option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

    def test_parseAndFillPartialCommandPriceEraseOptionValue(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = None
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'

        inputStr = "-ceth -v0 -ugbp -d11/8/15 -t22:46 -eKraken"
        commandPrice = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandPrice, self.commandPrice)
        parsedParmData = commandPrice.parsedParmData
        self.assertEqual(parsedParmData[CommandPrice.CRYPTO], 'eth')
        self.assertEqual(parsedParmData[CommandPrice.UNIT], 'gbp')
        self.assertEqual(parsedParmData[CommandPrice.DAY], '11')
        self.assertEqual(parsedParmData[CommandPrice.MONTH], '8')
        self.assertEqual(parsedParmData[CommandPrice.YEAR], '15')
        self.assertEqual(parsedParmData[CommandPrice.HOUR], '22')
        self.assertEqual(parsedParmData[CommandPrice.MINUTE], '46')
        self.assertEqual(parsedParmData[CommandPrice.EXCHANGE], 'Kraken')
        self.assertEqual(parsedParmData[CommandPrice.HOUR_MINUTE], None)
        self.assertEqual(parsedParmData[CommandPrice.DAY_MONTH_YEAR], None)
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_VALUE_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.UNSUPPORTED_OPTION_MODIFIER])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SYMBOL])
        self.assertIsNone(None, parsedParmData[CommandPrice.OPTION_FIAT_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_FIAT_SAVE])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_DATA])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_AMOUNT])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SYMBOL])
        self.assertEqual(None, parsedParmData[CommandPrice.OPTION_PRICE_SAVE])

    def test_parseAndFillPartialCommandPriceIneffectiveOptionValueSaveSpec(self):
        commandPrice = self.requester.commandPrice

        parsedParmData = commandPrice.parsedParmData

        # prefil commandPrice parsedParmData dictionary to simulate first entry of full command price entry
        parsedParmData[CommandPrice.CRYPTO] = 'btc'
        parsedParmData[CommandPrice.UNIT] = 'usd'
        parsedParmData[CommandPrice.DAY] = '10'
        parsedParmData[CommandPrice.MONTH] = '9'
        parsedParmData[CommandPrice.YEAR] = '16'
        parsedParmData[CommandPrice.HOUR] = '12'
        parsedParmData[CommandPrice.MINUTE] = '45'
        parsedParmData[CommandPrice.EXCHANGE] = 'CCEX'
        parsedParmData[CommandPrice.HOUR_MINUTE] = None
        parsedParmData[CommandPrice.DAY_MONTH_YEAR] = None
        parsedParmData[CommandPrice.OPTION_VALUE_AMOUNT] = '500'
        parsedParmData[CommandPrice.OPTION_VALUE_SYMBOL] = 'gbp'
        parsedParmData[CommandPrice.OPTION_VALUE_SAVE] = False

        inputStr = "-ceth -vs -ugbp -d11/8/15 -t22:46 -eKraken"
        commandError = self.requester._parseAndFillCommandPrice(inputStr)
        self.assertEqual(commandError, self.commandError)
        resultData = self.commandError.execute()

        #formatting of request input string has been moved to end of Requester.getCommand !
        self.assertEqual("ERROR - invalid partial request : -vs option violates the -v option format. See help for more information.", resultData.getValue(ResultData.RESULT_KEY_ERROR_MSG))

    def runTests(self):
        unittest.main()

if __name__ == '__main__':
    unittest.main()