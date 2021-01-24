from helputil import HelpUtil
from scrollablelabelpopup import ScrollableLabelPopup


class HelpPopup(ScrollableLabelPopup):
	def __init__(self, title, **kwargs):
		super().__init__(title, **kwargs)

		with open('help.txt') as helpFile:
			formattedHelpTextPageList = HelpUtil.sizeParagraphsForKivyLabelFromFile(helpFile, self.textWidth)

		self.setContentPageList(formattedHelpTextPageList)