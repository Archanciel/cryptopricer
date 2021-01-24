from helputil import HelpUtil
from scrollablelabelpopup import ScrollableLabelPopup


class HelpPopup(ScrollableLabelPopup):
	def getContPageList(self):
		with open('help.txt') as helpFile:
			formattedHelpTextPageList = HelpUtil.sizeParagraphsForKivyLabelFromFile(helpFile, self.textWidth)

		return formattedHelpTextPageList
