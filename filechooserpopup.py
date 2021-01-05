import os

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

SD_CARD_DIR_TABLET = '/storage/0000-0000'
SD_CARD_DIR_SMARTPHONE = '/storage/9016-4EF8'
LOAD_AT_START_MSG = ' (load at start activated)'

class FileChooserPopup(BoxLayout):
	"""
	
	"""
	load = ObjectProperty(None)
#	save = ObjectProperty(None)
	cancel = ObjectProperty(None)
	
	def __init__(self, rootGUI, **kwargs):
		super(FileChooserPopup, self).__init__(**kwargs)
		
		self.sdCardDir = None
		self.rootGUI = rootGUI
		
		# fillig the drive list (on Windows) or memory list (on Android)
		self.fillDriveOrMemoryList()

		# sizing FileChooserPopup widgets. Method defined in sub classes
		self.sizeFileChooser()
		
		# specify pre-selected node by its index in the data
		self.diskRecycleBoxLayout.selected_nodes = [0]

	def sizeFileChooser(self):
		if os.name != 'posix':
			self.popupSizeProportion_x = 0.8
			self.popupSizeProportion_y = 0.8
			self.gridLayoutPathField.size_hint_y = 0.12
		else:
			self.popupSizeProportion_x = 0.8

			if self.sdCardDir == SD_CARD_DIR_SMARTPHONE:
				self.popupSizeProportion_y = 0.72
				self.gridLayoutPathField.size_hint_y = 0.08
			else:
				self.popupSizeProportion_y = 0.82
				self.gridLayoutPathField.size_hint_y = 0.05

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

class SaveFileChooserPopup(FileChooserPopup):
	"""
	
	"""
	def __init__(self, rootGUI, **kwargs):
		super(SaveFileChooserPopup, self).__init__(rootGUI, **kwargs)

		self.loadAtStartFilePathName = ''

	def sizeFileChooser(self):
		"""
		
		:return:
		"""
		super().sizeFileChooser()

		if os.name != 'posix':
			self.loadAtStartChkBox.size_hint_x = 0.06
		else:
			if self.sdCardDir == SD_CARD_DIR_SMARTPHONE:
				self.loadAtStartChkBox.size_hint_x = 0.12
			else:
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

		self.rootGUI.saveHistoryToFile(pathOnly, pathFileName, isLoadAtStart)
		self.rootGUI.dismissPopup()

	def setCurrentLoadAtStartFile(self, loadAtStartFilePathName):
		self.loadAtStartFilePathName = loadAtStartFilePathName
	
	def updateLoadAtStartCheckBox(self):
		"""
		Method called when the currentPath TextInput field content is modified.
		"""
		currentSaveFilePathName = self.currentPathField.text
		if currentSaveFilePathName == self.loadAtStartFilePathName:
			self.loadAtStartChkBox.active = True
		else:
			self.loadAtStartChkBox.active = False
	
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
