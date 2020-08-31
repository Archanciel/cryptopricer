import json

class RateDictionary:
	def __init__(self):
		self.dic = {}
		
	def getRate(self, crypto, unit, timeStampUTCStr, exchange):
		pass
		
	def saveRate(self, crypto, unit, timeStampUTCStr, exchange, rate):
		self.dic[crypto + unit + timeStampUTCStr + exchange] = rate
		
	def saveDic(self):
		with open("/storage/emulated/0/CryptoPricerData/text.txt",'w') as f:
			json.dump(self.dic, 
					  f, 
					  indent=4,
					  sort_keys=True)	

if __name__ == "__main__":
#	d = {"one":1, "two":2}
#	json.dump(d, open("/storage/emulated/0/CryptoPricerData/text.txt",'w'))

#	d2 = json.load(open("/storage/emulated/0/CryptoPricerData/text.txt"))
#	print(d2)
#	print(d2["one"])	

	rd = RateDictionary()
	rd.saveRate('btc', 'usd', '15234867', 'binance', 11000.8542)
	rd.saveRate('btc', 'eur', '15234847', 'binance', 10500.42)
	rd.saveDic()		