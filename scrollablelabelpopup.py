from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.utils import platform

from guiutil import GuiUtil

class ScrollableLabelPopup(Popup):
	contentBox = ObjectProperty()
	scrollView = ObjectProperty

	def __init__(self, title, **kwargs):
		popupSize = None
		width = 50
		
		# defining ScrollableLabelPopup size parameters
		if platform == 'android':
			popupSize = (980, 1200)
			width = 45
		elif platform == 'win':
			popupSize = (400, 450)
			width = 54
		
		# adding FileChooserPopup size parameters to the kwargs dic for the
		# super class
		kwargs['size_hint'] = (None, None)
		kwargs['size'] = popupSize
		kwargs['title'] = title
		
		super().__init__(**kwargs)
		
		with open('help.txt') as helpFile:
			formatedHelpTextPageList = GuiUtil.sizeParagraphsForKivyLabelFromFile(helpFile, width)

		self.setContentPageList(formatedHelpTextPageList)

	def setContentPageList(self, formatedTextPageList):
		self.formatedTextPageList = formatedTextPageList
		self.currentPage = 0
		self.setContentTextToCurrentPage()
		self.prevPageButton.disabled = True

	def setContentTextToCurrentPage(self):
		self.contentBox.content.text = self.formatedTextPageList[self.currentPage]
	
	def previousPage(self):
		self.currentPage -= 1

		if self.currentPage == 0:
			self.prevPageButton.disabled = True
		else:
			self.prevPageButton.disabled = False

		self.nextPageButton.disabled = False
		self.setContentTextToCurrentPage()
		self.scrollView.scroll_y = 0 # force scrolling to bottom

	def nextPage(self):
		self.currentPage += 1
		
		helpPageNumber = len(self.formatedTextPageList)
		
		if self.currentPage == helpPageNumber - 1:
			self.nextPageButton.disabled = True
		else:
			self.nextPageButton.disabled = False

		self.prevPageButton.disabled = False
		self.setContentTextToCurrentPage()
		self.scrollView.scroll_y = 1 # force scrolling to top