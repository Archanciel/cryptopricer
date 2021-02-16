import json, os, atexit

if os.name == 'posix':
	RATE_DIC_FILE_PATH = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/cryptopricer/test/rateDicSavedData.txt'
else:
	RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\CryptoPricer\\test\\rateDicSavedData.txt'

class RateDictionary:
	dic = {}
	wasDicUpdated = False
	cachedRateAccessNumber = 0

	def __init__(self):
		atexit.register(self._saveDic)

		if RateDictionary.dic == {}:
			if os.path.isfile(RATE_DIC_FILE_PATH):
				with open(RATE_DIC_FILE_PATH, 'r') as f:
					RateDictionary.dic = json.load(f)

	def __del__(self):
		if RateDictionary.cachedRateAccessNumber > 0:
			print('\nCached rates access number: ', RateDictionary.cachedRateAccessNumber)
			RateDictionary.cachedRateAccessNumber = 0
	
	def getRate(self, crypto, unit, timeStampUTCStr, exchange):
		rate = None

		try:
			rate = RateDictionary.dic[self._getDicKey(crypto, unit, timeStampUTCStr, exchange)]
			RateDictionary.cachedRateAccessNumber += 1
		except KeyError:
			# rate not yet in rate dic file
			pass

		return rate

	def saveRate(self, crypto, unit, timeStampUTCStr, exchange, rate):
		RateDictionary.dic[self._getDicKey(crypto, unit, timeStampUTCStr, exchange)] = rate
		RateDictionary.wasDicUpdated = True
		
	def _saveDic(self):
		if RateDictionary.wasDicUpdated:
			with open(RATE_DIC_FILE_PATH, 'w') as f:
				json.dump(RateDictionary.dic,
				          f,
				          indent=4,
				          sort_keys=True)

			RateDictionary.wasDicUpdated = False

	def _getDicKey(self, crypto, unit, timeStampUTCStr, exchange):
		return crypto + unit + str(timeStampUTCStr) + exchange
		
if __name__ == "__main__":
	rd = RateDictionary()
	rd.saveRate('btc', 'chf', '15234867', 'binance', 11000.8542)
	rd.saveRate('neo', 'usd', '15234847', 'binance', 22.42)
	print(rd.getRate('btc', 'eth', '15234847', 'binance'))
	print(rd.getRate('neo', 'eth', '15234847', 'binance'))