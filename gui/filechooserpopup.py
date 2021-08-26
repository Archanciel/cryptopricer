import os
from os.path import sep

from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.utils import platform

from gui.abstractpopup import AbstractPopup
from guiutil import GuiUtil

LOAD_AT_START_MSG = ' (load at start activated)'


class SelectableLabelFileChooser(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	
	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.index = index
		return super(SelectableLabelFileChooser, self).refresh_view_attrs(
			rv, index, data)
	
	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if super(SelectableLabelFileChooser, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	
	def apply_selection(self, rv, index, is_selected):
		''' Respond to the selection of items in the view. '''
		self.selected = is_selected
		
		if is_selected:
			rootGUI = rv.parent.parent.parent.parent.parent
			selectedPath = rv.data[index]['pathOnly']
			
			selectedPath = selectedPath + sep  # adding '\\' is required, otherwise,
			# on Windows, when selecting D:, the
			# directory hosting the utility is
			# selected ! On Android, the file save
			# text input field is not ended by '/'
			# which causes a bug corrected on 15.1.21
			
			rootGUI.fileChooser.path = selectedPath
			rootGUI.currentPathField.text = selectedPath


class SelectableRecycleBoxLayoutFileChooser(FocusBehavior, LayoutSelectionBehavior,
											RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	
	# required to authorise unselecting a selected item
	touch_deselect_last = BooleanProperty(True)


class FileChooserPopup(AbstractPopup):
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
		
		# filling the drive list (on Windows) or memory list (on Android)
		self.fillDriveOrMemoryList()

		# sizing FileChooserPopup widgets. Method defined in sub classes
		self._sizeFileChooser()
		
		# specify pre-selected node by its index in the data
		self.diskRecycleBoxLayout.selected_nodes = [0]
	
	def _sizeFileChooser(self):
		"""
		This method sets the popup size and position values used by the rootGUI
		openFileLoadPopup() or openFileSavePopup() methods as well as the file
		chooser	fields size.
		"""
		if platform == 'android':
			if self.onSmartPhone():
				self.gridLayoutPathField.size_hint_y = 0.08
			else:
				self.gridLayoutPathField.size_hint_y = 0.05
		elif platform == 'win':
			self.gridLayoutPathField.size_hint_y = 0.12
	
	def fillDriveOrMemoryList(self):
		"""
		
		:return:
		"""
		dataLocationFromSetting = self.rootGUI.configMgr.dataPath
		
		if platform == 'android':
			self.pathList.data.append({'text': 'Data file location setting', 'selectable': True,
									   'pathOnly': dataLocationFromSetting})
			self.pathList.data.append({'text': 'Main RAM', 'selectable': True, 'pathOnly': '/storage/emulated/0'})
			
			if self.onSmartPhone():
				self.sdCardDir = GuiUtil.SD_CARD_DIR_SMARTPHONE
			else:
				self.sdCardDir = GuiUtil.SD_CARD_DIR_TABLET
			
			self.pathList.data.append({'text': 'SD card', 'selectable': True, 'pathOnly': self.sdCardDir})
		elif platform == 'win':
			import string
			available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
			
			self.pathList.data.append(
				{'text': 'Data file location setting', 'selectable': True, 'pathOnly': dataLocationFromSetting})
			
			for drive in available_drives:
				self.pathList.data.append({'text': drive, 'selectable': True, 'pathOnly': drive})


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
	
	def _sizeFileChooser(self):
		"""

		:return:
		"""
		super()._sizeFileChooser()
		
		if platform == 'android':
			if self.onSmartPhone():
				self.loadAtStartChkBox.size_hint_x = 0.06
				self.gridLayoutPathField.size_hint_y = 0.16
			else:
				self.loadAtStartChkBox.size_hint_x = 0.06
				self.gridLayoutPathField.size_hint_y = 0.10
		elif platform == 'win':
			self.loadAtStartChkBox.size_hint_x = 0.06
			self.gridLayoutPathField.size_hint_y = 0.30
	
	def handleSelection(self, selection):
		selectionStr = selection[0]
		selectionElemLst = selectionStr.split(sep)
		
		if os.path.isfile(selectionStr):
			pathContainedInSelection = sep.join(selectionElemLst[:-1]) + sep
			fileNameContainedInSelection = selectionElemLst[-1]
		else:
			pathContainedInSelection = selectionStr + sep
			fileNameContainedInSelection = ''
		
		self.currentPathField.text = pathContainedInSelection
		self.currentFileNameField.text = fileNameContainedInSelection
	
	def save(self, pathOnly, pathName, fileName, isLoadAtStart):
		"""

		:param pathOnly:
		:param pathName:
		:param isLoadAtStart:
		:return:
		"""
		if fileName == '':
			# no file selected or file name defined. Load dialog remains open ..
			return
		
		self.rootGUI.saveHistoryToFile(pathOnly, pathName + fileName, isLoadAtStart)
		self.rootGUI.dismissPopup()
	
	def setCurrentLoadAtStartFile(self, loadAtStartFilePathName):
		self.loadAtStartFilePathName = loadAtStartFilePathName
	
	def updateLoadAtStartCheckBox(self):
		"""
		Method called when the currentPath or the currentFileName TextInput field
		content is modified.
		"""
		
		currentSavePath = self.currentPathField.text
		
		# ensure path ends with / or \ according to the OS
		
		if currentSavePath[-1] != sep:
			currentSavePath += sep
			self.currentPathField.text = currentSavePath
		
		currentSaveFileName = self.currentFileNameField.text
		currentSavePathFileName = currentSavePath + currentSaveFileName
		
		# update load at start checkbox
		
		if currentSavePathFileName == self.loadAtStartFilePathName:
			self.loadAtStartChkBox.active = True
		else:
			self.loadAtStartChkBox.active = False
		
		# update save file chooser popup title
		
		self._updateSaveFileChooserPopupTitle(currentSavePath,
											  currentSaveFileName,
											  self.loadAtStartChkBox.active)
	
	def _updateSaveFileChooserPopupTitle(self, currentSavePath, currentSaveFileName, isLoadAtStartChkboxActive):
		if currentSaveFileName == '':
			# the case when opening the save file dialog after loading a file
			return
		
		if isLoadAtStartChkboxActive:
			self.rootGUI.popup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE,
													  currentSaveFileName) + LOAD_AT_START_MSG
		else:
			self.rootGUI.popup.title = '{} {}'.format(FileChooserPopup.SAVE_FILE_POPUP_TITLE, currentSaveFileName)
	
	def toggleLoadAtStart(self, isChkBoxActive):
		"""
		Method called when checking/unchecking the load at start checkbox

		:param isChkBoxActive:
		"""
		self._updateSaveFileChooserPopupTitle(self.currentPathField.text,
											  self.currentFileNameField.text,
											  isChkBoxActive)
