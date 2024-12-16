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
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y
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
        
    @when(AST.String)
    def visit(self, node):
        return str(node.string)
        
    @when(AST.Condition)
    def visit(self, node):
        return operators[node.op](node.left.accept(self), node.right.accept(self))

    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.instr.accept(self)
        return r

    @when(AST.Vector)
    def visit(self, node):
        vector = []
        for item in node.vector:
            vector.append(item.accept(self))
        return vector
    
    @when(AST.Matrix)
    def visit(self, node):
        matrix = []
        for item in node.matrix:
            matrix.append(item.accept(self))
        return matrix

    @when(AST.Range)
    def visit(self, node):
        return range(node.left, node.right)
    
    @when(AST.If)
    def visit(self, node):
        if node.cond.accept(self):
            return node.instr.accept(self)
        
    @when(AST.Ifelse)
    def visit(self, node):
        if node.cond.accept(self):
            return node.instr.accept(self)
        return node.instr_else.accept(self)