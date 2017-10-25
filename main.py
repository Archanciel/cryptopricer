from controller import Controller

def mainTrial():
    import os, sys
    from io import StringIO

    stdin = sys.stdin
    # sys.stdin = StringIO('btc usd 0 Bittrex' +
    #                      '\n-t22:34' + ERROR: exception !
    #                      '\n-d23/10/17') ERROR: exception  !

    sys.stdin = StringIO('btc usd 23/10 2.56 bittrex' + #ERROR: bad error msg !
                         '\nbtc usd 24/10/2017 22:33 Bittrex' +
                         '\ngbyte btc 24/10/2017 22:33 Bittrex' +
                         '\ngbyte usd 24/10/2017 22:33 Bittrex' +
                         '\n-ceth' +
                         '\n-d23/10' +
                         '\n-t12:56' +
                         '\n-ekraken' +
                         '\nltc ils 0 bit2c' +
                         '\n-eccex' +
                         '\n-ebit2c' +
                         '\n-ebtc38' +
                         '\nbtc usd 12/10/2017 12:00 Unknown\nq\ny') #noticenq\ny to nicely quit the program

    c = Controller()
    c.run()

    sys.stdin = stdin


def main():
    c = Controller()
    c.run()

    
if __name__ == '__main__':
    main()
