import os

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

SD_CARD_DIR_TABLET = '/storage/0000-0000'
path_file_name_text_input = '/storage/9016-4EF8'
LOAD_AT_START_MSG = ' (load at start activated)'

class FileChooserPopup(BoxLayout):
	"""
	
	"""
	POPUP_SIZE_PROPORTION = 0.8
	
	load = ObjectProperty(None)
#	save = ObjectProperty(None)
	cancel = ObjectProperty(None)
	
	def __init__(self, rootGUI, **kwargs):
		super(FileChooserPopup, self).__init__(**kwargs)
		
		self.rootGUI = rootGUI
		
		# sizing FileChooserPopup widgets. Method defined in sub classes
		self.sizeFileChooser()
		
		# fillig the drive list (on Windows) or memory list (on Android)
		self.fillDriveOrMemoryList()

		# specify pre-selected node by its index in the data
		self.diskRecycleBoxLayout.selected_nodes = [0]

	def fillDriveOrMemoryList(self):
		"""
		
		:return:
		"""
		dataLocationFromSetting = self.rootGUI.configMgr.dataPath
		import logging
		logging.info(dataLocationFromSetting)
		
		if os.name != 'posix':
			import string
			available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
			
			self.pathList.data.append(
				{'text': 'Data file location setting', 'selectable': True, 'pathOnly': dataLocationFromSetting})
			
			for drive in available_drives:
				self.pathList.data.append({'text': drive, 'selectable': True, 'pathOnly': drive})
		
		else:
			self.pathList.data.append({'text': 'Data file location setting', 'selectable': True,
			                           'pathOnly': dataLocationFromSetting})
			self.pathList.data.append({'text': 'Main RAM', 'selectable': True, 'pathOnly': '/storage/emulated/0'})
			
			self.sdCardDir = SD_CARD_DIR_SMARTPHONE
			
			if not os.path.isdir(self.sdCardDir):
				self.sdCardDir = SD_CARD_DIR_TABLET
			
			self.pathList.data.append({'text': 'SD card', 'selectable': True, 'pathOnly': self.sdCardDir})


class LoadFileChooserPopup(FileChooserPopup):
	"""
	
	"""
	def __init__(self, rootGUI, **kwargs):
		super(LoadFileChooserPopup, self).__init__(rootGUI, **kwargs)
	
	def sizeFileChooser(self):
		"""
		
		:return:
		"""
		if os.name != 'posix':
			self.popupBoxLayout.size_hint_y = 0.17
			self.currentPathField.size_hint_y = 0.12
		else:
			self.popupBoxLayout.size_hint_y = 0.16
			self.currentPathField.size_hint_y = 0.08

class SaveFileChooserPopup(FileChooserPopup):
	"""
	
	"""
	def __init__(self, rootGUI, **kwargs):
		super(SaveFileChooserPopup, self).__init__(rootGUI, **kwargs)
	
	def sizeFileChooser(self):
		"""
		
		:return:
		"""
		if os.name != 'posix':
			self.gridLayoutPathField.size_hint_y = 0.12
			self.loadAtStartChkBox.size_hint_x = 0.06
		else:
			if self.sdCardDir == SD_CARD_DIR_SMARTPHONE:
				self.gridLayoutPathField.size_hint_y = 0.035
				self.loadAtStartChkBox.size_hint_x = 0.17
			else:
				self.gridLayoutPathField.size_hint_y = 0.023
				self.loadAtStartChkBox.size_hint_x = 0.06
	
	def save(self, pathOnly, pathFileName, isLoadAtStart):
		"""
		
		:param pathOnly:
		:param pathFileName:
		:param isLoadAtStart:
		:return:
		"""
		if pathOnly == pathFileName:
			# no file selected or file name defined. Load dialog remains open ..
			return

		self.rootGUI.saveHistoryToFile(pathOnly,pathFileName, isLoadAtStart)
		self.rootGUI.dismissPopup()

	def toggleLoadAtStart(self, active):
		"""
		
		:param active:
		:return:
		"""
		popupTitle = self.rootGUI.popup.title
		
		if active:
			self.rootGUI.popup.title = popupTitle + LOAD_AT_START_MSG
		else:
			self.rootGUI.popup.title = popupTitle.replace(LOAD_AT_START_MSG, '')
