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

    # symbol startowy
    @_('instructions_opt')
    def program(self, p):
        pass

    # po symbolu startowym albo instrukcje, albo nic, żeby akceptowany był pusty plik
    @_('instructions',
       '')
    def instructions_opt(self, p):
        pass

    # możliwość wielu instrukcji
    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        pass

    # wyrażenia binarne, w tym opracje macierzowe
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

    # wyrażenia relacyjne
    @_('expr LT expr',
       'expr LE expr',
       'expr GT expr',
       'expr GE expr',
       'expr EQ expr',
       'expr NE expr',)
    def condition(self, p):
        pass

    # negacja unarna
    @_('"-" expr %prec UMINUS')
    def uminus(self, p):
        pass

    # transpozycja macierzy TODO: naprawić akceptowanie czegoś takiego: B = 5';
    @_('expr "\'"') # np. A'
    def transposition(self, p):
        pass

    # konstrukcja macierzy
    @_('"[" vectors "]"') # macierz zbudowana jest z wektorów
    def matrix(self, p):
        pass

    # możliwość wielu wektorów
    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        pass
    
    # konstrukcja wektora
    @_('"[" elements "]"') # wektor zbudowany jest z elementów
    def vector(self, p):
        pass

    # możliwość wielu elementow
    @_('elements "," element',
       'element')
    def elements(self, p):
        pass
    
    # konstrukcja elementu
    @_('ID', # może być albo zmienną
       'number',) # albo liczbą
    def element(self, p):
        pass

    # konstrukcja liczby
    @_('INTNUM', # albo int
       'FLOATNUM') # albo float
    def number(self, p):
        pass

    # inicjalizacja macierzy (dla przypisania konkretnych wartości)
    @_('ID "[" INTNUM "," INTNUM "]"') # np. A[1, 3]
    def matrix_init(self, p):
        pass
    
    # inicjalizacja wektora (dla przypisania konkretnych wartości)
    @_('ID "[" INTNUM "]"') # np. A[3]
    def vector_init(self, p):
        pass

    # macierzowe funkcje specjalne
    @_('EYE "(" INTNUM ")"', # np. eye(4)
       'ONES "(" INTNUM ")"', # np. ones(4)
       'ZEROS "(" INTNUM ")"') # np. zeros(4)
    def matrix_function(self, p):
        pass

    # przypisanie
    @_('ID assign_op expr', # np. A += 3 + 2
       'matrix_init assign_op expr', # inicjalizacja macierzy konkretnymi wartościami np. A[1,3] = 0
       'vector_init assign_op expr') # inicjalizacja wektora konkretnymi wartościami np. A[3] = 0
    def assignment(self, p):
        pass
    
    # konkretne instrukcje i pętle
    @_('IF "(" condition ")" instruction %prec IFX', # instrukcja if (%prec IFX dla usunięca niejednoznaczności)
       'IF "(" condition ")" instruction ELSE instruction', # instrukcja if-else
       'WHILE "(" condition ")" instruction', # pętla while       
       'FOR ID "=" expr ":" expr instruction', # pętla for (np. for i = 1:N)
       '"{" instructions "}"', # instrukcje mogą być 'mnogie' jeżeli są w nawiasach klamrowych
       'instruction_end ";"') # instrukcje zakończone po których nie wystąpią kolejne
    def instruction(self, p):
        pass

    # instrukcje zakończone ';'
    @_('assignment', # instrukcja przypisania
       'RETURN expr',
       'BREAK',
       'CONTINUE',
       'PRINT to_print')
    def instruction_end(self, p):
        pass

    # operatory przypisania
    @_('=',
       'ADDASSIGN',
       'SUBASSIGN',
       'MULASSIGN',
       'DIVASSIGN')
    def assign_op(self,p):
        pass

    # możliwości funkcji print
    @_('STRING', # np. print "N<10"
       'expr', # np. print 1 + 2
       'expr "," to_print', # np. print 1 + 2, "N<10"
       'STRING "," to_print') # np. print "N<10", 1 + 2
    def to_print(self, p):
        pass

    # czym może być wyrażenie
    @_('ID',
       'uminus',
       'matrix',
       'transposition',
       'matrix_function',
       'number')
    def expr(self, p):
        pass