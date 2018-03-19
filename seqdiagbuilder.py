import traceback, re, ast, importlib, inspect
from inspect import signature

SEQDIAG_RETURN_TAG = ":seqdiag_return"
SEQDIAG_SELECT_METHOD_TAG = ":seqdiag_select_method"

SEQDIAG_RETURN_TAG_PATTERN = r"%s (.*)" % SEQDIAG_RETURN_TAG
SEQDIAG_SELECT_METHOD_TAG_PATTERN = r"%s(.*)" % SEQDIAG_SELECT_METHOD_TAG
PYTHON_FILE_AND_FUNC_PATTERN = r"([\w:\\]+\\)(\w+)\.py, line (\d*) in (.*)"
FRAME_PATTERN = r"(?:<FrameSummary file ([\w:\\,._\s]+)(?:>, |>\]))"


TAB_CHAR = '\t'


class FlowEntry:
    def __init__(self, fromClass='', fromMethod='', toClass='', toMethod='', toMethodCalledFromLineNumber='',
                 toSignature='', toReturnType=''):
        '''

        :param fromClass:                       class containing the fromMethod
        :param fromMethod:                      method calling the toMethod
        :param toClass:                         class containing the toMethod
        :param toMethod:                        method called from the fromMethod
        :param toMethodCalledFromLineNumber:    line number in the fromMethod from which
                                                the toMethod was called
        :param toSignature:                     toMethod signature
        :param toReturnType:                    return type of the toMethod
        '''
        self.fromClass = fromClass
        self.fromMethod = fromMethod
        self.toClass = toClass
        self.toMethod = toMethod
        self.toMethodCalledFromLineNumber = toMethodCalledFromLineNumber
        self.toSignature = toSignature
        self.toReturnType = toReturnType


    def __eq__(self, other):
        return self.fromClass == other.fromClass and \
               self.fromMethod == other.fromMethod and \
               self.toClass == other.toClass and \
               self.toMethod == other.toMethod and \
               self.toMethodCalledFromLineNumber == other.toMethodCalledFromLineNumber and \
               self.toSignature == other.toSignature and \
               self.toReturnType == other.toReturnType


    def isEntryPoint(self, targetClass, targetMethod):
        '''
        Returns True if the passed targetClass/targetMethod are equal to the toClass and
        toMethod of the flow entry, which means the flow entry corresponds to the seq diag
        entry point.

        :param targetClass:
        :param targetMethod:
        :return:
        '''
        return self.toClass == targetClass and \
               self.toMethod == targetMethod


    def equalFrom(self, entry):
        return self.fromClass == entry.fromClass and self.fromMethod == entry.fromMethod


    def differByLineNumberOnly(self, entry):
        '''
        Return True if entry and self denote the same class.method but called from a
        different location
        :param entry:
        :return:
        '''
        return self.equalFrom(entry) and self.toMethodCalledFromLineNumber != entry.toMethodCalledFromLineNumber


    def __str__(self):
        return "{}.{}, {}.{}, {}, {}, {}".format(self.fromClass, self.fromMethod, self.toClass, self.toMethod, self.toMethodCalledFromLineNumber, self.toSignature, self.toReturnType)


class RecordedFlowPath:
    def __init__(self, entryClass, entryMethod):
        self.entryClass = entryClass
        self.entryMethod = entryMethod
        self.entryPointReached = False
        self.list = []


    def addIfNotIn(self, newFlowEntry):
        '''
        This method adds an flow entry to the internal list if the internal list does already
        contains the entry point and procvided this flow entry is not alreay in the list.

        But the addition is only possible if the entry point was reached. For example, if
        we have TestClass.testCaseMethod() --> A.f() --> A.g() --> B.h() and the entry class
        and toMethod is A.f(), flow entries will be added only once A.f() was added to the list
        :param newFlowEntry:
        :return:
        '''
        if newFlowEntry.isEntryPoint(self.entryClass, self.entryMethod):
            self.entryPointReached = True

        if not self.entryPointReached:
            # flow entries preceeding entry point are ignored
            return

        if self.list == []:
            # first encountered occurrence of entry point is added
            self.list.append(newFlowEntry)
            return

        for flowEntry in self.list:
            if flowEntry == newFlowEntry:
                return

        self.list.append(newFlowEntry)


    def size(self):
        return len(self.list)


    def isEmpty(self):
        return self.size() == 0


    def __str__(self):
        outStr = ''

        for flowEntry in self.list:
            outStr += str(flowEntry) + '\n'

        return outStr


