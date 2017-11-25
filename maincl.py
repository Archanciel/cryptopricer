from controller import Controller
from commandlineprinter import CommandLinePrinter

def main():
    c = Controller(CommandLinePrinter())
    c.run()

    
if __name__ == '__main__':
    main()
