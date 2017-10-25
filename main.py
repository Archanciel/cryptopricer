from controller import Controller

def main():
    import os, sys
    from io import StringIO

    # stdin = sys.stdin
    # sys.stdin = StringIO('btc usd 0 Bittrex' + \
    #                      '\nbtc usd 24/10/2017 22:33 Bittrex' + \
    #                      '\ngbyte btc 24/10/2017 22:33 Bittrex' + \
    #                      '\ngbyte usd 24/10/2017 22:33 Bittrex' + \
    #                      '\nbtc usd 0 Bittrex' + \
    #                      '\ngbyte btc 0 Bittrex' + \
    #                      '\nbtc usd 12/10/2017 12:00 Unknown' + \
    #                      '\nbtc usd 12/10/2017 12:00 bittrex\nq\ny') #notice \nq\ny to nicely quit the program

    c = Controller()
    c.run()

    # sys.stdin = stdin

if __name__ == '__main__':
    main()