class SeqDiagCommandStack:
    '''
    This list stores the embeded calls used to build the sequence diagram commands. It is
    used to build the return commands of the diagram.
    '''


    def __init__(self):
        self.stack = []


    def pop(self):
        if self.isEmpty():
            return None
        else:
            return self.stack.pop()


    def push(self, flowEntry):
        '''
        Push on the list a 2 elements list, the first element being the couple <class name>.<toMethod name>
        and the second one being the string denoting the information returned to the caller by the toMethod.
        :param flowEntry:
        :return:
        '''
        self.stack.append(flowEntry)

        return self.stack


    def peek(self):
        if self.isEmpty():
            return None
        else:
            return self.stack[-1]


    def size(self):
        return len(self.stack)


    def isEmpty(self):
        return self.size() == 0


    def containsFromCall(self, flowEntry):
        '''
        Return True if the passed flow entry is in the SeqDiagCommandStack.
        :param flowEntry:
        :return:
        '''
        for entry in self.stack:
            if entry.equalFrom(flowEntry):
                return True

        return False


class SeqDiagBuilder:
    '''
    This class contains a static utility methods used to build a sequence diagram from the
    call list as at the point in the python code were it is called.

    To build the diagram, type seqdiag -Tsvg list.txt in a command line window.
    This build a svg file which can be displayed in a browsxer.
    '''

    seqDiagWarningList = []
    _isActive = False
    _recordFlowCalled = False
    seqDiagEntryClass = None
    seqDiagEntryMethod = None
    recordedFlowPath = None


    @staticmethod
    def activate(entryClass, entryMethod):
        SeqDiagBuilder.seqDiagEntryClass = entryClass
        SeqDiagBuilder.seqDiagEntryMethod = entryMethod
        SeqDiagBuilder.recordedFlowPath = RecordedFlowPath(SeqDiagBuilder.seqDiagEntryClass, SeqDiagBuilder.seqDiagEntryMethod)
        SeqDiagBuilder._isActive = True


    @staticmethod
    def deactivate():
        '''
        Reinitialise the class level seq diag variables and data structures and sets its
        build mode to False
        :return:
        '''
        SeqDiagBuilder.seqDiagEntryClass = None
        SeqDiagBuilder.seqDiagEntryMethod = None
        SeqDiagBuilder.recordedFlowPath = None
        SeqDiagBuilder.seqDiagWarningList = []
        SeqDiagBuilder._isActive = False
        SeqDiagBuilder._recordFlowCalled = False


    @staticmethod
    def _buildCommandFileHeaderSection():
        '''
        This toMethod create the first line of the PlantUML command file,
        adding a header section in case of warnings.
        :return:
        '''
        commandFileHeaderSectionStr = "@startuml\n"

        if len(SeqDiagBuilder.seqDiagWarningList) > 0:
            # building a header containing the warnings
            commandFileHeaderSectionStr += "left header\n<b><font color=red >Warnings</font></b>\n"

            for warning in SeqDiagBuilder.seqDiagWarningList:
                commandFileHeaderSectionStr += "<font color=red>{}</font>\n".format(warning)

            commandFileHeaderSectionStr += "endheader\n\n"

        return commandFileHeaderSectionStr


    @staticmethod
    def createSeqDiaqCommands(actorName):
        '''
        This method use the control flow data collected during execution to create
        the commands Plantuml will use to draw a sequence diagram.

        To build the diagram itself, type java -jar plantuml.jar -tsvg seqdiagcommands.txt
        in a command line window. This build a svg file which can be displayed in a browser.

        :param actorName:
        :return:
        '''
        isFlowRecorded = True

        if SeqDiagBuilder.recordedFlowPath == None or SeqDiagBuilder.recordedFlowPath.isEmpty():
            SeqDiagBuilder._issueWarning("No control flow recorded. Method activate() called: {}. Method recordFlow() called: {}. Specified entry point: {}.{}.".format(SeqDiagBuilder._isActive, SeqDiagBuilder._recordFlowCalled, SeqDiagBuilder.seqDiagEntryClass, SeqDiagBuilder.seqDiagEntryMethod))
            isFlowRecorded = False

        indentStr = ''
        seqDiagCommandStr = SeqDiagBuilder._buildCommandFileHeaderSection()

        if isFlowRecorded:
            classMethodReturnStack = SeqDiagCommandStack()
            seqDiagCommandStr += "\nactor {}\n".format(actorName)

            firstFlowEntry = SeqDiagBuilder.recordedFlowPath.list[0]
            firstFlowEntry.fromClass = actorName
            fromClass = firstFlowEntry.fromClass
            commandStr, indentStr = SeqDiagBuilder._handleSeqDiagForwardMesssageCommand(fromClass, firstFlowEntry,
                                                                                        indentStr,
                                                                                        classMethodReturnStack)
            seqDiagCommandStr += commandStr
            fromClass = firstFlowEntry.toClass

            for flowEntry in SeqDiagBuilder.recordedFlowPath.list[1:]:
                if not classMethodReturnStack.containsFromCall(flowEntry):
                    commandStr, indentStr = SeqDiagBuilder._handleSeqDiagForwardMesssageCommand(fromClass, flowEntry,
                                                                                                indentStr,
                                                                                                classMethodReturnStack)
                    seqDiagCommandStr += commandStr
                    fromClass = flowEntry.toClass
                    deepestReached = True
                else:
                    stopUnfolding = False
                    while not stopUnfolding and classMethodReturnStack.containsFromCall(flowEntry):
                        returnEntry = classMethodReturnStack.pop()
                        if deepestReached:
                            # handle deepest or leaf return message, the one which did not
                            # generate an entry in the classMethodReturnStack
                            indentStr += TAB_CHAR
                            commandStr = SeqDiagBuilder._handleSeqDiagReturnMesssageCommand(indentStr, returnEntry)
                            seqDiagCommandStr += commandStr

                            # handle return message for the method which called the
                            # deepest or leaf method and which generated an entry in the
                            # classMethodReturnStack
                            if flowEntry.differByLineNumberOnly(returnEntry):
                                stopUnfolding = True
                                fromClass = flowEntry.fromClass
                                continue
                            returnEntry = classMethodReturnStack.pop()
                            indentStr = indentStr[:-1]
                            commandStr = SeqDiagBuilder._handleSeqDiagReturnMesssageCommand(indentStr, returnEntry)
                            seqDiagCommandStr += commandStr

                            deepestReached = False
                        else:
                            returnEntry = classMethodReturnStack.pop()
                            indentStr = indentStr[:-1]
                            commandStr = SeqDiagBuilder._handleSeqDiagReturnMesssageCommand(indentStr, returnEntry)
                            seqDiagCommandStr += commandStr
                        fromClass = returnEntry.fromClass
                    indentStr = indentStr[:-2]
                    commandStr, indentStr = SeqDiagBuilder._handleSeqDiagForwardMesssageCommand(fromClass, flowEntry,
                                                                                                indentStr,
                                                                                                classMethodReturnStack)
                    seqDiagCommandStr += commandStr
                    # fromClass = flowEntry.toClass this assignation has no utility !
                    deepestReached = True
            indentStr += TAB_CHAR

            while not classMethodReturnStack.isEmpty():
                returnEntry = classMethodReturnStack.pop()
                commandStr = SeqDiagBuilder._handleSeqDiagReturnMesssageCommand(indentStr, returnEntry)
                seqDiagCommandStr += commandStr
                indentStr = indentStr[:-1]

        seqDiagCommandStr += "@enduml"

        return seqDiagCommandStr


    @staticmethod
    def _handleSeqDiagReturnMesssageCommand(indentStr, returnEntry):
        fromClass = returnEntry.toClass
        toClass = returnEntry.fromClass
        toReturnType = returnEntry.toReturnType
        commandStr = SeqDiagBuilder._addReturnSeqDiagCommand(fromClass, toClass, toReturnType, indentStr)

        return commandStr

    @staticmethod
    def _handleSeqDiagForwardMesssageCommand(fromClass, flowEntry, indentStr, classMethodReturnStack):
        classMethodReturnStack.push(flowEntry)
        toClass = flowEntry.toClass
        toMethod = flowEntry.toMethod
        toSignature = flowEntry.toSignature
        indentStr += TAB_CHAR
        commandStr = SeqDiagBuilder._addForwardSeqDiagCommand(fromClass, toClass, toMethod, toSignature, indentStr)

        return commandStr, indentStr

    @staticmethod
    def _addForwardSeqDiagCommand(fromClass, toClass, method, signature, indentStr):
        return "{}{} -> {}: {}{}\n{}activate {}\n".format(indentStr,
                                                          fromClass,
                                                          toClass,
                                                          method,
                                                          signature,
                                                          indentStr + TAB_CHAR,
                                                          toClass)


    @staticmethod
    def _addReturnSeqDiagCommand(fromClass, toClass, returnType, indentStr):
        returnMessage = ''

        if returnType != '':
            returnMessage = 'return {}'.format(returnType)

        return "{}{} <-- {}: {}\n{}deactivate {}\n".format(indentStr,
                                                         toClass,
                                                         fromClass,
                                                         returnMessage,
                                                           indentStr,
                                                         fromClass)

    @staticmethod
    def recordFlow(maxSigArgNum=None, maxSigArgCharLen=None):
        '''
        Records in a class list the control flow information which will be used to build
        the seqdiag creation commands.

        :param maxSigArgNum:        maximum arguments number of a called toMethod
                                    toSignature
        :param maxSigArgCharLen:    maximum length a toMethod toSignature can occupy
        :return:
        '''
        SeqDiagBuilder._recordFlowCalled = True

        if not SeqDiagBuilder._isActive:
            return

        SeqDiagBuilder.recordedFlowPath.entryPointReached = False

        frameListLine = repr(traceback.extract_stack())
        frameList = re.findall(FRAME_PATTERN, frameListLine)

        if frameList:
            fromClass = ''
            fromMethod = ''
            toMethodCalledFromLineNumber = ''   # line number in the calling method from
                                                # which the current method was called
            fromMethodReturnDoc = ''
            for frame in frameList[:-1]: #last line in frameList is the call to this toMethod !
                match = re.match(PYTHON_FILE_AND_FUNC_PATTERN, frame)
                if match:
                    pythonClassFilePath = match.group(1)
                    moduleName = match.group(2)
                    methodCallLineNumber = match.group(3)
                    methodName = match.group(4)
                    with open(pythonClassFilePath + moduleName + '.py', "r") as sourceFile:
                        source = sourceFile.read()
                        parsedSource = ast.parse(source)
                        moduleClassNameList = [node.name for node in ast.walk(parsedSource) if isinstance(node, ast.ClassDef)]
                        instanceList = SeqDiagBuilder._getInstancesForClassSupportingMethod(methodName,
                                                                                            moduleName,
                                                                                            moduleClassNameList)
                        if instanceList == []:
                            continue
                        filteredInstanceList, toMethodReturnDoc, methodSignature = SeqDiagBuilder._getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName)
                        instance = filteredInstanceList[0]
                        if len(filteredInstanceList) > 1:
                            filteredClassNameList = []
                            for filteredInstance in filteredInstanceList:
                                filteredClassNameList.append(filteredInstance.__class__.__name__)
                            SeqDiagBuilder._issueWarning(
                                "More than one class {} found in module {} do support toMethod {}{}. Class {} chosen by default for building the sequence diagram. To override this selection, put tag {} somewhere in the toMethod documentation.".format(str(filteredClassNameList), moduleName, methodName, methodSignature, instance.__class__.__name__,
                                                                                                                                                                                                                                                       SEQDIAG_SELECT_METHOD_TAG))

                        toClass = instance.__class__.__name__
                        toMethod = methodName
                        flowEntry = FlowEntry(fromClass, fromMethod, toClass, toMethod, toMethodCalledFromLineNumber,
                                              methodSignature, toMethodReturnDoc)
                        fromClass = toClass
                        fromMethod = toMethod
                        toMethodCalledFromLineNumber = methodCallLineNumber
                        fromMethodReturnDoc = toMethodReturnDoc
                        SeqDiagBuilder.recordedFlowPath.addIfNotIn(flowEntry)
