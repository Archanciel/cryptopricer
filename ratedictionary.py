import json, os, atexit

class RateDictionary:
	dic = {}

	def __init__(self):
		atexit.register(self.saveDic)

		if os.name == 'posix':
			RATE_DIC_FILE_PATH = '/sdcard/rateDic.txt'
		else:
			RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\CryptoPricer\\test\\rateDicSavedData.txt'

		if os.path.isfile(RATE_DIC_FILE_PATH):
			with open(RATE_DIC_FILE_PATH, 'r') as f:
				RateDictionary.dic = json.load(f)

	def getRate(self, crypto, unit, timeStampUTCStr, exchange):
		rate = None

		try:
			rate = self.dic[self.getDicKey(crypto, unit, timeStampUTCStr, exchange)]
		except KeyError:
			# rate not yet in rate dic file
			pass

		return rate

	def saveRate(self, crypto, unit, timeStampUTCStr, exchange, rate):
		self.dic[self.getDicKey(crypto, unit, timeStampUTCStr, exchange)] = rate
		
	def saveDic(self):
		if os.name == 'posix':
			RATE_DIC_FILE_PATH = '/sdcard/rateDic.txt'
		else:
			RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\CryptoPricer\\test\\rateDicSavedData.txt'
		with open(RATE_DIC_FILE_PATH, 'w') as f:
			json.dump(RateDictionary.dic,
			          f,
			          indent=4,
			          sort_keys=True)

	def getDicKey(self, crypto, unit, timeStampUTCStr, exchange):
		return crypto + unit + str(timeStampUTCStr) + exchange
		
if __name__ == "__main__":
	rd = RateDictionary()
	rd.saveRate('btc', 'chf', '15234867', 'binance', 11000.8542)
	rd.saveRate('neo', 'usd', '15234847', 'binance', 22.42)
	print(rd.getRate('btc', 'eth', '15234847', 'binance'))
	print(rd.getRate('neo', 'eth', '15234847', 'binance'))