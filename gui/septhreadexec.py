import threading, time

class SepThreadExec:
	def __init__(self, callerGUI,
				 func,
				 endFunc=None,
				 funcArgs=None,
				 endFuncArgs=None):
		self.callerGUI = callerGUI
		
		if endFuncArgs is None:
			endFuncArgs = ()
		if funcArgs is None:
			funcArgs = {}
		
		args = (func, endFunc) + endFuncArgs
		
		def _callback(func, endFunc, *a, **kw):
			func(**kw)
			
			if endFunc is not None:
				endFunc(*a)
		
		self.t = threading.Thread(target=_callback, args=args, kwargs=funcArgs)
		self.t.setName('Exec thread ' + self.t.getName())
		self.t.daemon = True
		
	def start(self):
		self.t.start()

if __name__ == "__main__":
	def myFunc(name='', age=0):
		for i in range(5):
			time.sleep(1)
			print('My name is {}. I am {} years old'.format(name, age))
	
	def myEndFunc(name='', age=0):
		print('MY SURNAME WAS {}. I was {} years old'.format(name.upper(), age))
		
	ste = SepThreadExec(callerGUI=None,
				  func=myFunc,
				  endFunc=myEndFunc,
				  funcArgs={'name': 'Jean-Pierre', 'age': 60},
				  endFuncArgs=('paulo le scientifique', 14))
	
	ste.start()
	time.sleep(6)
