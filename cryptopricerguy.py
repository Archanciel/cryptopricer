# ---------- KIVY TUTORIAL PT 4  ----------
 
# In this part of my Kivy tutorial I'll show how to use
# the ListView, ListAdapter and how to create a toolbar
 
# ---------- cryptopricerguy.py  ----------
 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.clock import Clock

from controller import Controller
from guioutputformaterr import GuiOutputFormater


class CommandListButton(ListItemButton):
    pass


class CryptoPricerGUY(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    commandInput = ObjectProperty()
    commandList = ObjectProperty()
    resultOutput = ObjectProperty()
    showCommandList = False
    controller = Controller(GuiOutputFormater())

  
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
                                             
                            
class CryptoPricerGUYApp(App):
    def build(self):
        return CryptoPricerGUY()
 
 
dbApp = CryptoPricerGUYApp()
 
dbApp.run()
