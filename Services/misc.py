from .managed_service import ManagedService
from Services.class_utils import exposify
from threading import Timer


@exposify
class Misc(ManagedService):
    def RegLoad(self, x):
        location = self.memory.get_i()
        values = self.memory.get_address(location, x)
        for index, value in enumerate(values):
            self.memory.set_register(index, value)

    def RegDump(self, x):
        values = []
        start_location = self.memory.get_i()
        for register in range(x + 1):
            values.append(self.memory.get_register(register))
        self.memory.set_range(start_location, values)

    def WaitForKey(self, x):
        print("Blocking until key press")
        keys = self.memory.get_io_keys()
        for _ in range(500):
            key_diff = self.memory.get_io_keys()
            # key_diff = new_keys ^ keys
            if key_diff > 0: # A key was pressed
                for shift in range(16):
                    if ((key_diff >> shift) & 1) == 1:
                        self.memory.set_register(x, shift)
                        return True
        else:
            return False

    # Code("F.0A")
    def GetDelayTimer(self, x):
        value = self.memory.get_timer(0)
        self.memory.set_register(x, value)
        # print(value)

    # Code("F.15")
    def SetDelayTimer(self, x):
        value = self.memory.get_register(x)
        self.memory.set_timer(0, value)


    # Code("F.18")
    def SetSoundTimer(self, x):
        value = self.memory.get_register(x)
        self.memory.set_timer(1, value)




_default = Misc