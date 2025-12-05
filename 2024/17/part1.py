USE_TEST_DATA = False

class Solution:
    def __init__(self):
        file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
        with open(file_name, "r") as file:
            lines = [line.split() for line in file.readlines()]
            self.a_register, self.b_register, self.c_register = [int(lines[i][-1]) for i in range(3)] # Registers
            program = [int(num) for num in lines[-1][-1].split(",")]
            self.instructions = [(program[i], program[i + 1]) for i in range(0, len(program), 2)]
            # OPCODE, OPERAND = 0, 1
            # print(f"{program=}")
            # print(f"{instructions=}")

            # print(f"{self.a_register,self.b_register,self.c_register=}")
            # print(f"{program=}")

            # def 
            # INSTRUCTION_POINTER = 0
            self.instruction_pointer = 0
            self.output = []
            self.ADV, self.BXL, self.BST, self.JNZ, self.BXC, self.OUT, self.BDV, self.CDV = 0, 1, 2, 3, 4, 5, 6, 7
            # OUTPUT = []

    def getComboOperandValue(self, combo_operand):
        assert 0 <= combo_operand < 7
        if 0 <= combo_operand <= 3:
            return combo_operand
        if combo_operand == 4:
            return self.a_register
        if combo_operand == 5:
            return self.b_register
        if combo_operand == 6:
            return self.c_register
        raise Exception("Unreachable Code!")
        
    def isJumpInstruction(self, instruction):
        return instruction == self.JNZ

    def adv(self, combo_operand):
        numerator = self.a_register
        power = self.getComboOperandValue(combo_operand)
        denominator = pow(2, power)
        self.a_register = numerator // denominator
    
    def bxl(self, literal_operand):
        self.b_register = self.b_register ^ literal_operand
    
    def bst(self, combo_operand):
        val = self.getComboOperandValue(combo_operand)
        self.b_register = val % 8
    
    def jnz(self, literal_operand):
        if self.a_register == 0:
            return
        
        self.instruction_pointer = literal_operand // 2
        # if self.instruction_pointer < len(self.instructions) and self.isJumpInstruction(self.instructions[self.instruction_pointer][0]):
        self.instruction_pointer -= 1 # Because we'll increment it right afterwards :)
    
    def bxc(self, operand):
        self.b_register = self.b_register ^ self.c_register
    
    def out(self, combo_operand):
        val = self.getComboOperandValue(combo_operand)
        self.output.append(val % 8)
    
    def bdv(self, combo_operand):
        numerator = self.a_register
        power = self.getComboOperandValue(combo_operand)
        denominator = pow(2, power)
        self.b_register = numerator // denominator

    def cdv(self, combo_operand):
        numerator = self.a_register
        power = self.getComboOperandValue(combo_operand)
        denominator = pow(2, power)
        self.c_register = numerator // denominator

    def run(self):
        # self.output = []
        opcode_to_method = {self.ADV: self.adv, self.BXL: self.bxl, self.BST: self.bst, self.JNZ: self.jnz, self.BXC: self.bxc, self.OUT: self.out, self.BDV: self.bdv, self.CDV: self.cdv}
        while self.instruction_pointer < len(self.instructions):
            opcode, operand = self.instructions[self.instruction_pointer]
            opcode_to_method[opcode](operand)
            self.instruction_pointer += 1
        print(",".join(str(digit) for digit in self.output))
    
    # print(",".join(OUTPUT))

s = Solution()
s.run()