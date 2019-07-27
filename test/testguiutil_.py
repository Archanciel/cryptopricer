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
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\nNext section\n\nThis section explains the preceeding section'

        list = GuiUtil._getListOfParagraphs(text)
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

    def test_getListOfSizedParagraphs(self):
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\nNext section\n\nThis section explains the preceeding section'
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
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\nNext section\n\nThis section explains the preceeding section'
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
        text = 'CryptoPricer full request\nbtc usd 0 all\nReturns the current price of 1 btc in usd.\nThe price is an average of the btc quotation on all the exchanges. It is computed by the crypto prices provider.\n\n\nNext section\nThis section explains the preceeding section'
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

if __name__ == '__main__':
    unittest.main()
