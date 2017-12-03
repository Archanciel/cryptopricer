from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from controller import Controller
from guioutputformater import GuiOutputFormater

import os


class LoadDialog(FloatLayout):
    textPathLoad = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    textInput = ObjectProperty(None)
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class CommandListButton(ListItemButton):
    pass
    

class CustomDropDown(DropDown):
    owner = None


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
    showCommandList = False
    controller = Controller(GuiOutputFormater())
    
    def __init__(self, **kwargs):
        super(CryptoPricerGUI, self).__init__(**kwargs)
        self.dropDMenu = CustomDropDown()
        self.dropDMenu.owner = self

  
    def toggleCommandList(self):
        if self.showCommandList:
            self.commandList.size_hint_y = None
            self.commandList.height = '0dp'
            self.disableHistoryItemControls()
            self.showCommandList = False
        else:
            self.commandList.height = '100dp'
            #self.commandList.size_hint_y = 0.5
            self.showCommandList = True
        
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
            outputResultStr = self.controller.getPrintableResultForInput(commandStr)
            self.outputResult(outputResultStr)
            
            # Add the command to the ListView if not already in
            if not commandStr in self.commandList.adapter.data:
                self.commandList.adapter.data.extend([commandStr])

            # Reset the ListView
            self.commandList._trigger_reset_populate()
            
            self.enableCommandListControls()
            self.commandInput.text = ''

        self.refocusOncommandInput()


    def enableCommandListControls(self):
        self.toggleHistoControl.disabled = False
        self.replayAllControl.disabled = False


    def disableCommandListControls(self):
        self.toggleHistoControl.state = 'normal'
        self.toggleHistoControl.disabled = True
        self.replayAllControl.disabled = True
        self.commandList.height = '0dp'


     
    def outputResult(self, resultStr):
        if len(self.resultOutput.text) == 0:
            self.resultOutput.text = resultStr
        else:
            self.resultOutput.text = self.resultOutput.text + '\n' + resultStr

                              
    def refocusOncommandInput(self):
        #defining a delay of 0.1 sec ensure the
        #refocus works in all situations. Leaving
        #it empty (== next frame) does not work
        #when pressing a button !
        Clock.schedule_once(self._refocusTextInput, 0.1)       


    def _refocusTextInput(self, *args):
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
            self.disableHistoryItemControls()
            
        if len(self.commandList.adapter.data) == 0:
            #command list is empty
            self.disableCommandListControls()
                        
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
            self.disableHistoryItemControls()
            
        self.refocusOncommandInput()


    def historyItemSelected(self, instance):
        commandStr = str(instance.text)
        
        #counter-intuitive, but test must be
        #that way !
        if instance.is_selected:
            self.disableHistoryItemControls()
        else:
            self.enableHistoryItemControls()

        self.commandInput.text = commandStr
        self.refocusOncommandInput()


    def enableHistoryItemControls(self):
        self.deleteControl.disabled = False
        self.replaceControl.disabled = False


    def disableHistoryItemControls(self):
        self.deleteControl.disabled = True
        self.replaceControl.disabled = True


    def replayAllCommands(self):
        self.outputResult('')
       
        for command in self.commandList.adapter.data:
             outputResultStr = self.controller.getPrintableResultForInput(command)
             self.outputResult(outputResultStr)

        self.refocusOncommandInput()
                                              

    def openDropDMenu(self, widget):
        self.dropDMenu.open(widget)


    def displayHelp(self):
        popup = Popup(title='Popup', content=Label(text='Help !'), size_hint=(None, None), size=(400, 400))
        popup.open()

                
# --- file chooser code ---  
  
    def dismissPopup(self):
        self._popup.dismiss()


    def openLoadHistoryFileChooser(self):
        content = LoadDialog(load=self.load, cancel=self.dismissPopup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def openSaveHistoryFileChooser(self):
        content = SaveDialog(save=self.save, cancel=self.dismissPopup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.textInput.text = stream.read()

        self.dismissPopup()


    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.textInput.text)

        self.dismissPopup()
                                
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
