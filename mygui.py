from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton


class CommandListButton(ListItemButton):
    pass


class MyGui(BoxLayout):
    commandInput = ObjectProperty()
    commandList = ObjectProperty()
    resultOutput = ObjectProperty()
    statusBar = ObjectProperty()
    showCommandList = False

    def __init__(self, **kwargs):
        super(MyGui, self).__init__(**kwargs)


    def toggleRequestList(self):
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
            self.commandList.adapter.data.extend(
                [])  # improves list view display, but only after user scrolled manually !
            self.resetListViewScrollToEnd(self.commandList)

            self.refocusOncommandInput()

    def submitRequest(self):
        '''
        Submit the command, output the result and add the command to the
        command list
        :return:
        '''
        # Get the student name from the TextInputs
        commandStr = self.commandInput.text
        self.outputResult(commandStr)
        self.updateStatusBar(commandStr)

        self.commandList.adapter.data.extend([commandStr])

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
            # command list is empty
            self.toggleHistoButton.state = 'normal'
            self.toggleHistoButton.disabled = True
            self.replayAllButton.disabled = True
            self.commandList.height = '0dp'
        else:
            self.toggleHistoButton.disabled = False
            self.replayAllButton.disabled = False

    def outputResult(self, resultStr):
        if len(self.resultOutput.text) == 0:
            self.resultOutput.text = resultStr
        else:
            self.resultOutput.text = self.resultOutput.text + '\n' + resultStr
            # self.outputResultScrollView.scroll_to(100000)
            # self.resultOutput.cursor = (10000,0)

    def refocusOncommandInput(self):
        # defining a delay of 0.1 sec ensure the
        # refocus works in all situations. Leaving
        # it empty (== next frame) does not work
        # when pressing a button !
        Clock.schedule_once(self.refocusTextInput, 0.1)

    def refocusTextInput(self, *args):
        self.commandInput.focus = True

    def deleteRequest(self, *args):
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

    def replaceRequest(self, *args):
        # If a list item is selected
        if self.commandList.adapter.selection:

            # Get the text from the item selected
            selection = self.commandList.adapter.selection[0].text

            # Remove the matching item
            self.commandList.adapter.data.remove(selection)

            # Get the command from the TextInputs
            commandStr = self.commandInput.text

            # Add the updated data to the list if not already in
            if not commandStr in self.commandList.adapter.data:
                self.commandList.adapter.data.extend([commandStr])

            # Reset the ListView
            self.commandList._trigger_reset_populate()
            self.commandInput.text = ''
            self.disableCommandListItemButtons()

        self.refocusOncommandInput()

    def historyItemSelected(self, instance):
        commandStr = str(instance.text)

        # counter-intuitive, but test must be defined that way !
        if instance.is_selected:
            # disabling the 2 history command list item related buttons
            self.disableCommandListItemButtons()
        else:
            self.enableCommandListItemButtons()

        self.commandInput.text = commandStr
        self.refocusOncommandInput()

    def enableCommandListItemButtons(self):
        self.deleteButton.disabled = False
        self.replaceButton.disabled = False

    def disableCommandListItemButtons(self):
        self.deleteButton.disabled = True
        self.replaceButton.disabled = True

    def replayAllRequests(self):
        self.outputResult('')

        for command in self.commandList.adapter.data:
            self.outputResult(command)

        # self.resultOutput.do_cursor_movement('cursor_pgdown')
        self.refocusOncommandInput()

    def updateStatusBar(self, messageStr):
        self.statusBar.text = messageStr

    def clearOutput(self):
        self.resultOutput.text = ''
        self.refocusOncommandInput()

class MyGuiApp(App):
    def build(self):
        return MyGui()

    # code moved from CryptoPricerGUI to CryptoPricerGUIApp ! Now, works !

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)

        pass

    # end of code moved from CryptoPricerGUI to CryptoPricerGUIApp ! Now, works !


if __name__ == '__main__':
    dbApp = MyGuiApp()

    dbApp.run() 

