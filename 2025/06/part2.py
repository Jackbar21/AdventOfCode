import re
import functools

USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line for line in file.readlines()]

    def parse_line(line: str) -> tuple[int]:
        res = []
        prev_index = 0
        index = 0
        while index < len(line):
            if line[index] != " ":
                index += 1
                continue

            res.append(int(line[prev_index:index]))
            index += 1
            while index < len(line) and line[index] == " ":
                index += 1
            prev_index = index

        last_num = line[prev_index:]
        if last_num.isnumeric():
            res.append(int(last_num))
        return res

    number_lists = [parse_line(line.strip()) for line in lines[:-1]]
    operations = [op for op in lines[-1] if op in ("+", "*")]

    max_lenghts = []
    for i in range(len(operations)):
        max_lenghts.append(max(len(str(nums[i])) for nums in number_lists))

    space_sensitive_number_lists = []
    for line in lines[:-1]:
        index = 0
        nums = []
        for length in max_lenghts:
            nums.append((line[index:index+length]))
            index += length + 1  # plus one for the space
        space_sensitive_number_lists.append(nums)

    length = len(operations)
    assert all([len(nums) == length for nums in number_lists])

    op_to_func = {"+": lambda a, b: a + b, "*": lambda a, b: a * b}
    op_to_identity = {"+": 0, "*": 1}

    res = 0
    for i, op in enumerate(operations):
        str_nums = [nums[i] for nums in space_sensitive_number_lists]
        max_length = max_lenghts[i]

        assert all([len(str_num) == max_length for str_num in str_nums])
        transposed = list(map(list, zip(*str_nums)))

        nums = [int("".join(digits).strip()) for digits in transposed]
        res += functools.reduce(
            op_to_func[op], nums, op_to_identity[op]
        )

    print(f"ANSWER: {res}")
