import os
import re

TAB_SPACES = '    '
TAB_CODE = '[t]'
TAB_SIZE = 4
LINE_BREAK_CODE = '[n]' # code used in the help file to force a line break
LINE_BREAK_CODE_REGEXP = '\[n\]' # regexp version
PAGE_BREAK_CODE = '[p]' # code used in the help file to indicate a page break
PAGE_BREAK_CODE_REGEXP = '\[p\].*' # regexp version

class HelpUtil:

    @staticmethod
    def _splitLongLineToShorterLines(longLine, shorterLinesMaxLen):
        '''
        Splits the longLine string into lines not exceeding shorterLinesMaxLen and returns the lines
        into a list.

        :param longLine:
        :param shorterLinesMaxLen:
        :return:
        '''
        if longLine == '':
            return []

        wordList = longLine.split(' ')
        shortenedLine = wordList[0]
        shortenedLineLen = len(shortenedLine)
        shortenedLineList = []

        for word in wordList[1:]:
            wordLen = len(word)

            if shortenedLineLen + wordLen + 1 > shorterLinesMaxLen:
                shortenedLineList.append(shortenedLine)
                shortenedLine = word
                shortenedLineLen = wordLen
            else:
                shortenedLine += ' ' + word
                shortenedLineLen += wordLen + 1

        shortenedLineList.append(shortenedLine)

        return shortenedLineList

    def _splitTabbedLineToShorterTabbedLines(longLine, shorterLinesMaxLen):
        '''
        Splits the longLine string into lines starting with a tab code and not exceeding
        shorterLinesMaxLen and returns the shortened lines into a list of tab coded lines.

        This method takes care of the existence of any Kivy markup, which must not be accounted
        into the size of the resized line.

        :param longLine:
        :param shorterLinesMaxLen:
        :return:
        '''
        if longLine == '':
            return []

        shorterLinesMaxLen -= TAB_SIZE
        wordList = longLine.split(' ')
        shortenedLine = wordList[0]
        markupsLen = HelpUtil._calculateMarkupsLength(shortenedLine)
        shortenedLineLen = len(shortenedLine) - markupsLen
        shortenedLineList = []

        for word in wordList[1:]:
            markupsLen = HelpUtil._calculateMarkupsLength(word)
            wordLen = len(word) - markupsLen

            if shortenedLineLen + wordLen + 1 > shorterLinesMaxLen:
                shortenedLineList.append(shortenedLine)
                shortenedLine = TAB_CODE + word
                shortenedLineLen = wordLen
            else:
                shortenedLine += ' ' + word
                shortenedLineLen += wordLen + 1

        shortenedLineList.append(shortenedLine)

        return shortenedLineList

    @staticmethod
    def _getListOfOriginalSizeParagraphs(text):
        '''
        The text input parm contains paragraphs separated by either \n\n\n, \n\n, or \n.
        The method split the input string into a list of paragraphs AND their separators \n\n\n,
        \n\n, or \n.

        :param text:
        :return: list of paragraphs AND their separators \n\n\n, \n\n, or \n.
        '''
        pattern = r'([\w .,:\-\[\]/*<>=\'\(\)!]+)(\n\n\n\n|\n\n\n|\n\n|\n|.*)'
        listOfParagraphs = []

        for match in re.finditer(pattern, text):
            for subGroup in match.groups():
                if subGroup:
                    if '\n' in subGroup:
                        subGroup = subGroup[:-1]
                    listOfParagraphs.append(subGroup)

        return listOfParagraphs

    @staticmethod
    def _getListOfParagraphsSizedForKivyLabel(longParagraphLineStr, width):
        '''
        The Kivy label handles correctly any sized lines, putting words on the next line when the
        label width is reached. But in case of right shifted paragraphs(i.e starting with a tab code),
        additional processing must be performed sto split the shifted paragraph into shifted lines,
        i.e lines starting with a tab code ([t]).

        Returns a list of lines corresponding to the input longParagraphLineStr parm.
        The returned lines correspond to the original paragraph if it contai×s no tab code. Otherwise,
        the tabbed paragraph is splitted into correctly sized tabbed lines since the Kivy label does
        not handles correctly right shifted lines.

        So, the width parm is relevant only for handling right shifted paragraphs.

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: list of lines and \n\n\n, \n\n or \n
        '''

        # first, split the longParagraphLineStr into original size paragraphs.
        listOfOriginalWidthParagraphs = HelpUtil._getListOfOriginalSizeParagraphs(longParagraphLineStr)

        # then, handles each original size paragraph either leaving it unchanged if it is
        # not a right shifted paragraph, or splitting it into correctly shortened lines if
        # it is right shifted.
        listOfLimitedWidthParagraphs = []

        for line in listOfOriginalWidthParagraphs:
            if '\n' in line:
                listOfLimitedWidthParagraphs.append(line)
            elif TAB_CODE in line:
                # handling right shifted paragraph
                shortenedLines = HelpUtil._splitTabbedLineToShorterTabbedLines(line, width)
                listOfLimitedWidthParagraphs.extend(shortenedLines)
            else:
                if line != '':
                    # leaving regular paragraph unchanged
                    listOfLimitedWidthParagraphs.extend([line])

        return listOfLimitedWidthParagraphs

    @staticmethod
    def _sizeParagraphsForKivyLabel(longParagraphLineStr, width):
        '''
        Returns a string corresponding to the input longParagraphLineStr parm,
        but with lines shortened to be smaller or equal to the passed width.

        This method is no longer used by CriptoPricerGui.py since it is simpler
        to use the capacity of the Kivy Label used in the ScrollableLabelPopup to
        format the lines of words according to the Label effective width. This
        width will be different on each Android device on which CriptoPricerGui
        is executed !

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: string of shorter lines and \n\n\n, \n\n or \n
        '''

        # replacing short markup codes by full Kivy markup codes
        decodedMarkupParagraphStr = HelpUtil._decodeMarkups(longParagraphLineStr)

        # replacing spaces in line beginning by spaces (shifted or tabbed lines) by a tab code ([t])
        # to facilitate futher resizing of paragraphs.
        tabEncodedLongParagraphLineStr = HelpUtil._encodeShiftedLinesWithTabCode(decodedMarkupParagraphStr.splitlines())

        # sizing the paragraph so that they are correctly displayed in a Kivy label. Only the tabbed
        # paragraphs are splitted in shorter tabbed lines
        listOfResizedParagraphs = HelpUtil._getListOfParagraphsSizedForKivyLabel(tabEncodedLongParagraphLineStr, width)

        # reconstructing a string for the Kivy label
        resizedParagraphLineStr = ''

        for line in listOfResizedParagraphs:
            if '\n' in line:
                resizedParagraphLineStr += line
            else:
                resizedParagraphLineStr += '\n' + line

        # replacing the [t] tab code by its correspnding spaces
        tabDecodedResizedParagraphLineStr = HelpUtil._decodeTabCodedShiftedLine(resizedParagraphLineStr)

        return tabDecodedResizedParagraphLineStr

    @staticmethod
    def _decodeMarkups(markupedStr):
        '''
        The input markupedStr parm contains coded markups ([cr] for setting the next words to red,
        for example). The method replaces the markup codes with full Kivy markups.

        :param markupedStr: string containing coded markups
        :return: string containing Kivy markups
        '''

        replaceTupleList = [("[cr]", "[color=ff0000]"),
                            ("[cg]", "[color=19ff52ff]"),
                            ("[cy]", "[color=ffff00ff]"),
                            ("[/cr]", "[/color]"),
                            ("[/cg]", "[/color]"),
                            ("[/cy]", "[/color]"),
                            ("[/c]", "[/color]")]
        
        # Iterate over the strings to be replaced
        for code, replCode in replaceTupleList:
            # Check if string is in the main string
            if code in markupedStr:
                # Replace the string
                markupedStr = markupedStr.replace(code, replCode)

        return markupedStr

    @staticmethod
    def _getListOfShiftedAndMarkedUpSizedParagraphs(longParagraphLineStr, width):
        '''
        Returns a list of lines corresponding to the input longParagraphLineStr parm.
        The returned lines do not exceed the passed width.

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: list of lines and \n\n\n, \n\n or \n
        '''
        listOfOriginalWidthParagraphs = HelpUtil._getListOfShiftedAndMarkedUpSizedParagraphs(longParagraphLineStr, width)
        listOfLimitedWidthParagraphs = []

        for line in listOfOriginalWidthParagraphs:
            if '\n' in line:
                listOfLimitedWidthParagraphs.append(line)
            else:
                shortenedLines = HelpUtil._splitLongLineToShorterLines(line, width)
                listOfLimitedWidthParagraphs.extend(shortenedLines)

        return listOfLimitedWidthParagraphs

    @staticmethod
    def _encodeShiftedLinesWithTabCode(lineList):
        '''
        Replaces line begin tab spaces by a tab code ([t]) in the lines contained in the lineList input
        parm. Returns a tab encoded string.

        Here are example of shifted lines which are correctly handled by the method:

        Shifted lines separated by a blank line:
        <date time> possible values:

            0 for RT

            21/12 or 21/12/19 or 21/12/2019. If no year is specified, current year is assumed. If no time is specified, current time is assumed.

        Shifted lines with no line break with forcing line break code ([n]):
        Output price qualifiers:

            [n]R = RT
            [n]M = Minute price (precision at the minute)
            [n]C = Close price

        Shifted lines with no line break with forcing line break code ([n]) except on the first
        shifted line:
        [b]Output price qualifiers[/b]:

            R = RT
            [n]M = Minute price (precision at the minute)
            [n]C = Close price

        :param lineList:
        :return: tab encoded string
        '''
        encodedLinesList = []
        leftShiftPattern = r'^' + TAB_SPACES
        leftShiftPatternWithForcedLineBreak = r' ' + TAB_SPACES + LINE_BREAK_CODE_REGEXP
        shiftedLines = None

        for line in lineList:
            if re.search(leftShiftPatternWithForcedLineBreak, line):
                # here, the line contains shifted lines not separated by a blank line,
                # but containing a force line break code ([n]).
                shiftedLines = re.compile(leftShiftPatternWithForcedLineBreak).split(line)
                for shiftedLine in shiftedLines:
                    # adding each sub line to the result list (encodedLinesList)
                    if re.match(leftShiftPattern, shiftedLine):
                        if re.match(leftShiftPatternWithForcedLineBreak[1:], shiftedLine):
                            # here, the first shifted line is tagged with the force line
                            # break code ([n]).
                            codedShiftedLine = re.sub(leftShiftPatternWithForcedLineBreak[1:], TAB_CODE, shiftedLine)
                        else:
                            # here, the first shifted line is NOT tagged with the force line
                            # break code ([n]).
                            codedShiftedLine = re.sub(leftShiftPattern, TAB_CODE, shiftedLine)
                    else:
                        codedShiftedLine = TAB_CODE + shiftedLine

                    encodedLinesList.append(codedShiftedLine)
            else:
                if re.match(leftShiftPattern, line):
                    line = re.sub(leftShiftPattern, TAB_CODE, line)

                encodedLinesList.append(line)

        return '\n'.join(encodedLinesList)

    @staticmethod
    def _decodeTabCodedShiftedLine(lineStr):
        return lineStr.replace(TAB_CODE, TAB_SPACES)

    @staticmethod
    def _calculateMarkupsLength(lineWithMarkups):
        '''
        Computes the length os any Kivy markup code contained into the passed lineWithMarkups.
        :param lineWithMarkups:
        :return:
        '''
        pattern = r"(\[[\w/=]+\])"
        markupsLen = 0

        for match in re.finditer(pattern, lineWithMarkups):
            markupsLen += len(match.group())

        return markupsLen

    @staticmethod
    def _removeEOLFromFile(breakedLineFile):
        '''
        Cleverly removes the EOL '\n' on a file content where the not shifted long lines are sized
        for better reading at creation time.

        :param breakedLineFile: file whose long line are split on several lines
        :return: cleverly EOL purged string
        '''
        begLineSpacePattern = r"    \[n\]|    "
        anyAlphaNumCharPattern = r"\w+"
        isLineRightShifted = False
        isFirstLine = True
        noEOLStr = ''

        for line in breakedLineFile.readlines():
            if not re.match(begLineSpacePattern, line) and re.search(anyAlphaNumCharPattern, line) and not re.match(PAGE_BREAK_CODE_REGEXP, line):
