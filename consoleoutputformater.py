from abstractoutputformater import AbstractOutputFormater


class ConsoleOutputFormater(AbstractOutputFormater):
	PRICE_FLOAT_FORMAT = '%.8f'

	def printDataToConsole(self, resultData):
		'''
		print the result to the console and
		paste it to the clipboard
		'''
		outputStr = super(ConsoleOutputFormater, self).getPrintableData(resultData)

		print(outputStr)


if __name__ == '__main__':
	pr = ConsoleOutputFormater()
	y = round(5.59, 1)
	y = 0.999999999
	y = 0.9084
	y = 40
	yFormatted = '%.8f' % y
	print()
	print('No formatting:                 ' + str(y))
	print('With formatting:               ' + yFormatted)
	print('With formatting no trailing 0: ' + pr._formatPriceFloatToStr(y))
	print()
