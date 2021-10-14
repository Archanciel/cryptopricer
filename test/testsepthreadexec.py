import unittest
import os, sys, inspect, glob
from os.path import sep
import time
from io import StringIO

currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from gui.septhreadexec import SepThreadExec

class TestSepThreadExec(unittest.TestCase):
	def testInitWithFuncAndEndFunc_with_funcArguments_with_endFuncArguments(self):
		def myFunc(name='', age=0):
			for i in range(2):
				time.sleep(1)
				print('My name is {}. I am {} years old'.format(name, age))
		
		def myEndFunc(name='', age=0):
			print('MY SURNAME WAS {}. I was {} years old'.format(name.upper(), age))
		
		ste = SepThreadExec(callerGUI=None,
							func=myFunc,
							endFunc=myEndFunc,
							funcArgs={'name': 'Jean-Pierre', 'age': 60},
							endFuncArgs=('paulo le scientifique', 14))

		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString

		ste.start()
		time.sleep(3)

		sys.stdout = stdout

		self.assertEqual(
			['My name is Jean-Pierre. I am 60 years old',
			 'My name is Jean-Pierre. I am 60 years old',
			 'MY SURNAME WAS PAULO LE SCIENTIFIQUE. I was 14 years old',
			 ''], outputCapturingString.getvalue().split('\n'))
	
	def testInitWithFuncNoEndFunc_with_funcArguments(self):
		def myFunc(name='', age=0):
			for i in range(2):
				time.sleep(1)
				print('My name is {}. I am {} years old'.format(name, age))
		
		ste = SepThreadExec(callerGUI=None,
							func=myFunc,
							endFunc=None,
							funcArgs={'name': 'Jean-Pierre', 'age': 60})
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		ste.start()
		time.sleep(3)
		
		sys.stdout = stdout
		
		self.assertEqual(
			['My name is Jean-Pierre. I am 60 years old',
			 'My name is Jean-Pierre. I am 60 years old',
			 ''], outputCapturingString.getvalue().split('\n'))
	
	def testInitWithFuncNoEndFunc_no_funcArguments(self):
		def myFunc():
			for i in range(2):
				time.sleep(1)
				print('My name is ?')
		
		ste = SepThreadExec(callerGUI=None,
							func=myFunc)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		ste.start()
		time.sleep(3)
		
		sys.stdout = stdout
		
		self.assertEqual(
			['My name is ?', 'My name is ?', ''], outputCapturingString.getvalue().split('\n'))
	
	def testInitWithFuncAndEndFunc_no_funcArguments_with_endFuncArguments(self):
		def myFunc():
			for i in range(2):
				time.sleep(1)
				print('My name is ?')
		
		def myEndFunc(name='', age=0):
			print('MY SURNAME WAS {}. I was {} years old'.format(name.upper(), age))
		
		ste = SepThreadExec(callerGUI=None,
							func=myFunc,
							endFunc=myEndFunc,
							funcArgs=None,
							endFuncArgs=('paulo le scientifique', 14))
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		ste.start()
		time.sleep(3)
		
		sys.stdout = stdout
		
		self.assertEqual(
			['My name is ?',
			 'My name is ?',
			 'MY SURNAME WAS PAULO LE SCIENTIFIQUE. I was 14 years old',
			 ''], outputCapturingString.getvalue().split('\n'))
	
	def testInitWithFuncAndEndFunc_no_funcArguments_no_endFuncArguments(self):
		def myFunc():
			for i in range(2):
				time.sleep(1)
				print('My name is ?')
		
		def myEndFunc():
			print('MY SURNAME WAS ??.')
		
		ste = SepThreadExec(callerGUI=None,
							func=myFunc,
							endFunc=myEndFunc)
		
		stdout = sys.stdout
		outputCapturingString = StringIO()
		sys.stdout = outputCapturingString
		
		ste.start()
		time.sleep(3)
		
		sys.stdout = stdout
		
		self.assertEqual(
			['My name is ?', 'My name is ?', 'MY SURNAME WAS ??.', ''], outputCapturingString.getvalue().split('\n'))


if __name__ == '__main__':
	#unittest.main()
	tst = TestSepThreadExec()
	tst.testReplaceUnauthorizedDirNameChars()
