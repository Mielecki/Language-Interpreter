class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class VariableSymbol(Symbol):
    def __init__(self, name, type, size, elem_type):
        super().__init__(name, str(type))
        self.size = size
        self.elem_type = elem_type
    
    def __repr__(self):
        return str(self.type)

class SymbolTable(object):
    loop_counter = 0

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        elif self.parent:
            return self.parent.get(name)

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        if name == "loop":
            SymbolTable.loop_counter += 1
        
        return SymbolTable(self, name)

    def popScope(self):
        if self.name == "loop":
            SymbolTable.loop_counter -= 1
        return self.parent
    
    def checkLoop(self):
        return SymbolTable.loop_counter > 0

