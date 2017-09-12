from abstractcommand import AbstractCommand

class CommandPrice(AbstractCommand):
    CRYPTO = "CRYPTO"
    FIAT = "FIAT"
    EXCHANGE = "EXCHANGE"
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
    HOUR_MINUTE = "HM"      #store HH:MM user input
    DAY_MONTH_YEAR = "DMH"  #store DD/MM/YY user input
    LOCAL_DATE_TIME_STR = "LDTS"

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        super().__init__(receiver, 'CommandPrice', rawParmData, parsedParmData)

    def execute(self):
        self.receiver.processCrypto(self.parsedParmData)
