USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    # For each line, find the maximum number (except the last), and the
    # second largest number after it
    res = 0
    for line in lines:
        max_num = float("-inf")
        index = None
        for i in range(len(line) - 1):
            digit = int(line[i])
            if digit > max_num:
                max_num = digit
                index = i
        second_max_num = max(int(digit) for digit in line[index + 1 :])
        joltage = max_num * 10 + second_max_num
        res += joltage

    print(f"ANSWER: {res}")
