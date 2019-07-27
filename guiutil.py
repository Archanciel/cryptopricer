import re

class GuiUtil:
    @staticmethod
    def splitLongLineToShorterLines(longLine, shorterLinesMaxLen):
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
    def getListOfParagraphs(text):
        '''
        The text input parm contains paragraphs separated by either \n\n\n, \n\n, or \n.

        :param text:
        :return: list of paragraphs AND their separators \n\n\n, \n\n, or \n.
        '''
        pattern = r'([\w .-]+)(\n\n\n|\n\n|\n|.*)'
        listOfParagraphs = []

        for match in re.finditer(pattern, text):
            for subGroup in match.groups():
                if subGroup:
                    listOfParagraphs.append(subGroup)

        return listOfParagraphs

    @staticmethod
    def splitLongWarningToFormattedLines(warningStr):
        '''

        :param warningStr:
        :return:
        '''
        formattedWarnings = ''
        lines = warningStr.split('\n')

        for line in lines:
            formattedWarnings += '<b><font color=red size=14>  {}</font></b>\n'.format(line)

        return formattedWarnings