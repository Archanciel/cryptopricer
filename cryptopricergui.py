from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.adapters.listadapter import ListAdapter

from controller import Controller
from guioutputformater import GuiOutputFormater
from configurationmanager import ConfigurationManager
import os


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
        super(CryptoPricerGUI, self).__init__(**kwargs)
        self.dropDownMenu = CustomDropDown(owner = self)

        if os.name == 'posix':
            configPath = '/sdcard/cryptopricer.ini'
        else:
            configPath = 'c:\\temp\\cryptopricer.ini'
            self.toggleAppSizeButton.text = 'Half' # correct on Windows version !

        self.configMgr = ConfigurationManager(configPath)
        self.controller = Controller(GuiOutputFormater(self.configMgr))
        self.dataPath = self.configMgr.dataPath
        self.histoListItemHeight = int(self.configMgr.histoListItemHeight)
        self.histoListMaxVisibleItems = int(self.configMgr.histoListVisibleSize)
        self.maxHistoListHeight = self.histoListMaxVisibleItems * self.histoListItemHeight

        self.appPosAndSize = self.configMgr.appPosSize
        self.defaultAppPosAndSize = self.configMgr.appPosSize
        self.applyAppPosAndSize()

        #loading the load at start history file if defined
        pathFilename = self.configMgr.loadAtStartPathFilename
        
        if pathFilename != '':
            self.loadPathFilename(pathFilename)


    def toggleAppPosAndSize(self):
        if self.appPosAndSize == self.configMgr.APP_POS_SIZE_HALF:
            self.appPosAndSize = self.configMgr.APP_POS_SIZE_FULL
            self.toggleAppSizeButton.text = 'Half'

            if self.defaultAppPosAndSize == self.configMgr.APP_POS_SIZE_FULL:
                # on the smartphone, we do not want to reposition the cursor ob
                # the input field since this would display the keyboard !
                self.refocusOnRequestInput()
        else:
            self.appPosAndSize = self.configMgr.APP_POS_SIZE_HALF
            self.toggleAppSizeButton.text = 'Full'

            # the case on the smartphone. Here, positioning the cursor on
            # the input field after having pressed the 'half' button
            # automatically displays the keyboard
            self.refocusOnRequestInput()

        self.applyAppPosAndSize()


    def applyAppPosAndSize(self):
        if self.appPosAndSize == self.configMgr.APP_POS_SIZE_HALF:
            self.size_hint_y = 0.56
            self.pos_hint = {'x': 0, 'y': 0.44}
        else:
            self.size_hint_y = 1
            self.pos_hint = {'x': 0, 'y': 0}


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

            self.resetListViewScrollToEnd(self.requestList, self.histoListMaxVisibleItems)

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
        outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions = self.controller.getPrintableResultForInput(requestStr)

        self.outputResult(outputResultStr)

        if fullRequestStrWithSaveModeOptions != None:
            if fullRequestStr in self.requestList.adapter.data:
                #if the full request string corresponding to the full request string with options is already
                #in the history list, it is removed before the full request string with options is added
                #to the list. Otherwise, this would engender a duplicate !
                self.requestList.adapter.data.remove(fullRequestStr)

            if not fullRequestStrWithSaveModeOptions in self.requestList.adapter.data:
                self.requestList.adapter.data.extend([fullRequestStrWithSaveModeOptions])

            # Reset the ListView
            self.resetListViewScrollToEnd(self.requestList, self.histoListMaxVisibleItems)
        elif fullRequestStr != '' and not fullRequestStr in self.requestList.adapter.data:
            # Add the full request to the ListView if not already in
            self.requestList.adapter.data.extend([fullRequestStr])

            # if an identical full request string with options is in the history, it is not
            # removed automatically. If the user wants to get rid of it, he must do it exolicitely
            # using the delete button !

            # Reset the ListView
            self.resetListViewScrollToEnd(self.requestList, self.histoListMaxVisibleItems)

        self.manageStateOfRequestListButtons()
        self.requestInput.text = ''

        #displaying request and result in status bar

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


    def resetListViewScrollToEnd(self, listView, maxVisibleItemNumber):
        listView._trigger_reset_populate()
        listLength = len(self.requestList.adapter.data)

        if listLength > maxVisibleItemNumber:
            listView.scroll_to(listLength - maxVisibleItemNumber)
        else:
            listView.scroll_to(0)

    def manageStateOfRequestListButtons(self):
        '''
        Enable or disable history request list related controls according to
        the status of the list: filled with items or empty.
        :return: 
        '''
        if len(self.requestList.adapter.data) == 0:
            #request list is empty
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
            #self.outputResultScrollView.scroll_to(100000)
            #self.resultOutput.cursor = (10000,0)

        self.clearResultOutputButton.disabled = False


    def refocusOnRequestInput(self):
        #defining a delay of 0.1 sec ensure the
        #refocus works in all situations. Leaving
        #it empty (== next frame) does not work
        #when pressing a button !
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
            self.requestList._trigger_reset_populate()
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
        
        #counter-intuitive, but test must be defined that way !
        if instance.is_selected:
            #disabling the 2 history request list item related buttons
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
        #output blank line
        self.outputResult('')

        for request in self.requestList.adapter.data:
             outputResultStr, fullRequestStr, fullRequestStrWithOptions, fullRequestStrWithSaveModeOptions = self.controller.getPrintableResultForInput(request)
             self.outputResult(outputResultStr)

        #self.resultOutput.do_cursor_movement('cursor_pgdown')
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
            #no file selected. Load dialog remains open ..
            return
        
        pathFilename = os.path.join(path, filename[0])
        self.loadPathFilename(pathFilename)
        self.dismissPopup()


    def loadPathFilename(self, pathFilename):
        #emptying the list
        self.requestList.adapter.data[:] = []

        with open(pathFilename) as stream:
            lines = stream.readlines()

        lines = list(map(lambda line : line.strip('\n'), lines))
        self.requestList.adapter.data.extend(lines)

        # Reset the ListView
        self.resetListViewScrollToEnd(self.requestList, self.histoListMaxVisibleItems)

        self.manageStateOfRequestListButtons()
        self.refocusOnRequestInput()


    def save(self, path, filename, isLoadAtStart):
        if not filename:
            #no file selected. Save dialog remains open ..
            return
            
        pathFileName = os.path.join(path, filename)   
        
        with open(pathFileName, 'w') as stream:
            for line in self.requestList.adapter.data:
                line = line + '\n'
                stream.write(line)

        #saving in config file if the saved file
        #is to be loaded at application start
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
    def build(self):
        return CryptoPricerGUI()


    # code moved from CryptoPricerGUI to CryptoPricerGUIApp ! Now, works !

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
       
        
          pass

    # end of code moved from CryptoPricerGUI to CryptoPricerGUIApp ! Now, works !


if __name__== '__main__':
    dbApp = CryptoPricerGUIApp()
 
    dbApp.run() 
     
