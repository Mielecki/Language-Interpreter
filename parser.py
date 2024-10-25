from sly import Parser
from scanner import Scanner



class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
    # to fill ...
        ("left", '+', '-'),
    # to fill ...
    )


    @_('expr "+" expr')
    def expr(self, p):
        return p[0] + p[2]
    
    @_('expr "-" expr')
    def expr(self, p):
        return p[0] + p[2]
    
    @_('expr "*" expr')
    def expr(self, p):
        return p[0] + p[2]

    @_('expr "/" expr')
    def expr(self, p):
        return p[0] + p[2]

    # tylko do testów
    @_('INTNUM')
    def expr(self, p):
        pass
    
