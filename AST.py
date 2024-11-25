from dataclasses import dataclass
from typing import Any, List

class Node(object):
    def __init__(self):
        self.type = None
        self.size = None

@dataclass
class BinExpr(Node):
    op: Any
    left: Any
    right: Any

    def __post_init__(self):
        super().__init__()

@dataclass
class Condition(Node):
    op: Any
    left: Any
    right: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Uminus(Node):
    right: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Assignment(Node):
    op: Any
    var: Any
    expr: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Var(Node):
    name: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class String(Node):
    string: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class If(Node):
    cond: Any
    instr: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Ifelse(Node):
    cond: Any
    instr: Any
    instr_else: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class While(Node):
    cond: Any
    instr: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class For(Node):
    var: Any
    range: Any
    instr: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Range(Node):
    left: Any
    right: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Break(Node):
    def __post_init__(self):
        super().__init__()

@dataclass
class Continue(Node):
    def __post_init__(self):
        super().__init__()

@dataclass
class Return(Node):
    expr: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Print(Node):
    to_print: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Instructions(Node):
    instructions: List[Any]
    def __post_init__(self):
        super().__init__()


@dataclass
class Transposition(Node):
    matrix: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class Matrix(Node):
    matrix: List[Any]
    def __post_init__(self):
        super().__init__()


@dataclass
class Vector(Node):
    vector: List[Any]
    def __post_init__(self):
        super().__init__()

            
@dataclass
class Number(Node):
    value: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class VectorRef(Node):
    id: Any
    index: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class MatrixRef(Node):
    id: Any
    row_index: Any
    col_index: Any
    def __post_init__(self):
        super().__init__()

@dataclass
class MatrixFunction(Node):
    name: Any
    arg: Any
    def __post_init__(self):
        super().__init__()


@dataclass
class ToPrint(Node):
   values: List[Any]
   def __post_init__(self):
        super().__init__()


@dataclass
class Error(Node):
    pass