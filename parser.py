from sly import Parser
from scanner import Scanner



class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'LT', 'GT', 'GE', 'LE', 'EQ', 'NE'),
        ("left", '+', '-'),
        ("left", "DOTADD", "DOTSUB"),
        ("left", '*', '/'),
        ("left", "DOTMUL", "DOTDIV"),
        ("right", "UMINUS"),
        ('left', "'")
    )

    def error(self, p):
        if p:
            print(p)
            print(f"Syntax error at line {p.lineno}")

    @_('instructions_opt')
    def program(self, p):
        pass

    @_('instructions',
       '')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        pass


    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr',)
    def expr(self, p):
        pass


    @_('expr LT expr',
       'expr LE expr',
       'expr GT expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NE expr',)
    def condition(self, p):
        pass


    @_('"-" expr %prec UMINUS')
    def uminus(self, p):
        pass


    @_('expr "\'"')
    def transposition(self, p):
        pass


    @_('"[" vectors "]"') 
    def matrix(self, p):
        pass


    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        pass
    

    @_('"[" elements "]"') 
    def vector(self, p):
        pass


    @_('elements "," element',
       'element')
    def elements(self, p):
        pass
    

    @_('ID',
       'number',) 
    def element(self, p):
        pass


    @_('INTNUM',
       'FLOATNUM') 
    def number(self, p):
        pass


    @_('ID "[" INTNUM "," INTNUM "]"')
    def matrix_init(self, p):
        pass
    

    @_('ID "[" INTNUM "]"') 
    def vector_init(self, p):
        pass


    @_('EYE "(" INTNUM ")"',
       'ONES "(" INTNUM ")"', 
       'ZEROS "(" INTNUM ")"') 
    def matrix_function(self, p):
        pass

    @_('ID assign_op expr', 
       'matrix_init assign_op expr', 
       'vector_init assign_op expr') 
    def assignment(self, p):
        pass
    

    @_('IF "(" condition ")" instruction %prec IFX', 
       'IF "(" condition ")" instruction ELSE instruction',
       'WHILE "(" condition ")" instruction',     
       'FOR ID "=" expr ":" expr instruction',
       '"{" instructions "}"', 
       'instruction_end ";"')
    def instruction(self, p):
        pass


    @_('assignment',
       'RETURN expr',
       'BREAK',
       'CONTINUE',
       'PRINT to_print')
    def instruction_end(self, p):
        pass


    @_('=',
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign_op(self,p):
        pass

    @_('STRING',
       'expr',
       'expr "," to_print', 
       'STRING "," to_print') 
    def to_print(self, p):
        pass


    @_('ID',
       'uminus',
       'matrix',
       'transposition',
       'matrix_function',
       'number')
    def expr(self, p):
        pass