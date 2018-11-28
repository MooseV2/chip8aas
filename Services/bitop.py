from .managed_service import ManagedService
from Services.class_utils import exposify

@exposify
class BitOp(ManagedService):

    # Code("8..1")
    def BitOpOr(self, x, y):
        value = self.memory.get_register(x) | self.memory.get_register(y)
        self.memory.set_register(x, value)
    
    
    # Code("8..2")
    def BitOpAnd(self, x, y):
        value = self.memory.get_register(x) & self.memory.get_register(y)
        self.memory.set_register(x, value)
    
    
    # Code("8..3")
    def BitOpXor(self, x, y):
        value = self.memory.get_register(x) ^ self.memory.get_register(y)
        self.memory.set_register(x, value)
    
    # Code("8..6")
    def BitOpSHR(self, x, y):
        # TODO: Spec may be faulty?
        value = self.memory.get_register(x)
        lsb = value & 1
        value = value >> 1
        self.memory.set_register(0xF, lsb)
        self.memory.set_register(x, value)

    # Code("8..E")
    def BitOpSHL(self, x, y):
        # TODO: Spec may be faulty?
        value = self.memory.get_register(x)
        msb = value & (0b10000000)
        value = (value << 1) & (0xFF)
        self.memory.set_register(0xF, msb)
        self.memory.set_register(x, value)
    
    
_default = BitOp