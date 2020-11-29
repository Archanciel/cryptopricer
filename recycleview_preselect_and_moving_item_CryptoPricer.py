import os, logging

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from configurationmanager import ConfigurationManager

MOVE_DIRECTION_UP = 'moveItemUp'
MOVE_DIRECTION_DOWN = 'moveItemDown'

kv = """
#: import ScrollEffect kivy.effects.scroll.ScrollEffect

<SelectableLabel>:
	# Draw a background to indicate selection
	canvas.before:
		Color:
			rgba: (0.4, 0.4, 0.4, 1) if self.selected else (0.5, 0.5, 0.5, 1)
		Rectangle:
			pos: self.pos
			size: self.size

<KivyPlayer>:
	orientation: 'vertical'
	#optimizing app size for your smartphone with Messagease keyboard
    size_hint: 1, .62
    pos_hint: {'x' : 0, 'y' : .38}
 
    requestListRV: request_RecycleView_list
    boxLayoutContainingRV: boxlayout_recycleview
    requestInput: request_TextInput

    padding: 5
    spacing: 5
    canvas.before:
        Color:
            rgb: [0.22,0.22,0.22]
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: "28dp"
        canvas.before:
            Color:
                rgb: [0,0,0]
            Rectangle:
                pos: self.pos
                size: self.size

        GridLayout:
            cols: 2
            TextInput:
                id: request_TextInput
                background_color: 0,0,0,0
                foreground_color: 1,1,1,1
                focus: True
                multiline: False
                #ENTER triggers root.submitRequest()
                on_text_validate: root.submitRequest()
                on_text: root.ensureLowercase()
            Button:
                id: toggle_app_size_Button
                text: 'Full'
                size_hint_x: None
                width: 130
                on_press: root.toggleAppPosAndSize()
                
	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
	        size_hint_y: None
	        height: "28dp"
	        ToggleButton:
	            id: toggle_history_list_Button
	            text: "History"
	            size_hint_x: 15
	            disabled:False
	            on_press: root.toggleRequestList()
	        Button:
	            id: delete_Button
	            text: "Delete"
	            size_hint_x: 15
	            disabled: True
	            on_press: root.deleteRequest()
	        Button:
	            id: replace_Button
	            text: "Replace"
	            size_hint_x: 15
	            disabled: True
	            on_press: root.replaceRequest()
			Button:
				id: moveItemUp
				text: "^"
	            size_hint_x: 8
	            disabled: True
				on_press: request_RecycleView_list.moveItemUp()
			Button:
				id: moveItemDown
				text: "v"
	            size_hint_x: 8
	            disabled: True
				on_press: request_RecycleView_list.moveItemDown()

		BoxLayout:
	        id: boxlayout_recycleview
	        size_hint_y: None
	        height: "0dp"
			RecycleView:
				id: RV_list_item
	            scroll_y: 0 # forces scrolling to list bottom after adding an entry
	            effect_cls: "ScrollEffect" # prevents overscrolling
				viewclass: 'SelectableLabel'
				scroll_type: ['bars', 'content']
				scroll_wheel_distance: dp(114)
				bar_width: dp(10)
				SelectableRecycleBoxLayout:
					id: request_RecycleView_list
					key_selection: 'selectable' # required so that 'selectable'
												# key/value can be added to
												# RecycleView data items
					default_size: None, dp(36)
					default_size_hint: 1, None
					size_hint_y: None
					height: self.minimum_height
					orientation: 'vertical'
					multiselect: False
					touch_multiselect: False
					spacing: dp(2)

    ScrollView:
        id: scrlv_out
        canvas.before:
            Color:
                rgb: [0,0,0]
            Rectangle:
                pos: self.pos
                size: self.size
        effect_cls: ScrollEffect #prevents overscrolling
        scroll_y: 0 # forces scrolling to bottom after adding text
        TextInput:
            id: ro_output_TextInput
            size_hint: (1, None)
            height: max(self.minimum_height, scrlv_out.height) #required to enable scrolling when output starts to grow
            readonly: True
            background_color: 0,0,0,0
            foreground_color: 1,1,1,1

"""

