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

MOVE_DIRECTION_UP = 'moveItemUp'
MOVE_DIRECTION_DOWN = 'moveItemDown'

kv = """

<SelectableLabel>:
	# Draw a background to indicate selection
	canvas.before:
		Color:
			rgba: (0.4, 0.4, 0.4, 1) if self.selected else (0.5, 0.5, 0.5, 1)
		Rectangle:
			pos: self.pos
			size: self.size

<KivyPlayer>:
	canvas:
		Color:
			rgba: 0.3, 0.3, 0.3, 1
		Rectangle:
			size: self.size
			pos: self.pos
	orientation: 'vertical'
	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			size_hint_y: 0.3
			Button:
				id: moveItemDown
				text: "Move item down"
				on_release: controller.moveItemDown()
			Button:
				id: moveItemUp
				text: "Move item up"
				on_release: controller.moveItemUp()
			Button:
				id: unselect_item
				text: "Unselect item"
				on_release: controller.unselectItem()
		BoxLayout:
			RecycleView:
				id: RV_list_item
				viewclass: 'SelectableLabel'
				scroll_type: ['bars', 'content']
				scroll_wheel_distance: dp(114)
				bar_width: dp(10)
				SelectableRecycleBoxLayout:
					id: controller
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

	def unselectItem(self):
		kivyPlayer = self.parent.parent.parent.parent
		kivyPlayer.isLineSelected = False
		self.clear_selection()
		
		# required to update buttons status if the unselect button was pressed
		# and the selected item was outside the visible part of the item list !
		self.updateButtonStatus(kivyPlayer)
	
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
			buttonIds.unselect_item.disabled = False
		else:
			buttonIds.moveItemDown.disabled = True
			buttonIds.moveItemUp.disabled = True
			buttonIds.unselect_item.disabled = True

class KivyPlayer(BoxLayout):
	''' Main Kivy class for creating the initial BoxLayout '''

	def __init__(self, **kwargs):
		super(KivyPlayer, self).__init__(**kwargs)

		# Set RV_list_item data
		self.ids.RV_list_item.data = [{'text': 'line {}'.format(x), 'selectable': True} for x in range(15)]
		
		# specify pre-selected node by its index in the data
		self.ids.controller.selected_nodes = [0]

class KivyApp(App):
	def build(self):
		self.title = 'For CryptoPricer'

		if os.name != 'posix':
			# running app om Windows
			Config.set('graphics', 'width', '600')
			Config.set('graphics', 'height', '500')
			Config.write()

		return KivyPlayer()
	
KivyApp().run()
