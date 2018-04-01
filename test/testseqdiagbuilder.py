import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
                              # the test is executed standalone

from seqdiagbuilder import SeqDiagBuilder
from seqdiagbuilder import FlowEntry
from seqdiagbuilder import RecordedFlowPath
from controller import Controller
from pricerequester import PriceRequester


class Foo:
    def f(self, fParm):
        '''

        :param fParm:
        :seqdiag_return fReturn
        :return:
        '''
        b = Bar()
        e = Egg()

        b.g()
        e.h(1, 2)


class Bar:
    def g(self):
        '''

        :seqdiag_return gReturn
        :return:
        '''
        lo = LeafOne()
        lo.i()


class Egg:
    def h(self, hParm1, hParm2):
        lt = LeafTwo()
        lt.j()


class LeafOne:
    def i(self):
        SeqDiagBuilder.recordFlow(3)


class LeafTwo:
    def j(self):
        SeqDiagBuilder.recordFlow(3)


class Client:
    def do(self):
        c1 = ChildOne()
        c1.getCoordinate()


    def make(self):
        c1 = ChildOne()
        c1.compute()


    def perform(self):
        c1 = ChildOne()
        c1.computeTwo()


    def doCall(self):
        c1 = ChildOne()
        c1.computeThree()


    def doProcess(self):
        c1 = ChildOfChildTwo()
        c1.computeFour()