Builder.load_string(kv)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
								 RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''

	# required to authorize unselecting a selected item.
	touch_deselect_last = BooleanProperty(True)

	def get_nodes(self):
		nodes = self.get_selectable_nodes()

		if self.nodes_order_reversed:
			nodes = nodes[::-1]
		if not nodes:
			return None, None
		
		selected = self.selected_nodes

		if not selected:  # nothing selected, select the first
			return None, None
		
		if len(nodes) == 1:  # the only selectable node is selected already
			return None, None
		
		last = nodes.index(selected[-1])
		self.clear_selection()

		return last, nodes
	
	def moveItemUp(self):
		last, nodes = self.get_nodes()
		
		if not nodes:
			return
		
		if not last:
			newSelIdx = -1
			self.updateLineValues(MOVE_DIRECTION_UP, last, newSelIdx)
			self.select_node(nodes[newSelIdx])
		else:
			newSelIdx = last - 1
			self.updateLineValues(MOVE_DIRECTION_UP, last, newSelIdx)
			self.select_node(nodes[newSelIdx])
	
	def moveItemDown(self):
		last, nodes = self.get_nodes()

		if not nodes:
			return

		if last == len(nodes) - 1:
			newSelIdx = 0
			self.updateLineValues(MOVE_DIRECTION_DOWN, last, newSelIdx)
			self.select_node(nodes[newSelIdx])
		else:
			newSelIdx = last + 1
			self.updateLineValues(MOVE_DIRECTION_DOWN, last, newSelIdx)
			self.select_node(nodes[newSelIdx])
	
	def updateLineValues(self, moveDirection, movedItemSelIndex, movedItemNewSeIndex):
		movedValue = self.parent.data[movedItemSelIndex]['text']

		if moveDirection == MOVE_DIRECTION_DOWN:
			if movedItemSelIndex > movedItemNewSeIndex:
				# we are moving down the last list item. The item will be inserted at top
				# of the list
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(0, {'text': movedValue, 'selectable': True})
			else:
				replacedValue = self.parent.data[movedItemNewSeIndex]['text']
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(movedItemSelIndex, {'text': replacedValue, 'selectable': True})
				
				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {'text': movedValue, 'selectable': True})
		else:
			# handling moving up
			if movedItemSelIndex == 0:
				# we are moving up the first item. The first item will be appended to the
				# end of the list
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.append({'text': movedValue, 'selectable': True})
			else:
				replacedValue = self.parent.data[movedItemNewSeIndex]['text']
				self.parent.data.pop(movedItemSelIndex)
				self.parent.data.insert(movedItemSelIndex, {'text': replacedValue, 'selectable': True})
				
				self.parent.data.pop(movedItemNewSeIndex)
				self.parent.data.insert(movedItemNewSeIndex, {'text': movedValue, 'selectable': True})
	
	def updateButtonStatus(self, kivyPlayer):
		buttonIds = kivyPlayer.ids
		
		if kivyPlayer.isLineSelected:
			buttonIds.moveItemDown.disabled = False
			buttonIds.moveItemUp.disabled = False
			buttonIds.unselect_item.disabled = False
		else:
			buttonIds.moveItemDown.disabled = True
			buttonIds.moveItemUp.disabled = True
			buttonIds.unselect_item.disabled = True

