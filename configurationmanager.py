class ConfigurationManager:
    def __init__(self):
        self._localTimeZone = 'Europe/Zurich'

    @property
    def localTimeZone(self):
        return self._localTimeZone

if __name__ == '__main__':
    pass