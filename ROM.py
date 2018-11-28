from Instruction import InstructionParser, OP
from service_manager import ServiceManager

class ROM:
    def __init__(self, fname):
        self.service_manager = ServiceManager()
        self.RAM = self.service_manager.Do("memory")
        self.RAM.reset()
        self.instruction_parser = InstructionParser(self.service_manager)
        self.RAM.set_range(0x200, self.load_rom(fname))
        self.RAM.print_memory()



    def load_rom(self, fname):
        with open(fname, 'rb') as f:
            return f.read()

    def get_instruction(self):
        while True:
            c = self.RAM.get_address(self.RAM.get_pc(), length=2)
            opcode = c[0] << 8 | c[1]
            print(OP(opcode))
            self.RAM.increment_pc()
            yield OP(opcode)

    def cycle(self):
        for opcode in self.get_instruction():
            self.instruction_parser.parse(opcode)

    def test(self):
        assert OP(0x2222) == "2..2"
        assert OP(0x2002) == "2..2"
        assert OP(0xABCD) == "AB.."
        assert OP(0xABCD) != "2..2"
