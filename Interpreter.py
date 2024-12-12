import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,

}

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    
    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return operators[node.op](r1, r2)

    @when(AST.Assignment)
    def visit(self, node):
        r1 = node.expr.accept(self)

        if isinstance(node.var, AST.Var):
            if node.op == "=":
                self.memory.insert(node.var.name, r1)
    
    @when(AST.Number)
    def visit(self, node):
        if isinstance(node.value, int):
            return int(node.value)
        else:
            return float(node.value)

    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

