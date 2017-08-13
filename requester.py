from command import Command

class Requester:
    '''
    Read in commands entered by the
    user, typically
    
    [btc 5/7 0.0015899 6/7 0.00153] [usd chf]

    and return a command dictionnary
    
    [CRYPTO: btc 5/7 0.0015899 6/7 0.00153] [FIAT: usd chf]
    '''
    def request(self):
        inp = input('Enter command (h for help)\n')
        inp = inp.upper()
        
        while inp == 'H':
            self._printHelp()
            inp = input('Enter command (h for help)\n')
        
        if inp == 'Q':   
            return {Command.QUIT : ''}
        else:
            return {Command.CRYPTO : []}

    def _printHelp(self):
        print('Usage:\n')
        print('[btc 5/7 0.0015899 6/7 0.00153] [usd chf]')
        inp = input('\nm for more or anything else to exit help\n')
        
        if inp.upper() == 'M':
            print("\nns - don't save retrieved prices")
            print("rm [1, 3, 4] - remove line numbers\n")


if __name__ == '__main__':
    r = Requester()
    r.request()