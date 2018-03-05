import traceback, re, ast, importlib, inspect

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
                        classes = [node.name for node in ast.walk(parsedSource) if isinstance(node, ast.ClassDef)]
                        pythonClassName = classes[0] # assumed only one class per module !
                        instance = SeqDiagBuilder.instanciateClass(pythonClassName, pythonModuleName)

                        if instance:
                            methodReturnDoc = SeqDiagBuilder.getMethodReturnDoc(instance, methodName)
                        else:
                            methodReturnDoc = ''

                        SeqDiagBuilder.sequDiagInformationList.append([pythonModuleName, pythonClassName, methodName, methodReturnDoc])


    def printSeqDiagCommands():
        for entry in SeqDiagBuilder.sequDiagInformationList:
            lineStr = "{} {}.{} <-- {}".format(entry[0], entry[1], entry[2], entry[3])
            print(lineStr)

    @staticmethod
    def getMethodReturnDoc(instance, methodName):
        '''
        This method returns the string associated to the :seqdiag_return tag defined in
        the method documentation

        :param instance:   instance of class containing the passed methodName
        :param methodName: name of the method from which the :seqdiag_return tag value is
                           extracted
        :return:
        '''
        methodTupplesList = inspect.getmembers(instance, predicate=inspect.ismethod)
        relevantMethodTupple = [x for x in methodTupplesList if x[0] == methodName][0]
        methodObj = relevantMethodTupple[1]
        methodDoc = methodObj.__doc__
        methodReturnDoc = None

        if methodDoc:
            match = re.search(SEQDIAG_RETURN_TAG_PATTERN, methodDoc)
            if match:
                methodReturnDoc = match.group(1)

        return methodReturnDoc

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