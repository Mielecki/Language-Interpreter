import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:
    @classmethod
    def indent(self, length):
        return ''.join('|  ' * length)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.code.printTree(indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Uminus)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "UMINUS")
        self.right.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.op)
        self.var.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Var)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.name)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.string)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "IF")
        self.cond.printTree(indent + 1)
        print(TreePrinter.indent(indent) + "THEN")
        self.instr.printTree(indent + 1)

    @addToClass(AST.Ifelse)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "IF")
        self.cond.printTree(indent + 1)
        print(TreePrinter.indent(indent) + "THEN")
        self.instr.printTree(indent + 1)
        print(TreePrinter.indent(indent) + "ELSE")
        self.instr_else.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "WHILE")
        self.cond.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "FOR")
        self.var.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "RANGE")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "CONTINUE")

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "PRINT")
        self.to_print.printTree(indent + 1)
    
    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instr in self.instructions:
            instr.printTree(indent)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "TRANSPOSE")
        self.matrix.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "VECTOR")
        for vector in self.matrix:
            vector.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "VECTOR")
        for elem in self.vector:
            elem.printTree(indent + 1)

    @addToClass(AST.Number)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + str(self.value))

    @addToClass(AST.MatrixRef)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "REF")
        self.id.printTree(indent + 1)
        self.row_index.printTree(indent + 1)
        self.col_index.printTree(indent + 1)

    @addToClass(AST.VectorRef)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "REF")
        self.id.printTree(indent + 1)
        self.index.printTree(indent + 1)

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.name)
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.ToPrint)
    def printTree(self, indent=0):
        for val in self.values:
            val.printTree(indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + "RETURN")
        self.expr.printTree(indent + 1)