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
    owner = None
    

    def toggleLoadAtStart(self, active):
        self.owner.toggleLoadAtStart(active)
            

class CommandListButton(ListItemButton):
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
 
    commandInput = ObjectProperty()
    commandList = ObjectProperty()
    resultOutput = ObjectProperty()
    #outputResultScrollView = ObjectProperty()
    showCommandList = False
    controller = Controller(GuiOutputFormater())
    
    def __init__(self, **kwargs):
        super(CryptoPricerGUI, self).__init__(**kwargs)
        self.dropDownMenu = CustomDropDown(owner = self)

        if os.name == 'posix':
            configPath = '/sdcard/cryptopricer.ini'
        else:
            configPath = 'c:\\temp\\cryptopricer.ini'

        self.configMgr = ConfigurationManager(configPath)
        self.dataPath = self.configMgr.dataPath

    def toggleCommandList(self):
        '''
        called by 'History' toggle button to toggle the display of the history
        command list.
        '''
        if self.showCommandList:
            self.commandList.size_hint_y = None
            self.commandList.height = '0dp'
            self.disableCommandListItemButtons()
            self.showCommandList = False
        else:
            self.commandList.height = '100dp'
            self.showCommandList = True

            # Reset the ListView
            self.commandList.adapter.data.extend([]) #improves list view display, but only after user scrolled manually !
            self.resetListViewScrollToEnd(self.commandList)

            self.refocusOncommandInput()


    def submitCommand(self):
        '''
        Submit the command, output the result and add the command to the
        command list
        :return:
        '''
        # Get the student name from the TextInputs
        commandStr = self.commandInput.text

        if commandStr != '':
            outputResultStr, fullCommandStr = self.controller.getPrintableResultForInput(commandStr)
            self.outputResult(outputResultStr)
            
            # Add the command to the ListView if not already in
            if fullCommandStr != '' and not fullCommandStr in self.commandList.adapter.data:
                self.commandList.adapter.data.extend([fullCommandStr])

                # Reset the ListView
                self.resetListViewScrollToEnd(self.commandList)
            
            self.manageStateOfCommandListButtons()
            self.commandInput.text = ''

        self.refocusOncommandInput()


    def resetListViewScrollToEnd(self, listView):
        listView._trigger_reset_populate()
        listView.scroll_to(len(self.commandList.adapter.data) - 1)


    def manageStateOfCommandListButtons(self):
        '''
        Enable or disable history command list related controls according to
        the status of the list: filled with items or empty.
        :return: 
        '''
        if len(self.commandList.adapter.data) == 0:
            #command list is empty
            self.toggleHistoButton.state = 'normal'
            self.toggleHistoButton.disabled = True
            self.replayAllButton.disabled = True
            self.commandList.height = '0dp'
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


    def refocusOncommandInput(self):
        #defining a delay of 0.1 sec ensure the
        #refocus works in all situations. Leaving
        #it empty (== next frame) does not work
        #when pressing a button !
        Clock.schedule_once(self.refocusTextInput, 0.1)       


    def refocusTextInput(self, *args):
        self.commandInput.focus = True

                                      
    def deleteCommand(self, *args):
        # If a list item is selected
        if self.commandList.adapter.selection:
 
            # Get the text from the item selected
            selection = self.commandList.adapter.selection[0].text
 
            # Remove the matching item
            self.commandList.adapter.data.remove(selection)
 
            # Reset the ListView
            self.commandList._trigger_reset_populate()
            self.commandInput.text = ''
            self.disableCommandListItemButtons()
            
        self.manageStateOfCommandListButtons()
                        
        self.refocusOncommandInput()

  
    def replaceCommand(self, *args):
        # If a list item is selected
        if self.commandList.adapter.selection:
 
            # Get the text from the item selected
            selection = self.commandList.adapter.selection[0].text
 
            # Remove the matching item
            self.commandList.adapter.data.remove(selection)
 
            # Get the student name from the TextInputs
            commandStr = self.commandInput.text
 
            # Add the updated data to the list
            self.commandList.adapter.data.extend([commandStr])
 
            # Reset the ListView
            self.commandList._trigger_reset_populate()
            self.commandInput.text = ''
            self.disableCommandListItemButtons()
            
        self.refocusOncommandInput()


    def historyItemSelected(self, instance):
        commandStr = str(instance.text)
        
        #counter-intuitive, but test must be defined that way !
        if instance.is_selected:
            #disabling the 2 history command list item related buttons 
            self.disableCommandListItemButtons()
        else:
            self.enableCommandListItemButtons()

        self.commandInput.text = commandStr
        self.refocusOncommandInput()

        self.dropDownMenu.saveButton.disabled = False


    def enableCommandListItemButtons(self):
        self.deleteButton.disabled = False
        self.replaceButton.disabled = False


    def disableCommandListItemButtons(self):
        self.deleteButton.disabled = True
        self.replaceButton.disabled = True


    def replayAllCommands(self):
        self.outputResult('')

        for command in self.commandList.adapter.data:
             outputResultStr, fullCommandStr = self.controller.getPrintableResultForInput(command)
             #print("command: {}\nfull command: {}\nres: {}".format(command, fullCommandStr, outputResultStr))
             self.outputResult(outputResultStr)

        #self.resultOutput.do_cursor_movement('cursor_pgdown')
        self.refocusOncommandInput()
                                              

    def openDropDownMenu(self, widget):
        self.dropDownMenu.open(widget)


    def displayHelp(self):
        self.dropDownMenu.dismiss()
        popup = Popup(title='CryptoPricer', content=Label(text='Version 2.1'), size_hint=(None, None), size=(400, 400))
        popup.open()


    def toggleLoadAtStart(self, active):
        if active:
            self.displayToggleLoadAtStart()
        
        
    def displayToggleLoadAtStart(self):
        popup = Popup(title='CryptoPricer', content=Label(text='Load at start activated !'), size_hint=(None, None), size=(600, 280))
        popup.open()
        
        
    # --- file chooser code ---
    def getStartPath(self):
        return "D:\\Users\\Jean-Pierre"

  
    def dismissPopup(self):
        '''
        Act as a call back function for the cancel button of the load and save dialog
        :return: nothing
        '''
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
        #emptying the list
        self.commandList.adapter.data[:] = []

        if not filename:
            #no file selected. Load dialog remains open ..
            return
            
        with open(os.path.join(path, filename[0])) as stream:
            lines = stream.readlines()

        lines = list(map(lambda line : line.strip('\n'), lines))
        self.commandList.adapter.data.extend(lines)

        self.dismissPopup()

        # Reset the ListView
        self.resetListViewScrollToEnd(self.commandList)

        self.manageStateOfCommandListButtons()
        self.refocusOncommandInput()


    def save(self, path, filename, isLoadAtStart):
        if not filename:
            #no file selected. Save dialog remains open ..
            return
            
        pathFileName = os.path.join(path, filename)   
        
        with open(pathFileName, 'w') as stream:
            for line in self.commandList.adapter.data:
                line = line + '\n'
                stream.write(line)

        if isLoadAtStart:
            self.configMgr.loadAtStartPathFileName = pathFileName
        else:
            self.configMgr.loadAtStartPathFileName = ''
           
        self.dismissPopup()
        self.refocusOncommandInput()

# --- end file chooser code ---  


    def on_pause(self):
        # Here you can save data if needed
        return True


    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass
                             
                                           
class CryptoPricerGUIApp(App):
    def build(self):
        return CryptoPricerGUI()
 

if __name__== '__main__':
    dbApp = CryptoPricerGUIApp()
 
    dbApp.run()
