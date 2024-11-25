from sly import Parser
from scanner import Scanner
import AST


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    valid = True

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ("left", '+', '-'),
        ("left", "DOTADD", "DOTSUB"),
        ("left", '*', '/'),
        ("left", "DOTMUL", "DOTDIV"),
        ("right", "UMINUS"),
        ('left', "'")
    )

    def error(self, p):
        self.valid = False
        if p:
            print(f"Syntax error at line {p.lineno}")

    @_('instructions_opt')
    def program(self, p):
        return p[0]

    @_('instructions',
       '')
    def instructions_opt(self, p):
        return p[0]

    @_('instructions instruction')
    def instructions(self, p):
        return AST.Instructions(p[0].instructions + [p[1]])
    
    @_('instruction')
    def instructions(self, p):
        return AST.Instructions([p[0]])

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
        return AST.Transposition(p[0])


    @_('"[" vectors "]"') 
    def matrix(self, p):
        return p[1]


    @_('vectors "," vector')
    def vectors(self, p):
        return AST.Matrix(p[0].matrix + [p[2]])
    
    @_('vector')
    def vectors(self, p):
        return AST.Matrix([p[0]])
    
    @_('"[" elements "]"') 
    def vector(self, p):
        return p[1]


    @_('elements "," element')
    def elements(self, p):
        return AST.Vector(p[0].vector+[p[2]])
    
    @_('element')
    def elements(self, p):
        return AST.Vector([p[0]])

    @_('var',
       'number',) 
    def element(self, p):
        return p[0]


    @_('INTNUM',
       'FLOATNUM') 
    def number(self, p):
        return AST.Number(p[0])


    @_('ID "[" INTNUM "," INTNUM "]"')
    def matrix_ref(self, p):
        return AST.MatrixRef(p[0], p[2], p[4])
    
    @_('ID "[" INTNUM "]"')
    def vector_ref(self, p):
        return AST.VectorRef(p[0], p[2])

    @_('EYE "(" INTNUM ")"',
       'ONES "(" INTNUM ")"', 
       'ZEROS "(" INTNUM ")"') 
    def matrix_function(self, p):
        return AST.MatrixFunction(p[0], p[2])

    @_('var assign_op expr', 
       'matrix_ref assign_op expr',
       'vector_ref assign_op expr',) 
    def assignment(self, p):
        return AST.Assignment(p[1], p[0], p[2])
    
    @_('ID')
    def var(self, p):
        return AST.Var(p[0])
    
    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p[2], p[4])

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.Ifelse(p[2], p[4], p[6])

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p[2], p[4])
        
    @_('FOR var "=" range instruction')
    def instruction(self, p):
        return AST.For(p[1], p[3], p[4])

    @_('expr ":" expr')
    def range(self, p):
        return AST.Range(p[0], p[2])

    @_('"{" instructions "}"')
    def instruction(self, p):
        return p[1]
    
    @_('instruction_end ";"')
    def instruction(self, p):
        return p[0]

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

    @_('expr "," to_print', 
       'string "," to_print') 
    def to_print(self, p):
        return AST.ToPrint([p[0]] + p[2].values)
    
    @_('string',
       'expr')
    def to_print(self, p):
        return AST.ToPrint([p[0]])
    
    @_('STRING')
    def string(self, p):
        return AST.String(p[0])


    @_('var',
       'uminus',
       'matrix',
       'vector',
       'transposition',
       'matrix_function',
       'number')
    def expr(self, p):
        return p[0]