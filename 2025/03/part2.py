USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    def solver(line: str, toggle: int) -> str:
        # 'toggle' is the amount of batteries left to turn on
        assert toggle >= 1
        assert len(line) >= toggle

        # Base Case:
        if len(line) == toggle:
            return line

        # Base Case:
        if toggle == 1:
            return max(line)

        max_num = -1
        index = None
        for i in range(len(line) - toggle + 1):
            digit = int(line[i])
            if digit > max_num:
                max_num = digit
                index = i
        
        return str(max_num) + solver(line[index + 1:], toggle - 1)

    res = 0
    TOGGLE = 12
    for line in lines:
        res += int(solver(line, TOGGLE))

    assert res
    print(f"ANSWER: {res}")
