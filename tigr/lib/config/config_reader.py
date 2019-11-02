from pathlib import Path

from .config_exception import ConfigException
from .ini_parser import IniPaser
from .strategic_config_context import ConfigParserContext
from .yaml_parser import YamlParser


class Config:
    def __init__(self, file):
        self.file = file
        self.strategic_config_context = ConfigParserContext(file)

    def read_config(self):
        f = Path(self.file)
        if not f.is_file():
            raise ConfigException('The config file does not exist')

        if f.suffix == '.ini':
            self.strategic_config_context.set_strategy(IniPaser())
        elif f.suffix in ['.yaml', '.yml']:
            self.strategic_config_context.set_strategy(YamlParser())
        else:
            raise ConfigException(
                'The format of file should be * .ini, *.yaml or *.yml')

        return self.strategic_config_context.read()
