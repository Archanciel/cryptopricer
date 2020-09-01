import json, os

class RateDictionary:
	def __init__(self):
		self.dicFilePath = "/storage/emulated/0/CryptoPricerData/text.txt"
		self.dic = {}

		
		if os.path.isfile(self.dicFilePath):
			with open(self.dicFilePath,'r') as f:
				self.dic = json.load(f)
		
	def getRate(self, crypto, unit, timeStampUTCStr, exchange):
		return self.dic[self.getDicKey(crypto, unit, timeStampUTCStr, exchange)]
		
	def saveRate(self, crypto, unit, timeStampUTCStr, exchange, rate):
		self.dic[self.getDicKey(crypto, unit, timeStampUTCStr, exchange)] = rate
		
	def saveDic(self):
		with open(self.dicFilePath,'w') as f:
			json.dump(self.dic, 
					  f, 
					  indent=4,
					  sort_keys=True)	

	def getDicKey(self, crypto, unit, timeStampUTCStr, exchange):
		return crypto + unit + timeStampUTCStr + exchange
		
if __name__ == "__main__":
#	d = {"one":1, "two":2}
#	json.dump(d, open("/storage/emulated/0/CryptoPricerData/text.txt",'w'))

#	d2 = json.load(open("/storage/emulated/0/CryptoPricerData/text.txt"))
#	print(d2)
#	print(d2["one"])	

	rd = RateDictionary()
	rd.saveRate('btc', 'chf', '15234867', 'binance', 11000.8542)
	rd.saveRate('btc', 'eth', '15234847', 'binance', 105.42)
	rd.saveDic()
	print(rd.getRate('btc', 'eth', '15234847', 'binance'))		