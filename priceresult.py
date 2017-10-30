

class PriceResult:
    RESULT_kEY_PRICE = 'PRICE'
    RESULT_KEY_PRICE_TYPE = 'PRICE TYPE'
    RESULT_kEY_PRICE_TIME_STAMP = 'PRICE TIMESTAMP'
    RESULT_kEY_ERROR_MSG = 'ERROR_MSG'

    PRICE_TYPE_HISTO_DAY = 'HISTO_DAY'
    PRICE_TYPE_CURRENT_OR_HISTO_MINUTE = 'CURRENT_OR_HISTO_MINUTE'


    def __init__(self):
        self._resultDataDic = {}


    def setValue(self, key, value):
        self._resultDataDic[key] = value


    def getValue(self, key):
        return self._resultDataDic[key]


if __name__ == '__main__':
    pass