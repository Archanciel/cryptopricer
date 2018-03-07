import traceback, re, ast, importlib, inspect
from inspect import signature


SEQDIAG_RETURN_TAG_PATTERN = r":seqdiag_return (.*)"
SEQDIAG_SELECT_METHOD_TAG_PATTERN = r":seqdiag_select_method(.*)"
PYTHON_FILE_AND_FUNC_PATTERN = r"([\w:\\]+\\)(\w+)\.py, line \d* in (.*)"
FRAME_PATTERN = r"(?:<FrameSummary file ([\w:\\,._\s]+)(?:>, |>\]))"


class SeqDiagBuilder:
    '''
    This class contains a static utility methods used to build a sequence diagram from the
    call stack as at the point in the python code were it is called.

    To build the diagram, type seqdiag -Tsvg stack.txt in a command line window.
    This build a svg file which can be displayed in a browsxer.
    '''

    sequDiagInformationList = []
    sequDiagWarningList = []
    isBuildMode = False

    @staticmethod
    def buildSeqDiag(maxDepth, startElemName, startMethName = None, outputFile ="c:\\temp\\stack.txt", maxSigArgNum = None, maxSigArgCharLen = None):
        '''
        Writes in a file a seqdiag specification file.
        To build the diagram, type seqdiag -Tsvg stack.txt in a command line window.
        This build a svg file which can be displayed in a browsxer.

        :param maxDepth:            max generarted stack depth calculated from the
                                    stack bottom.
                                    Ex: if f(g(h(i(j()))))), maxDepth of 3 draw a
                                    seq diagr starting at h for calls h --> i--> j
        :param startElemName:       string indicating the element (class, module, actor)
                                    name which constitutes the left most vertical diagram
                                    element
        :param startMethName:       optional string indicating the method name called
                                    by startElemName
        :param outputFile:          file receiving the sequence diagram
        :param maxSigArgNum:        maximum arguments number of a called method
                                    signature
        :param maxSigArgCharLen:    maximum length a method signature can occupy
        :return:
        '''
        if not SeqDiagBuilder.isBuildMode:
            return

        frameListLine = repr(traceback.extract_stack(limit = maxDepth + 1))
        frameList = re.findall(FRAME_PATTERN, frameListLine)

        if frameList:
            for frame in frameList[:-1]: #last line in frameList is the call to this method !
                match = re.match(PYTHON_FILE_AND_FUNC_PATTERN, frame)
                if match:
                    pythonClassFilePath = match.group(1)
                    moduleName =  match.group(2)
                    methodName = match.group(3)
                    with open(pythonClassFilePath + moduleName + '.py', "r") as sourceFile:
                        source = sourceFile.read()
                        parsedSource = ast.parse(source)
                        moduleClassNameList = [node.name for node in ast.walk(parsedSource) if isinstance(node, ast.ClassDef)]
                        instanceList = SeqDiagBuilder.getInstancesForClassSupportingMethod(methodName,
                                                                                           moduleName,
                                                                                           moduleClassNameList)
                        filteredInstanceList, methodReturnDoc, methodSignature = SeqDiagBuilder.getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName)
                        instance = filteredInstanceList[0]
                        if len(filteredInstanceList) > 1:
                            SeqDiagBuilder.issueWarning("More than one class {} found in module {} do support method {}{}. Class {} chosen by default for building the sequence diagram. To override this selection, put tag :seqdiag_select_method somewhere in the method documentation.".format(str(instanceList), moduleName, methodName, methodSignature, instance))

                        SeqDiagBuilder.sequDiagInformationList.append([moduleName, instance.__class__.__name__, methodName, methodSignature, methodReturnDoc])


    @staticmethod
    def issueWarning(warningStr):
        SeqDiagBuilder.sequDiagWarningList.append(warningStr)
        print('************* WARNING - ' + warningStr + ' *************')


    @staticmethod
    def getWarningList():
        return SeqDiagBuilder.sequDiagWarningList


    @staticmethod
    def getInstancesForClassSupportingMethod(methodName, moduleName, moduleClassNameList):
        '''
        Returns a list of instances of classes located in moduleName which support the method methodName.
        Normally, the returned list should contain only one instance. If more than one instance are
        returned, which is the case if the module contains a class hierarchy with method methodName
        defined in the base class (and so inherited or overridden by the subclasses) or if the module
        contains two unrelated classes with the same method name, the first encountered class will be
        selected by default, i.e. the first defined class in the module - the root class in case of
        a hierarchy.

        To override this choice, use the tag :seq_diag_select_method in the method documentation.

        :param moduleName:
        :param moduleClassNameList:
        :param methodName:
        :return:
        '''
        instanceList = []

        for className in moduleClassNameList:
            instance = SeqDiagBuilder.instanciateClass(className, moduleName)
            methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)

            for methodTupple in methodTupplesList:
                if methodName == methodTupple[0]:
                    # methodName is a member of className
                    instanceList.append(instance)

        return instanceList


    @staticmethod
    def printSeqDiagInstructions():
        for entry in SeqDiagBuilder.sequDiagInformationList:
            lineStr = "{} {}.{}{} <-- {}".format(entry[0], entry[1], entry[2], entry[3], entry[4])
            print(lineStr)


    @staticmethod
    def getSeqDiagInstructionsStr():
        seqDiagInstructionsStr = ''

        for entry in SeqDiagBuilder.sequDiagInformationList:
            lineStr = "{} {}.{}{} <-- {}\n".format(entry[0], entry[1], entry[2], entry[3], entry[4])
            seqDiagInstructionsStr += lineStr

        return seqDiagInstructionsStr


    @staticmethod
    def getFilteredInstanceListAndMethodSignatureAndReturnDoc(instanceList, moduleName, methodName):
        '''
        This method returns the passed instance List filtered so that it only contains instances
        supporting the passed methodName. The string associated to the :seqdiag_return tag defined in
        the (selected) method documentation aswell as the (selected) method signature are returned.

        :param instanceList:    list of instances of the classes defined in the module moduleName
        :param moduleName:      name of module containing the class definitions of the passed instances
        :param methodName:      name of the method from the doc of which the :seqdiag_return tag value
                                is extracted and the :seqdiag_select_method tag is searched in
        :return: filteredInstanceList, methodReturnDoc, signatureStr
        '''

        if not instanceList:
            return ''

        filteredInstanceList = []
        methodReturnDoc = ''

        for instance in instanceList:
            filteredInstanceList.append(instance)
            methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)
            relevantMethodTupple = [x for x in methodTupplesList if x[0] == methodName][0]
            methodObj = relevantMethodTupple[1]
            methodDoc = methodObj.__doc__

            if methodDoc:
                # get method return type from method doc
                match = re.search(SEQDIAG_RETURN_TAG_PATTERN, methodDoc)
                if match:
                    methodReturnDoc = match.group(1)

                # get method tagged by :seqdiag_select_method
                match = re.search(SEQDIAG_SELECT_METHOD_TAG_PATTERN, methodDoc)
                if match:
                    filteredInstanceList = [instance]
                    break

        # get method signature

        signatureStr = str(signature(methodObj))

        return filteredInstanceList, methodReturnDoc, signatureStr


    @staticmethod
    def instanciateClass(className, moduleName):
        '''
        This method instanciate the passed className dxfined in the passed module name
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


    @staticmethod
    def reset():
        '''
        Reinitialise the class level seq diag information list and seq diag warning list
        :return:
        '''
        SeqDiagBuilder.sequDiagInformationList = []
        SeqDiagBuilder.sequDiagWarningList = []

if __name__ == '__main__':
    pass