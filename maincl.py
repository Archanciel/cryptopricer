from controller import Controller
from consoleoutputformater import ConsoleOutputFormater

def main():
    c = Controller(ConsoleOutputFormater())
    c.run()

    
if __name__ == '__main__':
    main()
