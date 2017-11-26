# ---------- KIVY TUTORIAL PT 4  ----------
 
# In this part of my Kivy tutorial I'll show how to use
# the ListView, ListAdapter and how to create a toolbar
 
# ---------- cryptopricerguy.py  ----------
 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
 
 
class CommandListButton(ListItemButton):
    pass


class CryptoPricerGUY(BoxLayout):
 
    # Connects the value in the TextInput widget to these
    # fields
    commandTextInput = ObjectProperty()
    commandList = ObjectProperty()
    ro_log_text_input = ObjectProperty()
 
    def submitCommand(self):
 
        # Get the student name from the TextInputs
        commandStr = self.commandTextInput.text
 
        # Add the student to the ListView
        if commandStr in self.commandList.adapter.data:
            self.ro_log_text_input.text = self.ro_log_text_input.text + '\nsubmitted ' + commandStr
        else:
            self.commandList.adapter.data.extend([commandStr])
            self.ro_log_text_input.text = self.ro_log_text_input.text + '\nsubmitted and added ' + commandStr

        # Reset the ListView
        self.commandList._trigger_reset_populate()

        self.clearName()
        
    def clearName(self):
        self.commandTextInput.text = ''

    def deleteCommand(self, *args):
 
        # If a list item is selected
        if self.commandList.adapter.selection:
 
            # Get the text from the item selected
            selection = self.commandList.adapter.selection[0].text
 
            # Remove the matching item
            self.commandList.adapter.data.remove(selection)
 
            # Reset the ListView
            self.commandList._trigger_reset_populate()
            self.ro_log_text_input.text = self.ro_log_text_input.text + '\ndeleted ' + selection
            self.clearName()
 
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
            self.ro_log_text_input.text = self.ro_log_text_input.text + '\n' + selection + ' replaced by ' + commandStr + '\nsubmitted ' + commandStr
            self.clearName()


    def commandSelected(self, instance):
        commandStr = str(instance.text)

        self.commandTextInput.text = commandStr


class CryptoPricerGUYApp(App):
    def build(self):
        return CryptoPricerGUY()
 
 
dbApp = CryptoPricerGUYApp()
 
dbApp.run()
