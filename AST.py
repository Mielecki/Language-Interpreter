from dataclasses import dataclass

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
    id: Any
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