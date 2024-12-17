USE_TEST_DATA = False

from collections import deque

class Solution:
    def __init__(self):
        file_name = "./copy_program.txt" if USE_TEST_DATA else "./data.txt"
        with open(file_name, "r") as file:
            lines = [line.split() for line in file.readlines()]
            self.a_register, self.b_register, self.c_register = [int(lines[i][-1]) for i in range(3)] # Registers
            program = [int(num) for num in lines[-1][-1].split(",")]
            self.instructions = [(program[i], program[i + 1]) for i in range(0, len(program), 2)]
            self.GOAL_STATE = [0,3,5,4,3,0] if USE_TEST_DATA else [2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0]
            assert program == self.GOAL_STATE
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

    def run(self, a_register):
        # self.output = []
        self.__init__()
        self.a_register = a_register # Overwrite A register's original value!
        opcode_to_method = {self.ADV: self.adv, self.BXL: self.bxl, self.BST: self.bst, self.JNZ: self.jnz, self.BXC: self.bxc, self.OUT: self.out, self.BDV: self.bdv, self.CDV: self.cdv}
        i = 1
        while self.instruction_pointer < len(self.instructions):
            opcode, operand = self.instructions[self.instruction_pointer]
            opcode_to_method[opcode](operand)
            self.instruction_pointer += 1

            # Termination help :)
            # if i == len(self.output):
            #     if self.output[i - 1] != self.GOAL_STATE[i - 1]:
            #         return False
            #     i += 1
            # elif len(self.output) > len(self.GOAL_STATE):
            #     return False
    
        # print(",".join(str(digit) for digit in self.output))
        if self.output == self.GOAL_STATE:
            # print(f"ANSWER: {a_register}")
            return True
        
        return False
    
    # print(",".join(OUTPUT))

# MIN_SOLUTION = 627_340_000
# s = Solution()
# for a_register in range(MIN_SOLUTION, 999999999999999999):
#     if s.run(a_register):
#         break
#     if a_register % 10000 == 0:
#         print(f"{a_register}...")

# s = Solution()
# # base = pow(8, 15) - 1
# MIN_VAL = pow(8, 15)
# MAX_VAL = pow(8, 16) - 1
# # base = MIN_VAL + 100
# base = 53*8
# for a_register in range(base, base+8):
#     if s.run(a_register):
#         break
#     print(f"{a_register}-->{s.output}, {len(s.output)}, {len([2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0])}")


