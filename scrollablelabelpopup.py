from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.utils import platform


class ScrollableLabelPopup(Popup):
	contentBox = ObjectProperty()
	scrollView = ObjectProperty
	
	def __init__(self, title, **kwargs):
		
		# defining ScrollableLabelPopup size parameters
		popupSize = None
		self.textWidth = 50

		if platform == 'android':
			popupSize = (980, 1200)
			self.textWidth = 45
		elif platform == 'win':
			popupSize = (400, 450)
			self.textWidth = 54

		# adding FileChooserPopup size parameters to the kwargs dic for the
		# super class
		kwargs['size_hint'] = (None, None)
		kwargs['size'] = popupSize
		kwargs['title'] = title

		super(ScrollableLabelPopup, self).__init__(**kwargs)

	def setContentPageList(self, formattedTextPageList):
		self.formattedTextPageList = formattedTextPageList
		self.currentPage = 0
		self.setContentTextToCurrentPage()
		self.prevPageButton.disabled = True

	def setContentTextToCurrentPage(self):
		self.contentBox.content.text = self.formattedTextPageList[self.currentPage]
	
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
		
		helpPageNumber = len(self.formattedTextPageList)
		
		if self.currentPage == helpPageNumber - 1:
			self.nextPageButton.disabled = True
		else:
			self.nextPageButton.disabled = False

		self.prevPageButton.disabled = False
		self.setContentTextToCurrentPage()
		self.scrollView.scroll_y = 1 # force scrolling to top