#            print(SeqDiagBuilder.recordedFlowPath)


    @staticmethod
    def _issueWarning(warningStr):
        SeqDiagBuilder.seqDiagWarningList.append(warningStr)


    @staticmethod
    def getWarningList():
        return SeqDiagBuilder.seqDiagWarningList


    @staticmethod
    def _getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList):
        '''
        Returns a list of instances of classes located in moduleName which support the toMethod methodName.
        Normally, the returned list should contain only one instance. If more than one instance are
        returned, which is the case if the module contains a class hierarchy with toMethod methodName
        defined in the base class (and so inherited or overridden by the subclasses) or if the module
        contains two unrelated classes with the same toMethod name, the first encountered class will be
        selected by default, i.e. the first defined class in the module - the root class in case of
        a hierarchy.

        To override this choice, use the tag :seq_diag_select_method in the toMethod documentation.

        :param moduleName:
        :param moduleClassNameList:
        :param methodName:
        :return:
        '''
        instanceList = []

        for className in moduleClassNameList:
            instance = SeqDiagBuilder._instanciateClass(className, moduleName)
            methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)

            for methodTupple in methodTupplesList:
                if methodName == methodTupple[0]:
                    # methodName is a member of className
                    instanceList.append(instance)

        return instanceList


    @staticmethod
    def _getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName):
        '''
        This toMethod returns the passed instance List filtered so that it only contains instances
        supporting the passed methodName. The string associated to the %s tag defined in
        the (selected) toMethod documentation aswell as the (selected) toMethod toSignature are returned.

        :param instanceList:    list of instances of the classes defined in the module moduleName
        :param moduleName:      name of module containing the class definitions of the passed instances
        :param methodName:      name of the toMethod from the doc of which the :seqdiag_return tag value
                                is extracted and the %s tag is searched in
        :return: filteredInstanceList, methodReturnDoc, signatureStr
        '''

        filteredInstanceList = []
        methodReturnDoc = ''
        signatureStr = ''

        if not instanceList:
            return filteredInstanceList, methodReturnDoc, signatureStr

        for instance in instanceList:
            filteredInstanceList.append(instance)
            methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)
            relevantMethodTupple = [x for x in methodTupplesList if x[0] == methodName][0]
            methodObj = relevantMethodTupple[1]
            methodDoc = methodObj.__doc__

            if methodDoc:
                # get toMethod return type from toMethod doc
                match = re.search(SEQDIAG_RETURN_TAG_PATTERN, methodDoc)
                if match:
                    methodReturnDoc = match.group(1)

                # get toMethod tagged by :seqdiag_select_method
                match = re.search(SEQDIAG_SELECT_METHOD_TAG_PATTERN, methodDoc)
                if match:
                    filteredInstanceList = [instance]
                    break

        # get toMethod toSignature

        signatureStr = str(signature(methodObj))

        return filteredInstanceList, methodReturnDoc, signatureStr


    @staticmethod
    def _instanciateClass(className, moduleName):
        '''
        This toMethod instanciate the passed className dxfined in the passed module name
        whatever the number
        :param className:
        :param moduleName:
        :return:
        '''
        module = None

        try:
            module = importlib.import_module(moduleName)
        except ModuleNotFoundError:
            return None

        class_ = getattr(module, className)
        instance = None
        noneStr = ''

        try:
            instance = eval('class_(' + noneStr + ')')
        except TypeError:
            noneStr = 'None'
            while not instance:
                try:
                    instance = eval('class_(' + noneStr + ')')
                except TypeError:
                    noneStr += ', None'

        return instance


if __name__ == '__main__':
    pass