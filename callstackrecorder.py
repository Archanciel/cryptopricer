import traceback, re

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
                for frame in frameList[:-1]: #last line is the call to this method !
                    f.write(frame + '\n')

