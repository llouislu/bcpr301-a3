import re

from tigr.lib.parser.parser_template import TemplateParser


class RegexParser(TemplateParser):

    def __init__(self, drawer):
        super().__init__(drawer)
        self.line_pattern = re.compile(
            # r'^(P|X|Y|D|W|N|E|S|U)\s{0,}(-?\d{0,}\.{0,1}\d{0,})\s{0,}(?=#{0,1})')
            r'^(P|X|Y|D|W|N|E|S|U)$|^(P|X|Y|D|W|N|E|S|U)\s{1,}(-?\d{0,}\.{0,1}\d{0,})\s{0,}(?=#{0,1})')

    def do_parse_line(self, line_number, line):
        line = line.strip()
        line_uppercased = line.upper()
        if not line_uppercased:
            raise self.SkipParseException()
        if line_uppercased.startswith('#'):
            raise self.SkipParseException()
        matched = self.line_pattern.match(line_uppercased)
        if not matched:
            raise self.ParseException('you have a syntax error at Line {}: {}'.format(
                line_number, line))

        may_be_no_parameter_command, command, data = matched.groups()
        if may_be_no_parameter_command:
            command = may_be_no_parameter_command
        if command not in self.no_parameter_commands:
            if not self.is_float(data):
                raise self.ParseException('you have a syntax error at Line {}: {}'.format(
                    line_number, line))
            data = float(data)
        return command, data
