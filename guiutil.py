import re

class GuiUtil:
    @staticmethod
    def _splitLongLineToShorterLines(longLine, shorterLinesMaxLen):
        '''
        Splits the longLine string into lines not exceeding maxNoteLineLen and returns the lines
        into a list.

        :param longLine:
        :param shorterLinesMaxLen:
        :return:
        '''
        if longLine == '':
            return []

        noteWordList = longLine.split(' ')
        noteLine = noteWordList[0]
        noteLineLen = len(noteLine)
        noteLineList = []

        for word in noteWordList[1:]:
            wordLen = len(word)

            if noteLineLen + wordLen + 1 > shorterLinesMaxLen:
                noteLineList.append(noteLine)
                noteLine = word
                noteLineLen = wordLen
            else:
                noteLine += ' ' + word
                noteLineLen += wordLen + 1

        noteLineList.append(noteLine)

        return noteLineList

    @staticmethod
    def _getListOfParagraphs(text):
        '''
        The text input parm contains paragraphs separated by either \n\n\n, \n\n, or \n.

        :param text:
        :return: list of paragraphs AND their separators \n\n\n, \n\n, or \n.
        '''
        pattern = r'([\w .-\[\]/]+)(\n\n\n|\n\n|\n|.*)'
        listOfParagraphs = []

        for match in re.finditer(pattern, text):
            for subGroup in match.groups():
                if subGroup:
                    listOfParagraphs.append(subGroup)

        return listOfParagraphs

    @staticmethod
    def _getListOfSizedParagraphs(longParagraphLineStr, width):
        '''
        Returns a list of lines corresponding to the input markupedStr parm.
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
            else:
                shortenedLines = GuiUtil._splitLongLineToShorterLines(line, width)
                listOfLimitedWidthParagraphs.extend(shortenedLines)

        return listOfLimitedWidthParagraphs

    @staticmethod
    def sizeParagraphsToSmallerWidth(longParagraphLineStr, width):
        '''
        Returns a string corresponding to the input markupedStr parm,
        but with lines shortened to be smaller or equal to the passed width.

        :param longParagraphLineStr: string containing paragraphs separated by \n\n\n, \n\n
                                     or \n
        :param width: line width in char number
        :return: string of shorter lines and \n\n\n, \n\n or \n
        '''
        listOfLimitedWidthParagraphs = GuiUtil._getListOfSizedParagraphs(longParagraphLineStr, width)
        sizedParagraphLineStr = ''

        for line in listOfLimitedWidthParagraphs:
            if '\n' in line:
                sizedParagraphLineStr += line
            else:
                sizedParagraphLineStr += '\n' + line

        return sizedParagraphLineStr

    @staticmethod
    def decodeMarkup(markupedStr):
        '''
        Returns a string corresponding to the input markupedStr parm containing coded
        markups with them replaced by Kivy markups.

        :param markupedStr: string containing coded markups
        :return: string containing Kivy markups
        '''

        replaceTupleList = [("[cr]", "[color=ff0000]"),
                            ("[cg]", "[color=19ff52ff]"),
                            ("[/c]", "[/color]")]
        
        # Iterate over the strings to be replaced
        for code, replCode in replaceTupleList:
            # Check if string is in the main string
            if code in markupedStr:
                # Replace the string
                markupedStr = markupedStr.replace(code, replCode)

        return '\n' + markupedStr