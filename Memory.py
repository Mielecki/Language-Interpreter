

class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.memory = {} 

    def has_key(self, name):  # variable name
        return name in self.memory

    def get(self, name):         # gets from memory current value of variable <name>
        return self.memory[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>        
        self.stack = [memory if memory is not None else Memory("global")]

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in self.stack[::-1]:
            value = memory.get(name)
            if value is not None:
                return value
        
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        self.stack[-1].put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        self.stack.pop()
