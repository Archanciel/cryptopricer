from controller import Controller
from consoleoutputformater import ConsoleOutputFormater

def main():
    '''
    Maincl means main command line !
    '''
    c = Controller(ConsoleOutputFormater())
    c.run()

    
if __name__ == '__main__':
    main()