class Parent:
    def getCoordinate(self, location=''):
        '''

        :param location:
        :seqdiag_return Coord
        :return:
        '''
        SeqDiagBuilder.recordFlow()


    def getCoordinateNoneSelected(self, location=''):
        '''

        :param location:
        :seqdiag_return Coord
        :return:
        '''
        SeqDiagBuilder.recordFlow()


    def compute(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_return Analysis
        :return:
        '''
        pass


    def computeTwo(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_select_method
        :seqdiag_return Analysis
        :return:
        '''
        pass


    def computeThree(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_select_method
        :seqdiag_return Analysis
        :return:
        '''
        iso = IsolatedClass()
        iso.analyse()


    def computeFour(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_return Analysis
        :return:
        '''
        pass


class ChildOne(Parent):
    def getCoordinate(self, location=''):
        iso = IsolatedClass()
        iso.analyse()

    def getCoordinateNoneSelected(self, location=''):
        iso = IsolatedClass()
        iso.analyse()

    def m(self):
        pass


    def compute(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_select_method
        :seqdiag_return Analysis
        :return:
        '''
        super().compute(size)
        iso = IsolatedClass()
        iso.analyse()


    def computeTwo(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_select_method
        :seqdiag_return Analysis
        :return:
        '''
        super().compute(size)
        iso = IsolatedClass()
        iso.analyse()


class ChildTwo(Parent):
    def l(self):
        pass


    def computeFour(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_select_method
        :seqdiag_return Analysis
        :return:
        '''
        iso = IsolatedClass()
        iso.analyse()


    def getCoordinateNoneSelected(self, location=''):
        SeqDiagBuilder.recordFlow()


class ChildThree(Parent):
    def getCoordinate(self, location=''):
        '''

        :param location:
        :seqdiag_return CoordSel
        :seqdiag_select_method
        :return:
        '''
        SeqDiagBuilder.recordFlow()


class ChildOfChildTwo(Parent):
    def l(self):
        pass


    def computeFour(self, size = 0):
        '''
        This a dummy merhod.
        :seqdiag_return Analysis
        :return:
        '''
        iso = IsolatedClass()
        iso.analyse()


class IsolatedClass:
    def analyse(self):
        '''

        :seqdiag_return Analysis
        :return:
        '''
        SeqDiagBuilder.recordFlow(3)


class ClassA:
    def doWork(self):
        '''
        :seqdiag_return ClassAdoWorkRes
        :return:
        '''
        self.internalCall()


    def internalCall(self):
        '''
        :seqdiag_return ResultPrice
        :return:
        '''
        pr = self.internalInnerCall()
        b = ClassB()
        res = b.createRequest(1, 2)


    def internalInnerCall(self):
        '''
        :seqdiag_return ResultPrice
        :return:
        '''
        b = ClassB()
        res = b.createInnerRequest(1)


class ClassB:
    def createInnerRequest(self, parm1):
        '''
        :seqdiag_return Bool
        :param parm1:
        :return:
        '''
        SeqDiagBuilder.recordFlow()


    def createRequest(self, parm1, parm2):
        '''
        :seqdiag_return Bool
        :param parm1:
        :return:
        '''
        SeqDiagBuilder.recordFlow()


class D:
    def d1(self, d1_p1):
        '''

        :param d1_p1:
        :seqdiag_return Dd1Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def d2(self, d2_p1):
        '''

        :param d2_p1:
        :seqdiag_return Dd2Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def d3(self, d3_p1):
        '''

        :param d3_p1:
        :seqdiag_return Dd3Return
        :return:
        '''
        return 'Dd3Return'

class C:
    def c1(self, c1_p1):
        '''

        :param c1_p1:
        :seqdiag_return Cc1Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def c2(self, c2_p1):
        '''

        :param c2_p1:
        :seqdiag_return Cc2Return
        :return:
        '''
        d = D()
        d.d1(1)
    def c3(self, c3_p1):
        '''

        :param c3_p1:
        :seqdiag_return Cc3Return
        :return:
        '''
        d = D()
        d.d2(1)
        SeqDiagBuilder.recordFlow()
        self.c4(1)
    def c4(self, c4_p1):
        '''

        :param c4_p1:
        :seqdiag_return Cc4Return
        :return:
        '''
        d = D()
        d.d2(1)
        SeqDiagBuilder.recordFlow()
    def c5(self, c5_p1):
        '''

        :param c5_p1:
        :seqdiag_return Cc5Return
        :return:
        '''
        d = D()
        d.d3(1)
    def fibonaci(self, number):
        '''

        :param number:
        :seqdiag_return CfibonaciReturn
        :return:
        '''
        if number == 1:
            SeqDiagBuilder.recordFlow()
            return 1
        else:
            return number + self.fibonaci(number - 1)

class B:
    def b0(self, b1_p1):
        '''

        :param b1_p1:
        :seqdiag_return Bb1Return
        :return:
        '''
        pass
    def b1(self, b1_p1):
        '''

        :param b1_p1:
        :seqdiag_return Bb1Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def b2(self, b2_p1):
        '''

        :param b2_p1:
        :seqdiag_return Bb2Return
        :return:
        '''
        c = C()
        c.c1(1)
    def b3(self, b3_p1):
        '''

        :param b3_p1:
        :seqdiag_return Bb3Return
        :return:
        '''
        c = C()
        c.c1(1)
        c.c1(1)
    def b4(self, b4_p1):
        '''

        :param b4_p1:
        :seqdiag_return Bb4Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def b5(self, b5_p1):
        '''

        :param b5_p1:
        :seqdiag_return Bb5Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def b6(self, b6_p1):
        '''

        :param b6_p1:
        :seqdiag_return Bb6Return
        :return:
        '''
        c = C()
        c.c2(1)
    def b7(self, b7_p1):
        '''

        :param b7_p1:
        :seqdiag_return Bb7Return
        :return:
        '''
        c = C()
        c.c3(1)
        SeqDiagBuilder.recordFlow()
        d = D()
        d.d2(1)
    def b8(self, b8_p1):
        '''

        :param b8_p1:
        :seqdiag_return Bb8Return
        :return:
        '''
        c = C()
        c.c5(1)
        d = D()
        d.d2(1)

class A:
    def a0(self, a1_p1, a1_p2):
        '''
        :param a1_p1:
        :param a1_p2:
        :seqdiag_return Aa1Return
        :return:
        '''
        pass
    def a1(self, a1_p1, a1_p2):
        '''
        :param a1_p1:
        :param a1_p2:
        :seqdiag_return Aa1Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def a2(self, a2_p1):
        '''
        :param a2_p1:
        :seqdiag_return Aa2Return
        :return:
        '''
        b = B()
        b.b1(1)
    def a3(self, a3_p1):
        '''
        :param a3_p1:
        :seqdiag_return Aa3Return
        :return:
        '''
        b = B()
        b.b2(1)
    def a4(self, a4_p1):
        '''
        :param a4_p1:
        :seqdiag_return Aa4Return
        :return:
        '''
        b = B()
        b.b1(1)
        b.b1(1)
    def a5(self, a5_p1):
        '''
        :param a5_p1:
        :seqdiag_return Aa5Return
        :return:
        '''
        b = B()
        b.b1(1)
        b.b1(1)
        b.b1(1)
    def a6(self, a6_p1):
        '''
        :param a6_p1:
        :seqdiag_return Aa6Return
        :return:
        '''
        b = B()
        b.b2(1)
        b.b2(1)
    def a7(self, a7_p1):
        '''
        :param a7_p1:
        :seqdiag_return Aa6Return
        :return:
        '''
        b = B()
        b.b3(1)
    def a8(self, a8_p1, a8_p2):
        '''
        :param a8_p1:
        :param a8_p2:
        :seqdiag_return Aa8Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def a9(self, a9_p1):
        '''
        :param a9_p1:
        :seqdiag_return Aa9Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()
    def a10(self, a10_p1):
        '''
        :param a10_p1:
        :seqdiag_return Aa10Return
        :return:
        '''
        b = B()
        b.b4(1)
        b.b5(1)
    def a11(self, a11_p1):
        '''
        :param a11_p1:
        :seqdiag_return Aa11Return
        :return:
        '''
        b = B()
        b.b6(1)
        b.b6(1)
    def a12(self, a12_p1):
        '''
        :param a12_p1:
        :seqdiag_return Aa12Return
        :return:
        '''
        b = B()
        b.b7(1)
        b.b7(1)
        SeqDiagBuilder.recordFlow()
    def a13(self, a13_p1):
        '''
        :param a13_p1:
        :seqdiag_return Aa13Return
        :return:
        '''
        b = B()
        b.b8(1)
        b.b8(1)


class TestSeqDiagBuilder(unittest.TestCase):
    def setUp(self):
        SeqDiagBuilder.deactivate()


    def testCreateSeqDiaqCommandsOnSimplestCallWithoutRecordFlowCall(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a0')  # activate sequence diagram building
        entryPoint.a0(1, 2)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 1)
        self.assertEqual(
'''@startuml
left header
<b><font color=red >Warnings</font></b>
<font color=red>No control flow recorded. Method activate() called: True. Method recordFlow() called: False. Specified entry point: A.a0.</font>
endheader

@enduml''', commands)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnSimplestCall(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a1')  # activate sequence diagram building
        entryPoint.a1(1, 2)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        self.assertEqual(
'''@startuml

actor USER
USER -> A: a1(a1_p1, a1_p2)
	activate A
	USER <-- A: return Aa1Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building

    def testCreateSeqDiaqCommandsTwoLevelCallTwoDiffMethods(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a10')  # activate sequence diagram building
        entryPoint.a10(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        self.assertEqual(
'''@startuml

actor USER
USER -> A: a10(a10_p1)
	activate A
	A -> B: b4(b4_p1)
		activate B
		A <-- B: return Bb4Return
		deactivate B
	A -> B: b5(b5_p1)
		activate B
		A <-- B: return Bb5Return
		deactivate B
	USER <-- A: return Aa10Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building

    def testCreateSeqDiaqCommandsOnTwoLevelCall(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a2')  # activate sequence diagram building
        entryPoint.a2(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a2(a2_p1)
	activate A
	A -> B: b1(b1_p1)
		activate B
		A <-- B: return Bb1Return
		deactivate B
	USER <-- A: return Aa2Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnThreeLevelCallingMidLevelMethodTwice(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a6')  # activate sequence diagram building
        entryPoint.a6(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a6(a6_p1)
	activate A
	A -> B: b2(b2_p1)
		activate B
		B -> C: c1(c1_p1)
			activate C
			B <-- C: return Cc1Return
			deactivate C
		A <-- B: return Bb2Return
		deactivate B
	A -> B: b2(b2_p1)
		activate B
		B -> C: c1(c1_p1)
			activate C
			B <-- C: return Cc1Return
			deactivate C
		A <-- B: return Bb2Return
		deactivate B
	USER <-- A: return Aa6Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnFiveLevelCallingSecondLevelMethodTwice(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a11')  # activate sequence diagram building
        entryPoint.a11(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a11(a11_p1)
	activate A
	A -> B: b6(b6_p1)
		activate B
		B -> C: c2(c2_p1)
			activate C
			C -> D: d1(d1_p1)
				activate D
				C <-- D: return Dd1Return
				deactivate D
			B <-- C: return Cc2Return
			deactivate C
		A <-- B: return Bb6Return
		deactivate B
	A -> B: b6(b6_p1)
		activate B
		B -> C: c2(c2_p1)
			activate C
			C -> D: d1(d1_p1)
				activate D
				C <-- D: return Dd1Return
				deactivate D
			B <-- C: return Cc2Return
			deactivate C
		A <-- B: return Bb6Return
		deactivate B
	USER <-- A: return Aa11Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building

    def testCreateSeqDiaqCommandsOnFiveLevelCallingSecondLevelMethodTwiceWithRecordFlowInEveryMethod(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a12')  # activate sequence diagram building
        entryPoint.a12(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a12(a12_p1)
	activate A
	A -> B: b7(b7_p1)
		activate B
		B -> C: c3(c3_p1)
			activate C
			C -> D: d2(d2_p1)
				activate D
				C <-- D: return Dd2Return
				deactivate D
			C -> C: c4(c4_p1)
				activate C
				C -> D: d2(d2_p1)
					activate D
					C <-- D: return Dd2Return
					deactivate D
				C <-- C: return Cc4Return
				deactivate C
			B <-- C: return Cc3Return
			deactivate C
		B -> D: d2(d2_p1)
			activate D
			B <-- D: return Dd2Return
			deactivate D
		A <-- B: return Bb7Return
		deactivate B
	A -> B: b7(b7_p1)
		activate B
		B -> C: c3(c3_p1)
			activate C
			C -> D: d2(d2_p1)
				activate D
				C <-- D: return Dd2Return
				deactivate D
			C -> C: c4(c4_p1)
				activate C
				C -> D: d2(d2_p1)
					activate D
					C <-- D: return Dd2Return
					deactivate D
				C <-- C: return Cc4Return
				deactivate C
			B <-- C: return Cc3Return
			deactivate C
		B -> D: d2(d2_p1)
			activate D
			B <-- D: return Dd2Return
			deactivate D
		A <-- B: return Bb7Return
		deactivate B
	USER <-- A: return Aa12Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building

    def testCreateSeqDiaqCommandsOnFiveLevelCallingSecondLevelMethodTwiceWithRecordFlowInOnePlaceOnly(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a13')  # activate sequence diagram building
        entryPoint.a13(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a13(a13_p1)
	activate A
	A -> B: b8(b8_p1)
		activate B
		B -> D: d2(d2_p1)
			activate D
			B <-- D: return Dd2Return
			deactivate D
		A <-- B: return Bb8Return
		deactivate B
	A -> B: b8(b8_p1)
		activate B
		B -> D: d2(d2_p1)
			activate D
			B <-- D: return Dd2Return
			deactivate D
		A <-- B: return Bb8Return
		deactivate B
	USER <-- A: return Aa13Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnThreeLevelCallingLastLevelMethodTwice(self):
        '''
        Calling two level deep method which calls last Level method twice
        :return:
        '''
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a7')  # activate sequence diagram building
        entryPoint.a7(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a7(a7_p1)
	activate A
	A -> B: b3(b3_p1)
		activate B
		B -> C: c1(c1_p1)
			activate C
			B <-- C: return Cc1Return
			deactivate C
		B -> C: c1(c1_p1)
			activate C
			B <-- C: return Cc1Return
			deactivate C
		A <-- B: return Bb3Return
		deactivate B
	USER <-- A: return Aa6Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnTwoLevelCallCallingMethodTwice(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a4')  # activate sequence diagram building
        entryPoint.a4(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a4(a4_p1)
	activate A
	A -> B: b1(b1_p1)
		activate B
		A <-- B: return Bb1Return
		deactivate B
	A -> B: b1(b1_p1)
		activate B
		A <-- B: return Bb1Return
		deactivate B
	USER <-- A: return Aa4Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnTwoLevelCallCallingMethodThreeTimes(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a5')  # activate sequence diagram building
        entryPoint.a5(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> A: a5(a5_p1)
	activate A
	A -> B: b1(b1_p1)
		activate B
		A <-- B: return Bb1Return
		deactivate B
	A -> B: b1(b1_p1)
		activate B
		A <-- B: return Bb1Return
		deactivate B
	A -> B: b1(b1_p1)
		activate B
		A <-- B: return Bb1Return
		deactivate B
	USER <-- A: return Aa5Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsOnThreeLevelCall(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a3')  # activate sequence diagram building
        entryPoint.a3(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        self.assertEqual(
'''@startuml

actor USER
USER -> A: a3(a3_p1)
	activate A
	A -> B: b2(b2_p1)
		activate B
		B -> C: c1(c1_p1)
			activate C
			B <-- C: return Cc1Return
			deactivate C
		A <-- B: return Bb2Return
		deactivate B
	USER <-- A: return Aa3Return
	deactivate A
@enduml''', commands)

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building

    def test_instanciateClassInitTwoArgs(self):
        className = 'Controller'
        moduleName = 'controller'

        instance = SeqDiagBuilder._instanciateClass(className, moduleName)

        self.assertIsInstance(instance, Controller)


    def test_instanciateClassInitNoArgs(self):
        className = 'PriceRequester'
        moduleName = 'pricerequester'

        instance = SeqDiagBuilder._instanciateClass(className, moduleName)

        self.assertIsInstance(instance, PriceRequester)


    def test_getFilteredInstanceListAndMethodSignatureAndReturnDoc(self):
        className = 'Controller'
        moduleName = 'controller'
        methodName = 'getPrintableResultForInput'

        instanceList = [SeqDiagBuilder._instanciateClass(className, moduleName)]
        filteredInstanceList, returnDoc, methodSignature = SeqDiagBuilder._getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName)

        self.assertEqual(len(filteredInstanceList), 1)
        self.assertEqual(returnDoc, 'printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions')
        self.assertEqual(methodSignature, '(inputStr)')


    def test_getFilteredInstanceListAndMethodSignatureAndReturnDocWhereMulitpleClassesSupportSameMethod(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'getCoordinate'
        instanceList = SeqDiagBuilder._getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        filteredInstanceList, returnDoc, methodSignature = SeqDiagBuilder._getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName)

        self.assertEqual(len(filteredInstanceList), 3)
        self.assertEqual(returnDoc, 'Coord')
        self.assertEqual(methodSignature, "(location='')")


    def test_getFilteredInstanceListAndMethodSignatureAndReturnDocWhereMulitpleClassesSupportSameMethodAndOneIsSelected(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'ChildThree', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'getCoordinate'
        instanceList = SeqDiagBuilder._getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        filteredInstanceList, returnDoc, methodSignature = SeqDiagBuilder._getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName)

        self.assertEqual(len(filteredInstanceList), 1)
        self.assertEqual(returnDoc, 'CoordSel')
        self.assertEqual(methodSignature, "(location='')")


    def testRecordFlowWhereMulitpleClassesSupportSameMethodAndOneIsSelected(self):
        entryPoint = ChildThree()

        SeqDiagBuilder.activate('ChildThree', 'getCoordinate')  # activate sequence diagram building
        entryPoint.getCoordinate()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> ChildThree: getCoordinate(location='')
	activate ChildThree
	USER <-- ChildThree: return CoordSel
	deactivate ChildThree
@enduml''', commands)

        SeqDiagBuilder.deactivate()


    def testRecordFlowWhereMulitpleClassesSupportSameMethodAndOneIsSelectedInOtherClass(self):
        entryPoint = ChildTwo()

        SeqDiagBuilder.activate('ChildTwo', 'getCoordinate')  # activate sequence diagram building
        entryPoint.getCoordinate()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> ChildThree: getCoordinate(location='')
	activate ChildTwo
	USER <-- ChildTwo: return Coord
	deactivate ChildThree
@enduml''', commands)

        SeqDiagBuilder.deactivate()


    def testRecordFlowWhereMulitpleClassesSupportSameMethodAndNoneIsSelected(self):
        entryPoint = ChildTwo()

        SeqDiagBuilder.activate('ChildTwo', 'getCoordinateNoneSelected')  # activate sequence diagram building
        entryPoint.getCoordinateNoneSelected()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> ChildThree: getCoordinateNoneSelected(location='')
    activate ChildTwo
    USER <-- ChildTwo: return Coord
    deactivate ChildThree
@enduml''', commands)

        SeqDiagBuilder.deactivate()


    def testCreateSeqDiaqCommandsOnFullRequestHistoDayPrice(self):
        from datetimeutil import DateTimeUtil
        from utilityfortest import UtilityForTest
        from configurationmanager import ConfigurationManager
        from guioutputformater import GuiOutputFormater
        from controller import Controller

        SeqDiagBuilder.activate('Controller', 'getPrintableResultForInput')  # activate sequence diagram building

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        self.controller = Controller(GuiOutputFormater(configMgr), configMgr)

        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(eightDaysBeforeArrowDate)

        requestYearStr = eightDaysBeforeYearStr
        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        inputStr = 'mcap btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = eightDaysBeforeHourStr
            minuteStr = eightDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr, priceType),
                                                        UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual('mcap btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr, minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        commands = SeqDiagBuilder.createSeqDiaqCommands('GUI')

        with open("c:\\temp\\ess.txt","w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor GUI
GUI -> Controller: getPrintableResultForInput(inputStr)
	activate Controller
	Controller -> Requester: getCommand(inputStr)
		activate Requester
		Requester -> Requester: _parseAndFillCommandPrice(inputStr)
			activate Requester
			Requester -> Requester: _buildFullCommandPriceOptionalParmsDic(optionalParmList)
				activate Requester
				Requester <-- Requester: return optionalParsedParmDataDic
				deactivate Requester
			Requester <-- Requester: return CommandPrice or CommandError
			deactivate Requester
		Controller <-- Requester: return AbstractCommand
		deactivate Requester
	Controller -> CommandPrice: execute()
		activate CommandPrice
		CommandPrice -> Processor: getCryptoPrice(crypto, fiat, exchange, day, month, year, hour, minute, priceValueSymbol=None, priceValueAmount=None, priceValueSaveFlag=None, requestInputString='')
			activate Processor
			Processor -> PriceRequester: getHistoricalPriceAtUTCTimeStamp(crypto, fiat, timeStampLocalForHistoMinute, timeStampUTCNoHHMMForHistoDay, exchange)
				activate PriceRequester
				PriceRequester -> PriceRequester: _getHistoDayPriceAtUTCTimeStamp(crypto, fiat, timeStampUTC, exchange, resultData)
					activate PriceRequester
					PriceRequester <-- PriceRequester: return ResultData
					deactivate PriceRequester
				Processor <-- PriceRequester: return ResultData
				deactivate PriceRequester
			CommandPrice <-- Processor: return ResultData
			deactivate Processor
		Controller <-- CommandPrice: return ResultData or False
		deactivate CommandPrice
	Controller -> GuiOutputFormater: getFullCommandString(resultData)
		activate GuiOutputFormater
		GuiOutputFormater -> GuiOutputFormater: _buildFullDateAndTimeStrings(commandDic, timezoneStr)
			activate GuiOutputFormater
			GuiOutputFormater <-- GuiOutputFormater: return requestDateDMY, requestDateHM
			deactivate GuiOutputFormater
		Controller <-- GuiOutputFormater: return printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions
		deactivate GuiOutputFormater
	GUI <-- Controller: return printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions
	deactivate Controller
@enduml''', commands)

        SeqDiagBuilder.deactivate()


    def testCreateSeqDiaqCommandsOnFullRequestHistoDayPriceWithSignatureLimitation(self):
        from datetimeutil import DateTimeUtil
        from utilityfortest import UtilityForTest
        from configurationmanager import ConfigurationManager
        from guioutputformater import GuiOutputFormater
        from controller import Controller

        SeqDiagBuilder.activate('Controller', 'getPrintableResultForInput')  # activate sequence diagram building

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        self.controller = Controller(GuiOutputFormater(configMgr), configMgr)

        timezoneStr = 'Europe/Zurich'
        now = DateTimeUtil.localNow(timezoneStr)
        eightDaysBeforeArrowDate = now.shift(days=-8)

        eightDaysBeforeYearStr, eightDaysBeforeMonthStr, eightDaysBeforeDayStr, eightDaysBeforeHourStr, eightDaysBeforeMinuteStr = UtilityForTest.getFormattedDateTimeComponentsForArrowDateTimeObj(
            eightDaysBeforeArrowDate)

        requestYearStr = eightDaysBeforeYearStr
        requestDayStr = eightDaysBeforeDayStr
        requestMonthStr = eightDaysBeforeMonthStr
        inputStr = 'mcap btc {}/{} all'.format(requestDayStr, requestMonthStr)
        printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions = self.controller.getPrintableResultForInput(
            inputStr)

        if DateTimeUtil.isDateOlderThan(eightDaysBeforeArrowDate, 7):
            hourStr = '00'
            minuteStr = '00'
            priceType = 'C'
        else:
            hourStr = eightDaysBeforeHourStr
            minuteStr = eightDaysBeforeMinuteStr
            priceType = 'M'

        self.assertEqual(
            'MCAP/BTC on CCCAGG: ' + '{}/{}/{} {}:{}{}'.format(requestDayStr, requestMonthStr, requestYearStr,
                                                               hourStr, minuteStr, priceType),
            UtilityForTest.removePriceFromResult(printResult))
        self.assertEqual(
            'mcap btc {}/{}/{} {}:{} all'.format(requestDayStr, requestMonthStr, requestYearStr, hourStr,
                                                 minuteStr), fullCommandStr)
        self.assertEqual(None, fullCommandStrWithSaveModeOptions)
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        commands = SeqDiagBuilder.createSeqDiaqCommands('GUI', None, 20)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor GUI
GUI -> Controller: getPrintableResultForInput(inputStr)
	activate Controller
	Controller -> Requester: getCommand(inputStr)
		activate Requester
		Requester -> Requester: _parseAndFillCommandPrice(inputStr)
			activate Requester
			Requester -> Requester: _buildFullCommandPriceOptionalParmsDic(optionalParmList)
				activate Requester
				Requester <-- Requester: return ...
				deactivate Requester
			Requester <-- Requester: return ...
			deactivate Requester
		Controller <-- Requester: return AbstractCommand
		deactivate Requester
	Controller -> CommandPrice: execute()
		activate CommandPrice
		CommandPrice -> Processor: getCryptoPrice(crypto, fiat, ...)
			activate Processor
			Processor -> PriceRequester: getHistoricalPriceAtUTCTimeStamp(crypto, fiat, ...)
				activate PriceRequester
				PriceRequester -> PriceRequester: _getHistoDayPriceAtUTCTimeStamp(crypto, fiat, ...)
					activate PriceRequester
					PriceRequester <-- PriceRequester: return ResultData
					deactivate PriceRequester
				Processor <-- PriceRequester: return ResultData
				deactivate PriceRequester
			CommandPrice <-- Processor: return ResultData
			deactivate Processor
		Controller <-- CommandPrice: return ResultData or False
		deactivate CommandPrice
	Controller -> GuiOutputFormater: getFullCommandString(resultData)
		activate GuiOutputFormater
		GuiOutputFormater -> GuiOutputFormater: _buildFullDateAndTimeStrings(commandDic, ...)
			activate GuiOutputFormater
			GuiOutputFormater <-- GuiOutputFormater: return requestDateDMY, ...
			deactivate GuiOutputFormater
		Controller <-- GuiOutputFormater: return printResult, ...
		deactivate GuiOutputFormater
	GUI <-- Controller: return printResult, ...
	deactivate Controller
@enduml''', commands)

        SeqDiagBuilder.deactivate()


    def testCreateSeqDiaqCommandsOnClassesWithEmbededSelfCalls(self):
        entryPoint = ClassA()

        SeqDiagBuilder.activate('ClassA', 'doWork')  # activate sequence diagram building
        entryPoint.doWork()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        with open("c:\\temp\\ess.txt","w") as f:
            f.write(commands)

        self.assertEqual(
'''@startuml

actor USER
USER -> ClassA: doWork()
	activate ClassA
	ClassA -> ClassA: internalCall()
		activate ClassA
		ClassA -> ClassA: internalInnerCall()
			activate ClassA
			ClassA -> ClassB: createInnerRequest(parm1)
				activate ClassB
				ClassA <-- ClassB: return Bool
				deactivate ClassB
			ClassA <-- ClassA: return ResultPrice
			deactivate ClassA
		ClassA -> ClassB: createRequest(parm1, parm2)
			activate ClassB
			ClassA <-- ClassB: return Bool
			deactivate ClassB
		ClassA <-- ClassA: return ResultPrice
		deactivate ClassA
	USER <-- ClassA: return ClassAdoWorkRes
	deactivate ClassA
@enduml''', commands)

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building


    def testCreateSeqDiaqCommandsWithoutActivatingSeqDiagBuilder(self):
        entryPoint = ClassA()

        SeqDiagBuilder.deactivate()  # deactivate sequence diagram building
        entryPoint.doWork()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 1)
        self.assertEqual('No control flow recorded. Method activate() called: False. Method recordFlow() called: True. Specified entry point: None.None.', SeqDiagBuilder.getWarningList()[0])


    def test_getInstancesForClassSupportingMethodInClassHierarchyInMultipleClasses(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'getCoordinate'
        instanceList = SeqDiagBuilder._getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        self.assertEqual(len(instanceList), 3)
        self.assertEqual('Parent', instanceList[0].__class__.__name__)
        self.assertEqual('ChildOne', instanceList[1].__class__.__name__)
        self.assertEqual('ChildTwo', instanceList[2].__class__.__name__)


    def test_getInstancesForClassSupportingMethodInClassHierarchyInOneClass(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'm'
        instanceList = SeqDiagBuilder._getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        self.assertEqual(len(instanceList), 1)
        self.assertEqual('ChildOne', instanceList[0].__class__.__name__)


    def test_getInstancesForClassSupportingMethodInOneClass(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo',
                               'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'analyse'
        instanceList = SeqDiagBuilder._getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        self.assertEqual(len(instanceList), 1)
        self.assertEqual('IsolatedClass', instanceList[0].__class__.__name__)


    def testFlowEntryEq(self):
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe2 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'f', '(a, b)', 'RetClass')
        fe5 = FlowEntry('A', 'e', 'g', '(a, b)', 'RetClass')
        fe6 = FlowEntry('A', 'e', 'f', '(a, w)', 'RetClass')
        fe7 = FlowEntry('A', 'e', 'f', '(a, b)', '')

        self.assertTrue(fe1 == fe2)
        self.assertTrue(fe1 == fe3)
        self.assertFalse(fe1 == fe4)
        self.assertFalse(fe1 == fe5)
        self.assertFalse(fe1 == fe6)
        self.assertFalse(fe1 == fe7)


    def testFlowEntryToString(self):
        fe1 = FlowEntry('A', 'e', 'B', 'f', '95', '(a, b)', 'f_RetType')
        self.assertEqual('A.e, B.f, 95, (a, b), f_RetType', str(fe1))


    def testFlowEntryCreateReturnTypeVaryingMaxArgNum(self):
        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', 'a, b, c, d')
        self.assertEqual(fe.createReturnType(None, None), 'a, b, c, d')
        self.assertEqual(fe.createReturnType(4, None), 'a, b, c, d')
        self.assertEqual(fe.createReturnType(5, None), 'a, b, c, d')
        self.assertEqual(fe.createReturnType(3, None), 'a, b, c, ...')
        self.assertEqual(fe.createReturnType(1, None), 'a, ...')
        self.assertEqual(fe.createReturnType(0, None), '...')

        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', '')
        self.assertEqual(fe.createReturnType(None, None), '')
        self.assertEqual(fe.createReturnType(0, None), '')
        self.assertEqual(fe.createReturnType(1, None), '')
        self.assertEqual(fe.createReturnType(2, None), '')

        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', 'a')
        self.assertEqual(fe.createReturnType(None, None), 'a')
        self.assertEqual(fe.createReturnType(0, None), '...')
        self.assertEqual(fe.createReturnType(1, None), 'a')
        self.assertEqual(fe.createReturnType(2, None), 'a')


    def testFlowEntryCreateSignatureVaryingMaxSigArgNum(self):
        fe = FlowEntry('A', 'e', 'B', 'f', '95', '(a, b, c, d)', 'f_RetType')
        self.assertEqual(fe.createSignature(None, None), '(a, b, c, d)')
        self.assertEqual(fe.createSignature(4, None), '(a, b, c, d)')
        self.assertEqual(fe.createSignature(5, None), '(a, b, c, d)')
        self.assertEqual(fe.createSignature(3, None), '(a, b, c, ...)')
        self.assertEqual(fe.createSignature(1, None), '(a, ...)')
        self.assertEqual(fe.createSignature(0, None), '(...)')

        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', 'f_RetType')
        self.assertEqual(fe.createSignature(None, None), '()')
        self.assertEqual(fe.createSignature(0, None), '()')
        self.assertEqual(fe.createSignature(1, None), '()')
        self.assertEqual(fe.createSignature(2, None), '()')

        fe = FlowEntry('A', 'e', 'B', 'f', '95', '(a)', 'f_RetType')
        self.assertEqual(fe.createSignature(None, None), '(a)')
        self.assertEqual(fe.createSignature(0, None), '(...)')
        self.assertEqual(fe.createSignature(1, None), '(a)')
        self.assertEqual(fe.createSignature(2, None), '(a)')


    def testFlowEntryCreateReturnTypeVaryingMaxReturnTypeCharLen(self):
        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', 'aaa, bbb, ccc, ddd')
        self.assertEqual(fe.createReturnType(None, None), 'aaa, bbb, ccc, ddd')
        self.assertEqual(fe.createReturnType(None, 100), 'aaa, bbb, ccc, ddd')
        self.assertEqual(fe.createReturnType(None, 0), '...')
        self.assertEqual(fe.createReturnType(None, 8), 'aaa, ...')
        self.assertEqual(fe.createReturnType(None, 7), '...')
        self.assertEqual(fe.createReturnType(None, 13), 'aaa, bbb, ...')
        self.assertEqual(fe.createReturnType(None, 12), 'aaa, ...')

        fe = FlowEntry('A', 'e', 'B', 'f', '95', '', '')
        self.assertEqual(fe.createReturnType(None, None), '')
        self.assertEqual(fe.createReturnType(None, 100), '')
        self.assertEqual(fe.createReturnType(None, 0), '')


    def testFlowEntryCreateSignatureVaryingMaxSigCharLen(self):
        fe = FlowEntry('A', 'e', 'B', 'f', '95', '(aaa, bbb, ccc, ddd)', 'f_RetType')
        self.assertEqual(fe.createSignature(None, None), '(aaa, bbb, ccc, ddd)')
        self.assertEqual(fe.createSignature(None, 100), '(aaa, bbb, ccc, ddd)')
        self.assertEqual(fe.createSignature(None, 0), '(...)')
        self.assertEqual(fe.createSignature(None, 10), '(aaa, ...)')
        self.assertEqual(fe.createSignature(None, 9), '(...)')
        self.assertEqual(fe.createSignature(None, 15), '(aaa, bbb, ...)')
        self.assertEqual(fe.createSignature(None, 14), '(aaa, ...)')

        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', 'f_RetType')
        self.assertEqual(fe.createSignature(None, None), '()')
        self.assertEqual(fe.createSignature(None, 100), '()')
        self.assertEqual(fe.createSignature(None, 0), '()')


    def testFlowEntryReturnTypeVaryingMaxArgNumAndMaxReturnTypeCharLen(self):
        fe = FlowEntry('A', 'e', 'B', 'f', '95', '()', 'aaaa, bbbb, cccc')
        self.assertEqual(fe.createReturnType(2, 14), 'aaaa, ...')
        self.assertEqual(fe.createReturnType(2, 15), 'aaaa, bbbb, ...')
        self.assertEqual(fe.createReturnType(2, 16), 'aaaa, bbbb, ...')
        self.assertEqual(fe.createReturnType(3, 15), 'aaaa, bbbb, ...')
        self.assertEqual(fe.createReturnType(3, 16), 'aaaa, bbbb, cccc')
        self.assertEqual(fe.createReturnType(3, 17), 'aaaa, bbbb, cccc')
        self.assertEqual(fe.createReturnType(4, 15), 'aaaa, bbbb, ...')
        self.assertEqual(fe.createReturnType(4, 16), 'aaaa, bbbb, cccc')
        self.assertEqual(fe.createReturnType(4, 17), 'aaaa, bbbb, cccc')


    def testFlowEntryCreateSignatureVaryingMaxSigArgNumAndMaxSigCharLen(self):
        fe = FlowEntry('A', 'e', 'B', 'f', '95', '(aaaa, bbbb, cccc)', 'f_RetType')
        self.assertEqual(fe.createSignature(2, 16), '(aaaa, ...)')
        self.assertEqual(fe.createSignature(2, 17), '(aaaa, bbbb, ...)')
        self.assertEqual(fe.createSignature(2, 18), '(aaaa, bbbb, ...)')
        self.assertEqual(fe.createSignature(3, 17), '(aaaa, bbbb, ...)')
        self.assertEqual(fe.createSignature(3, 18), '(aaaa, bbbb, cccc)')
        self.assertEqual(fe.createSignature(3, 19), '(aaaa, bbbb, cccc)')
        self.assertEqual(fe.createSignature(4, 17), '(aaaa, bbbb, ...)')
        self.assertEqual(fe.createSignature(4, 18), '(aaaa, bbbb, cccc)')
        self.assertEqual(fe.createSignature(4, 19), '(aaaa, bbbb, cccc)')


    @unittest.skip
    def testAddIfNotInNoCallBeforeEntryPoint(self):
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'f', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'f')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('A.e, B.f, (a, b), RetClass\nA.e, C.f, (a, b), RetClass\nC.f, B.f, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInOneCallBeforeEntryPoint(self):
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'f', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('C', 'f')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('A.e, C.f, (a, b), RetClass\nC.f, B.f, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInNCallsBeforeEntryPoint(self):
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'j', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'j')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('C.f, B.j, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInNCallsBeforeEntryPointEntryPointAddedTwice(self):
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'j', '(a, b)', 'RetClass')
        fe5 = FlowEntry('C', 'f', 'j', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'j')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        rfp.addIfNotIn(fe5)
        self.assertEqual('C.f, B.j, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInNCallsBeforeEntryPointEntryPointAddedTwiceWithSubsequentEntries(self):
        fe4 = FlowEntry('C', 'f', 'j', '(a, b)', 'RetClass')
        fe5 = FlowEntry('C', 'f', 'j', '(a, b)', 'RetClass')
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'j')
        rfp.addIfNotIn(fe1) # before entry point: will not be added
        rfp.addIfNotIn(fe3) # before entry point: will not be added
        rfp.addIfNotIn(fe4)
        rfp.addIfNotIn(fe5)
        rfp.addIfNotIn(fe1) # after entry point: will  be added
        rfp.addIfNotIn(fe3) # after entry point: will  be added
        self.assertEqual('C.f, B.j, (a, b), RetClass\nA.e, B.f, (a, b), RetClass\nA.e, C.f, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInEntryPointNeverReached(self):
        fe1 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'j', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('A', 'a')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('',str(rfp))


    @unittest.skip
    def testWithBackSlash(self):
        from datetimeutil import DateTimeUtil
        from configurationmanager import ConfigurationManager
        from guioutputformater import GuiOutputFormater
        from controller import Controller
        import os

        SeqDiagBuilder.activate('Controller', 'getPrintableResultForInput')  # activate sequence diagram building

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        controller = Controller(GuiOutputFormater(configMgr), configMgr)

        inputStr = 'mcap btc 0 all'
        _, _, _, _ = controller.getPrintableResultForInput(
            inputStr)

        SeqDiagBuilder.createDiagram('c:\\temp\\', 'GUI', None, 20)


    @unittest.skip
    def testWithSlash(self):
        from datetimeutil import DateTimeUtil
        from configurationmanager import ConfigurationManager
        from guioutputformater import GuiOutputFormater
        from controller import Controller
        import os

        SeqDiagBuilder.activate('Controller', 'getPrintableResultForInput')  # activate sequence diagram building

        if os.name == 'posix':
            FILE_PATH = '/sdcard/cryptopricer.ini'
        else:
            FILE_PATH = 'c:\\temp\\cryptopricer.ini'

        configMgr = ConfigurationManager(FILE_PATH)
        controller = Controller(GuiOutputFormater(configMgr), configMgr)

        inputStr = 'mcap btc 0 all'
        _, _, _, _ = controller.getPrintableResultForInput(
            inputStr)

        SeqDiagBuilder.createDiagram('c:/temp', 'GUI', None, 20)


if __name__ == '__main__':
    unittest.main()
