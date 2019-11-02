class ConfigParserContext:
    def __init__(self, config_file):
        self.__config_parser = None
        self.__config_file = config_file

    def read(self):
        return self.__config_parser.parse(self.__config_file)

    def set_strategy(self, new_strategy):
        self.__config_parser = new_strategy
