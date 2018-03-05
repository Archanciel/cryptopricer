import traceback, re, ast, importlib, inspect
from inspect import signature

SEQDIAG_RETURN_TAG_PATTERN = r":seqdiag_return (.*)"

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
                    pythonModuleName =  match.group(2)
                    methodName = match.group(3)
                    with open(pythonClassFilePath + pythonModuleName + '.py', "r") as sourceFile:
                        source = sourceFile.read()
                        parsedSource = ast.parse(source)
                        moduleClassNameList = [node.name for node in ast.walk(parsedSource) if isinstance(node, ast.ClassDef)]
                        pythonClassNameList = SeqDiagBuilder.getClassNameList(pythonModuleName, moduleClassNameList, methodName)
                        pythonClassName = pythonClassNameList[0]
                        methodReturnDoc, methodSignature = SeqDiagBuilder.getMethodSignatureAndReturnDoc(pythonClassName, pythonModuleName, methodName)
                        if len(pythonClassNameList) > 1:
                            SeqDiagBuilder.raiseWarning("More than one class {} found in module {} do support method {}{}. Class {} arbitrarily chosen for building the sequence diagram".format(str(pythonClassNameList), pythonModuleName, methodName, methodSignature, pythonClassName))

                        SeqDiagBuilder.sequDiagInformationList.append([pythonModuleName, pythonClassName, methodName, methodSignature, methodReturnDoc])


    @staticmethod
    def raiseWarning(warningStr):
        print('************* WARNING - ' + warningStr + ' *************')


    @staticmethod
    def getClassNameList(moduleName, moduleClassNameList, methodName):
        '''
        Returns a list of class names which are located in moduleName, belong to the passed
        moduleClassNameList and support the method methodName

        :param moduleName:
        :param moduleClassNameList:
        :param methodName:
        :return:
        '''
        classNameList = []

        for className in moduleClassNameList:
            instance = SeqDiagBuilder.instanciateClass(className, moduleName)
            methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)

            for methodTupple in methodTupplesList:
                if methodName == methodTupple[0]:
                    # methodName is a member of className
                    classNameList.append(className)

        return classNameList


    @staticmethod
    def printSeqDiagInstructions():
        for entry in SeqDiagBuilder.sequDiagInformationList:
            lineStr = "{} {}.{}{} <-- {}".format(entry[0], entry[1], entry[2], entry[3], entry[4])
            print(lineStr)

    @staticmethod
    def getMethodSignatureAndReturnDoc(className, moduleName, methodName):
        '''
        This method returns the string associated to the :seqdiag_return tag defined in
        the method documentation

        :param instance:   instance of class containing the passed methodName
        :param methodName: name of the method from which the :seqdiag_return tag value is
                           extracted
        :return:
        '''
        instance = SeqDiagBuilder.instanciateClass(className, moduleName)

        if not instance:
            return ''

        # get method return type from method doc

        methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)
        relevantMethodTupple = [x for x in methodTupplesList if x[0] == methodName][0]
        methodObj = relevantMethodTupple[1]
        methodDoc = methodObj.__doc__
        methodReturnDoc = ''

        if methodDoc:
            match = re.search(SEQDIAG_RETURN_TAG_PATTERN, methodDoc)
            if match:
                methodReturnDoc = match.group(1)

        # get method signature

        signatureStr = str(signature(methodObj))

        return methodReturnDoc, signatureStr

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


if __name__ == '__main__':
    pass