#            if not re.match(begLineSpacePattern, line) and re.search(anyAlphaNumCharPattern, line):
                # line is not shifted and contains char (is not only \n)
                if isFirstLine:
                    noEOLStr += line[:-1]
                    isFirstLine = False
                else:
                    # handling the next not shifted line, simply concatenating it to the previous
                    # not shifted lines
                    noEOLStr += ' ' + line[:-1]
            elif re.match(begLineSpacePattern, line) and not isLineRightShifted:
                # handling the first right shifted line
                noEOLStr += line[:-1]
                isLineRightShifted = True
                isFirstLine = True
            elif re.match(begLineSpacePattern, line) and isLineRightShifted:
                # handling the next right shifted line, simply concatenating it to the previous
                # shifted lines
                if LINE_BREAK_CODE in line:
                    line = line[:-1]
                else:
                    line = line[4:-1]  # removing the tab spaces and the EOL \n
                noEOLStr += ' ' + line
                isFirstLine = True
            else:
                # handling empty break line
                noEOLStr += '\n' + line
                isLineRightShifted = False
                isFirstLine = True

        return noEOLStr

    @staticmethod
    def sizeParagraphsForKivyLabelFromFile(breakedLineFile, width):
        '''
        Returns a string corresponding to the content of the file breakedLineFile,
        but with lines shortened to be smaller or equal to the passed width.

        This method is no longer used by CriptoPricerGui.py since it is simpler
        to use the capacity of the Kivy Label used in the ScrollableLabelPopup to
        format the lines of words according to the Label effective width. This
        width will be different on each Android device on which CriptoPricerGui
        is executed !

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: string of shorter lines and \n\n\n, \n\n or \n
        '''

        # cleverly removing line end '\n' in order to simplify further processing
        # for resizinf the text fot the Kivy destination label.
        noEOLText = HelpUtil._removeEOLFromFile(breakedLineFile)

        # resizing the text
        resizedText = HelpUtil._sizeParagraphsForKivyLabel(noEOLText, width)

        # replacing forced line break codes by '\n'
        lineBreakDecodedText = HelpUtil._decodeForcedLineBreak(resizedText)

        # splitting the text into pages according to page break codes
        return HelpUtil._splitTextIntoListOfPages(lineBreakDecodedText)

    @staticmethod
    def _decodeForcedLineBreak(codedStr):
        '''
        This method handles forced line break codes, replacing them with a \n.
        :param codedStr:
        :return:
        '''
        decodedStr = codedStr.replace('    ' + LINE_BREAK_CODE, '\n    ')
        decodedStr = decodedStr.replace(' ' + LINE_BREAK_CODE, '\n')
        decodedStr = decodedStr.replace('\n' + LINE_BREAK_CODE, '\n')

        return decodedStr

    @staticmethod
    def _splitTextIntoListOfPages(textStr):
        '''
        This method handles page break codes, returning a list of page string.
        :param textStr:
        :return:
        '''
        return textStr.split(PAGE_BREAK_CODE)