class SelectableLabel(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.rv = rv
		self.index = index

		return super(SelectableLabel, self).refresh_view_attrs(
			rv, index, data)

	def on_touch_down(self, touch):
		''' Add selection on touch down '''

		kivyPlayer = self.rv.parent.parent.parent
		logging.info('on_touch_down, index {}, text {}, selected {}'.format(self.index, self.text, self.selected))

		# reinitializing the current selection index. The index will be set - or not -
		# in the apply_selection method !
		kivyPlayer.isLineSelected = False

		if super(SelectableLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		''' Respond to the selection of items in the view. '''
		self.selected = is_selected
		
		kivyPlayer = rv.parent.parent.parent
		
		if is_selected:
			logging.info("selection set for {0}".format(rv.data[index]))
			kivyPlayer.isLineSelected = True # will cause the buttons to be enabled
		else:
			logging.info("selection removed for {0}".format(rv.data[index]))
		
		self.updateButtonStatus(kivyPlayer)
	
	def updateButtonStatus(self, kivyPlayer):
		buttonIds = kivyPlayer.ids
		
		if kivyPlayer.isLineSelected:
			buttonIds.moveItemDown.disabled = False
			buttonIds.moveItemUp.disabled = False
		else:
			buttonIds.moveItemDown.disabled = True
			buttonIds.moveItemUp.disabled = True

class KivyPlayer(BoxLayout):
	''' Main Kivy class for creating the initial BoxLayout '''

	showRequestList = False

	def __init__(self, **kwargs):
		super(KivyPlayer, self).__init__(**kwargs)

		# Set RV_list_item data
		self.ids.RV_list_item.data = [{'text': 'line {}'.format(x), 'selectable': True} for x in range(7)]
		
		# specify pre-selected node by its index in the data
#		self.requestListRV.selected_nodes = [0]
		if os.name == 'posix':
			configPath = '/sdcard/cryptopricer.ini'
			requestListRVSpacing = 2
		else:
			configPath = 'c:\\temp\\cryptopricer.ini'
#			self.toggleAppSizeButton.text = 'Half'  # correct on Windows version !

		self.configMgr = ConfigurationManager(configPath)
#		self.controller = Controller(GuiOutputFormater(self.configMgr, activateClipboard=True), self.configMgr, PriceRequester())
		self.dataPath = self.configMgr.dataPath
		self.histoListItemHeight = int(self.configMgr.histoListItemHeight)
		self.histoListMaxVisibleItems = int(self.configMgr.histoListVisibleSize)
		self.maxHistoListHeight = self.histoListMaxVisibleItems * self.histoListItemHeight

		self.isLineSelected = False

	def toggleRequestList(self):
		'''
		called by 'History' toggle button to toggle the display of the history
		request list.
		'''
		if self.showRequestList:
			# hiding RecycleView list
			self.boxLayoutContainingRV.height = '0dp'

#			self.disableRequestListItemButtons()
			self.showRequestList = False
		else:
			# showing RecycleView list
			self.adjustRequestListSize()
			self.showRequestList = True
			# self.resetListViewScrollToEnd()
			# self.refocusOnRequestInput()

	def adjustRequestListSize(self):
		listItemNumber = len(self.requestListRV.recycleview.data)
		self.boxLayoutContainingRV.height = min(listItemNumber * self.histoListItemHeight, self.maxHistoListHeight)

		return listItemNumber

	def resetListViewScrollToEnd(self):
		maxVisibleItemNumber = self.histoListMaxVisibleItems
		listLength = len(self.requestListRV.data)

		if listLength > maxVisibleItemNumber:
			# for the moment, I do not know how to scroll to end of RecyclweView !
			# listView.scroll_to(listLength - maxVisibleItemNumber)
			pass
		else:
			if self.showRequestList:
				listItemNumber = self.adjustRequestListSize()
				if listItemNumber == 0:
					self.showRequestList = False
					self.manageStateOfRequestListButtons()

	def ensureLowercase(self):
		'''
		Ensure the input text control only contains lower cases.
		'''
		# Get the request from the TextInput
		requestStr = self.requestInput.text
		self.requestInput.text = requestStr.lower()

class KivyApp(App):
	def build(self):
		self.title = 'For CryptoPricer'

		if os.name != 'posix':
			# running app om Windows
			Config.set('graphics', 'width', '600')
			Config.set('graphics', 'height', '260')
			Config.write()

		return KivyPlayer()
	
KivyApp().run()
