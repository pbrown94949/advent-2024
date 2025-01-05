class HandheldDevice:

    def __init__(self, a, b, c, instructions):
        self.register_a = a
        self.register_b = b
        self.register_c = c
        self.instruction_pointer = 0
        self.instructions = list(instructions)
        self.output = ''
        self._opcode_handlers = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def run(self):
        while True:
            opcode, operand = self._get_next_intruction()
            if opcode is None:
                break
            self._opcode_handlers[opcode](operand)

    def _get_next_intruction(self):
        if self.instruction_pointer >= len(self.instructions):
            return None, None
        return self.instructions[self.instruction_pointer], self.instructions[self.instruction_pointer + 1]

    def _evaluate_combo_operand(self, operand):
        if operand in [0, 1, 2, 3]:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        raise Exception(f'Invalid combon operand: {operand}')

    def adv(self, operand):
        numerator = self.register_a
        denominator = 2 ** self._evaluate_combo_operand(operand)
        self.register_a = numerator // denominator
        self.instruction_pointer += 2

    def bdv(self, operand):
        numerator = self.register_a
        denominator = 2 ** self._evaluate_combo_operand(operand)
        self.register_b = numerator // denominator
        self.instruction_pointer += 2

    def cdv(self, operand):
        numerator = self.register_a
        denominator = 2 ** self._evaluate_combo_operand(operand)
        self.register_c = numerator // denominator
        self.instruction_pointer += 2

    def bxl(self, operand):
        self.register_b = self.register_b ^ operand
        self.instruction_pointer += 2

    def bst(self, operand):
        operand = self._evaluate_combo_operand(operand)
        self.register_b = operand % 8
        self.instruction_pointer += 2

    def jnz(self, operand):
        if self.register_a == 0:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = operand

    def bxc(self, operand):
        self.register_b = self.register_b ^ self.register_c
        self.instruction_pointer += 2

    def out(self, operand):
        operand = self._evaluate_combo_operand(operand)
        if len(self.output) > 0:
            self.output += ','
        self.output += str(operand % 8)
        self.instruction_pointer += 2


def run(lines):
    hd = get_handheld_device(lines)
    hd.run()
    return hd.output


def get_handheld_device(lines):
    a = b = c = 0
    for line in lines:
        if line.startswith('Register'):
            _, id, value = line.split()
            if id == 'A:':
                a = int(value)
            elif id == 'B:':
                b = int(value)
            elif id == 'C:':
                c = int(value)
        elif line.startswith('Program'):
            _, program = line.split()
    program = [int(x) for x in program.split(',')]
    return HandheldDevice(a, b, c, program)
