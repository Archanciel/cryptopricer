import os
from configobj import ConfigObj

CONFIG_KEY_TIME_ZONE = 'timezone'
DEFAULT_TIME_ZONE = 'Europe/Zurich'

CONFIG_KEY_DATE_TIME_FORMAT = 'dateTimeFormat'
DEFAULT_DATE_TIME_FORMAT = 'DD/MM/YY HH:mm'

CONFIG_KEY_DATE_ONLY_FORMAT = 'dateOnlyFormat'
DEFAULT_DATE_ONLY_FORMAT = 'DD/MM/YY'

CONFIG_KEY_DATA_PATH = 'dataPath'
DEFAULT_DATA_PATH_ANDROID = '/sdcard/CryptoPricerData'
DEFAULT_DATA_PATH_WINDOWS = 'c:\\temp'

CONFIG_KEY_LOAD_AT_START_PATH_FILENAME = 'loadAtStartPathFilename'
DEFAULT_LOAD_AT_START_PATH_FILENAME = ''

CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE = 'histoListVisibleSize'
DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE = '3'

CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT = 'histoListItemHeight'
DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT = '90'

CONFIG_KEY_APP_POS_SIZE = 'defaultAppPosSize'
CONFIG_KEY_APP_SIZE_HALF_PROPORTION = 'appSizeHalfProportion'
DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION = '0.56'


class ConfigurationManager:
    # those two constants are used outside of ConfigurationManager. For this reason,
    # they are declared inside the class
    APP_POS_SIZE_HALF = 'appPosSizeHalf'
    APP_POS_SIZE_FULL = 'appPosSizeFull'

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

        try:
            self.__dataPath = self.config[CONFIG_KEY_DATA_PATH]
        except KeyError:
            if os.name == 'posix':
                self.__dataPath = DEFAULT_DATA_PATH_ANDROID
            else:
                self.__dataPath = DEFAULT_DATA_PATH_WINDOWS
                
            self._updated = True

        try:
            self.__loadAtStartPathFilename = self.config[CONFIG_KEY_LOAD_AT_START_PATH_FILENAME]
        except KeyError:
            self.__loadAtStartPathFilename = DEFAULT_LOAD_AT_START_PATH_FILENAME
            self._updated = True

        try:
            self.__histoListVisibleSize = self.config[CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE]
        except KeyError:
            self.__histoListVisibleSize = DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE
            self._updated = True

        try:
            self.__histoListItemHeight = self.config[CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT]
        except KeyError:
            self.__histoListItemHeight = DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT
            self._updated = True

        try:
            self.__appPosSize = self.config[CONFIG_KEY_APP_POS_SIZE]
        except KeyError:
            self.__appPosSize = self.APP_POS_SIZE_HALF
            self._updated = True

        try:
            self.__appSizeHalfProportion = self.config[CONFIG_KEY_APP_SIZE_HALF_PROPORTION]
        except KeyError:
            self.__appSizeHalfProportion = DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
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

        if os.name == 'posix':
            self.dataPath = DEFAULT_DATA_PATH_ANDROID
        else:
            self.dataPath = DEFAULT_DATA_PATH_WINDOWS

        self.loadAtStartPathFilename = DEFAULT_LOAD_AT_START_PATH_FILENAME
        self.histoListVisibleSize = DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE
        self.histoListItemHeight = DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT
        self.appPosSize = self.APP_POS_SIZE_HALF
        self.appSizeHalfProportion = DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
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


    @property
    def dataPath(self):
        return self.__dataPath

    @dataPath.setter
    def dataPath(self, dataPathStr):
        self.__dataPath = dataPathStr
        self._updated = True


    @property
    def loadAtStartPathFilename(self):
        return self.__loadAtStartPathFilename

    @loadAtStartPathFilename.setter
    def loadAtStartPathFilename(self, loadAtStartPathFilenameStr):
        self.__loadAtStartPathFilename = loadAtStartPathFilenameStr
        self._updated = True


    @property
    def histoListVisibleSize(self):
        return self.__histoListVisibleSize

    @histoListVisibleSize.setter
    def histoListVisibleSize(self, histoListVisibleSizeStr):
        self.__histoListVisibleSize = histoListVisibleSizeStr
        self._updated = True


    @property
    def histoListItemHeight(self):
        return self.__histoListItemHeight

    @histoListItemHeight.setter
    def histoListItemHeight(self, histoListItemHeightStr):
        self.__histoListItemHeight = histoListItemHeightStr
        self._updated = True


    @property
    def appPosSize(self):
        return self.__appPosSize

    @appPosSize.setter
    def appPosSize(self, appPosSizeStr):
        self.__appPosSize = appPosSizeStr
        self._updated = True


    @property
    def appSizeHalfProportion(self):
        return self.__appSizeHalfProportion

    @appSizeHalfProportion.setter
    def appSizeHalfProportion(self, appSizeHalfProportionStr):
        self.__appSizeHalfProportion = appSizeHalfProportionStr
        self._updated = True


    def storeConfig(self):
        if not self._updated:
            return
            
        self.config[CONFIG_KEY_TIME_ZONE] = self.localTimeZone
        self.config[CONFIG_KEY_DATE_TIME_FORMAT] = self.dateTimeFormat
        self.config[CONFIG_KEY_DATE_ONLY_FORMAT] = self.dateOnlyFormat
        self.config[CONFIG_KEY_DATA_PATH] = self.dataPath
        self.config[CONFIG_KEY_LOAD_AT_START_PATH_FILENAME] = self.loadAtStartPathFilename
        self.config[CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE] = self.histoListVisibleSize
        self.config[CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT] = self.histoListItemHeight
        self.config[CONFIG_KEY_APP_POS_SIZE] = self.appPosSize
        self.config[CONFIG_KEY_APP_SIZE_HALF_PROPORTION] = self.appSizeHalfProportion

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
    print(cm.dataPath)
    print("loadAtStartPathFilename: '" + cm.loadAtStartPathFilename + "'")
