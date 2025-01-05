class HandheldDevice:

    def __init__(self, a, b, c, instructions):
        self.register_a, self.register_b, self.register_c = a, b, c
        self.instruction_pointer, self.instructions = 0, list(instructions)
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

    def step(self):
        opcode, operand = self._get_next_instruction()
        if opcode is None:
            return True
        self._opcode_handlers[opcode](operand)
        return False

    def _get_next_instruction(self):
        if self.instruction_pointer >= len(self.instructions):
            return None, None
        return self.instructions[self.instruction_pointer], self.instructions[self.instruction_pointer + 1]

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

    def print(self):
        print(f'\n\nRegister A: {self.register_a}')
        print(f'Register B: {self.register_b}')
        print(f'Register C: {self.register_c}')
        print(f'Output: {self.output}')


def run(lines):
    program = get_program(lines)
    a_values = [0]
    for desired_output in [str(x) for x in reversed(program)]:
        temp = set()
        for a in a_values:
            temp.update(get_solutions(program, a, desired_output))
        a_values = temp
    return min(a_values)


def get_solutions(program, target_a, target_output):
    """For a given program, find all values for register A that result in the desired end conditions.
        program = the list of instructions to run.
        target_a = the desired value in register A.
        desired_output = the desired value in the output.

        We start looking for solutions at target_a * 8 due to the nature of the program we are given. That wouldn't work for any random program. 
        We stop looping once the value in register A exceeds the target value. 
    """
    result = []
    a = target_a * 8
    while True:
        hd = run_until_output(program, a)
        if hd.register_a == target_a and hd.output == target_output:
            result.append(a)
        if hd.register_a > target_a:
            break
        a += 1
    return result


def run_until_output(program, a):
    """Run the provided program until there is one character of output."""
    hd = HandheldDevice(a, 0, 0, program)
    while len(hd.output) < 1:
        hd.step()
    return hd


def get_program(lines):
    for line in lines:
        if line.startswith('Program'):
            _, program = line.split()
            return [int(x) for x in program.split(',')]
