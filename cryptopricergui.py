import os

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.settings import SettingOptions
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.settings import SettingSpacer
from kivy.uix.button import Button
from kivy.metrics import dp

from configurationmanager import ConfigurationManager
from controller import Controller
from guioutputformater import GuiOutputFormater

# global var in order tco avoid multiple call to CryptpPricerGUI __init__ !
fromAppBuilt = False


class SettingScrollOptions(SettingOptions):
    '''
    This class is used in the Kivy Settings dialog to display in a sccrollable way
    the long list of time zones

    Source URL: https://github.com/kivy/kivy/wiki/Scollable-Options-in-Settings-panel
    '''

    def _create_popup(self, instance):
        # global oORCA
        # create the popup

        content = GridLayout(cols=1, spacing='5dp')
        scrollview = ScrollView(do_scroll_x=False)
        scrollcontent = GridLayout(cols=1, spacing='5dp', size_hint=(None, None))
        scrollcontent.bind(minimum_height=scrollcontent.setter('height'))
        self.popup = popup = Popup(content=content, title=self.title, size_hint=(0.5, 0.9), auto_dismiss=False)

        # we need to open the popup first to get the metrics
        popup.open()
        # Add some space on top
        content.add_widget(Widget(size_hint_y=None, height=dp(2)))
        # add all the options
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid, size=(popup.width, dp(55)), size_hint=(None, None))
            btn.bind(on_release=self._set_option)
            scrollcontent.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        scrollview.add_widget(scrollcontent)
        content.add_widget(scrollview)
        content.add_widget(SettingSpacer())
        # btn = Button(text='Cancel', size=((oORCA.iAppWidth/2)-sp(25), dp(50)),size_hint=(None, None))
        btn = Button(text='Cancel', size=(popup.width, dp(50)), size_hint=(0.9, None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    fileChooser = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    fileChooser = ObjectProperty(None)
    loadAtStartChkb = ObjectProperty(None)
    filePathName = ObjectProperty(None)
    owner = None

    def toggleLoadAtStart(self, active):
        if active:
            self.owner.updateStatusBar('Load at start activated')
        else:
            self.owner.updateStatusBar('')

    def saveFileSelected(self, filePathName):
        self.filePathName.text = filePathName

        if self.owner.isLoadAtStart(filePathName):
            self.loadAtStartChkb.active = True
            self.owner.updateStatusBar('Load at start active')
        else:
            self.loadAtStartChkb.active = False
            self.owner.updateStatusBar('')


class RequestListButton(ListItemButton):
    pass


class CustomDropDown(DropDown):
    saveButton = ObjectProperty(None)

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def showLoad(self):
        self.owner.openLoadHistoryFileChooser()

    def showSave(self):
        self.owner.openSaveHistoryFileChooser()

    def help(self):
        self.owner.displayHelp()


class CryptoPricerGUI(BoxLayout):
    requestInput = ObjectProperty()
    requestList = ObjectProperty()
    resultOutput = ObjectProperty()
    statusBar = ObjectProperty()
    showRequestList = False

    def __init__(self, **kwargs):
        global fromAppBuilt

        if not fromAppBuilt:
            return

        super(CryptoPricerGUI, self).__init__(**kwargs)
        self.dropDownMenu = CustomDropDown(owner=self)

        if os.name == 'posix':
            configPath = '/sdcard/cryptopricer.ini'
        else:
            configPath = 'c:\\temp\\cryptopricer.ini'
            self.toggleAppSizeButton.text = 'Half'  # correct on Windows version !

        self.configMgr = ConfigurationManager(configPath)
        self.controller = Controller(GuiOutputFormater(self.configMgr, activateClipboard=True), self.configMgr)
        self.dataPath = self.configMgr.dataPath
        self.histoListItemHeight = int(self.configMgr.histoListItemHeight)
        self.histoListMaxVisibleItems = int(self.configMgr.histoListVisibleSize)
        self.maxHistoListHeight = self.histoListMaxVisibleItems * self.histoListItemHeight

        self.appSize = self.configMgr.appSize
        self.defaultAppPosAndSize = self.configMgr.appSize
        self.appSizeHalfProportion = float(self.configMgr.appSizeHalfProportion)
        self.applyAppPosAndSize()

        # loading the load at start history file if defined
        pathFilename = self.configMgr.loadAtStartPathFilename

        if pathFilename != '':
            self.loadPathFilename(pathFilename)

    def toggleAppPosAndSize(self):
        if self.appSize == self.configMgr.APP_SIZE_HALF:
            self.appSize = self.configMgr.APP_SIZE_FULL

            if self.defaultAppPosAndSize == self.configMgr.APP_SIZE_FULL:
                # on the smartphone, we do not want to reposition the cursor ob
                # the input field since this would display the keyboard !
                self.refocusOnRequestInput()
        else:
            self.appSize = self.configMgr.APP_SIZE_HALF

            # the case on the smartphone. Here, positioning the cursor on
            # the input field after having pressed the 'half' button
            # automatically displays the keyboard
            self.refocusOnRequestInput()

        self.applyAppPosAndSize()

    def applyAppPosAndSize(self):
        if self.appSize == self.configMgr.APP_SIZE_HALF:
            sizeHintY = float(self.appSizeHalfProportion)
            self.size_hint_y = sizeHintY
            self.pos_hint = {'x': 0, 'y': 1 - sizeHintY}
            self.toggleAppSizeButton.text = 'Full'
        else:
            self.size_hint_y = 1
            self.pos_hint = {'x': 0, 'y': 0}
            self.toggleAppSizeButton.text = 'Half'

    def toggleRequestList(self):
        '''
        called by 'History' toggle button to toggle the display of the history
        request list.
        '''
        if self.showRequestList:
            self.requestList.size_hint_y = None
            self.requestList.height = '0dp'
            self.disableRequestListItemButtons()
            self.showRequestList = False
        else:
            listItemNumber = len(self.requestList.adapter.data)
            self.requestList.height = min(listItemNumber * self.histoListItemHeight, self.maxHistoListHeight)
            self.showRequestList = True

            self.resetListViewScrollToEnd()

            self.refocusOnRequestInput()

    def submitRequest(self):
        '''
        Submit the request, output the result and add the request to the
        request list
        :return:
        '''
        # Get the request from the TextInput
        requestStr = self.requestInput.text
        self.updateStatusBar(requestStr)

        # purpose of the informations obtained from the business layer:
        #   outputResultStr - for the output text zone
        #   fullRequestStr - for the request history list
        #   fullRequestStrWithOptions - for the status bar
        #   fullRequestStrWithSaveModeOptions - for the request history list
        outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            requestStr)

        self.outputResult(outputResultStr)

        if fullRequestStrWithSaveModeOptions != None:
            if fullRequestStr in self.requestList.adapter.data:
                # if the full request string corresponding to the full request string with options is already
                # in the history list, it is removed before the full request string with options is added
                # to the list. Otherwise, this would engender a duplicate !
                self.requestList.adapter.data.remove(fullRequestStr)

            if not fullRequestStrWithSaveModeOptions in self.requestList.adapter.data:
                self.requestList.adapter.data.extend([fullRequestStrWithSaveModeOptions])

            # Reset the ListView
            self.resetListViewScrollToEnd()
        elif fullRequestStr != '' and not fullRequestStr in self.requestList.adapter.data:
            # Add the full request to the ListView if not already in
            self.requestList.adapter.data.extend([fullRequestStr])

            # if an identical full request string with options is in the history, it is not
            # removed automatically. If the user wants to get rid of it, he must do it exolicitely
            # using the delete button !

            # Reset the ListView
            self.resetListViewScrollToEnd()

        self.manageStateOfRequestListButtons()
        self.requestInput.text = ''

        # displaying request and result in status bar

        if 'ERROR' in outputResultStr:
            if requestStr == '':
                self.updateStatusBar('REPLAY --> ' + outputResultStr)
            elif requestStr:
                self.updateStatusBar(requestStr + ' --> ' + outputResultStr)
        else:
            if fullRequestStrWithSaveModeOptions:
                if requestStr == '':
                    self.updateStatusBar('REPLAY --> ' + fullRequestStrWithSaveModeOptions)
                elif requestStr:
                    self.updateStatusBar(requestStr + ' --> ' + fullRequestStrWithSaveModeOptions)
            else:
                if not fullRequestStrWithOptions:
                    fullRequestStrWithOptions = fullRequestStr

                if requestStr == '':
                    self.updateStatusBar('REPLAY --> ' + fullRequestStrWithOptions)
                elif requestStr:
                    self.updateStatusBar(requestStr + ' --> ' + fullRequestStrWithOptions)

        self.refocusOnRequestInput()

    def clearOutput(self):
        self.resultOutput.text = ''
        self.statusBar.text = ''
        self.clearResultOutputButton.disabled = True
        self.refocusOnRequestInput()

    def resetListViewScrollToEnd(self):
        listView = self.requestList
        maxVisibleItemNumber = self.histoListMaxVisibleItems
        listLength = len(listView.adapter.data)

        if listLength > maxVisibleItemNumber:
            listView.scroll_to(listLength - maxVisibleItemNumber)
        else:
            listView.scroll_to(0)

        listView._trigger_reset_populate()

    def manageStateOfRequestListButtons(self):
        '''
        Enable or disable history request list related controls according to
        the status of the list: filled with items or empty.
        :return: 
        '''
        if len(self.requestList.adapter.data) == 0:
            # request list is empty
            self.toggleHistoButton.state = 'normal'
            self.toggleHistoButton.disabled = True
            self.replayAllButton.disabled = True
            self.requestList.height = '0dp'
            self.dropDownMenu.saveButton.disabled = True
        else:
            self.toggleHistoButton.disabled = False
            self.replayAllButton.disabled = False
            self.dropDownMenu.saveButton.disabled = False

    def outputResult(self, resultStr):
        if len(self.resultOutput.text) == 0:
            self.resultOutput.text = resultStr
        else:
            self.resultOutput.text = self.resultOutput.text + '\n' + resultStr
            # self.outputResultScrollView.scroll_to(100000)
            # self.resultOutput.cursor = (10000,0)

        self.clearResultOutputButton.disabled = False

    def refocusOnRequestInput(self):
        # defining a delay of 0.1 sec ensure the
        # refocus works in all situations. Leaving
        # it empty (== next frame) does not work
        # when pressing a button !
        Clock.schedule_once(self._refocusTextInput, 0.1)

    def _refocusTextInput(self, *args):
        '''
        This method is here to be used as callback by Clock and must not be called directly
        :param args:
        :return:
        '''
        self.requestInput.focus = True

    def deleteRequest(self, *args):
        # If a list item is selected
        if self.requestList.adapter.selection:
            # Get the text from the item selected
            selection = self.requestList.adapter.selection[0].text

            # Remove the matching item
            self.requestList.adapter.data.remove(selection)

            # Reset the ListView
            self.resetListViewScrollToEnd()

            self.requestInput.text = ''
            self.disableRequestListItemButtons()

        self.manageStateOfRequestListButtons()

        self.refocusOnRequestInput()

    def replaceRequest(self, *args):
        # If a list item is selected
        if self.requestList.adapter.selection:

            # Get the text from the item selected
            selection = self.requestList.adapter.selection[0].text

            # Remove the matching item
            self.requestList.adapter.data.remove(selection)

            # Get the request from the TextInputs
            requestStr = self.requestInput.text

            # Add the updated data to the list if not already in
            if not requestStr in self.requestList.adapter.data:
                self.requestList.adapter.data.extend([requestStr])

            # Reset the ListView
            self.requestList._trigger_reset_populate()
            self.requestInput.text = ''
            self.disableRequestListItemButtons()

        self.refocusOnRequestInput()

    def historyItemSelected(self, instance):
        requestStr = str(instance.text)

        # counter-intuitive, but test must be defined that way !
        if instance.is_selected:
            # disabling the 2 history request list item related buttons
            self.disableRequestListItemButtons()
        else:
            self.enableRequestListItemButtons()

        self.requestInput.text = requestStr
        self.refocusOnRequestInput()

        self.dropDownMenu.saveButton.disabled = False

    def enableRequestListItemButtons(self):
        self.deleteButton.disabled = False
        self.replaceButton.disabled = False

    def disableRequestListItemButtons(self):
        self.deleteButton.disabled = True
        self.replaceButton.disabled = True

    def replayAllRequests(self):
        # output blank line
        self.outputResult('')

        for request in self.requestList.adapter.data:
            outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
                request)
            self.outputResult(outputResultStr)

        # self.resultOutput.do_cursor_movement('cursor_pgdown')
        self.refocusOnRequestInput()

    def openDropDownMenu(self, widget):
        self.dropDownMenu.open(widget)

    def displayHelp(self):
        self.dropDownMenu.dismiss()
        popup = Popup(title='CryptoPricer', content=Label(text='Version 2.1'), size_hint=(None, None), size=(400, 400))
        popup.open()

    def updateStatusBar(self, messageStr):
        self.statusBar.text = messageStr

    # --- file chooser code ---
    def getStartPath(self):
        return "D:\\Users\\Jean-Pierre"

    def dismissPopup(self):
        '''
        Act as a call back function for the cancel button of the load and save dialog
        :return: nothing
        '''
        self.updateStatusBar('')
        self.popup.dismiss()

    def openLoadHistoryFileChooser(self):
        fileChooserDialog = LoadDialog(load=self.load, cancel=self.dismissPopup)
        fileChooserDialog.fileChooser.rootpath = self.dataPath
        self.popup = Popup(title="Load file", content=fileChooserDialog,
                           size_hint=(0.9, 0.6), pos_hint={'center': 1, 'top': 1})
        self.popup.open()
        self.dropDownMenu.dismiss()

    def openSaveHistoryFileChooser(self):
        fileChooserDialog = SaveDialog(save=self.save, cancel=self.dismissPopup)
        fileChooserDialog.owner = self
        fileChooserDialog.fileChooser.rootpath = self.dataPath
        self.popup = Popup(title="Save file", content=fileChooserDialog,
                           size_hint=(0.9, 0.6), pos_hint={'center': 1, 'top': 1})
        self.popup.open()
        self.dropDownMenu.dismiss()

    def load(self, path, filename):
        if not filename:
            # no file selected. Load dialog remains open ..
            return

        pathFilename = os.path.join(path, filename[0])
        self.loadPathFilename(pathFilename)
        self.dismissPopup()

    def loadPathFilename(self, pathFilename):
        # emptying the list
        self.requestList.adapter.data[:] = []

        with open(pathFilename) as stream:
            lines = stream.readlines()

        lines = list(map(lambda line: line.strip('\n'), lines))
        self.requestList.adapter.data.extend(lines)

        # Reset the ListView
        self.resetListViewScrollToEnd()

        self.manageStateOfRequestListButtons()
        self.refocusOnRequestInput()

    def save(self, path, filename, isLoadAtStart):
        if not filename:
            # no file selected. Save dialog remains open ..
            return

        pathFileName = os.path.join(path, filename)

        with open(pathFileName, 'w') as stream:
            for line in self.requestList.adapter.data:
                line = line + '\n'
                stream.write(line)

        # saving in config file if the saved file
        # is to be loaded at application start
        if isLoadAtStart:
            self.configMgr.loadAtStartPathFilename = pathFileName
        else:
            if self.configMgr.loadAtStartPathFilename == pathFileName:
                self.configMgr.loadAtStartPathFilename = ''

        self.configMgr.storeConfig()

        self.dismissPopup()
        self.refocusOnRequestInput()

    # --- end file chooser code ---

    def isLoadAtStart(self, filePathName):
        return self.configMgr.loadAtStartPathFilename == filePathName


