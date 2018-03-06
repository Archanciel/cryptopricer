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
        SeqDiagBuilder.buildSeqDiag(3, 'USER')


class LeafTwo:
    def j(self):
        SeqDiagBuilder.buildSeqDiag(3, 'USER')


class Client:
    def do(self):
        c1 = ChildOne()
        c1.getCoordinate()


class Parent:
    def getCoordinate(self, location=''):
        '''

        :param location:
        :seqdiag_return Coord
        :return:
        '''
        pass


class ChildOne(Parent):
    def getCoordinate(self, location=''):
        iso = IsolatedClass()
        iso.analyse()

    def m(self):
        pass


class ChildTwo(Parent):
    def l(self):
        pass


class IsolatedClass:
    def analyse(self):
        '''

        :seqdiag_return Analysis
        :return:
        '''
        SeqDiagBuilder.buildSeqDiag(3, "START")


class TestSeqDiagBuilder(unittest.TestCase):
    def setUp(self):
        SeqDiagBuilder.buildSeqDiag(3, 'USER')


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

        returnDoc, methodSignature = SeqDiagBuilder.getMethodSignatureAndReturnDoc(className, moduleName, methodName)

        self.assertEqual(returnDoc, 'printResult, fullCommandStr, fullCommandStrWithOptions, fullCommandStrWithSaveModeOptions')
        self.assertEqual(methodSignature, '(inputStr)')


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
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building


    def testBuildSeqDiagOnSimpleClasses(self):
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
''', SeqDiagBuilder.getSeqDiagInstructionsStr())
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building


    def testBuildSeqDiagOnSimpleClassesWithMorethanOneClasssupportingMethod(self):
        cl = Client()

        SeqDiagBuilder.isBuildMode = True  # activate sequence diagram building
        cl.do()
        SeqDiagBuilder.printSeqDiagInstructions()
        SeqDiagBuilder.isBuildMode = False  # deactivate sequence diagram building


    def testGetClassNameListMethodInClassHierarchyInMultipleClasses(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'getCoordinate'
        classNameList = SeqDiagBuilder.getClassNameList(moduleName, moduleClassNameList, methodName)
        self.assertEqual(len(classNameList), 3)
        self.assertIn('Parent', classNameList)
        self.assertIn('ChildOne', classNameList)
        self.assertIn('ChildTwo', classNameList)


    def testGetClassNameListMethodInClassHierarchyInOneClass(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo', 'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'm'
        classNameList = SeqDiagBuilder.getClassNameList(moduleName, moduleClassNameList, methodName)
        self.assertEqual(len(classNameList), 1)
        self.assertIn('ChildOne', classNameList)


    def testGetClassNameListMethodInOneClass(self):
        moduleName = 'testseqdiagbuilder'
        moduleClassNameList = ['Foo', 'Bar', 'Egg', 'LeafOne', 'LeafTwo', 'Parent', 'ChildOne', 'ChildTwo',
                               'TestSeqDiagBuilder', 'IsolatedClass']
        methodName = 'analyse'
        classNameList = SeqDiagBuilder.getClassNameList(moduleName, moduleClassNameList, methodName)
        self.assertEqual(len(classNameList), 1)
        self.assertIn('IsolatedClass', classNameList)


if __name__ == '__main__':
    unittest.main()
