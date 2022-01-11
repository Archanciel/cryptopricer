import os
from configobj import ConfigObj


class ConfigurationManager:
    # those constants are used outside of ConfigurationManager. For this reason,
    # they are declared inside the class
    CONFIG_SECTION_GENERAL = 'General'
    CONFIG_SECTION_LAYOUT = 'Layout'

    CONFIG_KEY_TIME_ZONE = 'timezone'
    DEFAULT_TIME_ZONE = 'Europe/Zurich'

    CONFIG_KEY_DATE_TIME_FORMAT = 'datetimeformat'
    DEFAULT_DATE_TIME_FORMAT = 'DD/MM/YY HH:mm'

    CONFIG_KEY_DATE_ONLY_FORMAT = 'dateonlyformat'
    DEFAULT_DATE_ONLY_FORMAT = 'DD/MM/YY'

    CONFIG_KEY_DATA_PATH = 'datapath'
    DEFAULT_DATA_PATH_ANDROID = '/sdcard/CryptoPricerData'
    DEFAULT_DATA_PATH_IOS = '~/Documents'
    DEFAULT_DATA_PATH_WINDOWS = 'c:\\temp'

    CONFIG_KEY_REFERENCE_CURRENCY = 'referencecurrency'
    DEFAULT_REFERENCE_CURRENCY = 'USD'

    CONFIG_KEY_LOAD_AT_START_PATH_FILENAME = 'loadatstartpathfilename'
    DEFAULT_LOAD_AT_START_PATH_FILENAME = ''

    CONFIG_KEY_APP_SIZE = 'defaultappsize'
    DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION = '0.62'

    CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT = 'histolistitemheight'
    DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID = '90'
    DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS = '35'

    CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE = 'histolistvisiblesize'
    DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE = '3'

    CONFIG_KEY_DROP_DOWN_MENU_WIDTH = 'dropdownmenuwidth'
    DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_ANDROID = '100'
    DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_WINDOWS = '25'

    CONFIG_KEY_STATUS_BAR_HEIGHT = 'statusbarheight'
    DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_ANDROID = '73'
    DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_WINDOWS = '43'

    CONFIG_KEY_CLEAR_BUTTON_WIDTH = 'clearbuttonwidth'
    DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_ANDROID = '150'
    DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_WINDOWS = '130'

    CONFIG_KEY_APP_SIZE_HALF_PROPORTION = 'appsizehalfproportion'
    APP_SIZE_HALF = 'Half'
    APP_SIZE_FULL = 'Full'

    def __init__(self, filename):
        self.config = ConfigObj(filename)
        self._updated = False

        if len(self.config) == 0:
            self._setAndStoreDefaultConf()

        try:
            self.__localTimeZone = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_TIME_ZONE]
        except KeyError:
            self.__localTimeZone = self.DEFAULT_TIME_ZONE
            self._updated = True

        try:
            self.__dateTimeFormat = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATE_TIME_FORMAT]
        except KeyError:
            self.__dateTimeFormat = self.DEFAULT_DATE_TIME_FORMAT
            self._updated = True

        try:
            self.__dateOnlyFormat = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATE_ONLY_FORMAT]
        except KeyError:
            self.__dateOnlyFormat = self.DEFAULT_DATE_ONLY_FORMAT
            self._updated = True

        try:
            self.__dataPath = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATA_PATH]
        except KeyError:
            if os.name == 'posix':
                self.__dataPath = self.DEFAULT_DATA_PATH_ANDROID
            else:
                self.__dataPath = self.DEFAULT_DATA_PATH_WINDOWS
                
            self._updated = True

        try:
            self.__loadAtStartPathFilename = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME]
        except KeyError:
            self.__loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
            self._updated = True

        try:
            self.__histoListVisibleSize = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE]
        except KeyError:
            self.__histoListVisibleSize = self.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE
            self._updated = True

        try:
            self.__histoListItemHeight = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT]
        except KeyError:
            if os.name == 'posix':
                self.__histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID
            else:
                self.__histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS
            self._updated = True

        try:
            self.__appSize = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE]
        except KeyError:
            self.__appSize = self.APP_SIZE_HALF
            self._updated = True

        try:
            self.__dropDownMenuWidth = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_DROP_DOWN_MENU_WIDTH]
        except KeyError:
            if os.name == 'posix':
                self.__dropDownMenuWidth = self.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_ANDROID
            else:
                self.__dropDownMenuWidth = self.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_WINDOWS
            self._updated = True

        try:
            self.__statusbarHeight = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_STATUS_BAR_HEIGHT]
        except KeyError:
            if os.name == 'posix':
                self.__statusbarHeight = self.DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_ANDROID
            else:
                self.__statusbarHeight = self.DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_WINDOWS
            self._updated = True

        try:
            self.__clearButtonWidth = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_CLEAR_BUTTON_WIDTH]
        except KeyError:
            if os.name == 'posix':
                self.__clearButtonWidth = self.DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_ANDROID
            else:
                self.__clearButtonWidth = self.DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_WINDOWS
            self._updated = True

        try:
            self.__appSizeHalfProportion = self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE_HALF_PROPORTION]
        except KeyError:
            self.__appSizeHalfProportion = self.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
            self._updated = True

        try:
            self.__referenceCurrency = self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_REFERENCE_CURRENCY]
        except KeyError:
            self.__referenceCurrency = self.DEFAULT_REFERENCE_CURRENCY
            self._updated = True

        self.storeConfig() #will save config file in case one config key raised an exception


    def _setAndStoreDefaultConf(self):
        '''
        In case no config file exists or if config file is empty,
        defines default values for config properties. Then creates
        or updates the config file.
        :return: nothing
        '''
        self.config[self.CONFIG_SECTION_GENERAL] = {}
        self.config[self.CONFIG_SECTION_LAYOUT] = {}
        self.localTimeZone = self.DEFAULT_TIME_ZONE
        self.dateTimeFormat = self.DEFAULT_DATE_TIME_FORMAT
        self.dateOnlyFormat = self.DEFAULT_DATE_ONLY_FORMAT

        if os.name == 'posix':
            self.dataPath = self.DEFAULT_DATA_PATH_ANDROID
            self.histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID
            self.dropDownMenuWidth = self.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_ANDROID
            self.statusbarHeight = self.DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_ANDROID
            self.clearButtonWidth = self.DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_ANDROID
            self.appSize = self.APP_SIZE_HALF
        else:
            self.dataPath = self.DEFAULT_DATA_PATH_WINDOWS
            self.histoListItemHeight = self.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS
            self.dropDownMenuWidth = self.DEFAULT_CONFIG_KEY_DROP_DOWN_MENU_WIDTH_WINDOWS
            self.statusbarHeight = self.DEFAULT_CONFIG_KEY_STATUS_BAR_HEIGHT_WINDOWS
            self.clearButtonWidth = self.DEFAULT_CONFIG_KEY_CLEAR_BUTTON_WIDTH_WINDOWS
            self.appSize = self.APP_SIZE_FULL

        self.loadAtStartPathFilename = self.DEFAULT_LOAD_AT_START_PATH_FILENAME
        self.histoListVisibleSize = self.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE
        self.appSizeHalfProportion = self.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION
        self.referenceCurrency = self.DEFAULT_REFERENCE_CURRENCY
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
    def dropDownMenuWidth(self):
        return self.__dropDownMenuWidth

    @dropDownMenuWidth.setter
    def dropDownMenuWidth(self, dropDownMenuWidthStr):
        self.__dropDownMenuWidth = dropDownMenuWidthStr
        self._updated = True

    @property
    def statusbarHeight(self):
        return self.__statusbarHeight

    @statusbarHeight.setter
    def statusbarHeight(self, statusbarHeightStr):
        self.__statusbarHeight = statusbarHeightStr
        self._updated = True

    @property
    def clearButtonWidth(self):
        return self.__clearButtonWidth

    @clearButtonWidth.setter
    def clearButtonWidth(self, clearButtonWidthStr):
        self.__clearButtonWidth = clearButtonWidthStr
        self._updated = True

    @property
    def appSize(self):
        return self.__appSize

    @appSize.setter
    def appSize(self, appSizeStr):
        self.__appSize = appSizeStr
        self._updated = True


    @property
    def appSizeHalfProportion(self):
        return self.__appSizeHalfProportion

    @appSizeHalfProportion.setter
    def appSizeHalfProportion(self, appSizeHalfProportionStr):
        self.__appSizeHalfProportion = appSizeHalfProportionStr
        self._updated = True


    @property
    def referenceCurrency(self):
        return self.__referenceCurrency

    @referenceCurrency.setter
    def referenceCurrency(self, referenceCurrencyStr):
        self.__referenceCurrency = referenceCurrencyStr
        self._updated = True


    def storeConfig(self):
        """
        Writes the config file on the disk.
        
        :return: True if config file save was successful, False otherwise.
        """
        if not self._updated:
            return

        self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_TIME_ZONE] = self.localTimeZone
        self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATE_TIME_FORMAT] = self.dateTimeFormat
        self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATE_ONLY_FORMAT] = self.dateOnlyFormat
        self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_DATA_PATH] = self.dataPath
        self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_LOAD_AT_START_PATH_FILENAME] = self.loadAtStartPathFilename
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE] = self.histoListVisibleSize
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT] = self.histoListItemHeight
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE] = self.appSize
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_DROP_DOWN_MENU_WIDTH] = self.dropDownMenuWidth
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_STATUS_BAR_HEIGHT] = self.statusbarHeight
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_CLEAR_BUTTON_WIDTH] = self.clearButtonWidth
        self.config[self.CONFIG_SECTION_LAYOUT][self.CONFIG_KEY_APP_SIZE_HALF_PROPORTION] = self.appSizeHalfProportion
        self.config[self.CONFIG_SECTION_GENERAL][self.CONFIG_KEY_REFERENCE_CURRENCY] = self.referenceCurrency

        try:
            self.config.write()
        except UnicodeEncodeError as e:
            import logging
            logging.info(str(e) + ". Reason: invalid file name {}".format(self.loadAtStartPathFilename))
            return False
        
        self._updated = False
        
        return True


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
    import pytz
    print(sorted(pytz.all_timezones_set))
