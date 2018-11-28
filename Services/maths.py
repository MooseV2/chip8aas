from .managed_service import ManagedService
from Services.class_utils import exposify
from random import randint

@exposify
class Maths(ManagedService):
    # Code("6...")
    def SetN(self, x, n):
        self.memory.set_register(x, n)

    # Code("7..0")
    def AddN(self, x, n):
        value = self.memory.get_register(x) + n
        self.memory.set_register(x, value)

    # Code("8..0")
    def Set(self, x, y):
        value = self.memory.get_register(y)
        self.memory.set_register(x, value)

    # Code("8..4")
    def MathAdd(self, x, y):
        value = self.memory.get_register(x) + self.memory.get_register(y)
        if value > 255:
            value -= 256
            self.memory.set_register(0xF, 1)
        else:
            self.memory.set_register(0xF, 0)
        self.memory.set_register(x, value)


    # Code("8..5")
    def MathSub(self, x, y):
        value = self.memory.get_register(x) - self.memory.get_register(y)
        if value < 0:
            value += 256
            self.memory.set_register(0xF, 0)
        else:
            self.memory.set_register(0xF, 1)
        self.memory.set_register(x, value)

    # Code("8..7")
    def MathDiff(self, x, y):
        value = self.memory.get_register(y) - self.memory.get_register(x)
        if value < 0:
            value += 256
            self.memory.set_register(0xF, 0)
        else:
            self.memory.set_register(0xF, 1)
        self.memory.set_register(x, value)

    # Code("A...")
    def MemSetI(self, n):
        self.memory.set_i(n)

    # Code("C...")
    def Rand(self, x, n):
        value = randint(0, 255) & n
        self.memory.set_register(x, value)

    # Code("F.1E")
    def MemAddI(self, x):
        value = self.memory.get_i() + self.memory.get_register(x)
        self.memory.set_i(value)

    # Code("F.33")
    def BCD(self, x):
        value_dec = self.memory.get_register(x)
        value = '%03d' % value_dec
        bytes = [int(x) for x in value]
        location = self.memory.get_i()
        self.memory.set_range(location, bytes)

_default = Maths