class CryptoPricerGUIApp(App):
    settings_cls = SettingsWithTabbedPanel

    def build(self): # implicitely looks for a kv file of name cryptopricergui.kv which is
                     # class name without App, in lowercases
        global fromAppBuilt
        fromAppBuilt = True

        return CryptoPricerGUI()


    def on_pause(self):
        # Here you can save data if needed
        return True


    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)

        pass


    def build_config(self, config):
        '''
        Defaults set in this method will be overwritten by the values obtained from the
        app ini file.
        :param config:
        :return:
        '''
        config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL,
                           {ConfigurationManager.CONFIG_KEY_TIME_ZONE: ConfigurationManager.DEFAULT_TIME_ZONE})
        config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL,
                           {ConfigurationManager.CONFIG_KEY_DATE_TIME_FORMAT: ConfigurationManager.DEFAULT_DATE_TIME_FORMAT})
        config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL,
                           {ConfigurationManager.CONFIG_KEY_DATE_ONLY_FORMAT: ConfigurationManager.DEFAULT_DATE_ONLY_FORMAT})
        config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL,
                           {ConfigurationManager.CONFIG_KEY_REFERENCE_CURRENCY: ConfigurationManager.DEFAULT_REFERENCE_CURRENCY})

        from kivy.utils import platform

        if platform == 'android':
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT,
                               {ConfigurationManager.CONFIG_KEY_APP_SIZE: ConfigurationManager.APP_SIZE_HALF})
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL, {
                ConfigurationManager.CONFIG_KEY_DATA_PATH: ConfigurationManager.DEFAULT_DATA_PATH_ANDROID})
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT, {
                ConfigurationManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigurationManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
        elif platform == 'ios':
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT,
                               {ConfigurationManager.CONFIG_KEY_APP_SIZE: ConfigurationManager.APP_SIZE_HALF})
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL, {
                ConfigurationManager.CONFIG_KEY_DATA_PATH: ConfigurationManager.DEFAULT_DATA_PATH_IOS})
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT, {
                ConfigurationManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigurationManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID})
        elif platform == 'win':
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT,
                               {ConfigurationManager.CONFIG_KEY_APP_SIZE: ConfigurationManager.APP_SIZE_FULL})
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_GENERAL, {
                ConfigurationManager.CONFIG_KEY_DATA_PATH: ConfigurationManager.DEFAULT_DATA_PATH_WINDOWS})
            config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT, {
                ConfigurationManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT: ConfigurationManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_WINDOWS})

        config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT, {
            ConfigurationManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE: ConfigurationManager.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE})
        config.setdefaults(ConfigurationManager.CONFIG_SECTION_LAYOUT, {
            ConfigurationManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION: ConfigurationManager.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION})


    def build_settings(self, settings):
        # removing kivy default settings page from the settings dialog
        self.use_kivy_settings = False

        settings.register_type('scrolloptions', SettingScrollOptions)

        # add 'General' settings pannel
        TIME_ZONE_LIST = """["Europe/Amsterdam", "Europe/Andorra", "Europe/Astrakhan", "Europe/Athens", "Europe/Belfast", "Europe/Belgrade", "Europe/Berlin", "Europe/Bratislava", "Europe/Brussels", "Europe/Bucharest", "Europe/Budapest", "Europe/Busingen", "Europe/Chisinau", "Europe/Copenhagen", "Europe/Dublin", "Europe/Gibraltar", "Europe/Guernsey", "Europe/Helsinki", "Europe/Isle_of_Man", "Europe/Istanbul", "Europe/Jersey", "Europe/Kaliningrad", "Europe/Kiev", "Europe/Kirov", "Europe/Lisbon", "Europe/Ljubljana", "Europe/London", "Europe/Luxembourg", "Europe/Madrid", "Europe/Malta", "Europe/Mariehamn", "Europe/Minsk", "Europe/Monaco", "Europe/Moscow", "Europe/Nicosia", "Europe/Oslo", "Europe/Paris", "Europe/Podgorica", "Europe/Prague", "Europe/Riga", "Europe/Rome", "Europe/Samara", "Europe/San_Marino", "Europe/Sarajevo", "Europe/Saratov", "Europe/Simferopol", "Europe/Skopje", "Europe/Sofia", "Europe/Stockholm", "Europe/Tallinn", "Europe/Tirane", "Europe/Tiraspol", "Europe/Ulyanovsk", "Europe/Uzhgorod", "Europe/Vaduz", "Europe/Vatican", "Europe/Vienna", "Europe/Vilnius", "Europe/Volgograd", "Europe/Warsaw", "Europe/Zagreb", "Europe/Zaporozhye", "Europe/Zurich", "GMT", "GMT+1", "GMT+2", "GMT+3", "GMT+4", "GMT+5", "GMT+6", "GMT+7", "GMT+8", "GMT+9", "GMT+10", "GMT+11", "GMT+12", "GMT+13", "GMT+14", "GMT+15", "GMT+16", "GMT+17", "GMT+18", "GMT+19", "GMT+20", "GMT+21", "GMT+22", "GMT+23", "GMT-1", "GMT-2", "GMT-3", "GMT-4", "GMT-5", "GMT-6", "GMT-7", "GMT-8", "GMT-9", "GMT-10", "GMT-11", "GMT-12", "GMT-13", "GMT-14", "GMT-15", "GMT-16", "GMT-17", "GMT-18", "GMT-19", "GMT-20", "GMT-21", "GMT-22", "GMT-23"]"""
        settings.add_json_panel("General", self.config, data=("""
            [
                {"type": "scrolloptions",
                    "title": "Time zone",
                    "desc": "Set the local time zone",
                    "section": "General",
                    "key": "timezone",
                    "options": %s
                },
                {"type": "options",
                    "title": "Date/time format",
                    "desc": "Set the full date/time format",
                    "section": "General",
                    "key": "datetimeformat",
                    "options": ["DD/MM/YY HH:mm"]
                },
                {"type": "options",
                    "title": "Date format",
                    "desc": "Set the date only format",
                    "section": "General",
                    "key": "dateonlyformat",
                    "options": ["DD/MM/YY"]
                },
                {"type": "options",
                    "title": "Reference currency",
                    "desc": "Set the reference currency in which all the returned crypto prices will be converted",
                    "section": "General",
                    "key": "referencecurrency",
                    "options": ["USD", "EURO", "CHF", "GBP"]
                },
                {"type": "path",
                    "title": "Data files location",
                    "desc": "Set the directory where the app data files like history files are stored",
                    "section": "General",
                    "key": "dataPath"
                }
            ]""" % TIME_ZONE_LIST)
                                )
        # add 'Layout' settings pannel
        settings.add_json_panel("Layout", self.config, data=("""
            [
                {"type": "options",
                    "title": "Default app size",
                    "desc": "Set the app size at start up",
                    "section": "Layout",
                    "key": "defaultappsize",
                    "options": ["Full", "Half"]
                },
                {"type": "numeric",
                    "title": "History list item height",
                    "desc": "Set the height of each item in the history list",
                    "section": "Layout",
                    "key": "histolistitemheight"
                },
                {"type": "numeric",
                    "title": "History list visible item number",
                    "desc": "Set the number of items displayed in the history list",
                    "section": "Layout",
                    "key": "histolistvisiblesize"
                },
                {"type": "numeric",
                    "title": "Half size application proportion",
                    "desc": "Set the proportion of vertical screen size the app occupies so that the smartphone keyboard does not hide part of the application. Must be between 0 and 1",
                    "section": "Layout",
                    "key": "appsizehalfproportion"
                }
            ]""")
                                )


    def on_config_change(self, config, section, key, value):
        if config is self.config:
            if key == ConfigurationManager.CONFIG_KEY_APP_SIZE:
                appSize = config.getdefault(ConfigurationManager.CONFIG_SECTION_LAYOUT, ConfigurationManager.CONFIG_KEY_APP_SIZE, "Half").upper()

                if appSize == "HALF":
                    self.root.appSize = ConfigurationManager.APP_SIZE_HALF
                else:
                    self.root.appSize = ConfigurationManager.APP_SIZE_FULL

                self.root.applyAppPosAndSize()
            elif key == ConfigurationManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT:
                self.root.histoListItemHeight = int(config.getdefault(ConfigurationManager.CONFIG_SECTION_LAYOUT, ConfigurationManager.CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT, ConfigurationManager.DEFAULT_CONFIG_KEY_HISTO_LIST_ITEM_HEIGHT_ANDROID))
            elif key == ConfigurationManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE:
                self.root.histoListMaxVisibleItems = int(config.getdefault(ConfigurationManager.CONFIG_SECTION_LAYOUT, ConfigurationManager.CONFIG_KEY_HISTO_LIST_VISIBLE_SIZE, ConfigurationManager.DEFAULT_CONFIG_HISTO_LIST_VISIBLE_SIZE))
            elif key == ConfigurationManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION:
                self.root.appSizeHalfProportion = float(config.getdefault(ConfigurationManager.CONFIG_SECTION_LAYOUT, ConfigurationManager.CONFIG_KEY_APP_SIZE_HALF_PROPORTION, ConfigurationManager.DEFAULT_CONFIG_KEY_APP_SIZE_HALF_PROPORTION))
                self.root.applyAppPosAndSize()
            elif key == ConfigurationManager.CONFIG_KEY_TIME_ZONE:
                self.root.configMgr.localTimeZone = config.getdefault(ConfigurationManager.CONFIG_SECTION_GENERAL, ConfigurationManager.CONFIG_KEY_TIME_ZONE, ConfigurationManager.DEFAULT_TIME_ZONE)
                self.root.configMgr.storeConfig()
            elif key == ConfigurationManager.CONFIG_KEY_DATE_TIME_FORMAT:
                self.root.configMgr.dateTimeFormat = config.getdefault(ConfigurationManager.CONFIG_SECTION_GENERAL, ConfigurationManager.CONFIG_KEY_DATE_TIME_FORMAT, ConfigurationManager.DEFAULT_DATE_TIME_FORMAT)
                self.root.configMgr.storeConfig()
            elif key == ConfigurationManager.CONFIG_KEY_DATE_ONLY_FORMAT:
                self.root.configMgr.dateOnlyFormat = config.getdefault(ConfigurationManager.CONFIG_SECTION_GENERAL, ConfigurationManager.CONFIG_KEY_DATE_ONLY_FORMAT, ConfigurationManager.DEFAULT_DATE_ONLY_FORMAT)
                self.root.configMgr.storeConfig()
            elif key == ConfigurationManager.CONFIG_KEY_REFERENCE_CURRENCY:
                self.root.configMgr.referenceCurrency = config.getdefault(ConfigurationManager.CONFIG_SECTION_GENERAL, ConfigurationManager.CONFIG_KEY_REFERENCE_CURRENCY, ConfigurationManager.DEFAULT_REFERENCE_CURRENCY)
                self.root.configMgr.storeConfig()


    def get_application_config(self, defaultpath="c:/temp/%(appname)s.ini"):
        '''
        Redefining super class method to control the name and location of the application
        settings ini file
        :param defaultpath: used under Windows
        :return:
        '''
        from kivy.utils import platform
        from os.path import sep

        if platform == 'android':
            defaultpath = '/sdcard/.%(appname)s.ini'
        elif platform == 'ios':
            defaultpath = '~/Documents/%(appname)s.ini'
        elif platform == 'win':
            defaultpath = defaultpath.replace('/', sep)

        return os.path.expanduser(defaultpath) % {
            'appname': 'cryptopricer', 'appdir': self.directory}


if __name__ == '__main__':
    dbApp = CryptoPricerGUIApp()

    dbApp.run()
