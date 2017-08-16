from commandenum import CommandEnum

class Processor:
    def execute(self, commands):
        if CommandEnum.CRYPTO in commands:
            result = 'CommandEnum.CRYPTO'
            return result
