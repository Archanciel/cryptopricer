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

    def test_getListOfParagraphs(self):
        text = 'CryptoPricer full request\n\n\nbtc usd 0 all\n\n\nReturns the current price of 1 btc in: usd.\n\nThe price is an average of the btc quotation, or: price, on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\n\nThis section explains the preceeding section'

        list = GuiUtil._getListOfParagraphs(text)
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

    def test_getListOfSizedParagraphs(self):
        text = 'CryptoPricer full request\n\n\nbtc usd 0 all\n\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\n\nThis section explains the preceeding section'
        width = 60
        list = GuiUtil._getListOfSizedParagraphs(text, width)
        self.assertEqual(len(list), 12)
        self.assertEqual(list[0],'CryptoPricer full request')
        self.assertEqual(list[1],'\n\n')
        self.assertEqual(list[2],'btc usd 0 all')
        self.assertEqual(list[3],'\n\n')
        self.assertEqual(list[4],'Returns the current price of 1 btc in usd.')
        self.assertEqual(list[5],'\n')
        self.assertEqual(list[6],'The price is an average of the btc quotation on all the')
        self.assertEqual(list[7],'exchanges. It is computed by the crypto prices provider.')
        self.assertEqual(list[8],'\n\n\n')
        self.assertEqual(list[9],'Next section')
        self.assertEqual(list[10],'\n\n')
        self.assertEqual(list[11],'This section explains the preceeding section')

    def test_getListOfSizedParagraphsSmallerWidth(self):
        text = 'CryptoPricer full request\n\n\nbtc usd 0 all\n\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\n\nThis section explains the preceeding section'
        width = 30
        list = GuiUtil._getListOfSizedParagraphs(text, width)
        self.assertEqual(len(list), 16)
        self.assertEqual(list[0],'CryptoPricer full request')
        self.assertEqual(list[1],'\n\n')
        self.assertEqual(list[2],'btc usd 0 all')
        self.assertEqual(list[3],'\n\n')
        self.assertEqual(list[4],'Returns the current price of 1')
        self.assertEqual(list[5],'btc in usd.')
        self.assertEqual(list[6],'\n')
        self.assertEqual(list[7],'The price is an average of the')
        self.assertEqual(list[8],'btc quotation on all the')
        self.assertEqual(list[9],'exchanges. It is computed by')
        self.assertEqual(list[10],'the crypto prices provider.')
        self.assertEqual(list[11],'\n\n\n')
        self.assertEqual(list[12],'Next section')
        self.assertEqual(list[13],'\n\n')
        self.assertEqual(list[14],'This section explains the')
        self.assertEqual(list[15],'preceeding section')


    def testSizeParagraphsToSmallerWidth(self):
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil.sizeParagraphsToSmallerWidth(text, width)
        self.assertEqual('''
CryptoPricer full request

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all
the exchanges. It is computed by the crypto prices
provider.



Next section

This section explains the preceeding section''',resizedText)

    def testSizeParagraphsToSmallerWidthWithMarkup(self):
        text = '[b]CryptoPricer full request[/b]\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\nNext section\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil.sizeParagraphsToSmallerWidth(text, width)
        self.assertEqual('''
[b]CryptoPricer full request[/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all
the exchanges. It is computed by the crypto prices
provider.



Next section

This section explains the preceeding section''',resizedText)

    def testSizeParagraphsToSmallerWidthWithMarkupColor(self):
        text = '[b][color=ff0000]CryptoPricer full request[/color][/b]\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\n[b][color=ff0000]Next section[/color][/b]\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil.sizeParagraphsToSmallerWidth(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all
the exchanges. It is computed by the crypto prices
provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''',resizedText)

    def testSizeParagraphsToSmallerWidthWithMarkupColorFromFile(self):
        FILE_PATH = 'popupMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as markupFile:
            text = markupFile.read()

        width = 54
        resizedText = GuiUtil.sizeParagraphsToSmallerWidth(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all
the exchanges. It is computed by the crypto prices
provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''', resizedText)

    def testSizeParagraphsToSmallerWidthWithMarkupColorAndTabbedParagraphsFromFile(self):
        FILE_PATH = 'regularAndShiftedPopupMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as file:
            text = file.read()

        width = 54
        resizedText = GuiUtil.sizeParagraphsToSmallerWidth(text, width)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

This is a long explanation which will occupy several
lines once reorganized by the Label itself.
    The price is an average of the btc quotation on 
    all the exchanges. It is computed by the crypto 
    prices provider.
no tab line

    * new tabbed line

    * other tabbed line
    
    * last tabbed line


[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''', resizedText)

    def test_encodeTabbedText(self):
        lineList = None

        with open('shiftedPopupMarkupTest.txt', 'r') as file:
            lineList = file.read().splitlines()

        encodedTabbedText = GuiUtil._encodeTabbedText(lineList)

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

    def testDecodeMarkup(self):
        text = '[b][color=ff0000]CryptoPricer full request[/color][/b]\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\n\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\n\n[b][color=ff0000]Next section[/color][/b]\n\nThis section explains the preceeding section'
        width = 54
        resizedText = GuiUtil.decodeMarkup(text)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''',resizedText)

    def testDecodeMarkupFromFile(self):
        FILE_PATH = 'scrollablePopupMarkupTest.txt'
        text = ''

        with open(FILE_PATH) as markupFile:
            text = markupFile.read()

        width = 54
        resizedText = GuiUtil.decodeMarkup(text)
        self.assertEqual('''
[b][color=ff0000]CryptoPricer full request[/color][/b]

btc usd 0 all

Returns the current price of 1 btc in usd.

The price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.



[b][color=ff0000]Next section[/color][/b]

This section explains the preceeding section''',resizedText)

    def testApplyRightShift(self):
        text = '''<date time> possible values:

    [b][cy]0[/cy][/b] for RT

    [b][cy]21/12 or 21/12/19 or 21/12/2019[/c][/b]. If no year is specified,
    current year is assumed. If no time is specified, current
    time is assumed.


    [b][cy]21/12 8:34[/c][/b] --> current year assumed'''

        width = 54
        leftShiftStr = '    '
        resizedText = GuiUtil.applyRightShift(text, width, leftShiftStr)
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
        text = '[b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is '
        self.assertEqual(GuiUtil._calculateMarkupsLength(text), 31)

    def test_splitShiftedLongLineToShorterLinesAccountingForCodedMarkup(self):
        line = '    [b][cy]21/12 or 21/12/19 or 21/12/2019[/c][/b]. If no year is specified,'
        width = 54
        leftShiftStr = '    '
        shortenedLineList = GuiUtil._splitLongLineToShorterLinesAccountingForMarkup(line, width, leftShiftStr)

        self.assertEqual(shortenedLineList[0], '    [b][cy]21/12 or 21/12/19 or 21/12/2019[/c][/b]. If no year is')
        self.assertEqual(shortenedLineList[1], '    specified,')

    def test_splitShiftedLongLineToShorterLinesAccountingForDecodedMarkup(self):
        line = '    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is specified,'
        width = 54
        leftShiftStr = '    '
        shortenedLineList = GuiUtil._splitLongLineToShorterLinesAccountingForMarkup(line, width, leftShiftStr)

        self.assertEqual(shortenedLineList[0],
                         '    [b][color=ffff00ff]21/12 or 21/12/19 or 21/12/2019[/color][/b]. If no year is')
        self.assertEqual(shortenedLineList[1], '    specified,')


if __name__ == '__main__':
    unittest.main()
