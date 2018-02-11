from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton


class RequestListButton(ListItemButton):
    pass


class MySimpleGui(BoxLayout):
    requestInput = ObjectProperty()
    requestList = ObjectProperty()
    resultOutput = ObjectProperty()
    showRequestList = False

    def __init__(self, **kwargs):
        super(MySimpleGui, self).__init__(**kwargs)


    def toggleRequestList(self):
        '''
        called by 'History' toggle button to toggle the display of the history
        command list.
        '''
        if self.showRequestList:
            self.requestList.size_hint_y = None
            self.requestList.height = '0dp'
            self.showRequestList = False
        else:
            self.requestList.height = '100dp'
            self.showRequestList = True

            # Reset the ListView
            self.requestList.adapter.data.extend(
                [])  # improves list view display, but only after user scrolled manually !
            self.resetListViewScrollToEnd(self.requestList)

            self.refocusOnrequestInput()

    def submitRequest(self):
        '''
        Submit the request, output the result and add the request to the
        request list
        :return:
        '''
        # Get the student name from the TextInputs
        requestStr = self.requestInput.text
        self.outputResult(requestStr)

        self.requestList.adapter.data.extend([requestStr])

        # Reset the ListView
        self.resetListViewScrollToEnd(self.requestList)
        self.manageStateOfRequestListButtons()
        self.requestInput.text = ''

        self.refocusOnrequestInput()

    def resetListViewScrollToEnd(self, listView):
        listView._trigger_reset_populate()
        listView.scroll_to(len(self.requestList.adapter.data) - 1)

    def manageStateOfRequestListButtons(self):
        '''
        Enable or disable history command list related controls according to
        the status of the list: filled with items or empty.
        :return:
        '''
        if len(self.requestList.adapter.data) == 0:
            # command list is empty
            self.toggleHistoButton.state = 'normal'
            self.toggleHistoButton.disabled = True
            self.replayAllButton.disabled = True
            self.requestList.height = '0dp'
        else:
            self.toggleHistoButton.disabled = False
            self.replayAllButton.disabled = False

    def outputResult(self, resultStr):
        if len(self.resultOutput.text) == 0:
            self.resultOutput.text = resultStr
        else:
            self.resultOutput.text = self.resultOutput.text + '\n' + resultStr

    def refocusOnrequestInput(self):
        # defining a delay of 0.1 sec ensure the
        # refocus works in all situations. Leaving
        # it empty (== next frame) does not work
        # when pressing a button !
        Clock.schedule_once(self.refocusTextInput, 0.1)

    def refocusTextInput(self, *args):
        self.requestInput.focus = True

    def historyItemSelected(self, instance):
        requestStr = str(instance.text)

        self.requestInput.text = requestStr
        self.refocusOnrequestInput()

    def replayAllRequests(self):
        self.outputResult('')

        for request in self.requestList.adapter.data:
            self.outputResult(request)

        self.refocusOnrequestInput()


class MySimpleGuiApp(App):
    def build(self):
        return MySimpleGui()

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)

        pass


if __name__ == '__main__':
    dbApp = MySimpleGuiApp()

    dbApp.run()

