from sly import Parser
from scanner import Scanner
import AST


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
            print(f"Syntax error at line {p.lineno}")

    @_('instructions_opt')
    def program(self, p):
        return p[0]

    @_('instructions',
       '')
    def instructions_opt(self, p):
        return p[0]

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
        return AST.BinExpr(p[1], p[0], p[2])


    @_('expr LT expr',
       'expr LE expr',
       'expr GT expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NE expr',)
    def condition(self, p):
        return AST.Condition(p[1], p[0], p[2])


    @_('"-" expr %prec UMINUS')
    def uminus(self, p):
        return AST.Uminus(p[1])


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
        return AST.Assignment(p[1], p[0], p[2])
    
    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p[2], p[4])

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.Ifelse(p[2], [4], p[6])

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p[2], [4])
        
    @_('FOR ID "=" range instruction')
    def instruction(self, p):
        return AST.For(p[1], p[3], p[4])

    @_('expr ":" expr')
    def range(self, p):
        return AST.Range(p[0], p[2])

    @_('"{" instructions "}"', 
       'instruction_end ";"')
    def instruction(self, p):
        pass

    @_('BREAK')
    def instruction_end(self, p):
        return AST.Break()
    
    @_('CONTINUE')
    def instruction_end(self, p):
        return AST.Continue()

    @_('RETURN expr')
    def instruction_end(self, p):
        return AST.Return(p[1])

    @_('PRINT to_print')
    def instruction_end(self, p):
        return AST.Print(p[1])

    @_('assignment')
    def instruction_end(self, p):
        return p[0]


    @_('=',
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign_op(self,p):
        return p[0]

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