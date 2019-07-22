import os
from os.path import sep

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
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
from kivy.config import Config
from kivy.utils import platform
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from configurationmanager import ConfigurationManager
from controller import Controller
from guioutputformater import GuiOutputFormater

# global var in order tco avoid multiple call to CryptpPricerGUI __init__ !
fromAppBuilt = False

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

    # required to authorise unselecting a selected item
    touch_deselect_last = BooleanProperty(True)


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        if not self.selected and not is_selected:
            # case when adding a new list item
            return
        elif self.selected and not is_selected:
            # toggling from selected to unselected
            self.selected = False
            rv.parent.parent.recycleViewSelectItem(index, is_selected)
        else:
            # toggling from unselected to selected
            self.selected = not self.selected
            rv.parent.parent.recycleViewSelectItem(index, is_selected)

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


class CustomDropDown(DropDown):
    saveButton = ObjectProperty(None)

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def showLoad(self):
        message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

        if self.owner.ensureDataPathExist(self.owner.dataPath, message):
            self.owner.openLoadHistoryFileChooser()

    def showSave(self):
        message = 'Data path ' + self.owner.dataPath + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

        if self.owner.ensureDataPathExist(self.owner.dataPath, message):
            self.owner.openSaveHistoryFileChooser()

    def help(self):
        self.owner.displayHelp()


