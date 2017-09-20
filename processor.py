from abstractcommand import AbstractCommand

class Processor:
    def execute(self, command):
        commandParms = command.parsedParmData
        return None
        
        
    def getCryptoPrice(self, \
    	                  crypto, \
    	                  fiat, \
    	                  exchange, \
    	                  day, \
    	                  month, \
    	                  year, \
    	                  hour, \
    	                  minute):
    	  print('getting {} price in {} at {} on {}/{}/{} {}:{} ...'.format(crypto,fiat,exchange,day,month,year,hour,minute))
