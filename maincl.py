import os

from controller import Controller
from consoleoutputformatter import ConsoleOutputFormatter
from configurationmanager import ConfigurationManager
from pricerequester import PriceRequester

def main():
	'''
	Maincl means main command line !
	Command line main which instanciate a Controller which uses a ConsoleOutputFormatter
	instead of a GuiOutputFormatter, what maingui does !
	'''
	if os.name == 'posix':
		configPath = '/sdcard/cryptopricer.ini'
	else:
		configPath = 'c:\\temp\\cryptopricer.ini'

	configMgr = ConfigurationManager(configPath)
	controller = Controller(ConsoleOutputFormatter(configMgr), configMgr, PriceRequester())

	controller.commandLineLoop()
	
if __name__ == '__main__':
	main()
