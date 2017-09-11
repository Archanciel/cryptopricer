from abstractcommand import AbstractCommand

class CommandPrice(AbstractCommand):
    CRYPTO = "CRYPTO"
    FIAT = "FIAT"
    EXCHANGE = "EXCHANGE"
    HOUR_MIN = "HM"
    LOCAL_DATE_TIME_STR = "LDTS"

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        super().__init__(receiver, 'CommandPrice', rawParmData, parsedParmData)

    def execute(self):
        self.receiver.processCrypto(self.parsedParmData)
