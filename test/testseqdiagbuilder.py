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
        pass


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


class C:
    def c1(self, c1_p1):
        '''

        :param c1_p1:
        :seqdiag_return Cc1Return
        :return:
        '''
        SeqDiagBuilder.recordFlow()

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

        :param b1_p1:
        :seqdiag_return Bb2Return
        :return:
        '''
        c = C()
        c.c1(1)

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
        :param a2_p1:
        :seqdiag_return Aa4Return
        :return:
        '''
        b = B()
        b.b1(1)
        b.b1(1)


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

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        self.assertEqual(
'''@startuml

actor USER
USER -> A: a1(a1_p1, a1_p2)
	activate A
	USER <-- A: return Aa1Return
	deactivate A
@enduml''', commands)

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

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

    def testCreateSeqDiaqCommandsOnThreeLevelCall(self):
        entryPoint = A()

        SeqDiagBuilder.activate('A', 'a3')  # activate sequence diagram building
        entryPoint.a3(1)

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

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

        with open("c:\\temp\\ess.txt", "w") as f:
            f.write(commands)

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
		Controller <-- Requester: return CommandPrice or CommandError
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
	GUI <-- Controller: return printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions
	deactivate Controller
@enduml''', commands)

        SeqDiagBuilder.deactivate()


    def testCreateSeqDiaqCommandsOnClassesWithEmbededSelfCalls(self):
        entryPoint = ClassA()

        SeqDiagBuilder.activate('ClassA', 'doWork')  # activate sequence diagram building
        entryPoint.doWork()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')

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
	USER <-- ClassA: 
	deactivate ClassA
@enduml''', commands)

        with open("c:\\temp\\ess.txt","w") as f:
            f.write(commands)

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
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe2 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'B', 'f', '(a, b)', 'RetClass')
        fe5 = FlowEntry('A', 'e', 'B', 'g', '(a, b)', 'RetClass')
        fe6 = FlowEntry('A', 'e', 'B', 'f', '(a, w)', 'RetClass')
        fe7 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', '')

        self.assertTrue(fe1 == fe2)
        self.assertFalse(fe1 == fe3)
        self.assertFalse(fe1 == fe4)
        self.assertFalse(fe1 == fe5)
        self.assertFalse(fe1 == fe6)
        self.assertFalse(fe1 == fe7)


    def testFlowEntryToString(self):
        fe1 = FlowEntry('A', 'e', 'e_RetType', 'B', 'f', '95', '(a, b)', 'f_RetType')
        self.assertEqual('A.e, e_RetType, B.f, 95, (a, b), f_RetType', str(fe1))


    @unittest.skip
    def testAddIfNotInNoCallBeforeEntryPoint(self):
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'B', 'f', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'f')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('A.e, B.f, (a, b), RetClass\nA.e, C.f, (a, b), RetClass\nC.f, B.f, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInOneCallBeforeEntryPoint(self):
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'B', 'f', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('C', 'f')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('A.e, C.f, (a, b), RetClass\nC.f, B.f, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInNCallsBeforeEntryPoint(self):
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'B', 'j', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'j')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('C.f, B.j, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInNCallsBeforeEntryPointEntryPointAddedTwice(self):
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'B', 'j', '(a, b)', 'RetClass')
        fe5 = FlowEntry('C', 'f', 'B', 'j', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('B', 'j')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        rfp.addIfNotIn(fe5)
        self.assertEqual('C.f, B.j, (a, b), RetClass\n',str(rfp))


    @unittest.skip
    def testAddIfNotInNCallsBeforeEntryPointEntryPointAddedTwiceWithSubsequentEntries(self):
        fe4 = FlowEntry('C', 'f', 'B', 'j', '(a, b)', 'RetClass')
        fe5 = FlowEntry('C', 'f', 'B', 'j', '(a, b)', 'RetClass')
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')

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
        fe1 = FlowEntry('A', 'e', 'B', 'f', '(a, b)', 'RetClass')
        fe3 = FlowEntry('A', 'e', 'C', 'f', '(a, b)', 'RetClass')
        fe4 = FlowEntry('C', 'f', 'B', 'j', '(a, b)', 'RetClass')

        rfp = RecordedFlowPath('A', 'a')
        rfp.addIfNotIn(fe1)
        rfp.addIfNotIn(fe3)
        rfp.addIfNotIn(fe4)
        self.assertEqual('',str(rfp))


if __name__ == '__main__':
    unittest.main()
