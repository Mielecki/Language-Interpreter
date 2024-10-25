import sys
from sly import Lexer


class Scanner(Lexer):
    tokens = {DOTADD, DOTSUB, DOTMUL, DOTDIV, 
              ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
              LT, LE, GT, GE, NE, EQ,
              ID,
              IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, PRINT, EYE, ZEROS, ONES,
              INTNUM, FLOATNUM,
              STRING
              }
    
    literals = {'+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', "'", ',', ';'}

    ignore = ' \t'

    ignore_comment = r'\#.*'

    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    EQ = r'=='
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['print'] = PRINT
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    
    @_(r'(\d+\.\d*|\.\d+)([eE][-]?\d+)?')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'".*"')
    def STRING(self, t):
        t.value = str(t.value[1:-1])
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)


    def error(self, t):
        raise Exception(f"({t.lineno}): Illegal character '{t.value[0]}'")

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(f'({tok.lineno}): {tok.type}({tok.value})')