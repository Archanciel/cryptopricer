import os

from controller import Controller
from consoleoutputformater import ConsoleOutputFormater
from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester

def main():
	'''
	Maincl means main command line !
	Command line main which instanciate a Controller which uses a ConsoleOutputFormater
	instead of a GuiOutputFormater, what maingui does !
	'''
	if os.name == 'posix':
		configPath = '/sdcard/cryptopricer.ini'
	else:
		configPath = 'c:\\temp\\cryptopricer.ini'

	configMgr = ConfigurationManager(configPath)
	controller = Controller(ConsoleOutputFormater(configMgr), configMgr, PriceRequester())

	controller.run()
	
if __name__ == '__main__':
	main()
