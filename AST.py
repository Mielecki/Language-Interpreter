from dataclasses import dataclass, field
from typing import Any, List

class Node(object):
    pass

@dataclass
class BinExpr(Node):
    op: Any
    left: Any
    right: Any

@dataclass
class Condition(Node):
    op: Any
    left: Any
    right: Any

@dataclass
class Uminus(Node):
    right: Any

@dataclass
class Assignment(Node):
    op: Any
    var: Any
    expr: Any

@dataclass
class Var(Node):
    name: Any

@dataclass
class String(Node):
    string: Any

@dataclass
class If(Node):
    cond: Any
    instr: Any

@dataclass
class Ifelse(Node):
    cond: Any
    instr: Any
    instr_else: Any

@dataclass
class While(Node):
    cond: Any
    instr: Any

@dataclass
class For(Node):
    var: Any
    range: Any
    instr: Any

@dataclass
class Range(Node):
    left: Any
    right: Any

@dataclass
class Break(Node):
    pass

@dataclass
class Continue(Node):
    pass

@dataclass
class Return(Node):
    expr: Any

@dataclass
class Print(Node):
    to_print: Any

@dataclass
class Instructions(Node):
    instructions: List[Any]


@dataclass
class Transposition(Node):
    matrix: Any

@dataclass
class Matrix(Node):
    matrix: List[Any]


@dataclass
class Vector(Node):
    vector: List[Any]

            
@dataclass
class Number(Node):
    value: Any


@dataclass
class MatrixInit(Node):
    id: Any
    row_index: Any
    col_index: Any

@dataclass
class VectorInit(Node):
    id: Any
    index: Any


@dataclass
class MatrixFunction(Node):
    name: Any
    arg: Any


@dataclass
class ToPrint(Node):
   values: List[Any]


@dataclass
class Error(Node):
    pass