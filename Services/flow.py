from .managed_service import ManagedService
from Services.class_utils import exposify

@exposify
class Flow(ManagedService):
    # Code("00EE")
    def Return(self):
        value = self.memory.pop_stack()
        self.memory.set_pc(value)

    # Code("1...")
    def Goto(self, n):
        self.memory.set_pc(n)

    # Code("2...")
    def Subroutine(self, n):
        value = self.memory.get_pc()
        self.memory.push_stack(value)
        self.memory.set_pc(n)

    # Code("3...")
    def SkipEqN(self, x, n): #3XNN
        value = self.memory.get_register(x)
        if n == value:
            self.memory.increment_pc()

    # Code("4...")
    def SkipNEqN(self, x, n):
        value = self.memory.get_register(x)
        if n != value:
            self.memory.increment_pc()

    # Code("5...")
    def SkipEq(self, x, y):
        value1 = self.memory.get_register(x)
        value2 = self.memory.get_register(y)
        if value1 == value2:
            self.memory.increment_pc()

    # Code("9..0")
    def SkipNEq(self, x, y):
        value1 = self.memory.get_register(x)
        value2 = self.memory.get_register(y)
        if value1 != value2:
            self.memory.increment_pc()

    # Code("B...")
    def JumpN(self, n):
        value = self.memory.get_register(0) + n
        self.memory.set_pc(value)

    # Code("E.9E")
    def KeyOpPressed(self, x):
        keys = self.memory.get_io_keys()
        if keys & x:
            self.memory.increment_pc()

    # Code("E.A1")
    def KeyOpReleased(self, x):
        keys = self.memory.get_io_keys()
        if not (keys & x):
            self.memory.increment_pc()
    
    
_default = Flow