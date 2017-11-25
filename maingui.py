from controller import Controller
from guiprinter import GuiPrinter

def main():
    c = Controller(GuiPrinter())
    c.run()

    
if __name__ == '__main__':
    main()
