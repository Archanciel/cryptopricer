from controller import Controller
from guioutputformater import GuiOutputFormater

def main():
    '''
    Command line main which instanciate a Controller which uses a GuiOutputFormater
    instead of a ConsoleOutputFormater, what maincl does !
    :return:
    '''
    c = Controller(GuiOutputFormater())
    c.run()

    
if __name__ == '__main__':
    main()
