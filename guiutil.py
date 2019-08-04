import re

TAB_SPACES = '    '
TAB_CODE = '[t]'
TAB_SIZE = 4


class GuiUtil:
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
        Splits the longLine string into lines not exceeding shorterLinesMaxLen and returns the lines
        into a list.

        :param longLine:
        :param shorterLinesMaxLen:
        :return:
        '''
        if longLine == '':
            return []

        shorterLinesMaxLen -= TAB_SIZE
        wordList = longLine.split(' ')
        shortenedLine = wordList[0]
        markupsLen = GuiUtil._calculateMarkupsLength(longLine)
        shortenedLineLen = -markupsLen + len(shortenedLine)
        shortenedLineList = []

        for word in wordList[1:]:
            wordLen = len(word)

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
    def _getListOfParagraphs(text):
        '''
        The text input parm contains paragraphs separated by either \n\n\n, \n\n, or \n.

        :param text:
        :return: list of paragraphs AND their separators \n\n\n, \n\n, or \n.
        '''
        pattern = r'([\w .,:\-\[\]/*<>=\'\(\)]+)(\n\n\n\n|\n\n\n|\n\n|\n|.*)'
        listOfParagraphs = []

        for match in re.finditer(pattern, text):
            for subGroup in match.groups():
                if subGroup:
                    if '\n' in subGroup:
                        subGroup = subGroup[:-1]
                    listOfParagraphs.append(subGroup)

        return listOfParagraphs

    @staticmethod
    def _getListOfSizedParagraphs(longParagraphLineStr, width):
        '''
        Returns a list of lines corresponding to the input longParagraphLineStr parm.
        The returned lines do not exceed the passed width.

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: list of lines and \n\n\n, \n\n or \n
        '''
        listOfOriginalWidthParagraphs = GuiUtil._getListOfParagraphs(longParagraphLineStr)
        listOfLimitedWidthParagraphs = []

        for line in listOfOriginalWidthParagraphs:
            if '\n' in line:
                listOfLimitedWidthParagraphs.append(line)
            elif TAB_CODE in line:
                shortenedLines = GuiUtil._splitTabbedLineToShorterTabbedLines(line, width)
                listOfLimitedWidthParagraphs.extend(shortenedLines)
            else:
                if line != '':
                    listOfLimitedWidthParagraphs.extend([line])

        return listOfLimitedWidthParagraphs

    @staticmethod
    def sizeParagraphsToSmallerWidth(longParagraphLineStr, width):
        '''
        Returns a string corresponding to the input longParagraphLineStr parm,
        but with lines shortened to be smaller or equal to the passed width.

        This method is no longer used by CriptoPricerGui.py since it is simpler
        to use the capacity of the Kivy Label used in the ScrollablePopup to
        format the lines of words according to the Label effective width. This
        width will be different on each Android device on which CriptoPricerGui
        is executed !

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: string of shorter lines and \n\n\n, \n\n or \n
        '''
        pattern = r''
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
            if code in longParagraphLineStr:
                # Replace the string
                longParagraphLineStr = longParagraphLineStr.replace(code, replCode)

        tabEncodedLongParagraphLineStr = GuiUtil._encodeTabbedText(longParagraphLineStr.splitlines())
        listOfLimitedWidthParagraphs = GuiUtil._getListOfSizedParagraphs(tabEncodedLongParagraphLineStr, width)
        sizedParagraphLineStr = ''

        for line in listOfLimitedWidthParagraphs:
            if '\n' in line:
                sizedParagraphLineStr += line
            else:
                sizedParagraphLineStr += '\n' + line

        tabDecodedLongParagraphLineStr = GuiUtil._decodeTabbedText(sizedParagraphLineStr)

        return tabDecodedLongParagraphLineStr

    @staticmethod
    def decodeMarkup(markupedStr):
        '''
        Returns a string corresponding to the input longParagraphLineStr parm containing coded
        markups with them replaced by Kivy markups.

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

        return '\n' + markupedStr

    @staticmethod
    def applyRightShift(longParagraphLineStr, width, leftShiftStr):
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
            if code in longParagraphLineStr:
                # Replace the string
                longParagraphLineStr = longParagraphLineStr.replace(code, replCode)

        listOfLimitedWidthParagraphs = GuiUtil._splitLongLineToShorterLinesAccountingForMarkup(longParagraphLineStr,
                                                                                               width)

        return '\n' + longParagraphLineStr

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
        listOfOriginalWidthParagraphs = GuiUtil._getListOfShiftedAndMarkedUpSizedParagraphs(longParagraphLineStr, width)
        listOfLimitedWidthParagraphs = []

        for line in listOfOriginalWidthParagraphs:
            if '\n' in line:
                listOfLimitedWidthParagraphs.append(line)
            else:
                shortenedLines = GuiUtil._splitLongLineToShorterLines(line, width)
                listOfLimitedWidthParagraphs.extend(shortenedLines)

        return listOfLimitedWidthParagraphs

    @staticmethod
    def _encodeTabbedText(lineList):
        encodedLinesList = []
        tabMode = False
        pattern = r'^' + TAB_SPACES

        for line in lineList:
            if re.match(pattern, line):
                tabMode = True
                line = re.sub(pattern, TAB_CODE, line)
            else:
                if tabMode:
                    tabMode = False

            encodedLinesList.append(line)

        return '\n'.join(encodedLinesList)

    @staticmethod
    def _decodeTabbedText(paragraphStr):
        return paragraphStr.replace(TAB_CODE, TAB_SPACES)

    @staticmethod
    def _calculateMarkupsLength(lineWithMarkups):
        pattern = r"(\[[\w/=]+\])"
        markupsLen = 0

        for match in re.finditer(pattern, lineWithMarkups):
            markupsLen += len(match.group())

        return markupsLen