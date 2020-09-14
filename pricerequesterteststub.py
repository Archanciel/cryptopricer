import os
from pricerequester import PriceRequester
from resultdata import ResultData
from ratedictionary import RateDictionary

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

	# NO INTEREST TO CACHE RATES FOR DATE TIMES WHICH CHANGES AT EACH UNIT TEST
	# EXECUTION !
	#
	# def _getHistoMinutePriceAtUTCTimeStamp(self, crypto, unit, timeStampUTC, exchange, resultData):
	# 	rate = self.rateDic.getRate(crypto, unit, timeStampUTC, exchange)
	#
	# 	if not rate:
	# 		# the rate is not cached and is queried for the first time
	# 		resultData = super()._getHistoMinutePriceAtUTCTimeStamp(crypto, unit, timeStampUTC, exchange, resultData)
	# 		rate = resultData.getValue(resultData.RESULT_KEY_PRICE)
	#
	# 		if rate:
	# 			# no exception indicating that the coin pair is not supported was raised
	# 			self.rateDic.saveRate(crypto, unit, timeStampUTC, exchange, rate)
	# 	else:
	# 		resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_MINUTE)
	# 		resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, timeStampUTC)
	# 		resultData.setValue(ResultData.RESULT_KEY_PRICE, rate)
	#
	# 	return resultData

	def _getHistoDayPriceAtUTCTimeStamp(self, crypto, unit, timeStampUTC, exchange, resultData):
		# fed up with this fucking provider which regurlarly return an invalid value of 1.06
		# for USD/CHF on CCCAGG on 12/9/17 !
		if crypto == 'USD' and unit == 'CHF' and exchange == 'CCCAGG' and timeStampUTC == 1536710400:
			rate = 0.9728
			resultData.setValue(resultData.RESULT_KEY_PRICE, rate)
		elif crypto == 'USD' and unit == 'CHF' and exchange == 'CCCAGG' and timeStampUTC == 1505174400:
			rate = 1.001
			resultData.setValue(resultData.RESULT_KEY_PRICE, rate)
		elif crypto == 'USD' and unit == 'EUR' and exchange == 'CCCAGG' and timeStampUTC == 1505174400:
			rate = 0.8346
			resultData.setValue(resultData.RESULT_KEY_PRICE, rate)
		else:
			rate = self.rateDic.getRate(crypto, unit, timeStampUTC, exchange)

		if not rate:
			# the rate is not cached and is queried for the first time
			resultData = super()._getHistoDayPriceAtUTCTimeStamp(crypto, unit, timeStampUTC, exchange, resultData)
			rate = resultData.getValue(resultData.RESULT_KEY_PRICE)

			if rate != None:
				# no exception indicating that the coin pair is not supported was raised
				self.rateDic.saveRate(crypto, unit, timeStampUTC, exchange, rate)
		else:
			resultData.setValue(ResultData.RESULT_KEY_PRICE_TYPE, resultData.PRICE_TYPE_HISTO_DAY)
			resultData.setValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP, timeStampUTC)
			resultData.setValue(ResultData.RESULT_KEY_PRICE, rate)

		return resultData

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

