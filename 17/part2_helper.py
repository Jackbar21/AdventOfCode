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
"""

# 1. B = A % 8
# 2. B = B ^ 3 == (A % 8) ^ 00000...011 --> i.e. flips last two bits!
# 3. C = A // pow(2, B) = A // pow(2, [(A % 8) ^ 3])
# 4. A = A // pow(2, 3) = A // 8
# 5. B = B ^ 5 == B ^ (101) == (A % 8) ^ (011) ^ (101) == (A % 8) ^ (110)
# 6. B = B ^ C
# 7. OUTPUT: B % 8
# 8. HALT if A == 0, else JUMP to beginning!
#
# Program: (2,4), (1,3), (7,5), (0,3), (1,5), (4,4), (5,5), (3,0)

output = [2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0]
LENGTH = len(output)

def apply(a, b, c):
    b = a % 8
    b ^= 3
    c = a // pow(2, b)
    a //= 8
    b ^= 5
    b ^= c
    # yield (a, b, c)
    # if a == 0:
    #     print("DONE\n")
    #     return
    # apply(a, b, c)
    return a, b, c

def getNext(start_val = 0):
    val = start_val
    for _ in range(51):
        a, b, c = val, 0, 0
        for value in apply(a, b, c):
            print(f"{value=}")
        val += 1

def checkEqual(a_register):
    a, b, c = a_register, 0, 0
    res = []
    for _ in range(LENGTH):
        res.append()

getNext()