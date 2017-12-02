from controller import Controller
from guioutputformater import GuiOutputFormater

def main():
    c = Controller(GuiOutputFormater())
    c.run()

    
if __name__ == '__main__':
    main()
