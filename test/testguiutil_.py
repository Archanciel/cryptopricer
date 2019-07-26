import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from guiutil import GuiUtil

class TestGuiUtil(unittest.TestCase):
    def setUp(self):
        pass

    def testSplitLongLineToShorterLines(self):
        note = 'a long class description. Which occupies several lines.'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], 'a long class description.')
        self.assertEqual(multilineNote[1], 'Which occupies several lines.')


    def testSplitLongLineToShorterLinesEmptyNote(self):
        note = ''
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 0)


    def testSplitLongLineToShorterLinesOneWordNoteLenEqualsMaxNoteLineLenMinusOne(self):
        note = '12345678911234567892123456789'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '12345678911234567892123456789')


    def testSplitLongLineToShorterLinesOneWordNoteLenEqualsMaxNoteLineLen(self):
        note = '123456789112345678921234567893'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '123456789112345678921234567893')


    def testSplitLongLineToShorterLinesOneWordNoteLenEqualsMaxNoteLineLenPlusOne(self):
        note = '1234567891123456789212345678931'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '1234567891123456789212345678931')


    def testSplitLongLineToShorterLinesTwoWordsNoteLenEqualsMaxNoteLineLen(self):
        note = '12345678911234 567892123456789'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 1)
        self.assertEqual(multilineNote[0], '12345678911234 567892123456789')


    def testSplitLongLineToShorterLinesTwoWordsNoteLenEqualsMaxNoteLineLenPlusOne(self):
        note = '123456789112345 678921234567893'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345')
        self.assertEqual(multilineNote[1], '678921234567893')


    def testSplitLongLineToShorterLinesTwoWordsNoteLenEqualsMaxNoteLineLenPlusTwo(self):
        note = '123456789112345 6789212345678931'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345')
        self.assertEqual(multilineNote[1], '6789212345678931')


    def testSplitLongLineToShorterLinesTwoWordsFirstEqualsMaxLen(self):
        note = '123456789112345678921234567893 2'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345678921234567893')
        self.assertEqual(multilineNote[1], '2')


    def testSplitLongLineToShorterLinesTwoWordsFirstEqualsMaxLenPlusOne(self):
        note = '1234567891123456789212345678931 3'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '1234567891123456789212345678931')
        self.assertEqual(multilineNote[1], '3')


    def testSplitLongLineToShorterLinesTwoWordsFirstAndSecondEqualsMaxLen(self):
        note = '123456789112345678921234567893 123456789112345678921234567893'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '123456789112345678921234567893')
        self.assertEqual(multilineNote[1], '123456789112345678921234567893')


    def testSplitLongLineToShorterLinesTwoWordsFirstAndSecondEqualsMaxLenPlusOne(self):
        note = '1234567891123456789212345678931 1234567891123456789212345678931'
        maxNoteLineLen = 30

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], '1234567891123456789212345678931')
        self.assertEqual(multilineNote[1], '1234567891123456789212345678931')

    def testSplitLongLineToShorterLinesLargeNote(self):
        note = 'ERROR - :seqdiag_loop_start tag located on line 53 of file containing class ClassLoopTagOnMethodNotInRecordFlow is placed on an instruction calling method doC4NotRecordedInFlow() which is not part of the execution flow recorded by GuiUtil.'
        maxNoteLineLen = 150

        multilineNote = GuiUtil.splitLongLineToShorterLines(note, maxNoteLineLen)

        self.assertEqual(len(multilineNote), 2)
        self.assertEqual(multilineNote[0], 'ERROR - :seqdiag_loop_start tag located on line 53 of file containing class ClassLoopTagOnMethodNotInRecordFlow is placed on an instruction calling')
        self.assertEqual(multilineNote[1], 'method doC4NotRecordedInFlow() which is not part of the execution flow recorded by GuiUtil.')

    def testSplitLongLineToShorterLinesLargeNoteWithEndOfLine(self):
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in USD. The price is an average of the btc quotation on all the exchanges.'
        maxNoteLineLen = 50

        multilineNote = GuiUtil.splitLongLineToShorterLines(text, maxNoteLineLen)

