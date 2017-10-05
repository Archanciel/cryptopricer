import arrow

class DateTimeConverter:
    @staticmethod
    def timestampToLocalDate(timestamp, timezoneStr):
        '''
        From timestamp, returns a localized arrow object
        :param timestamp: UTC/GMT timezone independent timestamp
        :param timezoneStr: like 'Europe/Zurich' or 'US/Pacific'
        :return: arrow.Arrow instance
        '''
        return arrow.Arrow.utcfromtimestamp(timestamp).to(timezoneStr)

if __name__ == '__main__':
    pass