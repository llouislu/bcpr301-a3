from abc import ABC, abstractmethod


class AbstractConfigParser(ABC):
    @abstractmethod
    def parse(self, config_file):
        pass