#        self.assertEqual(len(multilineNote), 6)
        self.assertEqual(multilineNote[0], 'CryptoPricer full request')
        self.assertEqual(multilineNote[1], '\n\n')
        self.assertEqual(multilineNote[2], 'btc usd 0 all')
        self.assertEqual(multilineNote[3], '\n\n')
        self.assertEqual(multilineNote[4], 'Returns the current price of 1 btc in USD. The')
        self.assertEqual(multilineNote[5], 'price is an average of the btc quotation on all the exchanges.')
        self.assertEqual(multilineNote[1], 'method doC4NotRecordedInFlow() which is not part of the execution flow recorded by GuiUtil.')

    def testGetListOfParagraphs(self):
        text = 'CryptoPricer full request\n\nbtc usd 0 all\n\nReturns the current price of 1 btc in usd.\nThe price is an average of the btc quotation on all the exchanges.\n\n\nNext section.\n'

        list = GuiUtil.getListOfParagraphs(text)
        self.assertEqual(len(list), 9)
        self.assertEqual(list[0],'CryptoPricer full request')
        self.assertEqual(list[1],'\n\n')
        self.assertEqual(list[2],'btc usd 0 all')
        self.assertEqual(list[3],'\n\n')
        self.assertEqual(list[4],'Returns the current price of 1 btc in usd.')
        self.assertEqual(list[5],'\n')
        self.assertEqual(list[6],'The price is an average of the btc quotation on all the exchanges.')
        self.assertEqual(list[7],'\n\n\n')
        self.assertEqual(list[8],'Next section.')

    def testSplitLongWarningWithDotsToFormattedLines(self):
        longWarning = "No control flow recorded.\nMethod activate() called with arguments projectPath=<D:\Development\Python\seqdiagbuilder>, entryClass=<Caller>, entryMethod=<call>, classArgDic=<{'FileReader_1': ['testfile.txt'], 'FileReader_2': ['testfile2.txt']}>: True.\nMethod recordFlow() called: True.\nSpecified entry point: Caller.call reached: False."

        multiLineFormattedWarning = GuiUtil.splitLongWarningToFormattedLines(longWarning)

        self.assertEqual(
"""<b><font color=red size=14>  No control flow recorded.</font></b>
<b><font color=red size=14>  Method activate() called with arguments projectPath=<D:\Development\Python\seqdiagbuilder>, entryClass=<Caller>, entryMethod=<call>, classArgDic=<{'FileReader_1': ['testfile.txt'], 'FileReader_2': ['testfile2.txt']}>: True.</font></b>
<b><font color=red size=14>  Method recordFlow() called: True.</font></b>
<b><font color=red size=14>  Specified entry point: Caller.call reached: False.</font></b>
""", multiLineFormattedWarning)

    def testSplitLongWarningWithBackslashNToFormattedLines(self):
        longWarning = "No control flow recorded.\nMethod activate() called with arguments projectPath=<D:\Development\Python\seqdiagbuilder>, entryClass=<Caller>, entryMethod=<call>, classArgDic=<{'FileReader_1': ['testfile.txt'], 'FileReader_2': ['testfile2.txt']}>: True.\nMethod recordFlow() called: True\nSpecified entry point: Caller.call reached: False."

        multiLineFormattedWarning = GuiUtil.splitLongWarningToFormattedLines(longWarning)

        self.assertEqual(
"""<b><font color=red size=14>  No control flow recorded.</font></b>
<b><font color=red size=14>  Method activate() called with arguments projectPath=<D:\Development\Python\seqdiagbuilder>, entryClass=<Caller>, entryMethod=<call>, classArgDic=<{'FileReader_1': ['testfile.txt'], 'FileReader_2': ['testfile2.txt']}>: True.</font></b>
<b><font color=red size=14>  Method recordFlow() called: True</font></b>
<b><font color=red size=14>  Specified entry point: Caller.call reached: False.</font></b>
""", multiLineFormattedWarning)

if __name__ == '__main__':
    unittest.main()
