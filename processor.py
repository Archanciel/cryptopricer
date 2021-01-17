from datetimeutil import DateTimeUtil
from resultdata import ResultData

# This error message is consistant with the provider error 'HitBTC market does not exist for this coin pair (BTC-USD)' !
MARKET_NOT_SUPPORTED_ERROR = "ERROR - {} market does not exist or is not yet supported by the application"

class Processor:
	'''
	This class is used as Receiver by the Command component in the Command pattern.
	'''
	def __init__(self,
				 configManager,
				 priceRequester,
				 crypCompExchanges):
		self.configManager = configManager
		self.priceRequester = priceRequester
		self.crypCompExchanges = crypCompExchanges

	def getCryptoPrice(self,
					   crypto,
					   unit,
					   exchange,
					   day,
					   month,
					   year,
					   hour,
					   minute,
					   optionValueSymbol=None,
					   optionValueAmount=None,
					   optionValueSaveFlag=None,
					   requestInputString='',
					   optionFiatSymbol=None,
					   optionFiatExchange=None,
					   optionFiatSaveFlag=None,
					   optionPriceSymbol=None,
					   optionPriceAmount=None,
					   optionPriceSaveFlag=None):
		'''
		Ask the PriceRequester either a RT price or a historical price. Then, in case a price value parm (-v)
		was specified, does the conversion and add its result to the returned ResultData
		:param optionFiatSymbol:
		:param optionFiatSaveFlag:
		:param optionPriceSymbol:
		:param optionPriceAmount:
		:param optionPriceSaveFlag:
		:param crypto: upper case crypto symbol
		:param unit: upper case counter party symbol
		:param exchange: exchange name
		:param day: int day number
		:param month: int month number
		:param year: int year number
		:param hour: int hour number
		:param minute: int minute number
		:param optionValueSymbol: upper case currency value symbol. If == crypto, this means that optionValueAmount provided
								 is in crypto and must be converted into unit (counter party) at the rate returned by
								 the PriceRequester.

								 If the currency value symbol == unit, this means that optionValueAmount provided
								 is in the counter party (unit or an other crypto) and must be converted into crypto at
								 the rate returned by the PriceRequester.

								 Ex 1:  -v0.001btc
										crypto == BTC
										unit == USD
										optionValueSymbol == BTC
										optionValueAmount == 0.001

										if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
										converted value will be 20000 USD * 0.001 BTC => 200 USD

								 Ex 2:  -v500usd
										crypto == BTC
										unit == USD
										optionValueSymbol == USD
										optionValueAmount == 500

										if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
										converted value will be 1 / 20000 USD * 500 USD => 0.025 BTC

		:param optionValueAmount:   float specified value option amount
		:param optionValueSaveFlag: used to refine warning if value option not applicable
		:param requestInputString): used for better error msg !
		:param optionFiatSymbol:    stores the fiat symbol, i.e. the fiat into which the returned
									unit amount is converted
		:param optionFiatSaveFlag:  used to refine warning if fiat option not applicable. May be suppressed if not used
		:param optionPriceSymbol:   upper case currency price symbol
		:param optionPriceAmount:   float specified price option amount
		:param optionPriceSaveFlag: used to refine warning if price option not applicable

		:seqdiag_return ResultData
		:return: a ResultData filled with result values
		'''

		# validating exchange and fiat exchange

		if exchange == None:
			resultData = ResultData()
			resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, "ERROR - exchange could not be parsed due to an error in your request ({})".format(requestInputString))
			return resultData
		else:
			try:
				validExchangeSymbol = self.crypCompExchanges.getExchange(exchange)
			except(KeyError):
				resultData = ResultData()
				resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG, MARKET_NOT_SUPPORTED_ERROR.format(exchange))
				return resultData

		validFiatExchangeSymbol = None

		if optionFiatExchange:
			try:
				validFiatExchangeSymbol = self.crypCompExchanges.getExchange(optionFiatExchange)
			except(KeyError):
				resultData = ResultData()
				resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG,
									MARKET_NOT_SUPPORTED_ERROR.format(optionFiatExchange))
				return resultData

		localTz = self.configManager.localTimeZone
		dateTimeFormat = self.configManager.dateTimeFormat

		resultData = self._getPrice(crypto,
									unit,
									validExchangeSymbol,
									year,
									month,
									day,
									hour,
									minute,
									dateTimeFormat,
									localTz)


		if resultData.isError():
			# since crypto/unit is not supported by the exchange, we try to request the unit/crypto inverted rate
			errorMsg = resultData.getValue(resultData.RESULT_KEY_ERROR_MSG)
			resultData = self._getPrice(unit,
										crypto,
										validExchangeSymbol,
										year,
										month,
										day,
										hour,
										minute,
										dateTimeFormat,
										localTz)

			resultData.setValue(resultData.RESULT_KEY_CRYPTO, crypto)
			resultData.setValue(resultData.RESULT_KEY_UNIT, unit)
			price = resultData.getValue(resultData.RESULT_KEY_PRICE)

			if price:
				resultData.setValue(resultData.RESULT_KEY_PRICE, 1 / price)
				resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, None)
			else:
				resultData.setValue(resultData.RESULT_KEY_ERROR_MSG, errorMsg)

		if optionFiatSymbol is not None and not resultData.isError():
			resultData = self._computeOptionFiatAmount(resultData,
													   optionFiatSymbol,
													   validFiatExchangeSymbol,
													   crypto,
													   unit,
													   validExchangeSymbol,
													   year,
													   month,
													   day,
													   hour,
													   minute,
													   dateTimeFormat,
													   localTz)

		if optionValueSymbol is not None and not resultData.isError():
			resultData = self._computeOptionValueAmount(resultData,
														crypto,
														unit,
														optionFiatSymbol,
														optionValueSymbol,
														optionValueAmount,
														optionValueSaveFlag)

		return resultData

	def _getPrice(self,
				  currency,
				  targetCurrency,
				  exchange,
				  year,
				  month,
				  day,
				  hour,
				  minute,
				  dateTimeFormat,
				  localTz):
		'''
		Returns the price of 1 unit of currency in targetCurrency. Ex: currency == btc,
		targetCurrency == usd --> returned price: 1 btc == 10000 usd.
		
		:param currency:
		:param targetCurrency:
		:param exchange:
		:param year:
		:param month:
		:param day:
		:param hour:
		:param minute:
		:param dateTimeFormat:
		:param localTz:

		:seqdiag_return ResultData

		:return:
		'''
		if (day + month + year) == 0:
			# when the user specifies 0 for the date, this means current price is asked and
			# date components are set to zero !
			resultData = self.priceRequester.getCurrentPrice(currency, targetCurrency, exchange)

			if resultData.isEmpty(ResultData.RESULT_KEY_ERROR_MSG):
				# adding date time info if no error returned
				timeStamp = resultData.getValue(ResultData.RESULT_KEY_PRICE_TIME_STAMP)
				requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStamp, localTz)
				requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)
				resultData.setValue(ResultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestedDateTimeStr)
		else:
			# getting historical price, either histo day or histo minute
			timeStampLocal = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, hour, minute, 0, localTz)
			timeStampUtcNoHHMM = DateTimeUtil.dateTimeComponentsToTimeStamp(day, month, year, 0, 0, 0, 'UTC')
			resultData = self.priceRequester.getHistoricalPriceAtUTCTimeStamp(currency,
																			  targetCurrency,
																			  timeStampLocal,
																			  localTz,
																			  timeStampUtcNoHHMM,
																			  exchange)

			if resultData.isEmpty(ResultData.RESULT_KEY_ERROR_MSG):
				# adding date time info if no error returned
				if resultData.getValue(ResultData.RESULT_KEY_PRICE_TYPE) == ResultData.PRICE_TYPE_HISTO_DAY:
					# histoday price returned
					requestedPriceArrowUtcDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampUtcNoHHMM, 'UTC')
					requestedDateTimeStr = requestedPriceArrowUtcDateTime.format(dateTimeFormat)
				else:
					# histominute price returned
					requestedPriceArrowLocalDateTime = DateTimeUtil.timeStampToArrowLocalDate(timeStampLocal, localTz)
					requestedDateTimeStr = requestedPriceArrowLocalDateTime.format(dateTimeFormat)

				resultData.setValue(ResultData.RESULT_KEY_PRICE_DATE_TIME_STRING, requestedDateTimeStr)

		price = resultData.getValue(ResultData.RESULT_KEY_PRICE)

		if price == 0:
			dateDMY, dateHM = DateTimeUtil._formatPrintDateTimeFromIntComponents(day,
																				 month,
																				 year,
																				 hour,
																				 minute,
																				 localTz,
																				 dateTimeFormat)

			resultData.setValue(ResultData.RESULT_KEY_ERROR_MSG,
								'PROVIDER ERROR - Requesting {}/{} price for date {} {} on exchange {} returned invalid value 0'.format(currency, targetCurrency, dateDMY, dateHM, exchange))

		return resultData

	def _computeOptionValueAmount(self,
								  resultData,
								  crypto,
								  unit,
								  optionFiatSymbol,
								  optionValueSymbol,
								  optionValueAmount,
								  optionValueSaveFlag):
		'''
		Compute the optionValueAmount according to the passed parms and put the result in
		the passed resultData.
		:param optionValueSymbol: upper case price value symbol. If == crypto, this means that optionValueAmount provided
								 is in crypto and must be converted into unit at the rate returned by the PriceRequester.

								 If the price value symbol == unit, this means that optionValueAmount provided
								 is in unit and must be converted into crypto at the rate returned by the PriceRequester.

								 Ex 1:  crypto == BTC
										unit == USD
										optionValueSymbol == BTC
										optionValueAmount == 0.001

										if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
										converted value will be 20000 USD * 0.001 BTC => 200 USD

								 Ex 2:  crypto == BTC
										unit == USD
										optionValueSymbol == USD
										optionValueAmount == 500

										if returned rate (stored in ResultData.RESULT_KEY_PRICE entry) is 20000,
										converted value will be 1 / 20000 USD * 500 USD => 0.025 BTC

		:param optionValueAmount: float price value amount
		:param optionValueSaveFlag: used to refine warning if value command not applicable.
									The flag is set in the ResultData in CommandPrice.execute().
		:return: a ResultData in which price value info has been added.
		'''
		conversionRate = resultData.getValue(resultData.RESULT_KEY_PRICE)

		if optionValueSymbol == crypto:
			#converting optionValueAmount in crypto to equivalent value in unit
			convertedValue = optionValueAmount * conversionRate
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, optionValueAmount)
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, convertedValue)
			if optionFiatSymbol:
				fiatConvertedUnitValuePrice = convertedValue * resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE)
				resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, fiatConvertedUnitValuePrice)
		elif optionValueSymbol == unit:
			#converting optionValueAmount in unit to equivalent value in crypto
			convertedValue = optionValueAmount / conversionRate
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, convertedValue)
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, optionValueAmount)
			if optionFiatSymbol:
				fiatConvertedUnitValuePrice = optionValueAmount * resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE)
				resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, fiatConvertedUnitValuePrice)
		elif optionValueSymbol == optionFiatSymbol:
			convertedCryptoValue = optionValueAmount / resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT)
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO, convertedCryptoValue)
			convertedUnitValue = optionValueAmount / resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_RATE)
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT, convertedUnitValue)
			resultData.setValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT, optionValueAmount)
		else:
			if optionValueSaveFlag:
				valueCommand = '-vs'
			else:
				valueCommand = '-v'

			if optionFiatSymbol:
				resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE,
									  "WARNING - currency value option symbol {} currently in effect differs from crypto ({}), unit ({}) and fiat ({}) of last request. {} option ignored".format(
										  optionValueSymbol, crypto, unit, optionFiatSymbol, valueCommand))
			else:
				resultData.setWarning(ResultData.WARNING_TYPE_COMMAND_VALUE,
									  "WARNING - currency value option symbol {} currently in effect differs from both crypto ({}) and unit ({}) of last request. {} option ignored".format(
										  optionValueSymbol, crypto, unit, valueCommand))

		return resultData

	def _computeOptionFiatAmount(self,
								 resultData,
								 fiat,
								 fiatExchange,
								 crypto,
								 unit,
								 cryptoUnitExchange,
								 year,
								 month,
								 day,
								 hour,
								 minute,
								 dateTimeFormat,
								 localTz):
		"""
		Compute the optionFiatAmount according to the passed parms and put the result in
		the passed resultData.
		
		:param resultData:
		:param fiat:
		:param fiatExchange:
		:param crypto:
		:param unit:
		:param cryptoUnitExchange: used in case the -f fiat symbol equals either the crypto
								   or the unit symbol
		
		:return: a ResultData in which price value info has been added.
		"""
		if fiatExchange == None:
			if fiat == unit or \
				fiat == crypto:
				fiatExchange = cryptoUnitExchange
			else:
				fiatExchange = 'CCCAGG'

		if unit == fiat:
			fiatConversionRate = 1

			return self._calculateAndStoreFiatData(fiat, fiatConversionRate, fiatExchange, resultData)