"""
Register A: X
Register B: 0
Register C: 0

Program: (2,4), (1,3), (7,5), (0,3), (1,5), (4,4), (5,5), (3,0)
                                                    I
output = []

### PLAYGROUND ###
1. B = A % 8
2. B = B ^ 3 == (A % 8) ^ 00000...011 --> i.e. flips last two bits!
3. C = A // pow(2, B) = A // pow(2, [(A % 8) ^ 3])
4. A = A // pow(2, 3) = A // 8
5. B = B ^ 5 == B ^ (101) == (A % 8) ^ (011) ^ (101) == (A % 8) ^ (110)
6. B = B ^ C
7. OUTPUT: B % 8
8. HALT if A == 0, else JUMP to beginning!


After first iteration, since we do A // 8, we know that A % 8 == 0.
Hence we start with: 
1. B == 0
2. B == 3
3. C == A // pow(2, 3) == A // 8 --> i.e. the next case!
4. A == A // 8 --> so same as C, LITERALLY!!!
5. B == B ^ 6 == 3 ^ 6 == (011) ^ (110) == (101) == 5
6. B == B ^ C == B ^ A (since C == A at this point!) == 5 ^ A --> next A % 8 == 5
7. OUTPUT: B % 8 --> 5

B % 8 == 2
--> B == 8k + 2, k >= 0
--> 
WANT: 2 == { [(A % 8) ^ 6] ^ [A // pow(2, (A%8)^3)] } % 8


### THOUGHTS ###
At the very last iteration, we want A == 0 so that we HALT. Since we know we set A = A // 8 each iteration, 
we need 0 < A < 8 at the very last iteration to make it 0. For the digits 0-8, these are the outputs of the program:
0-->[6], 1, 16
1-->[7], 1, 16
2-->[5], 1, 16
3-->[6], 1, 16
4-->[2], 1, 16
5-->[3], 1, 16
6-->[0], 1, 16
7-->[1], 1, 16
8-->[7, 7], 2, 16

As we can see, 6 is the ONLY one that produces a 0 at the end. Which means it's likely that we need A to be a 6 at the
very last iteration. Which means in the second to last iteration, we need A such that A // 8 == 6, so it must be that
A is between 48 and 55, inclusive. Printing these results we see that:
48-->[0, 0], 2, 16
49-->[3, 0], 2, 16
50-->[5, 0], 2, 16
51-->[6, 0], 2, 16
52-->[2, 0], 2, 16
53-->[3, 0], 2, 16
54-->[1, 0], 2, 16
55-->[2, 0], 2, 16

The program is 2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0 so clearly we need to either terminate eventually with 49 or 53. So
we need A to have previous iteration A to have been a 49 or 53, i.e. such that A // 8 == 49 or A // 8 == 53, giving
us ranges of (49*8 -- 49*8+7)==392-399 and (53*8 -- 53*8+7)==424-431, respectively. Printing these out we get:
392-->[7, 3, 0], 3, 16
393-->[5, 3, 0], 3, 16
394-->[1, 3, 0], 3, 16
395-->[6, 3, 0], 3, 16
396-->[1, 3, 0], 3, 16
397-->[5, 3, 0], 3, 16
398-->[4, 3, 0], 3, 16
399-->[1, 3, 0], 3, 16
424-->[3, 3, 0], 3, 16
425-->[5, 3, 0], 3, 16
426-->[1, 3, 0], 3, 16
427-->[6, 3, 0], 3, 16
428-->[1, 3, 0], 3, 16
429-->[5, 3, 0], 3, 16
430-->[5, 3, 0], 3, 16
431-->[3, 3, 0], 3, 16

# Since we know the Program is 2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0 then evidently the only values we care about will be
# the ones that end in 5,3,0. In this case, these are: 393, 397, 425, 429, 430. Now we can keep applying this same
# methodology/algorithm recursively, until we reach the complete full program backwards.
"""
# candidates = deque([393, 397, 425, 429, 430])
# Instead of starting from 393, 397, 425, 429, 430 as our possible candidates, let's first write the program and have
# it start from 6 (which we know must be our final A result in last iteration!) and see if it behaves appropriately
# by generating 49 and 53 as only valid candidates, then 393, 397, 425, 429, 430, etc... Even better than starting 
# A from 6, we can start it from 0, since we know the program only terminates when A == 0, and it will find itself
# to be 6 anyway using this exact same logic!
s = Solution()
candidates = deque([0])
program = [2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0]
# for _ in range(10):
while True:
    candidate = candidates.popleft()
    candidate_times_eight = candidate * 8
    for i in range(8):
        a_register = candidate_times_eight + i
        if s.run(a_register):
            # If this returns true, we found optimal solution, so exit!
            print(f"ANSWER: {a_register}")
            exit()

        length = len(s.output)
        assert length <= 16
        if s.output == program[-length:]:
            # if len(s.output) == 16:
            #     print(f"ANSWER: {candidate}")
            #     exit()
            candidates.append(a_register)
    # print(f"{candidates=}")


# print(f"{answers=}, {min(answers)=}")    

# s = Solution()
# # base = pow(8, 15) - 1
# MIN_VAL = pow(8, 15)
# MAX_VAL = pow(8, 16) - 1
# # base = MIN_VAL + 100
# base = 53*8
# for a_register in range(base, base+8):
#     if s.run(a_register):
#         break
#     print(f"{a_register}-->{s.output}, {len(s.output)}, {len([2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0])}")