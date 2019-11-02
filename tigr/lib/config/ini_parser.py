import configparser
from .abstract_config_parser import AbstractConfigParser
from .config_exception import ConfigException

class IniPaser(AbstractConfigParser):

    def parse(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        if 'default' not in config.sections():
            raise ConfigException('ini config file does not have a default section')
        result = {}
        for k,v in config['default'].items():
            result[k] = v
        return result
