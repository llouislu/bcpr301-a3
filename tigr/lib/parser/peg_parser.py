from parsimonious import Grammar
from parsimonious.nodes import NodeVisitor
from tigr.lib.parser.parser_template import TemplateParser


class PegParser(TemplateParser):

    class TigrVisitor(NodeVisitor):
        def visit_line(self, node, visited_children):
            """ Makes a dict of the section (as key) and the key/value pairs. """
            s, *_ = visited_children
            return s

        def visit_statement(self, node, visited_children):
            directive, _, parameter = visited_children
            if parameter:
                return directive.text, parameter[0].text
            else:
                return directive.text, ''

        def generic_visit(self, node, visited_children):
            """ The generic visit method. """
            return visited_children or node

    def __init__(self, drawer):
        super().__init__(drawer)
        self.peg_grammar = Grammar(r'''
            line = statement ws? comment? ws
            statement   = directive ws? parameter?
            directive   = ~"P|X|Y|D|W|N|E|S|U"
            parameter   = ~"-?\d{0,}\.{0,1}\d{0,}"
            comment     = ~"#.*"
            ws          = ~"\s*"
        ''')
        self.peg_visitor = self.TigrVisitor()

    def do_parse_line(self, line_number, line):
        line_uppercased = line.upper()
        if not line_uppercased:
            # skip empty line
            raise self.SkipParseException()
        if line_uppercased.startswith('#'):
            # skip comment line
            raise self.SkipParseException()
        try:
            ast = self.peg_grammar.parse(line_uppercased)
            command, data = self.peg_visitor.visit(ast)
        except Exception:
            raise self.ParseException('you have a syntax error at Line {}: {}'.format(
                line_number, line))
        else:
            return command, data
