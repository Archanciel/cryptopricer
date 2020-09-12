import json, os, atexit, arrow

from datetimeutil import DateTimeUtil
from resultdata import ResultData

FR_DATE_TIME_FORMAT_ARROW = 'DD/MM/YYYY HH:mm:ss'

class RateDictionary:
	dic = {}
	wasDicUpdated = False

	def __init__(self):
		atexit.register(self.saveDic)

		if os.name == 'posix':
			RATE_DIC_FILE_PATH = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/cryptopricer/test/rateDic.txt'
		else:
			RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\CryptoPricer\\test\\rateDicSavedData.txt'

		if os.path.isfile(RATE_DIC_FILE_PATH):
			with open(RATE_DIC_FILE_PATH, 'r') as f:
				RateDictionary.dic = json.load(f)

	def getResultData(self, crypto, unit, timeStampUTCStr, exchange, optionValueSymbol=None, optionFiatSymbol=None):
		resultData = None

		try:
			resultDataDic = self.dic[self.getDicKey(crypto, unit, timeStampUTCStr, exchange, optionValueSymbol, optionFiatSymbol)]
			resultData = ResultData(resultDataDic)
		except KeyError:
			# resultData not yet in resultData dic file
			pass
		
		return resultData # either None, Not supported or ResultData instance

	def saveResultData(self, crypto, unit, timeStampUTCStr, exchange, resultData, optionValueSymbol=None, optionFiatSymbol=None):
		self.dic[self.getDicKey(crypto, unit, timeStampUTCStr, exchange, optionValueSymbol, optionFiatSymbol)] = resultData._resultDataDic
		RateDictionary.wasDicUpdated = True
		
	def saveDic(self):
		if RateDictionary.wasDicUpdated:
			if os.name == 'posix':
				RATE_DIC_FILE_PATH = '/sdcard/rateDic.txt'
			else:
				RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\CryptoPricer\\test\\rateDicSavedData.txt'
			with open(RATE_DIC_FILE_PATH, 'w') as f:
				json.dump(RateDictionary.dic,
				          f,
				          indent=4,
				          sort_keys=True)

			RateDictionary.wasDicUpdated = False

	def getDicKey(self, crypto, unit, timeStampUTCStr, exchange, optionValueSymbol, optionFiatSymbol):
		if not optionValueSymbol:
			optionValueSymbol = ''
			
		if not optionFiatSymbol:
			optionFiatSymbol = ''
			
		return crypto + unit + str(timeStampUTCStr) + exchange + optionValueSymbol + optionFiatSymbol
		
if __name__ == "__main__":
	rd = RateDictionary()

	resultData = ResultData()
	
	crypto = 'ETH'
	unit = 'USD'
	ts = '15234867'
	exchange = 'BitTrex'

	resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
	resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
	resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
	resultData.setValue(resultData.RESULT_KEY_EXCHANGE, exchange)
	resultData.setValue(resultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
	resultData.setValue(resultData.RESULT_KEY_PRICE, 465.52)
	resultData.setValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING, '5/12/17 09:30')
	resultData.setValue(resultData.RESULT_KEY_PRICE_TIME_STAMP, 1512462600)
	resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
	                    {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': None,
	                     'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None})
	resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
	                    {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
	                     'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None,
	                     'OPTION_VALUE_SYMBOL': None,
	                     'OPTION_FIAT_SYMBOL': None, 'OPTION_FIAT_EXCHANGE': None})
	
	rd.saveResultData(crypto, unit, ts, exchange, resultData)
	resData = rd.getResultData(crypto, unit, ts, exchange)
	print(resData)

	resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, 'btc')
	resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, 'chf')
	resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
	                    {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': None,
	                     'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None})
	resultData.setValue(resultData.RESULT_KEY_INITIAL_COMMAND_PARMS,
	                    {'CRYPTO': 'eth', 'UNIT': 'usd', 'EXCHANGE': 'bittrex', 'DAY': '5', 'MONTH': '12', 'YEAR': '17',
	                     'HOUR': '9', 'MINUTE': '30', 'DMY': None, 'HM': None, 'OPTION_VALUE_AMOUNT': None,
	                     'OPTION_VALUE_SYMBOL': 'btc',
	                     'OPTION_FIAT_SYMBOL': 'chf', 'OPTION_FIAT_EXCHANGE': None})
	rd.saveResultData(crypto, unit, ts, exchange, resultData, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
	resData = rd.getResultData(crypto, unit, ts, exchange, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
	print(resData)
