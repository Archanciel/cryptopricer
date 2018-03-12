import unittest
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0,currentdir) # this instruction is necessary for successful importation of utilityfortest module when
                              # the test is executed standalone

from seqdiagbuilder import SeqDiagBuilder
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
        pr = self.internalInnerCall()
        b = ClassB()
        res = b.createRequest(1, 2)


    def internalInnerCall(self):
        '''
        @seqdiaf_return ResultPrice
        :return:
        '''
        b = ClassB()
        res = b.createInnerRequest(1)


class ClassB:
    def createInnerRequest(self, parm1):
        '''
        @seqdiaf_return Bool
        :param parm1:
        :return:
        '''
        SeqDiagBuilder.recordFlow()


    def createRequest(self, parm1, parm2):
        '''
        @seqdiaf_return Bool
        :param parm1:
        :return:
        '''
        SeqDiagBuilder.recordFlow()


class TestSeqDiagBuilder(unittest.TestCase):
    def setUp(self):
        SeqDiagBuilder.reset()


    def testInstanciateClassInitTwoArgs(self):
        className = 'Controller'
        moduleName = 'controller'

        instance = SeqDiagBuilder.instanciateClass(className, moduleName)

        self.assertIsInstance(instance, Controller)


    def testInstanciateClassInitNoArgs(self):
        className = 'PriceRequester'
        moduleName = 'pricerequester'

        instance = SeqDiagBuilder.instanciateClass(className, moduleName)

        self.assertIsInstance(instance, PriceRequester)


    def testGetMethodSignatureAndReturnDoc(self):
        className = 'Controller'
        moduleName = 'controller'
        methodName = 'getPrintableResultForInput'

        instanceList = [SeqDiagBuilder.instanciateClass(className, moduleName)]
        filteredInstanceList, returnDoc, methodSignature = SeqDiagBuilder.getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName)

        self.assertEqual(len(filteredInstanceList), 1)
        self.assertEqual(returnDoc, 'printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions')
        self.assertEqual(methodSignature, '(inputStr)')

    @unittest.skip
    def testBuildSeqDiagOnFullRequestHistoDayPrice(self):
        from datetimeutil import DateTimeUtil
        from utilityfortest import UtilityForTest
        from configurationmanager import ConfigurationManager
        from guioutputformater import GuiOutputFormater
        from controller import Controller

        SeqDiagBuilder.isBuildMode = True #activate sequence diagram building

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
        SeqDiagBuilder.printSeqDiagInstructions()
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building

    def testGetSeqDiagInstructionsStrOnClassesWithEmbededSelfCalls(self):
        entryPoint = ClassA()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        entryPoint.doWork()

        commands = SeqDiagBuilder.createSeqDiaqCommands('USER')
        print(commands)

        with open("c:\\temp\\ess.txt","w") as f:
            f.write(commands)

        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building

    @unittest.skip
    def testCreateSeqDiaqCommandsOnSimpleClasses(self):
        foo = Foo()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        foo.f(1)
        # SeqDiagBuilder.printSeqDiagInstructions()
        # print('')
        # print(SeqDiagBuilder.getSeqDiagInstructionsStr())
        self.assertEqual('''testseqdiagbuilder Foo.f(fParm) <-- fReturn
testseqdiagbuilder Bar.g() <-- gReturn
testseqdiagbuilder LeafOne.i() <-- 
testseqdiagbuilder Foo.f(fParm) <-- fReturn
testseqdiagbuilder Egg.h(hParm1, hParm2) <-- 
testseqdiagbuilder LeafTwo.j() <-- 
''', SeqDiagBuilder.createSeqDiaqCommands('GUI'))
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building

    @unittest.skip
    def testGetSeqDiagInstructionsStrOnSimpleClassesWithMorethanOneClassSupportingMethodOneUsingMethodSelectTag(self):
        cl = Client()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        cl.make()
        SeqDiagBuilder.printSeqDiagInstructions()
        self.assertEqual('''testseqdiagbuilder Client.make() <-- 
testseqdiagbuilder ChildOne.compute(size=0) <-- Analysis
testseqdiagbuilder IsolatedClass.analyse() <-- Analysis
''', SeqDiagBuilder.getSeqDiagInstructionsStr())
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building


    @unittest.skip
    def testGetSeqDiagInstructionsStrOnSimpleClassesWithMorethanOneClassSupportingMethodBothUsingMethodSelectTag(self):
        cl = Client()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        cl.perform()
        SeqDiagBuilder.printSeqDiagInstructions()
        # here, Parent and ChildOne support computeTwo with both methods having
        # the :seqdiag_select_method tag. The first encountred class/method with
        # the tag is selected !
        self.assertEqual('''testseqdiagbuilder Client.perform() <-- 
testseqdiagbuilder Parent.computeTwo(size=0) <-- Analysis
testseqdiagbuilder IsolatedClass.analyse() <-- Analysis
''', SeqDiagBuilder.getSeqDiagInstructionsStr())
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building


    @unittest.skip
    def testGetSeqDiagInstructionsStrOnSimpleClassesWithOnlyParentClassSupportingMethod(self):
        cl = Client()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        cl.doCall()
        SeqDiagBuilder.printSeqDiagInstructions()
        # here, Parent only support computeThree without any :seqdiag_select_method tag.
        # The Parent method is selected
        self.assertEqual('''testseqdiagbuilder Client.doCall() <-- 
testseqdiagbuilder Parent.computeThree(size=0) <-- Analysis
testseqdiagbuilder IsolatedClass.analyse() <-- Analysis
''', SeqDiagBuilder.getSeqDiagInstructionsStr())
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building

    @unittest.skip
    def testGetSeqDiagInstructionsStrOnThreeLevelClasseHierarchyWithOnlyAllLevelsSupportingMethod(self):
        cl = Client()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        cl.doProcess()
        SeqDiagBuilder.printSeqDiagInstructions()
        # here, all three level, Parenr, ChildTwo and ChildOfChildTwo support
        # computeFour, but only ChildTwo.computeFour is tagged with
        # :seqdiag_select_method tag. So, the ChildTwo method is selected
        self.assertEqual('''testseqdiagbuilder Client.doProcess() <-- 
testseqdiagbuilder ChildTwo.computeFour(size=0) <-- Analysis
testseqdiagbuilder IsolatedClass.analyse() <-- Analysis
''', SeqDiagBuilder.getSeqDiagInstructionsStr())
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 0)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building

    @unittest.skip
    def testGetSeqDiagInstructionsStrOnSimpleClassesWithMorethanOneClassSupportingMethod(self):
        cl = Client()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        cl.do()
        SeqDiagBuilder.printSeqDiagInstructions()
        self.assertEqual('''testseqdiagbuilder Client.do() <-- 
testseqdiagbuilder Parent.getCoordinate(location='') <-- Coord
testseqdiagbuilder IsolatedClass.analyse() <-- Analysis
''', SeqDiagBuilder.getSeqDiagInstructionsStr())
        self.assertEqual(len(SeqDiagBuilder.getWarningList()), 1)
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building


    def testGetClassNameListMethodInClassHierarchyInMultipleClasses(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'getCoordinate'
        instanceList = SeqDiagBuilder.getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        self.assertEqual(len(instanceList), 3)
        self.assertEqual('Parent', instanceList[0].__class__.__name__)
        self.assertEqual('ChildOne', instanceList[1].__class__.__name__)
        self.assertEqual('ChildTwo', instanceList[2].__class__.__name__)


    def testGetClassNameListMethodInClassHierarchyInOneClass(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'm'
        instanceList = SeqDiagBuilder.getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        self.assertEqual(len(instanceList), 1)
        self.assertEqual('ChildOne', instanceList[0].__class__.__name__)


    def testGetClassNameListMethodInOneClass(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo',
                               'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'analyse'
        instanceList = SeqDiagBuilder.getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList)
        self.assertEqual(len(instanceList), 1)
        self.assertEqual('IsolatedClass', instanceList[0].__class__.__name__)


if __name__ == '__main__':
    unittest.main()
