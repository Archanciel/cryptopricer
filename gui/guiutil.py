import os

class GuiUtil:
    SD_CARD_DIR_TABLET = '/storage/0000-0000'
    SD_CARD_DIR_SMARTPHONE = '/storage/9016-4EF8'
    
    @staticmethod
    def onSmartPhone():
        return os.path.isdir(GuiUtil.SD_CARD_DIR_SMARTPHONE)
        
if __name__ == "__main__":
	gu = GuiUtil()
	
	print(gu.onSmartPhone())
