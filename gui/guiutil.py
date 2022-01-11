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
		
if __name__ == "__main__":
	gu = GuiUtil()
	
	print(gu.onSmartPhone())
