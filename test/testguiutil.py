import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from guiutil import GuiUtil

class TestGuiUtil(unittest.TestCase):
    def setUp(self):
        pass

    def test_splitLongLineToShorterLines(self):
        note = 'a long class description. Which occupies several lines.'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], 'a long class description.')
        self.assertEqual(multilineNote[1], 'Which occupies several lines.')


    def test_splitLongLineToShorterLinesEmptyNote(self):
        note = ''
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 0)


    def test_splitLongLineToShorterLinesOneWordNoteLenEqualsMaxNoteLineLenMinusOne(self):
        note = '12345678911234567892123456789'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '12345678911234567892123456789')


    def test_splitLongLineToShorterLinesOneWordNoteLenEqualsMaxNoteLineLen(self):
        note = '123456789112345678921234567893'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '123456789112345678921234567893')


    def test_splitLongLineToShorterLinesOneWordNoteLenEqualsMaxNoteLineLenPlusOne(self):
        note = '1234567891123456789212345678931'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '1234567891123456789212345678931')


    def test_splitLongLineToShorterLinesTwoWordsNoteLenEqualsMaxNoteLineLen(self):
        note = '12345678911234 567892123456789'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '12345678911234 567892123456789')


    def test_splitLongLineToShorterLinesTwoWordsNoteLenEqualsMaxNoteLineLenPlusOne(self):
        note = '123456789112345 678921234567893'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345')
        self.assertEqual(multilineNote[1], '678921234567893')


    def test_splitLongLineToShorterLinesTwoWordsNoteLenEqualsMaxNoteLineLenPlusTwo(self):
        note = '123456789112345 6789212345678931'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345')
        self.assertEqual(multilineNote[1], '6789212345678931')


    def test_splitLongLineToShorterLinesTwoWordsFirstEqualsMaxLen(self):
        note = '123456789112345678921234567893 2'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345678921234567893')
        self.assertEqual(multilineNote[1], '2')


    def test_splitLongLineToShorterLinesTwoWordsFirstEqualsMaxLenPlusOne(self):
        note = '1234567891123456789212345678931 3'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '1234567891123456789212345678931')
        self.assertEqual(multilineNote[1], '3')


    def test_splitLongLineToShorterLinesTwoWordsFirstAndSecondEqualsMaxLen(self):
        note = '123456789112345678921234567893 123456789112345678921234567893'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345678921234567893')
        self.assertEqual(multilineNote[1], '123456789112345678921234567893')


    def test_splitLongLineToShorterLinesTwoWordsFirstAndSecondEqualsMaxLenPlusOne(self):
        note = '1234567891123456789212345678931 1234567891123456789212345678931'
        maxNoteLineLen = 30

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '1234567891123456789212345678931')
        self.assertEqual(multilineNote[1], '1234567891123456789212345678931')

    def test_splitLongLineToShorterLinesLargeNote(self):
        note = 'ERROR - :seqdiag_loop_start tag located on line 53 of file containing class ClassLoopTagOnMethodNotInRecordFlow is placed on an instruction calling method doC4NotRecordedInFlow() which is not part of the execution flow recorded by GuiUtil.'
        maxNoteLineLen = 150

        multilineNote = GuiUtil._splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], 'ERROR - :seqdiag_loop_start tag located on line 53 of file containing class ClassLoopTagOnMethodNotInRecordFlow is placed on an instruction calling')
        self.assertEqual(multilineNote[1], 'method doC4NotRecordedInFlow() which is not part of the execution flow recorded by GuiUtil.')

    def test_getListOfOriginalSizeParagraphs(self):
        text = 'CryptoPricer full request\n\n\nbtc usd 0 all\n\n\nReturns the current price of 1 btc in: usd.\n\nThe price is an average of the btc quotation, or: price, on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\n\nThis section explains the preceeding section'

        list = GuiUtil._getListOfOriginalSizeParagraphs(text)
        self.assertEqual(len(list), 11)
        self.assertEqual(list[0],'CryptoPricer full request')
        self.assertEqual(list[1],'\n\n')
        self.assertEqual(list[2],'btc usd 0 all')
        self.assertEqual(list[3],'\n\n')
        self.assertEqual(list[4],'Returns the current price of 1 btc in: usd.')
        self.assertEqual(list[5],'\n')
        self.assertEqual(list[6],'The price is an average of the btc quotation, or: price, on all the exchanges. It is computed by the crypto prices provider.')
        self.assertEqual(list[7],'\n\n\n')
        self.assertEqual(list[8],'Next section')
        self.assertEqual(list[9],'\n\n')
        self.assertEqual(list[10],'This section explains the preceeding section')

    def test_getListOfParagraphsSizedForKivyLabel(self):
        text = 'CryptoPricer full request\n\n\nbtc usd 0 all\n\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\n\nThis section explains the preceeding section'
        width = 60
        list = GuiUtil._getListOfParagraphsSizedForKivyLabel(text, width)
        self.assertEqual(len(list), 11)
        self.assertEqual(list[0],'CryptoPricer full request')
        self.assertEqual(list[1],'\n\n')
        self.assertEqual(list[2],'btc usd 0 all')
        self.assertEqual(list[3],'\n\n')
        self.assertEqual(list[4],'Returns the current price of 1 btc in usd.')
        self.assertEqual(list[5],'\n')
        self.assertEqual(list[6],'The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.')
        self.assertEqual(list[7],'\n\n\n')
        self.assertEqual(list[8],'Next section')
        self.assertEqual(list[9],'\n\n')
        self.assertEqual(list[10],'This section explains the preceeding section')

    def test_getListOfParagraphsSizedForKivyLabelWithTabCodedParagraph(self):
        text = '[t]a first right shifted paragraph\n\n\n[t]btc usd 0 all\n\n\nReturns the current price of 1 btc in usd.\n\n[t]The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\n\n[t]This section explains the preceeding section'

        width = 30
        list = GuiUtil._getListOfParagraphsSizedForKivyLabel(text, width)
        self.assertEqual(17, len(list))
        self.assertEqual(list[0],'[t]a first right shifted')
        self.assertEqual(list[1],'[t]paragraph')
        self.assertEqual(list[2],'\n\n')
        self.assertEqual(list[3],'[t]btc usd 0 all')
        self.assertEqual(list[4],'\n\n')
        self.assertEqual(list[5],'Returns the current price of 1 btc in usd.')
        self.assertEqual(list[6],'\n')
        self.assertEqual(list[7],'[t]The price is an average of')
        self.assertEqual(list[8],'[t]the btc quotation on all')
        self.assertEqual(list[9],'[t]the exchanges. It is')
        self.assertEqual(list[10],'[t]computed by the crypto')
        self.assertEqual(list[11],'[t]prices provider.')
        self.assertEqual(list[12],'\n\n\n')
        self.assertEqual(list[13],'Next section')
        self.assertEqual(list[14],'\n\n')
        self.assertEqual(list[15],'[t]This section explains the')
        self.assertEqual(list[16],'[t]preceeding section')

    def test_splitTabbedLineToShorterTabbedLines(self):
        text = '[t]a first right shifted paragraph'

        width = 30
        list = GuiUtil._splitTabbedLineToShorterTabbedLines(text, width)
        self.assertEqual(2, len(list))
        self.assertEqual(list[0],'[t]a first right shifted')
        self.assertEqual(list[1],'[t]paragraph')

    def test_splitTabbedLineToShorterTabbedLinesShortTabbedParagraph(self):
        text = '[t]a first right shifted'

        width = 30
        list = GuiUtil._splitTabbedLineToShorterTabbedLines(text, width)
        self.assertEqual(1, len(list))
        self.assertEqual(list[0],'[t]a first right shifted')

    def test_sizeParagraphsForKivyLabel(self):
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
CryptoPricer full request

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



