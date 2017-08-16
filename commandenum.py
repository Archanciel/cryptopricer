from enum21 import Enum  # not possiple in bullshit python 3.2 !


class CommandEnum(Enum):
    QUIT = 1

    # CRYPTO : ['BTC' : [5/7, 0.0015899, 6/7, 0.00153]
    CRYPTO = 2

    # FIAT : ['USD', 'CHF']
    FIAT = 3

    # Don't save retrieved prices
    NOSAVE = 4

    # Remove saved prices using displayej
    # line numbers
    # REMOVE : [1, 3, 5]
    REMOVE = 5

    ERROR = 6


if __name__ == '__main__':
    for c in CommandEnum:  # no  working for this version of enum
        print(c)
