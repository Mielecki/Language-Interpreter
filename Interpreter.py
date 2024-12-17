import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

# not all possible combinations were considered (e.g., matrix .+ vector, matrix .+ int)
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
    '!=': lambda x, y: x != y,
    '.+': lambda x, y: [[x[i][j] + y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    '.-': lambda x, y: [[x[i][j] - y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    '.*': lambda x, y: [[x[i][j] * y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    './': lambda x, y: [[x[i][j] / y[i][j] for j in range(len(x[0]))] for i in range(len(x))],
    "zeros": lambda x, y: [[0 for _ in range(y)] for _ in range(x)],
    "ones": lambda x, y: [[1 for _ in range(y)] for _ in range(x)],
    "eye": lambda x, y: [[0 if i != j else 1 for j in range(y)] for i in range(x)],
    "'": lambda x: [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
}

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass
    
    @when(AST.Program)
    def visit(self, node):
        try:
            node.code.accept(self)
        except ReturnValueException as e:
            print(e.value)
    
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
            else:
                r2 = node.var.accept(self)
                op = node.op[0]
                self.memory.set(node.var.name, operators[op](r2, r1))
        elif isinstance(node.var, AST.MatrixRef):
            matrix = node.var.id.accept(self)
            row = node.var.row_index.accept(self)
            col = node.var.col_index.accept(self)
            for i in row[:-1] if isinstance(node.var.row_index, AST.Range) else range(row):
                for j in col[:-1] if isinstance(node.var.row_index, AST.Range) else range(col):
                    matrix[i][j] = r1
            self.memory.set(node.var.id.name, matrix)
        elif isinstance(node.var, AST.VectorRef):
            vector = node.var.id.accept(self)
            index = node.var.index.accept(self)
            for i in index[:-1] if isinstance(node.var.index, AST.Range) else range(index):
                    index[i] = r1
            vector[index] = r1
            self.memory.set(node.var.id.name, vector)

    
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
        self.memory.push(Memory("while"))
        while node.cond.accept(self):
            try:
                node.instr.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory.pop()

    @when(AST.For)
    def visit(self, node):
        r = node.range.accept(self)
        self.memory.push(Memory("for"))

        i = node.var.name
        self.memory.insert(i, r[0])
        
        while self.memory.get(i) in r:
            try:
                node.instr.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
            finally:
                self.memory.set(i, self.memory.get(i) + 1)
        self.memory.pop()

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
        return range(node.left.accept(self), node.right.accept(self) + 1)

    @when(AST.If)
    def visit(self, node):
        if node.cond.accept(self):
            return node.instr.accept(self)
        
    @when(AST.Ifelse)
    def visit(self, node):
        if node.cond.accept(self):
            return node.instr.accept(self)
        return node.instr_else.accept(self)
    
    @when(AST.Var)
    def visit(self, node):
        return self.memory.get(node.name)
    
    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.expr.accept(self))
    
    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.Break)
    def visit(self, node):
        raise BreakException()
    
    @when(AST.Print)
    def visit(self, node):
        node.to_print.accept(self)

    @when(AST.ToPrint)
    def visit(self, node):
        for value in node.values:
            print(value.accept(self))

    @when(AST.MatrixFunction)
    def visit(self, node):
        args = node.args
        if len(args) == 1:
            arg = args[0].accept(self)
            x, y = arg, arg
        else:
            x, y = args[0].accept(self), args[1].accept(self)
        return operators[node.name](x, y)
    
    @when(AST.Transposition)
    def visit(self, node):
        return operators["'"](node.matrix.accept(self))
    
    @when(AST.MatrixRef)
    def visit(self, node):
        var = node.id.name
        row = node.row_index.accept(self)
        col = node.col_index.accept(self)
        if isinstance(node.row_index, AST.Number):
            start_row = row
            end_row = start_row + 1
        else:
            start_row = row[0]
            end_row = row[-1]
        if isinstance(node.col_index, AST.Number):
            start_col = col
            end_col = start_col + 1
        else:
            start_col = col[0]
            end_col = col[-1]

        matrix = self.memory.get(var)
        new_matrix = [[matrix[start_row + i][start_col + j] for j in range(end_col-start_col)] for i in range(end_row-start_row)]
        
        return new_matrix
    
    @when(AST.VectorRef)
    def visit(self, node):
        var = node.id.name
        index = node.index.accept(self)
        if isinstance(node.index, AST.Number):
            start_index = index
            end_index = index + 1
        else:
            start_index = index[0]
            end_index = index[-1]

        vector = self.memory.get(var)
        new_vector = [vector[start_index + i] for i in range(end_index - start_index)]

        return new_vector
    
    @when(AST.Uminus)
    def visit(self, node):
        return -node.right.accept(self)