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
    commandTextInput = ObjectProperty()
    commandList = ObjectProperty()
    resultOutputROTextInput = ObjectProperty()
    showCommandList = False
    controller = Controller(GuiOutputFormater())

  
    def toggleCommandList(self):
        if self.showCommandList:
            self.commandList.size_hint_y = None
            self.commandList.height = '0dp'
            self.showCommandList = False
        else:
            self.commandList.size_hint_y = 0.5
            self.showCommandList = True
        
        self.refocusOnCommandTextInput()

                
    def submitCommand(self):
        '''
        Submit the command, output the result and add the command to the
        command list
        :return:
        '''
        # Get the student name from the TextInputs
        commandStr = self.commandTextInput.text

        if commandStr != '':
            outputResultStr = self.controller.getPrintableResultForInput(commandStr)
            self.resultOutputROTextInput.text = self.resultOutputROTextInput.text + '\n' + outputResultStr

            # Add the command to the ListView if not already in
            if not commandStr in self.commandList.adapter.data:
                self.commandList.adapter.data.extend([commandStr])

            # Reset the ListView
            self.commandList._trigger_reset_populate()

            self.commandTextInput.text = ''

        self.refocusOnCommandTextInput()

        
    def refocusOnCommandTextInput(self):
        #defining a delay of 0.1 sec ensure the
        #refocus works in all situations. Leaving
        #it empty (== next frame) does not work
        #when pressing a button !
        Clock.schedule_once(self._refocusTextInput, 0.1)       


    def _refocusTextInput(self, *args):
        self.commandTextInput.focus = True

                                      
    def deleteCommand(self, *args):
        # If a list item is selected
        if self.commandList.adapter.selection:
 
            # Get the text from the item selected
            selection = self.commandList.adapter.selection[0].text
 
            # Remove the matching item
            self.commandList.adapter.data.remove(selection)
 
            # Reset the ListView
            self.commandList._trigger_reset_populate()
            self.resultOutputROTextInput.text = self.resultOutputROTextInput.text + '\ndeleted ' + selection
            self.commandTextInput.text = ''
            
        self.refocusOnCommandTextInput()

  
    def replaceCommand(self, *args):
        # If a list item is selected
        if self.commandList.adapter.selection:
 
            # Get the text from the item selected
            selection = self.commandList.adapter.selection[0].text
 
            # Remove the matching item
            self.commandList.adapter.data.remove(selection)
 
            # Get the student name from the TextInputs
            commandStr = self.commandTextInput.text
 
            # Add the updated data to the list
            self.commandList.adapter.data.extend([commandStr])
 
            # Reset the ListView
            self.commandList._trigger_reset_populate()
            self.resultOutputROTextInput.text = self.resultOutputROTextInput.text + '\n' + selection + ' replaced by ' + commandStr + '\nsubmitted ' + commandStr
            self.commandTextInput.text = ''
            
        self.refocusOnCommandTextInput()


    def commandSelected(self, instance):
        commandStr = str(instance.text)

        self.commandTextInput.text = commandStr
        self.refocusOnCommandTextInput()


class CryptoPricerGUYApp(App):
    def build(self):
        return CryptoPricerGUY()
 
 
dbApp = CryptoPricerGUYApp()
 
dbApp.run()
