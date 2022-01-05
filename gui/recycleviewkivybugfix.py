import logging

from kivy.uix.recycleview import RecycleView


class RecycleViewKivyBugFix(RecycleView):
	"""
	This class fixes a Kivy bug which sometimes causes an app failure when the
	first selected item in a displayed list is the last item.
	"""
	def on_scroll_stop(self, touch, check_children=True):
		try:
			super().on_scroll_stop(touch, check_children)
		except IndexError as e:
			# avoids app failure due to the uncaught IndexError exception
			logging.info('Selecting the last list item caused this Kivy bug: ' + str(e))