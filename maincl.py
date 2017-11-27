from controller import Controller
from consoleprinter import ConsolePrinter

def main():
    c = Controller(ConsolePrinter())
    c.run()

    
if __name__ == '__main__':
    main()
