USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    dial = 50
    res = 0
    for line in lines:
        sign = -1 if line[0] == "L" else 1
        abs_degree = int(line[1:])

        extra_rotations = abs_degree // 100
        res += extra_rotations
        abs_degree -= 100 * extra_rotations

        degree = sign * abs_degree
        prev_dial = dial
        dial += degree
        if prev_dial != 0 and (dial < 0 or dial > 100):
            res += 1
        dial %= 100
        if dial == 0:
            res += 1

    print(f"ANSWER: {res}")
