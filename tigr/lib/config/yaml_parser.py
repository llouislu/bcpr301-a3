import yaml
from .abstract_config_parser import AbstractConfigParser


class YamlParser(AbstractConfigParser):

    def parse(self, config_file):
        with open(config_file) as f:
            return yaml.safe_load(f)