#si fiatExchange = cryptoUnitExchange, alors _getPrice not useful !

		fiatResultData = self._getPrice(unit,
										fiat,
										fiatExchange,
										year,
										month,
										day,
										hour,
										minute,
										dateTimeFormat,
										localTz)

		if not fiatResultData.isError():
			fiatConversionRate = fiatResultData.getValue(resultData.RESULT_KEY_PRICE)

			return self._calculateAndStoreFiatData(fiat, fiatConversionRate, fiatExchange, resultData)
		else:
			# since fiat/unit is not supported by the exchange, we try to request the unit/fiat inverted rate
			fiatResultData = self._getPrice(fiat,
											unit,
											fiatExchange,
											year,
											month,
											day,
											hour,
											minute,
											dateTimeFormat,
											localTz)
			if not fiatResultData.isError():
				fiatConversionRate = 1 / fiatResultData.getValue(resultData.RESULT_KEY_PRICE)

				return self._calculateAndStoreFiatData(fiat, fiatConversionRate, fiatExchange, resultData)
			else:
				errorMsg = fiatResultData.getValue(fiatResultData.RESULT_KEY_ERROR_MSG)
				dateDMY, dateHM = DateTimeUtil._formatPrintDateTimeFromIntComponents(day,
																					 month,
																					 year,
																					 hour,
																					 minute,
																					 localTz,
																					 dateTimeFormat)
				
				if 'market does not exist for this coin pair' in errorMsg:
					errorMsg = 'PROVIDER ERROR - fiat option coin pair {}/{} or {}/{} not supported by exchange {} on date {} {}'.format(fiat, unit, unit, fiat, fiatExchange, dateDMY, dateHM)
				else:
					# making the error msg specific to the fiat option
					errorMsg = errorMsg.replace('Requesting', 'Requesting fiat option coin pair {}/{} or'.format(unit, fiat))
					errorMsg += ' on date {} {}'.format(dateDMY, dateHM)

				fiatResultData.setValue(fiatResultData.RESULT_KEY_ERROR_MSG, errorMsg)

				return fiatResultData

	def _calculateAndStoreFiatData(self, fiat, fiatConversionRate, fiatExchange, resultData):
		price = resultData.getValue(resultData.RESULT_KEY_PRICE)
		fiatConvertedPrice = price * fiatConversionRate
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_RATE, fiatConversionRate)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT, fiatConvertedPrice)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL, fiat)
		resultData.setValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE, fiatExchange)

		return resultData


if __name__ == '__main__':
	from configurationmanager import ConfigurationManager
	from pricerequester import PriceRequester
	from crypcompexchanges import CrypCompExchanges
	import os

	if os.name == 'posix':
		FILE_PATH = '/sdcard/cryptopricer.ini'
	else:
		FILE_PATH = 'c:\\temp\\cryptopricer.ini'

	cm = ConfigurationManager(FILE_PATH)
	pr = PriceRequester()
	cryp = CrypCompExchanges()
	proc = Processor(cm, pr, cryp)

	crypto = 'BTC'
	unit = 'USD'
	exchange = 'bittrex'
	day = 12
	month = 9
	year = 2017
	hour = 10
	minute = 5

	print('HISTORICAL')
	print(proc.getCryptoPrice(crypto, unit, exchange, day, month, year, hour, minute))

	print(proc.getCryptoPrice(crypto, unit, 'unknown_exchange', day, month, year, hour, minute))

	day = 0
	month = 0
	year = 0
	hour = 0
	minute = 0

	print('\nREAL TIME')
	print(proc.getCryptoPrice(crypto, unit, exchange, day, month, year, hour, minute))

	print(proc.getCryptoPrice(crypto, unit, 'unknown_exchange', day, month, year, hour, minute))
