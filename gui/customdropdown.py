import os

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown

from gui.cryptopricergui import STATUS_BAR_ERROR_SUFFIX, STATUS_BAR_WARNING_SUFFIX
from gui.guiutil import GuiUtil


class CustomDropDown(DropDown):
	saveButton = ObjectProperty(None)
	statusToRequestInputButton = ObjectProperty(None)
	
	def __init__(self, owner):
		super().__init__()
		self.owner = owner

		if os.name == 'posix':
			if GuiUtil.onSmartPhone():
				self.auto_width = False
				self.width = dp(self.owner.configMgr.dropDownMenuWidth)

	def showLoad(self):
		message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.dataPath, message):
			self.owner.openFileLoadPopup()

	def showSave(self):
		message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

		if self.owner.ensureDataPathExist(self.owner.dataPath, message):
			self.owner.openFileSavePopup()

	def help(self):
		self.owner.displayHelp()
	
	def copyStatusBarStrToRequestEntry(self):
		statusBarStr = self.owner.statusBarTextInput.text
		statusBarStr = statusBarStr.replace(STATUS_BAR_ERROR_SUFFIX, '').replace(STATUS_BAR_WARNING_SUFFIX, '')

		self.owner.requestInput.text = statusBarStr
		self.owner.statusBarTextInput.text = ''
		self.statusToRequestInputButton.disabled = True
		self.owner.refocusOnRequestInput()
		self.dismiss()