class CryptoPricerGUI(BoxLayout):
    requestInput = ObjectProperty()
    resultOutput = ObjectProperty()
    statusBar = ObjectProperty()
    showRequestList = False
    recycleViewCurrentSelIndex = -1

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

        # setting RecycleView list item height from config
        self.requestListRVSelBoxLayout.default_size = None, self.histoListItemHeight

        self.appSize = self.configMgr.appSize
        self.defaultAppPosAndSize = self.configMgr.appSize
        self.appSizeHalfProportion = float(self.configMgr.appSizeHalfProportion)
        self.applyAppPosAndSize()

    def ensureDataPathExist(self, dataPath, message):
        '''
        Display a warning in a popup if the data path defined in the settings
        does nor exist and return False. If path ok, returns True. This prevents
        exceptions at load or save or settings save time.
        :return:
        '''
        if not (os.path.isdir(dataPath) or os.path.isfile(dataPath)):
            popupSize = None

            if platform == 'android':
                popupSize = (980, 450)
            elif platform == 'win':
                popupSize = (300, 150)

            popup = Popup(title='CryptoPricer WARNING', content=Label(
                text=message),
                          auto_dismiss=True, size_hint=(None, None),
                          size=popupSize)
            popup.open()

            return False
        else:
            return True

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
            # hiding RecycleView list
            self.boxLayoutContainingRV.height = '0dp'

            self.disableRequestListItemButtons()
            self.showRequestList = False
        else:
            # showing RecycleView list
            listItemNumber = len(self.requestListRV.data)
            self.boxLayoutContainingRV.height = min(listItemNumber * self.histoListItemHeight, self.maxHistoListHeight)

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

        fullRequestListEntry = {'text': fullRequestStr}

        if fullRequestStrWithSaveModeOptions != None:
            if fullRequestListEntry in self.requestListRV.data:
                # if the full request string corresponding to the full request string with options is already
                # in the history list, it is removed before the full request string with options is added
                # to the list. Otherwise, this would engender a duplicate !
                self.requestListRV.data.remove(fullRequestListEntry)

            fullRequestStrWithSaveModeOptionsListEntry = {'text': fullRequestStrWithSaveModeOptions}

            if not fullRequestStrWithSaveModeOptionsListEntry in self.requestListRV.data:
                self.requestListRV.data.append(fullRequestStrWithSaveModeOptionsListEntry)

            # Reset the ListView
            self.resetListViewScrollToEnd()
        elif fullRequestStr != '' and not fullRequestListEntry in self.requestListRV.data:
            # Add the full request to the ListView if not already in

            # if an identical full request string with options is in the history, it is not
            # removed automatically. If the user wants to get rid of it, he must do it exolicitely
            # using the delete button !
            self.requestListRV.data.append(fullRequestListEntry)

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

    def recycleViewSelectItem(self, index, isSelected):
        if isSelected:
            self.recycleViewCurrentSelIndex = index
            requestStr = self.requestListRV.data[index]['text']
            self.requestInput.text = requestStr
            self.enableRequestListItemButtons()
            self.refocusOnRequestInput()
        else:
            self.recycleViewCurrentSelIndex = -1
            self.requestInput.text = ''
            self.disableRequestListItemButtons()

    def clearOutput(self):
        self.resultOutput.text = ''
        self.statusBar.text = ''
        self.clearResultOutputButton.disabled = True
        self.refocusOnRequestInput()

    def resetListViewScrollToEnd(self):
        # listView = self.requestList
        # maxVisibleItemNumber = self.histoListMaxVisibleItems
        # listLength = len(listView.adapter.data)
        #
        # if listLength > maxVisibleItemNumber:
        #     listView.scroll_to(listLength - maxVisibleItemNumber)
        # else:
        #     if self.showRequestList:
        #         listItemNumber = len(self.requestList.adapter.data)
        #         self.requestList.height = min(listItemNumber * self.histoListItemHeight, self.maxHistoListHeight)
        #         if listItemNumber == 0:
        #             self.showRequestList = False
        #             self.manageStateOfRequestListButtons()
        #
        # listView._trigger_reset_populate()

        maxVisibleItemNumber = self.histoListMaxVisibleItems
        listLength = len(self.requestListRV.data)

        if listLength > maxVisibleItemNumber:
            # for the moment, I do not know how to scroll to end of RecyclweView !
            # listView.scroll_to(listLength - maxVisibleItemNumber)
            pass
        else:
            if self.showRequestList:
                listItemNumber = len(self.requestListRV.data)
                self.boxLayoutContainingRV.height = min(listItemNumber * self.histoListItemHeight, self.maxHistoListHeight)
                if listItemNumber == 0:
                    self.showRequestList = False
                    self.manageStateOfRequestListButtons()

    def manageStateOfRequestListButtons(self):
        '''
        Enable or disable history request list related controls according to
        the status of the list: filled with items or empty.
        :return: 
        '''
        if len(self.requestListRV.data) == 0:
            # request list is empty
            self.toggleHistoButton.state = 'normal'
            self.toggleHistoButton.disabled = True
            self.replayAllButton.disabled = True
            self.boxLayoutContainingRV.height = '0dp'
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
        # deleting from RecycleView list
        self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)
        self.requestListRV._get_layout_manager().clear_selection()

        if len(self.requestListRV.data) == 0:
            self.disableRequestListItemButtons()
            self.toggleHistoButton.disabled = True
            self.requestInput.text = ''

        self.manageStateOfRequestListButtons()

        self.refocusOnRequestInput()

    def replaceRequest(self, *args):
        # Remove the selected item
        self.requestListRV.data.pop(self.recycleViewCurrentSelIndex)

        # Get the request from the TextInputs
        requestStr = self.requestInput.text

        # Add the updated data to the list if not already in
        requestListEntry = {'text': requestStr}

        if not requestListEntry in self.requestListRV.data:
            self.requestListRV.data.append(requestListEntry)

        # Clear selection
        self.requestListRV._get_layout_manager().clear_selection()
        self.requestInput.text = ''
        self.disableRequestListItemButtons()

        self.refocusOnRequestInput()

    def enableRequestListItemButtons(self):
        self.deleteButton.disabled = False
        self.replaceButton.disabled = False

    def disableRequestListItemButtons(self):
        self.deleteButton.disabled = True
        self.replaceButton.disabled = True

    def replayAllRequests(self):
        # output blank line
        self.outputResult('')

        for listEntry in self.requestListRV.data:
            outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
                listEntry['text'])
            self.outputResult(outputResultStr)

        # self.resultOutput.do_cursor_movement('cursor_pgdown')
        self.refocusOnRequestInput()

    def openDropDownMenu(self, widget):
        self.dropDownMenu.open(widget)

    def displayHelp(self):
        self.dropDownMenu.dismiss()
        popup = Popup(title='CryptoPricer', content=Label(text='Version 2.2'), size_hint=(None, None), size=(400, 400))
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
        fileChooserDialog = SaveDialog(save=self.saveHistoryToFile, cancel=self.dismissPopup)
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
        self.loadHistoryFromPathFilename(pathFilename)
        self.dismissPopup()

    def loadHistoryFromPathFilename(self, pathFilename):
        dataFileNotFoundMessage = 'Data file\n' + pathFilename + 'not found. No history loaded.'

        if not self.ensureDataPathExist(pathFilename, dataFileNotFoundMessage):
            return

        with open(pathFilename) as stream:
            lines = stream.readlines()

        lines = list(map(lambda line: line.strip('\n'), lines))
        histoLines = [{'text' : val} for val in lines]
        self.requestListRV.data.extend(histoLines)

        # Reset the ListView
        self.resetListViewScrollToEnd()

        self.manageStateOfRequestListButtons()
        self.refocusOnRequestInput()

    def saveHistoryToFile(self, path, filename, isLoadAtStart):
        dataPathNotExistMessage = self.buildDataPathNotExistMessage(path)

        if not filename or not self.ensureDataPathExist(filename, dataPathNotExistMessage):
            # no file selected. Save dialog remains open ..
            return

        pathFileName = os.path.join(path, filename)

        with open(pathFileName, 'w') as stream:
            for listEntry in self.requestListRV.data:
                line = listEntry['text']
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

    def buildDataPathNotExistMessage(self, path):
        return 'Data path ' + path + '\nas defined in the settings does not exist !\nEither create the directory or change the\ndata path value using the Settings menu.'

    def isLoadAtStart(self, filePathName):
        return self.configMgr.loadAtStartPathFilename == filePathName

    def buildFileNotFoundMessage(self, filePathFilename):
        return 'Data file\n' + filePathFilename + '\nnot found. No history loaded.'

