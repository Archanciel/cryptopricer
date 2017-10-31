import os

class Printer:
    def __init__(self):
        if os.name == 'posix':
            import android
            self._clipboard = android.Android()
        else:
            pass
           
    
    def print(self, result):
        print(result)
        
        
    def toClipboard(self, value):
        if os.name == 'posix':
            self._clipboard.setClipboard(str(value))
        else:
            pass


    def fromClipboard(self):
        if os.name == 'posix':
            return self._clipboard.getClipboard().result
        else:
            pass


if __name__ == '__main__':
    pr = Printer()

    a = 12.56
    pr.toClipboard(a)
    print('Clip: ' + pr.fromClipboard())

