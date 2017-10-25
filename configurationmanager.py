import os
from configobj import ConfigObj

CONFIG_KEY_TIME_ZONE = 'timezone'
DEFAULT_TIME_ZONE = 'Europe/Zurich'

CONFIG_KEY_DATE_TIME_FORMAT = 'dateTimeFormat'
DEFAULT_DATE_TIME_FORMAT = 'DD/MM/YY HH:mm'

CONFIG_KEY_DATE_ONLY_FORMAT = 'dateOnlyFormat'
DEFAULT_DATE_ONLY_FORMAT = 'DD/MM/YY'

class ConfigurationManager:
    def __init__(self, filename):
        self.config = ConfigObj(filename)
        self._updated = False

        if len(self.config) == 0:
            self._setAndStoreDefaultConf()

        try:
            self.__localTimeZone = self.config[CONFIG_KEY_TIME_ZONE]
        except KeyError:
            self.__localTimeZone = DEFAULT_TIME_ZONE
            self._updated = True

        try:
            self.__dateTimeFormat = self.config[CONFIG_KEY_DATE_TIME_FORMAT]
        except KeyError:
            self.__dateTimeFormat = DEFAULT_DATE_TIME_FORMAT
            self._updated = True

        try:
            self.__dateOnlyFormat = self.config[CONFIG_KEY_DATE_ONLY_FORMAT]
        except KeyError:
            self.__dateOnlyFormat = DEFAULT_DATE_ONLY_FORMAT
            self._updated = True

        self.storeConfig() #will save config file in case one config key raised an exception


    def _setAndStoreDefaultConf(self):
        '''
        In case no config file exists or if config file is empty,
        defines default values for config properties. Then creates
        or updates the config file.
        :return: nothing
        '''
        self.localTimeZone = DEFAULT_TIME_ZONE
        self.dateTimeFormat = DEFAULT_DATE_TIME_FORMAT
        self.dateOnlyFormat = DEFAULT_DATE_ONLY_FORMAT

        self._updated = True

        self.storeConfig()

    @property
    def localTimeZone(self):
        return self.__localTimeZone
        

    @localTimeZone.setter
    def localTimeZone(self, timezoneStr):
        self.__localTimeZone = timezoneStr
        self._updated = True

    @property
    def dateTimeFormat(self):
        return self.__dateTimeFormat

    @dateTimeFormat.setter
    def dateTimeFormat(self, dateTimeFormatStr):
        self.__dateTimeFormat = dateTimeFormatStr
        self._updated = True

    @property
    def dateOnlyFormat(self):
        return self.__dateOnlyFormat

    @dateOnlyFormat.setter
    def dateOnlyFormat(self, dateOnlyFormatStr):
        self.__dateOnlyFormat = dateOnlyFormatStr
        self._updated = True

    def storeConfig(self):
        if not self._updated:
            return
            
        self.config[CONFIG_KEY_TIME_ZONE] = self.localTimeZone
        self.config[CONFIG_KEY_DATE_TIME_FORMAT] = self.dateTimeFormat
        self.config[CONFIG_KEY_DATE_ONLY_FORMAT] = self.dateOnlyFormat

        self.config.write()
        
        self._updated = False


if __name__ == '__main__':
    if os.name == 'posix':
        FILE_PATH = '/sdcard/cryptopricer.ini'
    else:
        FILE_PATH = 'c:\\temp\\cryptopricer.ini'
        
    cm = ConfigurationManager(FILE_PATH)
    print(cm.localTimeZone)
    print(cm.dateTimeFormat)
    print(cm.dateOnlyFormat)
