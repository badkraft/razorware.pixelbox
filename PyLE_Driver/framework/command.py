class Command:
    def __init__(self, can_execute, execute):
        self.__can_execute = can_execute
        self.__execute = execute

    def can_execute(self, param):
        return self.__can_execute(param)

    def execute(self, param):
        self.__execute(param)
