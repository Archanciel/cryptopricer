import os
from pricerequester import PriceRequester
from resultdata import ResultData
from ratedictionary import RateDictionary

COIN_PAIR_NOT_SUPPORTED = 'NOT SUPPORTED'

if os.name == 'posix':
	RATE_DIC_FILE_PATH = '/sdcard/rateDic.txt'
else:
	RATE_DIC_FILE_PATH = 'D:\\Development\\Python\\CryptoPricer\\test\\rateDicSavedData.txt'

MINUTE_PRICE_DAY_NUMBER_LIMIT = 7   # if the request date is older than current time - this value,
									# the price returned is a day close price, not a minute price !

IDX_DATA_ENTRY_TO = 1

class PriceRequesterTestStub(PriceRequester):
	'''
	This class is used for testing purposes only to solve the fact that sometimes requesting
	a fiat/fiat (USD/CHF for example) historical price does not return a correct price.
	'''

	def __init__(self):
		super(PriceRequesterTestStub, self).__init__()
		self.rateDic = RateDictionary()

	def _getHistoMinutePriceAtUTCTimeStamp(self, crypto, unit, timeStampUTC, exchange, resultData):
		cachedResultData = self.rateDic.getResultData(crypto, unit, timeStampUTC, exchange, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))

		if not cachedResultData:
			# resultData not available in the rate dictionary

			cachedResultData = super()._getHistoMinutePriceAtUTCTimeStamp(crypto, unit, timeStampUTC, exchange, resultData)
			self.rateDic.saveResultData(crypto, unit, timeStampUTC, exchange, cachedResultData, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))

		return cachedResultData

	def _getHistoDayPriceAtUTCTimeStamp(self, crypto, unit, timeStampUTC, exchange, resultData):
		cachedResultData = self.rateDic.getResultData(crypto, unit, timeStampUTC, exchange, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))

		if not cachedResultData:
			# resultData not available in the rate dictionary
			
			cachedResultData = super()._getHistoDayPriceAtUTCTimeStamp(crypto, unit, timeStampUTC, exchange, resultData)
			self.rateDic.saveResultData(crypto, unit, timeStampUTC, exchange, cachedResultData, resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO), resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
			
		return cachedResultData

	def getCurrentPrice(self,
						crypto,
						unit,
						exchange):
		resultData = super().getCurrentPrice(crypto,
											 unit,
											 exchange)

		return resultData

if __name__ == '__main__':
	pr = PriceRequesterTestStub()

