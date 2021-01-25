from helputil import HelpUtil
from scrollablelabelpopup import ScrollableLabelPopup

from kivy import platform

class HelpPopup(ScrollableLabelPopup):
	def getContPageList(self):
		if platform == 'win':
			helpFileName = 'gui\\help.txt'
		else:
			helpFileName = 'help.txt'

		with open(helpFileName) as helpFile:
			formattedHelpTextPageList = HelpUtil.sizeParagraphsForKivyLabelFromFile(helpFile, self.textWidth)

		return formattedHelpTextPageList