Next section

This section explains the preceeding section''',resizedText)

    def test_sizeParagraphsForKivyLabelWithMarkup(self):
        text = '[b]CryptoPricer full request[/b]\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
[b]CryptoPricer full request[/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



Next section

This section explains the preceeding section''',resizedText)

    def test_sizeParagraphsForKivyLabelWithMarkupColor(self):
        text = '[b][color=ff0000]CryptoPricer full request[/color][/b]\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\n[b][color=ff0000]Next section[/color][/b]\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''',resizedText)

    def test_sizeParagraphsForKivyLabelWithMarkupColorFromFile(self):
        FILE_PATH = 'popupMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as markupFile:
            text = markupFile.read()

        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''', resizedText)

    def test_sizeParagraphsForKivyLabelWithMarkupColorAndTabbedParagraphsFromFile(self):
        FILE_PATH = 'regularAndShiftedPopupMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as file:
            text = file.read()

        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

This is a long explanation which will occupy several lines once reorganized by the Label itself.
    The price is an average of the btc quotation on
    all the exchanges. It is computed by the crypto
    prices provider.
no tab line

    * new tabbed line

    * other tabbed line
    
    * last tabbed line


[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''', resizedText)

    def test_sizeParagraphsForKivyLabelWithLongMarkupColorAndTabbedParagraphsFromFile(self):
        FILE_PATH = 'regularAndShiftedPopupLongMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as file:
            text = file.read()

        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full and long title request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

