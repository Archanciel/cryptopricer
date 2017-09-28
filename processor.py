from abstractcommand import AbstractCommand

class Processor:
    def __init__(self, priceRequester):
        self.priceRequester = priceRequester
            
        
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
