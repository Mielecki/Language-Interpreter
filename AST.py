from dataclasses import dataclass
from typing import Any, List, Optional

class Node(object):
    type: Optional[Any] = None
    size: Optional[Any] = None
    elem_type: Optional[Any] = None

    def accept(self, visitor):
        return visitor.visit(self)

@dataclass
class Program(Node):
    code: Any
    line: Optional[int] = 0

@dataclass
class BinExpr(Node):
    op: Any
    left: Any
    right: Any
    line: Optional[int] = 0

@dataclass
class Condition(Node):
    op: Any
    left: Any
    right: Any
    line: Optional[int] = 0

@dataclass
class Uminus(Node):
    right: Any
    line: Optional[int] = 0

@dataclass
class Assignment(Node):
    op: Any
    var: Any
    expr: Any
    line: Optional[int] = 0

@dataclass
class Var(Node):
    name: Any
    line: Optional[int] = 0

@dataclass
class String(Node):
    string: Any
    line: Optional[int] = 0

@dataclass
class If(Node):
    cond: Any
    instr: Any
    line: Optional[int] = 0

@dataclass
class Ifelse(Node):
    cond: Any
    instr: Any
    instr_else: Any
    line: Optional[int] = 0

@dataclass
class While(Node):
    cond: Any
    instr: Any
    line: Optional[int] = 0

@dataclass
class For(Node):
    var: Any
    range: Any
    instr: Any
    line: Optional[int] = 0

@dataclass
class Range(Node):
    left: Any
    right: Any
    line: Optional[int] = 0

@dataclass
class Break(Node):
    line: Optional[int] = 0

@dataclass
class Continue(Node):
    line: Optional[int] = 0

@dataclass
class Return(Node):
    expr: Any
    line: Optional[int] = 0

@dataclass
class Print(Node):
    to_print: Any
    line: Optional[int] = 0

@dataclass
class Instructions(Node):
    instructions: List[Any]
    line: Optional[int] = 0


@dataclass
class Transposition(Node):
    matrix: Any
    line: Optional[int] = 0

@dataclass
class Matrix(Node):
    matrix: List[Any]
    line: Optional[int] = 0


@dataclass
class Vector(Node):
    vector: List[Any]
    line: Optional[int] = 0

            
@dataclass
class Number(Node):
    value: Any
    line: Optional[int] = 0

@dataclass
class VectorRef(Node):
    id: Any
    index: Any
    line: Optional[int] = 0

@dataclass
class MatrixRef(Node):
    id: Any
    row_index: Any
    col_index: Any
    line: Optional[int] = 0

@dataclass
class MatrixFunction(Node):
    name: Any
    args: List[Any]
    line: Optional[int] = 0


@dataclass
class ToPrint(Node):
   values: List[Any]
   line: Optional[int] = 0


@dataclass
class Error(Node):
    pass