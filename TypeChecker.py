import AST
from collections import defaultdict
from SymbolTable import *

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['<', '>', '>=', '<=', '==', '!=']:
    ttype[op]['int']['int'] = 'boolean'
    ttype[op]['float']['float'] = 'boolean'
    ttype[op]['int']['float'] = 'boolean'
    ttype[op]['float']['int'] = 'boolean'

for op in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    ttype[op]['int']['int'] = 'int'
    ttype[op]['float']['float'] = 'float'
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['matrix']['matrix'] = 'matrix'
    ttype[op]['vector']['vector'] = 'vector'

for op in ['.+', '.-', '.*', './']:
    ttype[op]['matrix']['matrix'] = 'matrix'
    ttype[op]['matrix']['int'] = 'matrix'
    ttype[op]['matrix']['float'] = 'matrix'
    ttype[op]['vector']['vector'] = 'vector'
    ttype[op]['vector']['int'] = 'vector' 
    ttype[op]['vector']['float'] = 'vector'
    ttype[op]['matrix']['vector'] = 'matrix'

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "program")
    
    def new_error(self, msg, line):
        print(f"[{line}]: {msg}")

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Assignment(self, node):
        self.visit(node.expr)
        self.visit(node.var)
        op = node.op

        if isinstance(node.var, AST.MatrixRef) or isinstance(node.var, AST.VectorRef):
            if node.expr.type not in ("int", "float"):
                self.new_error(f"Reference error: wrong type ({node.expr.type})", node.line)
                return
            return

        if op == '=':
            if node.expr.type in ("matrix", "vector"):
                self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, node.expr.type, node.expr.size, node.expr.elem_type))
                return
            if isinstance(node.expr, AST.MatrixRef) or isinstance(node.expr, AST.VectorRef):
                self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, node.expr.type, None, None))
                return
            self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, node.expr.type, None, None))
            return 
        else:
            if node.var.type is None:
                self.new_error(f"Compound assignment error: {node.var.name} is not initalized", node.line)
                return
            type_res = ttype[op][node.var.type][node.expr.type]
            if type_res == None:
                self.new_error(f"Compound assignment error: Cannot assign {node.expr.type} type to {node.var.type} type", node.line)
                return
            
            self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, type_res, None, None))

            return

    def visit_Var(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is not None:
            node.type = symbol.type
            node.size = symbol.size
            node.elem_type = symbol.elem_type
        return


    def visit_Number(self, node):
        if isinstance(node.value, int):
            node.type = "int"
        else:
            node.type = "float"
    
    def visit_Matrix(self, node):
        self.visit(node.matrix)

        first_len = node.matrix[0].size
        first_elem_type = node.matrix[0].elem_type
        if not all([vector.size == first_len for vector in node.matrix]):
            self.new_error("Matrix error: All vectors must have the same size", node.line)
            return

        if not all([vector.elem_type == first_elem_type for vector in node.matrix]):
            self.new_error("Matrix error: All vectors must have the same element type", node.line)
            return

        node.type = "matrix"
        node.size = (len(node.matrix), first_len[1])
        node.elem_type = first_elem_type
        return
        
    def visit_Vector(self, node):
        self.visit(node.vector)
        if node.vector[0].type not in ("int", "float"):
            self.new_error(f"Vector error: Wrong element type ({node.vector[0].type})", node.line)
            return

        if not all([element.type == node.vector[0].type for element in node.vector]):
            self.new_error(f"Vector error: All elements must have the same type ({node.vector[0].type})", node.line)
            return

        node.type = "vector"
        node.size = (1, len(node.vector))
        node.elem_type = node.vector[0].type
        return

    def visit_BinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)   
        op = node.op
        type = ttype[op][node.left.type][node.right.type]
        if type is None:
            self.new_error(f"BinExpr error: Cannot perform '{op}' operation between {node.left.type} type and {node.right.type} type", node.line)
            return 
        
        if type in ("matrix", "vector"):
            if node.left.type == node.right.type and node.left.size != node.right.size:
                self.new_error(f"BinExpr error: Unmatching {type} sizes ({node.left.size}, {node.right.size})", node.line)
                return
            elif node.left.type in ("matrix", "vector") and node.right.type in ("matrix", "vector") and node.left.size[1] != node.right.size[1]:
                self.new_error(f"BinExpr error: Unmatching {type} sizes ({node.left.size}, {node.right.size})", node.line)
                return

        node.type = type
        node.size = node.left.size
        return

    def visit_For(self, node):
        self.visit(node.var)
        self.visit(node.range)
        self.symbol_table = self.symbol_table.pushScope("loop")
        self.symbol_table.put(node.var.name, VariableSymbol(node.var.name, "int", None, None))
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Range(self, node):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.type != "int" or node.right.type != "int":
            self.new_error(f"Range error: Wrong range types ({node.left.type}, {node.right.type})", node.line)

    def visit_Print(self, node):
        self.visit(node.to_print)

    def visit_ToPrint(self, node):
        self.visit(node.values)
        for val in node.values:
            if val.type == None:
                self.new_error("Print error: Cannot print an uninitialized variable", node.line)
                return

    def visit_While(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope("loop")
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op = node.op

        type = ttype[op][node.left.type][node.right.type]
        
        if type is None or type != "boolean":
            self.new_error(f"Condition error: Cannnot perform '{op}' comparison between {node.left.type} type and {node.right.type} type", node.line)
            return
        
    def visit_Ifelse(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

        self.symbol_table = self.symbol_table.pushScope("else")
        self.visit(node.instr_else)
        self.symbol_table = self.symbol_table.popScope()
    
    def visit_If(self, node):
        self.visit(node.cond)
        self.symbol_table = self.symbol_table.pushScope("if")
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Transposition(self, node):
        self.visit(node.matrix)

        if node.matrix.type not in ("matrix", "vector"):
            self.new_error(f"Transpositon error: {node.matrix.type} cannot be transposed", node.line)
            return
        
        node.type = "matrix"
        node.size = (node.matrix.size[1], node.matrix.size[0])

    def visit_MatrixFunction(self, node):
        self.visit(node.args)

        if len(node.args) == 2:
            if node.args[0].type != "int" or node.args[1].type != "int":
                self.new_error(f"{node.name} error: Argument must be of type int", node.line)
                return

            node.type = "matrix"
            node.size = (int(node.args[0].value), int(node.args[1].value))
            node.elem_type = "int"
        else:
            if node.args[0].type != "int":
                self.new_error(f"{node.name} error: Argument must be of type int", node.line)
                return

            node.type = "matrix"
            node.size = (int(node.args[0].value), int(node.args[0].value))
            node.elem_type = "int"

    def visit_MatrixRef(self, node):
        self.visit(node.row_index)
        self.visit(node.col_index)
        self.visit(node.id)

        if node.id.type != "matrix":
            self.new_error(f"Reference error: cannot refer to an uninitialized matrix", node.line)
            return
            

        if isinstance(node.row_index, AST.Range):
            if node.row_index.left.value < 0:
                self.new_error("Matrix error: index out of range", node.line)
                return
            
            if node.row_index.right.value > node.id.size[0]:
                self.new_error("Matrix error: index out of range", node.line)
                return
        else:
            if node.row_index.type != "int":
                self.new_error("Matrix error: index must be of type int", node.line)
                return

            if node.row_index.value < 0 or node.row_index.value + 1 > node.id.size[0]:
                self.new_error("Matrix error: index out of range", node.line)
                return
            
        if isinstance(node.col_index, AST.Range):
            if node.col_index.left.value < 0:
                self.new_error("Matrix error: index out of range", node.line)
                return
            
            if node.col_index.right.value > node.id.size[1]:
                self.new_error("Matrix error: index out of range", node.line)
                return
        else:
            if node.col_index.type != "int":
                self.new_error("Matrix error: index must be of type int", node.line)
                return

            if node.col_index.value < 0 or node.col_index.value > node.id.size[1]:
                self.new_error("Matrix error: index out of range", node.line)
                return
            
        node.type = node.id.elem_type
            
    def visit_VectorRef(self, node):
        self.visit(node.index)
        self.visit(node.id)

        if node.id.type != "vector":
            self.new_error(f"Reference error: cannot refer to an uninitialized vector", node.line)
            return

        if isinstance(node.index, AST.Range):
            if node.index.left.value < 0:
                self.new_error("Vector error: index out of range", node.line)
                return
            
            if node.index.right.value > node.id.size[1]:
                self.new_error("Vector error: index out of range", node.line)
                return
        else:
            if node.index.type != "int":
                self.new_error("Vector error: index must be of type int", node.line)
                return

            if node.index.value < 0 or node.index.value > node.id.size[1]:
                self.new_error("Vector error: index out of range", node.line)
                return
        
        node.type = node.id.elem_type
            
    def visit_Break(self, node):
        if not self.symbol_table.checkLoop():
            self.new_error("Break error: break statement must be in a loop", node.line)
            return
    
    def visit_Continue(self, node):
        if not self.symbol_table.checkLoop():
            self.new_error("Continue error: continue statement must be in a loop", node.line)
            return
        
    def visit_Return(self, node):
        self.visit(node.expr)
        if node.expr.type == None:
            self.new_error("Return error: Cannot return an uninitialized variable", node.line)
            return
        
    def visit_Uminus(self, node):
        self.visit(node.right)
        if node.right.type not in ('int', 'float'):
            self.new_error(f"Uminus error: wrong type {node.right.type}", node.line)
            return
        
        node.type = node.right.type

    def visit_String(self, node):
        node.type = "String"