from .managed_service import ManagedService
from Services.class_utils import exposify

@exposify
class Draw(ManagedService):
    # Code("00E0")
    def DispClear(self):
        self.memory.set_range(self.memory.get_display_start(), [0x00] * self.memory.get_display_length())
        self.memory.set_refresh(True)

    # Code("D...")
    def Draw(self, x, y, height):
        # TODO: Comment this hack
        
        # for i in range(16):
        #     print(f"Register {i}: {self.memory.get_register(i)}")
        display_start = self.memory.get_display_start()
        x_pos = self.memory.get_register(x)
        y_pos = self.memory.get_register(y)
        i = self.memory.get_i()
        collision = 0

        bin64 = lambda dec: '{0:064b}'.format(dec)
        bin8 = lambda dec: '{0:08b}'.format(dec)

        for row in range(height):
            old_row = self.memory.get_address(display_start + (y_pos+row) * 8, 8)
            old_row = bin64(int.from_bytes(old_row, byteorder="big", signed=False))
            sprite_value = self.memory.get_address(i + row)
            sprite_value = bin8(int.from_bytes(sprite_value, byteorder="big", signed=False))
            new_value = ""
            for index, pos in enumerate(range(x_pos, min(x_pos + 8, 64))):
                result = old_row[pos] + sprite_value[index]
                if result == "01":
                    new_value += "1"
                elif result == "10":
                    new_value += "1"
                elif result == "11":
                    new_value += "0"
                    collision = 1
                elif result == "00":
                    new_value += "0"
            new_row = old_row[0:x_pos] + new_value + old_row[min(64, x_pos+8):]
            assert len(new_row) == 64
            new_row = int(new_row, 2).to_bytes(len(new_row) // 8, byteorder='big')
            self.memory.set_range(display_start + (y_pos+row) * 8, new_row)
        self.memory.set_register(0xF, collision)
        self.memory.set_refresh(True)

    # Code("F.29")
    def MemSetISprite(self, x):
        # Each character is 5 bytes (4 bits wide by 5 bits tall)
        value = self.memory.get_register(x)
        location = self.memory.get_font_start() + (5 * value)
        self.memory.set_i(location)
    
_default = Draw