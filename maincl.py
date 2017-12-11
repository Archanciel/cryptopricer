from controller import Controller
from consoleoutputformater import ConsoleOutputFormater

def main():
    '''
    Maincl means main command line !
    Command line main which instanciate a Controller which uses a ConsoleOutputFormater
    instead of a GuiOutputFormater, what maingui does !
    '''
    c = Controller(ConsoleOutputFormater())
    c.run()

    
if __name__ == '__main__':
    main()
