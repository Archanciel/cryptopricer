import unittest
import os, sys, inspect
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
                              # the test is executed standalone

import re
from guioutputformater import GuiOutputFormater
from resultdata import ResultData
from datetimeutil import DateTimeUtil
from configurationmanager import ConfigurationManager
from utilityfortest import UtilityForTest

class TestGuiOutputFormater(unittest.TestCase):
    def setUp(self):
        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        self.printer = GuiOutputFormater(configMgr)


    def testPrintCryptoPriceHistorical(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'BitTrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


    def testPrintCryptoPriceHistoricalPriceValue(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'BitTrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01698205')
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '70')

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('0.01698205 BTC/70 USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


    def testGetFullCommandStringYearDefinedDupl(self):
        crypto = 'ETH'
        unit = 'USD'

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
                            {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
                             'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None})

        fullCommandString, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.printer.getFullCommandString(resultData)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual(fullCommandString, "eth usd 05/12/17 09:30 bittrex")


    def testPrintCryptoPriceHistoricalPriceValueDupl(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'BitTrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01698205')
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '70')

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('0.01698205 BTC/70 USD on BitTrex: 12/09/17 00:00C 4122\n', capturedStdout.getvalue())


    def testPrintCryptoPriceHistoricalPriceValueWarning(self):
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'BitTrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, None)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, None)
        resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE,
                              "WARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD). -v option ignored !")

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: 12/09/17 00:00C 4122\nWARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD). -v option ignored !\n', capturedStdout.getvalue())


    def testGetCryptoPriceHistoricalRecent(self):
        #here, requested date is less than 7 days ago
        now = DateTimeUtil.localNow('Europe/Zurich')
        recent = now.shift(days = -2)
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = recent.day
        month = recent.month
        year = recent.year
        hour = 10
        minute = 5

        resultData = ResultData()

        recentDay = recent.day

        if recentDay < 10:
            recentDayStr = '0' + str(recentDay)
        else:
            recentDayStr = str(recentDay)

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122.09)

        dateTimeString = '{}/{}/{} 10:05'.format(recentDayStr, month, year - 2000)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: {}M 4122.09\n'.format(dateTimeString), capturedStdout.getvalue())


    def testGetCryptoPriceHistoricalWrongExchange(self):    
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'unknown'
        day = 12
        month = 9
        year = 2017
        hour = 10
        minute = 5

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


    def testGetCryptoPriceRealTime(self):    
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        #rt price not provided here !
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())


    def testGetCryptoPriceRealTimeWrongExchange(self):    
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'unknown'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()
        
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - unknown market does not exist for this coin pair (BTC-USD)")
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, None)
        resultData.setValue(resultData.RESULT_KEY_UNIT, None)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, None)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual("ERROR - unknown market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


    def testGetCryptoPriceRealTimeExchangeNotSupportPair(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'BTC38'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, "ERROR - BTC38 market does not exist for this coin pair (BTC-USD)")
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        resultData.setValue(resultData.RESULT_KEY_PRICE, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, None)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, None)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual("ERROR - BTC38 market does not exist for this coin pair (BTC-USD)\n", capturedStdout.getvalue())


    def testFormatFloatToStrRoundedFloat(self):
        y = round(5.59, 1)
        self.assertEqual('5.6', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrEmptystr(self):
        y = ''
        self.assertEqual('', self.printer.formatFloatToStr(y))


    def testFormatFloatToStrNone(self):
        y = None
        self.assertEqual('', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrNineDigits(self):
        y = 	0.999999999
        self.assertEqual('1', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrFourDigits(self):
        y = 0.9084   
        self.assertEqual('0.9084', self.printer.formatFloatToStr(y))

    
    def testFormatFloatToStrinteger(self):
        y = 40 
        self.assertEqual('40', self.printer.formatFloatToStr(y))


    def testFormatFloatToStrNormal(self):
        y = 2000.085  
        self.assertEqual('2000.085', self.printer.formatFloatToStr(y)) 


    def testToFromClipboard(self):
        if os.name != 'posix':
            #causes an exception after updating all conda packages on 7.2.2018 !
            pass
        else:
            y = 2000.085
            self.printer.toClipboard(y)
            self.assertEqual(str(y), self.printer.fromClipboard())


    def testGetFullCommandStringYearNone(self):
        now = DateTimeUtil.localNow('Europe/Zurich')

        nowYearStr, nowMonthStr, nowDayStr,nowHourStr, nowMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(now)

        crypto = 'ETH'
        unit = 'USD'

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS, {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': None, 'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None})
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
                            {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
                             'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None})

        fullCommandString, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.printer.getFullCommandString(resultData)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual(fullCommandString, "eth usd 05/12/17 09:30 bittrex")


    def testGetFullCommandStringYearDefined(self):
        crypto = 'ETH'
        unit = 'USD'

        resultData = ResultData()

        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
                            {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
                             'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None, 'OPTION_VALUE_SYMBOL': None})

        fullCommandString, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.printer.getFullCommandString(resultData)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual(fullCommandString, "eth usd 05/12/17 09:30 bittrex")


    def testGetCryptoPriceRealTimeWithOptionValue(self):
        #correspond to command btc usd 0 bittrex -v0.01btc
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        #rt price not provided here !
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01')
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '160')
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
                            {'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
                             'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
                             'OPTION_VALUE_AMOUNT': '0.01', 'OPTION_VALUE_SYMBOL': 'btc', 'OPTION_VALUE_SAVE': False})

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('0.01 BTC/160 USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())
        fullCommandString, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.printer.getFullCommandString(resultData)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual('btc usd 0 bittrex', fullCommandString)


    def testGetCryptoPriceRealTimeWithOptionValueGenerateWarning(self):
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        #rt price not provided here !
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
        resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE,
                              "WARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD). -v option ignored !")

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD on BitTrex: {}R \nWARNING - currency value symbol ETH differs from both crypto (BTC) and unit (USD). -v option ignored !\n'.format(dateTimeString), capturedStdout.getvalue())


    def testGetCryptoPriceRealTimeWithValueSaveFlag(self):
        #correspond to command btc usd 0 bittrex -vs0.01btc
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        #rt price not provided here !
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, '0.01')
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, '160')
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_SAVE, True)
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
                            {'CRYPTO': 'btc', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '0', 'MONTH': '0', 'YEAR': '0', 'HOUR': None,
                             'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'REAL_TIME', 'OPTION_VALUE_DATA': None,
                             'OPTION_VALUE_AMOUNT': '0.01', 'OPTION_VALUE_SYMBOL': 'btc', 'OPTION_VALUE_SAVE': True})
        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('0.01 BTC/160 USD on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())
        fullCommandString, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.printer.getFullCommandString(resultData)
        self.assertEqual('btc usd 0 bittrex -vs0.01btc', fullCommandStrWithSaveModeOptions)
        self.assertEqual('btc usd 0 bittrex', fullCommandString)

    def testGetCryptoPriceRealTimeOptionFiat(self):
        # btc usd 0 bittrex -fchf
        now = DateTimeUtil.localNow('Europe/Zurich')
        crypto = 'BTC'
        unit = 'USD'
        fiat = 'CHF'
        exchange = 'bittrex'
        day = 0
        month = 0
        year = 0
        hour = 1
        minute = 1

        resultData = ResultData()

        nowMinute = now.minute

        if nowMinute < 10:
            if nowMinute > 0:
                nowMinuteStr = '0' + str(nowMinute)
            else:
                nowMinuteStr = '00'
        else:
            nowMinuteStr = str(nowMinute)

        nowHour = now.hour

        if nowHour < 10:
            if nowHour > 0:
                nowHourStr = '0' + str(nowHour)
            else:
                nowHourStr = '00'
        else:
            nowHourStr = str(nowHour)

        nowDay = now.day

        if nowDay < 10:
            nowDayStr = '0' + str(nowDay)
        else:
            nowDayStr = str(nowDay)

        #rt price not provided here !
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, 'BitTrex')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_RT)
        dateTimeString = '{}/{}/{} {}:{}'.format(nowDayStr, now.month, now.year - 2000, nowHourStr, nowMinuteStr)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, dateTimeString)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD/CHF.CCCAGG on BitTrex: {}R \n'.format(dateTimeString), capturedStdout.getvalue())

    def testPrintCryptoPriceHistoricalOptionFiat(self):
        # btc usd 12/9/17 bittrex -feur
        crypto = 'BTC'
        unit = 'USD'
        fiat = 'EUR'
        exchange = 'BitTrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 3463.7166)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD/EUR.CCCAGG on BitTrex: 12/09/17 00:00C 4122 3463.7166\n', capturedStdout.getvalue())

    def testPrintCryptoPriceHistoricalOptionFiatSave(self):
        # btc usd 12/9/17 bittrex -fseur
        crypto = 'BTC'
        unit = 'USD'
        fiat = 'EUR'
        exchange = 'BitTrex'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 4122)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, 'CCCAGG')
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 3463.7166)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SAVE, True)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('BTC/USD/EUR.CCCAGG on BitTrex: 12/09/17 00:00C 4122 3463.7166\n', capturedStdout.getvalue())

    def testPrintCryptoPriceHistoricalOptionFiatExchange(self):
        # mco eth 12/9/17 binance -fbtc.kraken
        crypto = 'MCO'
        unit = 'ETH'
        fiat = 'BTC'
        exchange = 'Binance'
        fiatExchange = 'Kraken'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 0.02802)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, fiatExchange)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 0.001975)

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('MCO/ETH/BTC.Kraken on Binance: 12/09/17 00:00C 0.02802 0.001975\n', capturedStdout.getvalue())

    def testPrintCryptoPriceHistoricalOptionValueAndFiatExchange(self):
        # mco btc 12/9/17 binance -feth.kraken -v1eth
        # 34.39239 MCO/0.07047 BTC/1 ETH.Kraken on Binance: 12/09/17 00:00C 0.002049 0.029076
        crypto = 'MCO'
        unit = 'BTC'
        fiat = 'ETH'
        exchange = 'Binance'
        fiatExchange = 'Kraken'

        resultData = ResultData()
        resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
        resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
        resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
        resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
        resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
        resultData.setValue(resultData.RESULT_KEY_PRICE, 0.002049)
        resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '12/09/17 00:00')
        resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1505174400)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, 34.39238653001464)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, 0.07047)
        resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, 1)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, fiatExchange)
        resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, 0.02907620263942103)
        resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
                            {'CRYPTO': crypto, 'UNIT': unit, 'EXCHANGE': exchange, 'DAY': '12', 'MONTH': '9', 'YEAR': '17', 'HOUR': None,
                             'MINUTE': None, 'DMY': None, 'HM': None, 'PRICE_TYPE': 'HISTO', 'OPTION_VALUE_DATA': None,
                             'OPTION_VALUE_AMOUNT': '1', 'OPTION_VALUE_SYMBOL': 'eth', 'OPTION_VALUE_SAVE': False})

        stdout = sys.stdout
        capturedStdout = StringIO()
        sys.stdout = capturedStdout

        self.printer.printDataToConsole(resultData)
        sys.stdout = stdout
        self.assertEqual('34.39239 MCO/0.07047 BTC/1 ETH.Kraken on Binance: 12/09/17 00:00C 0.002049 0.029076\n', capturedStdout.getvalue())

if __name__ == '__main__':
    unittest.main()
