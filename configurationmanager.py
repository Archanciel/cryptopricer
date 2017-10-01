from configobj import ConfigObj
import os

TIME_ZONE = 'timezone'

class ConfigurationManager:
    def __init__(self, filename):
        self.config = ConfigObj(filename)
        self._updated = False

        if len(self.config) == 0:
            self._setAndStoreDefaultConf()

        self.__localTimeZone = self.config[TIME_ZONE]


    def _setAndStoreDefaultConf(self):
        '''
        In case no config file exists or if config file is empty,
        defines default values for config properties. Then creates
        or updates the config file.
        :return: nothing
        '''
        self.localTimeZone = 'Europe/Zurich'

        self.storeConfig()

    @property
    def localTimeZone(self):
        return self.__localTimeZone
        

    @localTimeZone.setter
    def localTimeZone(self, timezoneStr):
        self.__localTimeZone = timezoneStr
        self._updated = True
     

    def storeConfig(self):
        if not self._updated:
            return
            
        self.config[TIME_ZONE] = self.localTimeZone
        
        self.config.write()
        
        self._updated = False


if __name__ == '__main__':
    if os.name == 'posix':
        FILE_PATH = '/sdcard/cryptopricer.ini'
    else:
        FILE_PATH = 'c:\\temp\\cryptopricer.ini'
        
    cm = ConfigurationManager(FILE_PATH)
    print(cm.localTimeZone)
