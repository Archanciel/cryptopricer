from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton


class CommandListButton(ListItemButton):
    pass


class MySimpleGui(BoxLayout):
    commandInput = ObjectProperty()
    commandList = ObjectProperty()
    resultOutput = ObjectProperty()
    showCommandList = False

    def __init__(self, **kwargs):
        super(MySimpleGui, self).__init__(**kwargs)


    def toggleCommandList(self):
        '''
        called by 'History' toggle button to toggle the display of the history
        command list.
        '''
        if self.showCommandList:
            self.commandList.size_hint_y = None
            self.commandList.height = '0dp'
            self.showCommandList = False
        else:
            self.commandList.height = '100dp'
            self.showCommandList = True

            # Reset the ListView
            self.commandList.adapter.data.extend(
                [])  # improves list view display, but only after user scrolled manually !
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
        self.outputResult(commandStr)

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

    def refocusOncommandInput(self):
        # defining a delay of 0.1 sec ensure the
        # refocus works in all situations. Leaving
        # it empty (== next frame) does not work
        # when pressing a button !
        Clock.schedule_once(self.refocusTextInput, 0.1)

    def refocusTextInput(self, *args):
        self.commandInput.focus = True

    def historyItemSelected(self, instance):
        commandStr = str(instance.text)

        self.commandInput.text = commandStr
        self.refocusOncommandInput()

    def replayAllCommands(self):
        self.outputResult('')

        for command in self.commandList.adapter.data:
            self.outputResult(command)

        # self.resultOutput.do_cursor_movement('cursor_pgdown')
        self.refocusOncommandInput()


class MySimpleGuiApp(App):
    def build(self):
        return MySimpleGui()

    # code moved from CryptoPricerGUI to CryptoPricerGUIApp ! Now, works !

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)

        pass

    # end of code moved from CryptoPricerGUI to CryptoPricerGUIApp ! Now, works !


if __name__ == '__main__':
    dbApp = MySimpleGuiApp()

    dbApp.run() 

