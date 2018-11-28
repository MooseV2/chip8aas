from rpyc import Service
from Services.class_utils import exposify, singleton
import _thread as thread
from time import sleep



@exposify
class Memory(Service):
    """
    Class variables
    """
    MEM_LENGTH = 4096 #bytes
    N_REGISTERS = 16

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Memory, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.init()
        return cls._instance


    def reset(self):
        self.init()

    def init(self):
        """
        The memory module handles read/write access to RAM and registers.
        The memory layout of the CHIP-8 system is as follows:
            0x000 to 0x200 (512): Font data
            0xF00 to 0xFFF: Display refresh
            0xEA0 to 0xEFF: Call stack and internal use
        The register layout is as follows:
            V0 to VF: 8 bit registers
            VF: Used as flag for some operations (eg carry)
        """
        self.RAM = [0] * self.__class__.MEM_LENGTH
        self.REGISTERS = [0] * self.__class__.N_REGISTERS
        # Constants

        self.callstack = []
        self.PC = 0x200
        self.I = 0
        self.KEYS = 0
        self.TIMERS = [0, 0]

        self.DISPLAY_START = 0xF00
        self.DISPLAY_LENGTH = 256
        self.FONT_START = 0x00
        self.init_fontset(self.FONT_START)

        def countdown_timers(x):
            while True:
                sleep(1/20.0)
                self.decrement_timers()
        thread.start_new_thread(countdown_timers, (None,))


    def get_address(self, address, length=1):
        """
        Returns the data stored at a memory address
        :param address: Memory address
        :param length: The number of bytes to return (default 1)

        :return: Byte(s) stored at that address
        """
        try:
            return self.RAM[address:address+length]
        except IndexError:
            raise IndexError("Memory address out of range")

    def set_address(self, address, value):
        """
        Sets the data stored at a memory address to a value
        :param address: Memory address
        :param value: Value to store
        """
        try:
            self.RAM[address] = value
        except IndexError:
            raise IndexError("Memory address out of range")

    def set_range(self, start, values):
        try:
            for index, value in enumerate(values):
                print(start+index, value)
                self.RAM[start+index] = value
        except IndexError:
            pass
            # raise IndexError("Memory address out of range")

    def get_register(self, register):
        """
        Gets a register
        :param register: Register number (0-15)
        :return: Byte stored in register
        """
        try:
            return self.REGISTERS[register]
        except IndexError:
            raise IndexError("Register number out of range")

    def set_register(self, register, value):
        """
        Sets the data stored at a register to a value
        :param register: Register number
        :param value: Value to store
        """
        try:
            self.REGISTERS[register] = value
        except IndexError:
            raise IndexError("Register number out of range")

    def print_memory(self, address=-1):
        if address > 0:
            print(f"{self.RAM[address]}")
        else:
            for i, x in enumerate(self.RAM):
                if i % 64 == 0:
                    print(f"\n{i:03x} [", end='')

                print(format(x, '02x'), end=' ')
            print()

    def get_io_keys(self):
        return self.KEYS

    def set_io_keys(self, new_keys):
        self.KEYS = new_keys

    def get_pc(self):
        return self.PC
    def set_pc(self, pc):
        self.PC = pc
    def push_stack(self, pc):
        self.callstack.append(pc)
    def pop_stack(self):
        return self.callstack.pop()
    def increment_pc(self):
        self.PC += 2
    def set_i(self, i):
        self.I = i
    def get_i(self):
        return self.I

    def get_timer(self, index):
        return self.TIMERS[index]

    def set_timer(self, index, value):
        self.TIMERS[index] = value

    def decrement_timers(self):
        self.TIMERS[0] = max(self.TIMERS[0] - 1, 0)
        self.TIMERS[1] = max(self.TIMERS[1] - 1, 0)
        return self.TIMERS

    def init_fontset(self, font_start):
        fontset =  [0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
                    0x20, 0x60, 0x20, 0x20, 0x70, # 1
                    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
                    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
                    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
                    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
                    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
                    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
                    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
                    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
                    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
                    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
                    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
                    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
                    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
                    0xF0, 0x80, 0xF0, 0x80, 0x80]  # F
        self.set_range(font_start, fontset)

    def get_font_start(self):
        return self.FONT_START

    def get_display_start(self):
        return self.DISPLAY_START

    def get_display_length(self):
        return self.DISPLAY_LENGTH
# export default
_default = Memory