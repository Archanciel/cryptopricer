

class PriceResult:
    RESULT_kEY_PRICE = 'PRICE'
    RESULT_kEY_PRICE_TYPE = 'PRICE TYPE'
    RESULT_kEY_PRICE_TIME_STAMP = 'PRICE TIMESTAMP'
    RESULT_kEY_ERROR_MSG = 'ERROR_MSG'

    def __init__(self):
        self._resultDataDic = {}


    def setValue(self, key, value):
        self._resultDataDic[key] = value


    def getValue(self, key):
        return self._resultDataDic[key]


if __name__ == '__main__':
    pass