import functools

def register(*decorators):
    def register_wrapper(func):
        for deco in decorators[::-1]:
            func=deco(func)
        func._decorators=decorators
        return func
    return register_wrapper

class OP:
    def __init__(self, code):
        self.code = format(code, '02x').zfill(4).upper()

    def match(self, pattern):
        result = True
        for chr in zip(list(self.code), list(str(pattern).upper())):
            if not chr[0] == chr[1] and chr[1] != '.':
                return False
        else:
            return True

    def get(self, pattern):
        zipped = list(zip(pattern, self.code))
        n = x = y = None
        if 'N' in pattern:
            n = int(''.join(x[1] for x in zipped if x[0] == 'N'), 16)
        if 'X' in pattern:
            x = int(''.join(x[1] for x in zipped if x[0] == 'X'), 16)
        if 'Y' in pattern:
            y = int(''.join(x[1] for x in zipped if x[0] == 'Y'), 16)
        return {'N': n, 'X': x, 'Y': y}

    def __eq__(self, other):
        if isinstance(other, str) or isinstance(other, self.__class__):
            return self.match(other)
        else:
            return super.__eq__(self, other)

    def __repr__(self):
        return str(self.code)

    def __str__(self):
        return str(self.code)

def Code(opcode):
    def CodeDec(f):
        @functools.wraps(f)
        def wrapper(*args, **kwds):
            f(*args, **kwds)
        wrapper._opcode = opcode
        return wrapper
    return CodeDec

class InstructionParser:
    def __init__(self, service_manager):
        self.op_functions = self.__class__._InstructionCommands()
        self.memory = None
        self.service_manager = service_manager
        self.Do = self.service_manager.Do

    def parse(self, opcode):
        for code in self.op_functions:
            if opcode == code._opcode:
                code(self, opcode)
                break
        else:
            # raise NotImplemented(f"Unknown opcode ({opcode}).")
            print(f"Unknown opcode ({opcode}).")

    """
    @Code("0...")
    def Call(self):
        raise NotImplemented("RCA 1802 call not implemented")
    """


    @Code("00E0")
    def DispClear(self, code):
        self.Do("draw").DispClear()


    @Code("00EE")
    def Return(self, code):
        self.Do("flow").Return()


    @Code("1...")
    def Goto(self, code):
        v = code.get('.NNN')
        self.Do("flow").Goto(v["N"])


    @Code("2...")
    def Subroutine(self, code): #2NNN
        v = code.get('.NNN')
        self.Do("flow").Subroutine(v["N"])


    @Code("3...")
    def SkipEqN(self, code): #3XNN
        v = code.get('.XNN')
        self.Do("flow").SkipEqN(v["X"], v["N"])


    @Code("4...")
    def SkipNEqN(self, code):
        v = code.get('.XNN')
        self.Do("flow").SkipNEqN(v["X"], v["N"])


    @Code("5...")
    def SkipEq(self, code):
        v = code.get('.XY.')
        self.Do("flow").SkipEq(v["X"], v["Y"])

    @Code("6...")
    def SetN(self, code):
        v = code.get('.XNN')
        self.Do("maths").SetN(v["X"], v["N"])


    @Code("7...")
    def AddN(self, code):
        v = code.get('.XNN')
        self.Do("maths").AddN(v["X"], v["N"])


    @Code("8..0")
    def Set(self, code):
        v = code.get('.XY.')
        self.Do("maths").Set(v["X"], v["Y"])


    @Code("8..1")
    def BitOpOr(self, code):
        v = code.get('.XY.')
        self.Do("bitop").BitOpOr(v["X"], v["Y"])


    @Code("8..2")
    def BitOpAnd(self, code):
        v = code.get('.XY.')
        self.Do("bitop").BitOpAnd(v["X"], v["Y"])


    @Code("8..3")
    def BitOpXor(self, code):
        v = code.get('.XY.')
        self.Do("bitop").BitOpXor(v["X"], v["Y"])


    @Code("8..4")
    def MathAdd(self, code):
        v = code.get('.XY.')
        self.Do("maths").MathAdd(v["X"], v["Y"])



    @Code("8..5")
    def MathSub(self, code):
        v = code.get('.XY.')
        self.Do("maths").MathSub(v["X"], v["Y"])


    @Code("8..6")
    def BitOpSHR(self, code):
        v = code.get('.XY.')
        self.Do("bitop").BitOpSHR(v["X"], v["Y"])


    @Code("8..7")
    def MathDiff(self, code):
        v = code.get('.XY.')
        self.Do("maths").MathDiff(v["X"], v["Y"])


    @Code("8..E")
    def BitOpSHL(self, code):
        v = code.get('.XY.')
        self.Do("bitop").BitOpSHL(v["X"], v["Y"])


    @Code("9..0")
    def SkipNEq(self, code):
        v = code.get('.XY.')
        raise NotImplemented("Goto call not implemented")


    @Code("A...")
    def MemSetI(self, code):
        v = code.get('.NNN')
        self.Do("maths").MemSetI(v["N"])


    @Code("B...")
    def JumpN(self, code):
        v = code.get('.NNN')
        self.Do("flow").JumpN(v["N"])


    @Code("C...")
    def Rand(self, code):
        v = code.get('.XNN')
        self.Do("maths").Rand(v["X"], v["N"])


    @Code("D...")
    def Draw(self, code):
        v = code.get('.XYN')
        self.Do("draw").Draw(v["X"], v["Y"], v["N"])


    @Code("E.9E")
    def KeyOpPressed(self, code):
        v = code.get('.X..')
        self.Do("flow").KeyOpPressed(v["X"])

    @Code("E.A1")
    def KepOpReleased(self, code):
        v = code.get('.X..')
        self.Do("flow").KeyOpReleased(v["X"])

    @Code("F.0A")
    def WaitForKey(self, code):
        v = code.get('.X..')
        while not self.Do("misc").WaitForKey(v["X"]):
            pass

    @Code("F.07")
    def GetDelayTimer(self, code):
        v = code.get('.X..')
        self.Do("misc").GetDelayTimer(v["X"])

    @Code("F.15")
    def SetDelayTimer(self, code):
        v = code.get('.X..')
        self.Do("misc").SetDelayTimer(v["X"])


    @Code("F.18")
    def SetSoundTimer(self, code):
        v = code.get('.X..')
        self.Do("misc").SetSoundTimer(v["X"])


    @Code("F.1E")
    def MemAddI(self, code):
        v = code.get('.X..')
        self.Do("maths").MemAddI(v["X"])

    @Code("F.29")
    def MemSetISprite(self, code):
        v = code.get('.X..')
        self.Do("draw").MemSetISprite(v["X"])


    @Code("F.33")
    def BCD(self, code):
        v = code.get('.X..')
        self.Do("maths").BCD(v["X"])


    @Code("F.55")
    def RegDump(self, code):
        v = code.get('.X..')
        self.Do("misc").RegDump(v["X"])


    @Code("F.65")
    def RegLoad(self, code):
        v = code.get('.X..')
        self.Do("misc").RegLoad(v["X"])

    @staticmethod
    def _InstructionCommands():
        all_methods = [getattr(InstructionParser, name) for name in dir(InstructionParser) if callable(getattr(InstructionParser, name))]
        return list(filter(lambda k: hasattr(k, "_opcode"), all_methods))