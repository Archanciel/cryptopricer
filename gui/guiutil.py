import os

class GuiUtil:
	SD_CARD_DIR_TABLET = '/storage/0000-0000'
	SD_CARD_DIR_SMARTPHONE_S20 = '/storage/9016-4EF8'
	SD_CARD_DIR_SMARTPHONE_S8 = '/storage/emulated/0'
	
	@staticmethod
	def onSmartPhone():
		if os.path.isdir(GuiUtil.SD_CARD_DIR_SMARTPHONE_S20) or \
		   os.path.isdir(GuiUtil.SD_CARD_DIR_SMARTPHONE_S8):
			return True
		else:
			return False
		
	@staticmethod
	def getSmartPhoneDir():
		"""
		Returns an Android smartphone base directory string or None if the
		application is run on a tablet.
		
		:return:  Android smartphone dir string or None if not on smartphone
		"""
		if os.path.isdir(GuiUtil.SD_CARD_DIR_SMARTPHONE_S20):
			return GuiUtil.SD_CARD_DIR_SMARTPHONE_S20
		elif os.path.isdir(GuiUtil.SD_CARD_DIR_SMARTPHONE_S8):
			return GuiUtil.SD_CARD_DIR_SMARTPHONE_S8
		else:
			return None
	
	@staticmethod
	def getTabletDir():
		"""
		Returns an Android tablet base directory string or None if the
		application is run on a smartphone.

		:return:  Android tablet dir string or None if not on tablet
		"""
		if os.path.isdir(GuiUtil.SD_CARD_DIR_TABLET):
			return GuiUtil.SD_CARD_DIR_TABLET
		else:
			return None
	
	@staticmethod
	def getAndroidSdCardDir():
		"""
		Returns the Android dir containing the cryptopricer.ini file
		"""
		return '/sdcard'
		
if __name__ == "__main__":
	gu = GuiUtil()
	
	print(gu.onSmartPhone())