This is a long explanation which will occupy several lines once reorganized by the Label itself.
    The [b][color=ffff00ff]price[/color][/b] is an average of the btc quotation on
    all the exchanges. It is computed by the crypto
    prices provider.
no tab line

    * new tabbed line

    * other tabbed line
    
    * last tabbed line


[b][color=19ff52ff]Next section[/color][/b]

This section explains the preceeding section''', resizedText)

    def test_decodeMarkupsOnRealPartialHelpFile(self):
        FILE_PATH = 'partial_help.txt'
        text = ''

        with open(FILE_PATH) as file:
            text = file.read()

        width = 54
        resizedText = GuiUtil._decodeMarkups(text)
        self.assertEqual('''[b][color=ff0000]Requesting RT and historical cryptocurrency prices[/b][/color]

CryptoPricer supports two kinds of requests: full requests and partial requests.

[b]Full request[/b]

<crypto> <unit> <date time> <exchange> <options>

<date time> possible values:

    [b][color=ffff00ff]0[/color][/b] for RT

    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is specified,
    current year is assumed. If no time is specified, current
    time is assumed.

    [b][color=ffff00ff]21/12 8:34[/color][/b] --> current year assumed

    21 8:34  --> here, since no month is specified,
    current month or previous month is assumed.

    8:34 --> here, since no date is specified, current
    date is assumed.

[b]WARNING[/b]: specifying time makes sense only for dates not older than 7 days. Prices older than 7 days are 'close' prices. Since there is no notion of a close price for crypto's, the last price of the date at UTC 23.59 is returned as 'close' price.

[b]Output price qualifiers[/b]:

R = RT
M = Minute price (precision at the minute)
C = Close price
''', resizedText)

    def test_sizeParagraphsForKivyLabelnRealPartialNoBreakLinesHelpFile(self):
        FILE_PATH = 'partial_help_nobreaked_lines.txt'
        text = ''

        with open(FILE_PATH) as file:
            text = file.read()

        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        #        resizedText = GuiUtil.decodeMarkup(text)
        self.assertEqual('''
[b][color=ff0000]Requesting RT and historical cryptocurrency prices[/b][/color]

CryptoPricer supports two kinds of requests: full requests and partial requests.

[b]Full request[/b]

<crypto> <unit> <date time> <exchange> <options>

<date time> possible values:

    [b][color=ffff00ff]0[/color][/b] for RT

    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is
    specified, current year is assumed. If no time is
    specified, current time is assumed.

    [b][color=ffff00ff]21/12 8:34[/color][/b] --> current year assumed

    21 8:34 --> here, since no month is specified,
    current month or previous month is assumed.

    8:34 --> here, since no date is specified, current
    date is assumed.

[b]WARNING[/b]: specifying time makes sense only for dates not older than 7 days. Prices older than 7 days are 'close' prices. Since there is no notion of a close price for crypto's, the last price of the date at UTC 23.59 is returned as 'close' price.