class CryptoPricerGUIApp(App):
    settings_cls = SettingsWithTabbedPanel
    cryptoPricerGUI = None

    def build(self): # implicitely looks for a kv file of name cryptopricergui.kv which is
                     # class name without App, in lowercases
        global fromAppBuilt
        fromAppBuilt = True

        if os.name != 'posix':
            # running app om Windows
            Config.set('graphics', 'width', '400')
            Config.set('graphics', 'height', '500')
            Config.write()

        self.cryptoPricerGUI = CryptoPricerGUI()

        return self.cryptoPricerGUI

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
        if platform == 'android':
            defaultpath = '/sdcard/.%(appname)s.ini'
        elif platform == 'ios':
            defaultpath = '~/Documents/%(appname)s.ini'
        elif platform == 'win':
            defaultpath = defaultpath.replace('/', sep)

        return os.path.expanduser(defaultpath) % {
            'appname': 'cryptopricer', 'appdir': self.directory}

    def on_start(self):
        '''
        Testing at app start if data path defined in settings does exist
        and if history file loaded at start app does exist. Since a warning popup
        is displayed in case of invalid data, this must be performed here and
        not in CryptoPricerGUI.__init__ where no popup could be displayed.
        :return:
        '''
        dataPathNotExistMessage = self.cryptoPricerGUI.buildDataPathNotExistMessage(self.cryptoPricerGUI.dataPath)

        if self.cryptoPricerGUI.ensureDataPathExist(self.cryptoPricerGUI.dataPath, dataPathNotExistMessage):
            # loading the load at start history file if defined
            historyFilePathFilename = self.cryptoPricerGUI.configMgr.loadAtStartPathFilename
            dataFileNotFoundMessage = self.cryptoPricerGUI.buildFileNotFoundMessage(historyFilePathFilename)

            if historyFilePathFilename != '' and self.cryptoPricerGUI.ensureDataPathExist(historyFilePathFilename, dataFileNotFoundMessage):
                self.cryptoPricerGUI.loadHistoryFromPathFilename(historyFilePathFilename)

if __name__ == '__main__':
    dbApp = CryptoPricerGUIApp()

    dbApp.run()
