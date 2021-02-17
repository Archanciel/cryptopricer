from kivy import platform
from kivy.uix.popup import Popup

from gui.guiutil import GuiUtil


class AbstractPopup(Popup):
	"""
	This class can not derive from both Popup and ABCMeta ! Its role is to uniformize the
	popup size and position setting of its subclasses.
	"""
	def __init__(self, **kwargs):
		
		popupSizeProportion_x = 1
		popupSizeProportion_y = 1
		popupPos_top = 1
		
		# defining FileChooserPopup size parameters
		if platform == 'android':
			popupSizeProportion_y = 0.62
			
			if self.onSmartPhone():
				popupSizeProportion_x = 0.95
				popupPos_top = 0.98
			else:
				# on tablet
				popupSizeProportion_x = 0.8
				popupPos_top = 0.92
		elif platform == 'win':
			popupSizeProportion_x = 0.8
			popupSizeProportion_y = 0.8
			popupPos_top = 0.92
		
		# adding FileChooserPopup size parameters to the kwargs dic for the
		# super class
		kwargs['size_hint'] = (popupSizeProportion_x, popupSizeProportion_y)
		kwargs['pos_hint'] = {'top': popupPos_top}
		
		super().__init__(**kwargs)
		
	def onSmartPhone(self):
		return GuiUtil.onSmartPhone()