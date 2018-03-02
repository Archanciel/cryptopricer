import traceback, re, ast, inspect

class CallStackRecorder:
    '''
    This class contains a static utility methods used to store in a file the call stack. This information
    will be used to draw a sequence diagram of the calls hierchy.

    To build the diagram, type seqdiag -Tsvg stack.txt in a command line window.
    This build a svg file which can be displayed in a browsxer.
    '''

    @staticmethod
    def storeCallStack():
        '''
        Writes in a file a call stack to help buiding a sequence diagram using seqdiag.
        To build the diagram, type seqdiag -Tsvg stack.txt in a command line window.
        This build a svg file which can be displayed in a browsxer.

        :return: nothing
        '''
        frameListLine = repr(traceback.extract_stack(limit=5))
        frameList = re.findall(r"(?:<FrameSummary file ([\w:\\,._\s]+)(?:>, |>\]))", frameListLine)
        if frameList:
            with open("c:\\temp\\stack.txt", "a") as f:
                for frame in frameList[:-1]: #last line in frameList is the call to this method !
                    match = re.match(r"([\w:\\,.]+), line \d* in (.*)", frame)
                    if match:
                        pythonFilePathName = match.group(1)
                        methodName = match.group(2)
                        with open(pythonFilePathName, "r") as sourceFile:
                            source = sourceFile.read()
                            p = ast.parse(source)
                            classes = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
                            f.write(classes[0] + '.' + methodName + '\n')

if __name__ == '__main__':
    import importlib
    module = importlib.import_module('controller')
    class_ = getattr(module, 'Controller')
    print(class_.__doc__)
    instance = None
    noneStr = ''

    try:
        instance = eval('class_('+ noneStr + ')')
    except TypeError:
        noneStr = 'None'
        while not instance:
            try:
                instance = eval('class_('+ noneStr + ')')
            except TypeError:
                noneStr += ', None'

    methods = inspect.getmembers(instance, predicate=inspect.ismethod)
    print(instance.__class__)

