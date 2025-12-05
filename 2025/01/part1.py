USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    dial = 50
    res = 0
    for line in lines:
        sign = -1 if line[0] == "L" else 1
        degree = sign * int(line[1:])
        dial += degree
        dial %= 100
        if dial == 0:
            res += 1

    print(f"ANSWER: {res}")
