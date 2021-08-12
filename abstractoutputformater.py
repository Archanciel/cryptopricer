from abc import ABCMeta
from abc import abstractmethod


class AbstractOutputFormater(metaclass=ABCMeta):
	'''
	'''
	PRICE_FLOAT_ROUNDING = 8
	VALUE_FLOAT_ROUNDING = 8
	PRICE_FLOAT_FORMAT = '%.{}f'.format(PRICE_FLOAT_ROUNDING) # format of crypto, unit or fiat prices returned by provider
	VALUE_FLOAT_FORMAT = '%.{}f'.format(VALUE_FLOAT_ROUNDING) # format of -v value option computed values

	def __init__(self, receiver=None, name='', rawParmData='', parsedParmData={}):
		pass

	@abstractmethod
	def printDataToConsole(self, resultData):
		'''
		Output formated data in the console
		:return: nothing
		'''
		pass

	def getCommandOutputResult(self, resultData):
		errorMsg = resultData.getErrorMessage()

		if errorMsg == None:
			price = resultData.getValue(resultData.RESULT_KEY_PRICE)
			formattedPriceStr = self._formatPriceFloatToStr(price, self.PRICE_FLOAT_FORMAT)
			dateTimeStr = resultData.getValue(resultData.RESULT_KEY_PRICE_DATE_TIME_STRING)
			priceType = resultData.getValue(resultData.RESULT_KEY_PRICE_TYPE)

			if priceType == resultData.PRICE_TYPE_HISTO_DAY:
				dateTimeStr += 'C'  # adding close symbol
			elif priceType == resultData.PRICE_TYPE_HISTO_MINUTE:
				dateTimeStr += 'M'  # adding histo MINUTE symbol
			elif priceType == resultData.PRICE_TYPE_EFFECTIVE:
				dateTimeStr += 'P'  # adding effective price symbol
			else:
				dateTimeStr += 'R'  # adding RT symbol

			cryptoUnitPart = self._formatCryptoUnitPart(resultData)
			fiatComputedAmount = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_COMPUTED_AMOUNT)
			cryptoExchange = self._convertCCCAGGExchangeName(resultData.getValue(resultData.RESULT_KEY_EXCHANGE))
			
			if fiatComputedAmount != None:
				formattedFiatComputedAmountStr = self._formatPriceFloatToStr(fiatComputedAmount, self.PRICE_FLOAT_FORMAT)
				outputStr = cryptoUnitPart + ' on {}: {} {} {}'.format(
					cryptoExchange,
					dateTimeStr,
					formattedPriceStr,
					formattedFiatComputedAmountStr)
			else:
				outputStr = cryptoUnitPart + ' on {}: {} {}'.format(
					cryptoExchange,
					dateTimeStr,
					formattedPriceStr)
		else:
			outputStr = '{}'.format(errorMsg)

		if resultData.containsWarnings():
			outputStr = outputStr + '\n' + '\n'.join(resultData.getAllWarningMessages())

		return outputStr

	def _formatCryptoUnitPart(self, resultData):
		if resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO) is None:
			if resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL) is None:
				return '{}/{}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
									  resultData.getValue(resultData.RESULT_KEY_UNIT))
			else:
				cryptoUnitExchange = resultData.getValue(resultData.RESULT_KEY_EXCHANGE)
				fiatOptionExchange = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE)
				
				if fiatOptionExchange == cryptoUnitExchange:
					# the case if the -f fiat symbol equals either the crypto or the unit symbol
					return '{}/{}/{}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
												resultData.getValue(resultData.RESULT_KEY_UNIT),
												resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
				else:
					convertedFiatExchange = self._convertCCCAGGExchangeName(exchangeName=fiatOptionExchange)
					
					return '{}/{}/{}.{}'.format(resultData.getValue(resultData.RESULT_KEY_CRYPTO),
												resultData.getValue(resultData.RESULT_KEY_UNIT),
												resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL),
												convertedFiatExchange)
		else:
			formattedPriceCryptoStr = self._formatPriceFloatToStr(
				float(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_CRYPTO)), self.PRICE_FLOAT_FORMAT)
			formattedPriceUnitStr = self._formatPriceFloatToStr(
				float(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_UNIT)), self.PRICE_FLOAT_FORMAT)
			
			if resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL) is None:
				return '{} {}/{} {}'.format(formattedPriceCryptoStr,
											resultData.getValue(resultData.RESULT_KEY_CRYPTO),
											formattedPriceUnitStr,
											resultData.getValue(resultData.RESULT_KEY_UNIT))
			else:
				formattedPriceFiatStr = self._formatPriceFloatToStr(
					float(resultData.getValue(resultData.RESULT_KEY_OPTION_VALUE_FIAT)), self.PRICE_FLOAT_FORMAT)
				cryptoUnitExchange = resultData.getValue(resultData.RESULT_KEY_EXCHANGE)
				fiatOptionExchange = resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_EXCHANGE)

				if fiatOptionExchange == cryptoUnitExchange:
					# the case if the -f fiat symbol equals either the crypto or the unit symbol
					return '{} {}/{} {}/{} {}'.format(formattedPriceCryptoStr,
														 resultData.getValue(resultData.RESULT_KEY_CRYPTO),
														 formattedPriceUnitStr,
														 resultData.getValue(resultData.RESULT_KEY_UNIT),
														 formattedPriceFiatStr,
														 resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL))
				else:
					convertedFiatExchange = self._convertCCCAGGExchangeName(exchangeName=fiatOptionExchange)
	
					return '{} {}/{} {}/{} {}.{}'.format(formattedPriceCryptoStr,
														 resultData.getValue(resultData.RESULT_KEY_CRYPTO),
														 formattedPriceUnitStr,
														 resultData.getValue(resultData.RESULT_KEY_UNIT),
														 formattedPriceFiatStr,
														 resultData.getValue(resultData.RESULT_KEY_OPTION_FIAT_SYMBOL),
														 convertedFiatExchange)
	
	def _convertCCCAGGExchangeName(self, exchangeName):
		if exchangeName == 'CCCAGG':
			exchangeName = 'AVG'
			
		return exchangeName
	
	def _formatPriceFloatToStr(self, floatNb, floatFormat):
		'''
		Format prices returned by crypto price provider.

		:param floatFormat:
		:param floatNb:
		:return:
		'''
		try:
			floatNbFormatted = floatFormat % floatNb
		except TypeError:
			return ''

		floatNbFormattedStripZero = floatNbFormatted.rstrip('0')
		return floatNbFormattedStripZero.rstrip('.')
