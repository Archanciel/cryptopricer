from kivy.properties import ObjectProperty
from kivy.utils import platform

from gui.abstractpopup import AbstractPopup

class ScrollableLabelPopup(AbstractPopup):
	contentBox = ObjectProperty()
	scrollView = ObjectProperty
	
	def __init__(self, title, **kwargs):
		
		# defining ScrollableLabelPopup size parameters
		self.textWidth = 50

		if platform == 'android':
			if self.onSmartPhone():
				self.textWidth = 45
			else:
				# on tablet
				self.textWidth = 75

		elif platform == 'win':
			self.textWidth = 54

		kwargs['title'] = title
		super(ScrollableLabelPopup, self).__init__(**kwargs)

		self._setContentPageList()
		
	def _setContentPageList(self):
		self.formattedTextPageList = self._getContentPageList()
		self.currentPage = 0
		self._setContentTextToCurrentPage()
		self.prevPageButton.disabled = True

	def _getContentPageList(self):
		return []
	
	def _setContentTextToCurrentPage(self):
		self.contentBox.content.text = self.formattedTextPageList[self.currentPage]
	
	def previousPage(self):
		self.currentPage -= 1

		if self.currentPage == 0:
			self.prevPageButton.disabled = True
		else:
			self.prevPageButton.disabled = False

		self.nextPageButton.disabled = False
		self._setContentTextToCurrentPage()
		self.scrollView.scroll_y = 0 # force scrolling to bottom

	def nextPage(self):
		self.currentPage += 1
		
		helpPageNumber = len(self.formattedTextPageList)
		
		if self.currentPage == helpPageNumber - 1:
			self.nextPageButton.disabled = True
		else:
			self.nextPageButton.disabled = False

		self.prevPageButton.disabled = False
		self._setContentTextToCurrentPage()
		self.scrollView.scroll_y = 1 # force scrolling to top
