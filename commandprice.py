from abstractcommand import AbstractCommand

class CommandPrice(AbstractCommand):
    CRYPTO = "CRYPTO"
    FIAT = "FIAT"
    EXCHANGE = "EXCHANGE"
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
    HOUR = "HOUR"           #store HH user input
    MINUTE = "MINUTE"       #store MM user input
    HOUR_MINUTE = "HM"      #temporary store HH:MM user input
    DAY_MONTH_YEAR = "DMY"  #temporary store DD/MM/YY user input

    def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
        super().__init__(receiver, 'CommandPrice', rawParmData, parsedParmData)

    def execute(self):
        self.receiver.getCryptoPrice(self.parsedParmData[self.CRYPTO], \
        	                            self.parsedParmData[self.FIAT], \
        	                            self.parsedParmData[self.EXCHANGE], \
        	                            self.parsedParmData[self.DAY], \
        	                            self.parsedParmData[self.MONTH], \
        	                            self.parsedParmData[self.YEAR], \
        	                            self.parsedParmData[self.HOUR], \
        	                            self.parsedParmData[self.MINUTE])
