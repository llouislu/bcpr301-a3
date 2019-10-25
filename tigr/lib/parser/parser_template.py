from abc import abstractmethod, ABCMeta
from collections.abc import Iterable
from tigr.lib.interface import AbstractParser

class TemplateParser(AbstractParser):
    __metaclass__ = ABCMeta

    class ParseException(Exception):
        pass

    class SkipParseException(Exception):
        pass

    def __init__(self, drawer, optional_file_name=None):
        self.drawer = drawer
        self.source = []
        self.command = ''
        self.data = 0
        self.no_parameter_commands = {
            'D': self.drawer.pen_down,
            'U': self.drawer.pen_up
        }

        self.one_parameter_commands = {
            'P': self.drawer.select_pen,
            'X': self.drawer.go_along,
            'Y': self.drawer.go_down,
        }
        self.draw_commands = {
            'N': self.drawer.draw_line,
            'E': self.drawer.draw_line,
            'S': self.drawer.draw_line,
            'W': self.drawer.draw_line,
        }

    def parse(self, raw_source):
        if not self.check_source(raw_source):
            raise TypeError('source not iterable!')

        for line_number, line in enumerate(raw_source, 1):
            try:
                self.command, self.data = self.do_parse_line(line_number, line)
            except self.ParseException as e:
                print(e)
            except self.SkipParseException:
                continue
            else:
                # parse success
                self.draw()

    def check_source(self, raw_source):
        if isinstance(raw_source, Iterable):
            return True
        return False

    def is_float(self, string):
        try:
            float(string)
        except:
            return False
        return True

    def draw(self):
        if self.command not in self.no_parameter_commands:
            if not self.is_float(self.data):
                raise ValueError()
            self.data = float(self.data)

        if self.command in self.no_parameter_commands:
            self.no_parameter_commands[self.command]()
        elif self.command in self.one_parameter_commands:
            self.one_parameter_commands[self.command](self.data)
        elif self.command in self.draw_commands:
            self.draw_commands[self.command](
                self.command, self.data)

    @abstractmethod
    def do_parse_line(self, line_number, line):
        raise NotImplementedError()