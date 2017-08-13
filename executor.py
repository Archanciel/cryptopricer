from command import Command

class Executor:
    def execute(self, commands):
        if Command.CRYPTO in commands:
            result = 'Command.CRYPTO'
            return result
