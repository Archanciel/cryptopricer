import os
from os.path import sep

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from guiutil import GuiUtil

LOAD_AT_START_MSG = ' (load at start activated)'

class FileChooserPopup(BoxLayout):
	LOAD_FILE_POPUP_TITLE = 'Select history file to load'
	SAVE_FILE_POPUP_TITLE = 'Save history to file'
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

	def onSmartPhone(self):
		return GuiUtil.onSmartPhone()
	
	def sizeFileChooser(self):
		"""
		This method sets the popup size and position values used by the rootGUI
		openFileLoadPopup() or openFileSavePopup() methods as well as the file
		chooser	fields size.
		"""
		if os.name != 'posix':
			self.popupSizeProportion_x = 0.8
			self.popupSizeProportion_y = 0.8
			self.popupPos_top = 0.92
			self.gridLayoutPathField.size_hint_y = 0.12
		else:
			self.popupSizeProportion_x = 0.8
			self.popupSizeProportion_y = 0.62

			if self.onSmartPhone():
				self.popupPos_top = 0.98
				self.gridLayoutPathField.size_hint_y = 0.08
			else:
				self.popupPos_top = 0.92
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
			
			if self.onSmartPhone():
				self.sdCardDir = GuiUtil.SD_CARD_DIR_SMARTPHONE
			else:
				self.sdCardDir = GuiUtil.SD_CARD_DIR_TABLET
			
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
			if self.onSmartPhone():
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

		# update load at start checkbox
		
		currentSaveFilePathName = self.currentPathField.text
		
		if currentSaveFilePathName == self.loadAtStartFilePathName:
			self.loadAtStartChkBox.active = True
		else:
			self.loadAtStartChkBox.active = False

		# update save file chooser popup title
		
		self.updateSaveFileChooserPopupTitle(currentSaveFilePathName, self.loadAtStartChkBox.active)
	
	def updateSaveFileChooserPopupTitle(self, currentSaveFilePathName, isLoadAtStartChkboxActive):
		currentSaveFileName = currentSaveFilePathName.split(sep)[-1]
		
		if currentSaveFileName == '':
			# the case when opening the save file dialog after loading a file
			return
		
		if isLoadAtStartChkboxActive:
			self.rootGUI.popup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE,
													  currentSaveFileName) + LOAD_AT_START_MSG
		else:
			self.rootGUI.popup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE, currentSaveFileName)
	
	def toggleLoadAtStart(self, active):
		"""
		Method called when checking/unchecking the load at start checkbox

		:param active:
		"""
		self.updateSaveFileChooserPopupTitle(self.currentPathField.text, active)