[b]Output price qualifiers[/b]:

    R = RT

    M = Minute price (precision at the minute)

    C = Close price''', resizedText)

    def test_encodeShiftedLinesWithTabCode(self):
        lineList = None

        with open('shiftedPopupMarkupTest.txt', 'r') as file:
            lineList = file.read().splitlines()

        encodedTabbedText = GuiUtil._encodeShiftedLinesWithTabCode(lineList)

        self.assertEqual('''[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

[t]The price is an average of the btc quotation on all
[t]the exchanges. It is computed by the crypto prices
[t]provider.
no tab line
[t]* new tabbed line

[t]* other tabbed line
[t]
[t]* last tabbed line


[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''', encodedTabbedText)

    def test_encodeShiftedLinesWithTabCodeAndForcedLineBreak(self):
        lineList = None

        with open('shiftedLineBreakPopupMarkupTest.txt', 'r') as file:
            lineList = file.read().splitlines()

        encodedTabbedText = GuiUtil._encodeShiftedLinesWithTabCode(lineList)

        self.assertEqual('''[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

[t]The price is an average of the btc quotation on all
[t]the exchanges. It is computed by the crypto prices
[t]provider.
no tab line
[t][n]* new tabbed line
[t][n]* other tabbed line
[t][n]* last tabbed line


[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''', encodedTabbedText)

    def test_decodeMarkups(self):
        text = '[b][color=ff0000]CryptoPricer full request[/color][/b]\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\n[b][color=ff0000]Next section[/color][/b]\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil._decodeMarkups(text)
        self.assertEqual('''[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''',resizedText)

    def test_decodeMarkupsFromFile(self):
        FILE_PATH = 'scrollablePopupMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as markupFile:
            text = markupFile.read()

        width = 54
        resizedText = GuiUtil._decodeMarkups(text)
        self.assertEqual('''[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''',resizedText)

    def test_sizeParagraphsForKivyLabelWithShiftedParagraphs(self):
        text = '''<date time> possible values:

    [b][cy]0[/cy][/b] for RT

    [b][cy]21/12 or 21/12/19 or 21/12/2019[/c][/b]. If no year is specified, current year is assumed. If no time is specified, current time is assumed.


    [b][cy]21/12 8:34[/c][/b] --> current year assumed'''

        width = 54
        resizedText = GuiUtil._sizeParagraphsForKivyLabel(text, width)
        self.assertEqual('''
<date time> possible values:

    [b][color=ffff00ff]0[/color][/b] for RT

    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is
    specified, current year is assumed. If no time is
    specified, current time is assumed.


    [b][color=ffff00ff]21/12 8:34[/color][/b] --> current year assumed''',resizedText)

    def test_calculateMarkupsLength(self):
        text = '[b][cy]0[/cy][/b] for RT'
        self.assertEqual(GuiUtil._calculateMarkupsLength(text), 16)
        text = '[b][cy]21/12 or 21/12/19 or 21/12/2019[/c][/b]. If no year is specified'
        self.assertEqual(GuiUtil._calculateMarkupsLength(text), 15)
        text = '[n][b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is '
        self.assertEqual(GuiUtil._calculateMarkupsLength(text), 34)

    def test_removeEOLFromFile(self):
        noEOLText = ''
        FILE_PATH = 'partial_help_breaked_lines.txt'

        with open(FILE_PATH) as breakedLineFile:
            noEOLText = GuiUtil._removeEOLFromFile(breakedLineFile)

        self.assertEqual('''[b][cr]Requesting RT and historical cryptocurrency prices[/b][/c]

CryptoPricer supports two kinds of requests: full requests and partial requests.

[b]Full request[/b]

<crypto> <unit> <date time> <exchange> <options>

<date time> possible values:

    [b][cy]0[/cy][/b] for RT

    [b][cy]21/12 or 21/12/19 or 21/12/2019[/c][/b]. If no year is specified, current year is assumed. If no time is specified, current time is assumed.

    [b][cy]21/12 8:34[/c][/b] --> current year assumed

    21 8:34 --> here, since no month is specified, current month or previous month is assumed.

    8:34 --> here, since no date is specified, current date is assumed.

[b]WARNING[/b]: specifying time makes sense only for dates not older than 7 days. Prices older than 7 days are 'close' prices. Since there is no notion of a close price for crypto's, the last price of the date at UTC 23.59 is returned as 'close' price.

[b]Output price qualifiers[/b]:

    R = RT

    M = Minute price (precision at the minute)

    C = Close price

Examples: assume we are on 16/12/17 at 22:10

[cy]btc usd 0 bittrex[/c] --> [n]BTC/USD on BitTrex: 16/12/17 22:10R 19120

[cy]eth btc 16/12 13:45 bitfinex[/c] --> [n]ETH/BTC on Bitfinex: 16/12/17 13:45M 0.03893

[cy]eth btc 13:45 bitfinex[/c] --> [n]ETH/BTC on Bitfinex: 16/12/17 13:45M 0.03893

[cy]eth btc 15 8:45 bitfinex[/c] --> [n]ETH/BTC on Bitfinex: 15/12/17 8:45M 0.03782

[cy]eth btc 21/1 13:45 bitfinex[/c] --> [n]ETH/BTC on Bitfinex: 21/01/17C 0.01185

[cy]btc usd 0 bittrex -v0.01btc[/c] --> [n]0.01 BTC/191.2 USD on BitTrex: 16/12/17 22:10R 19120

[b][cr]WARNING[/c][/b]: <options> must be specified at the end of the full command price''', noEOLText)

    def testSizeParagraphsForKivyLabelnRealPartialWithBreakLinesHelpFile(self):
        '''
        This test ensures that text resizing for the Kivy label destination works
        on a help file where the not shifted long lines are sized for better reading
        at help write time.
        '''
        FILE_PATH = 'partial_help_breaked_lines.txt'
        resizedText = ''
        width = 54

        with open(FILE_PATH) as file:
            resizedText = GuiUtil.sizeParagraphsForKivyLabelFromFile(file, width)

        self.assertEqual('''
[b][color=ff0000]Requesting RT and historical cryptocurrency prices[/b][/color]

CryptoPricer supports two kinds of requests: full requests and partial requests.

[b]Full request[/b]

<crypto> <unit> <date time> <exchange> <options>

<date time> possible values:

    [b][color=ffff00ff]0[/color][/b] for RT

    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is
    specified, current year is assumed. If no time is
    specified, current time is assumed.

    [b][color=ffff00ff]21/12 8:34[/color][/b] --> current year assumed

    21 8:34 --> here, since no month is specified,
    current month or previous month is assumed.

    8:34 --> here, since no date is specified, current
    date is assumed.

[b]WARNING[/b]: specifying time makes sense only for dates not older than 7 days. Prices older than 7 days are 'close' prices. Since there is no notion of a close price for crypto's, the last price of the date at UTC 23.59 is returned as 'close' price.

[b]Output price qualifiers[/b]:

    R = RT

    M = Minute price (precision at the minute)

    C = Close price

Examples: assume we are on 16/12/17 at 22:10

[color=ffff00ff]btc usd 0 bittrex[/color] -->
BTC/USD on BitTrex: 16/12/17 22:10R 19120

[color=ffff00ff]eth btc 16/12 13:45 bitfinex[/color] -->
ETH/BTC on Bitfinex: 16/12/17 13:45M 0.03893

[color=ffff00ff]eth btc 13:45 bitfinex[/color] -->
ETH/BTC on Bitfinex: 16/12/17 13:45M 0.03893

[color=ffff00ff]eth btc 15 8:45 bitfinex[/color] -->
ETH/BTC on Bitfinex: 15/12/17 8:45M 0.03782

[color=ffff00ff]eth btc 21/1 13:45 bitfinex[/color] -->
ETH/BTC on Bitfinex: 21/01/17C 0.01185

[color=ffff00ff]btc usd 0 bittrex -v0.01btc[/color] -->
0.01 BTC/191.2 USD on BitTrex: 16/12/17 22:10R 19120

[b][color=ff0000]WARNING[/color][/b]: <options> must be specified at the end of the full command price''', resizedText)

    def testSizeParagraphsForKivyLabelnRealPartialWithNoBreakLinesHelpFile(self):
        '''
        This test ensures that text resizing for the Kivy label destination works
        on a help file where the not shifted long lines do not include any break.
        '''
        FILE_PATH = 'partial_help_nobreaked_lines.txt'
        resizedText = ''
        width = 54

        with open(FILE_PATH) as file:
            resizedText = GuiUtil.sizeParagraphsForKivyLabelFromFile(file, width)

        self.assertEqual('''
[b][color=ff0000]Requesting RT and historical cryptocurrency prices[/b][/color]

CryptoPricer supports two kinds of requests: full requests and partial requests.

[b]Full request[/b]

<crypto> <unit> <date time> <exchange> <options>

<date time> possible values:

    [b][color=ffff00ff]0[/color][/b] for RT

    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is
    specified, current year is assumed. If no time is
    specified, current time is assumed.

    [b][color=ffff00ff]21/12 8:34[/color][/b] --> current year assumed

    21 8:34 --> here, since no month is specified,
    current month or previous month is assumed.

    8:34 --> here, since no date is specified, current
    date is assumed.

[b]WARNING[/b]: specifying time makes sense only for dates not older than 7 days. Prices older than 7 days are 'close' prices. Since there is no notion of a close price for crypto's, the last price of the date at UTC 23.59 is returned as 'close' price.

[b]Output price qualifiers[/b]:

    R = RT

    M = Minute price (precision at the minute)

    C = Close price''', resizedText)

    def test_decodeForcedBreakLine(self):
        codedString = ' [n]text to put on nxt line'

        self.assertEqual('''
text to put on nxt line''', GuiUtil._decodeForcedLineBreak(codedString))

if __name__ == '__main__':
    unittest.main()
