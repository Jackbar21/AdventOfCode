USE_TEST_DATA = True
from collections import deque

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    problems = []
    for line in lines:
        line = line.split(" ")

        indicator_lights = line[0][1:-1]

        options = [option[1:-1].split(",") for option in line[1:-1]]
        options = [tuple(int(op) for op in option) for option in options]

        joltage_requirements = tuple(map(int, line[-1][1:-1].split(",")))

        problems.append((indicator_lights, options, joltage_requirements))

    def dp(i, memo, options, requirements):
        # Want requirements to be all zeros
        if all(r == 0 for r in requirements):
            return 0

        if i >= len(options):
            return float("inf")

        if (i, requirements) in memo:
            return memo[(i, requirements)]

        option = options[i]

        # Case 1: skip this option
        case1 = dp(i + 1, memo, options, requirements)

        # Case 2: use this option (if valid)
        valid = True
        new_requirements = list(requirements)
        for idx in option:
            new_requirements[idx] -= 1
            if new_requirements[idx] < 0:
                valid = False
                break
        case2 = (
            float("inf")
            if not valid
            else 1 + dp(i, memo, options, tuple(new_requirements))
        )

        memo[(i, requirements)] = min(case1, case2)
        return memo[(i, requirements)]

    res = 0
    for _, options, joltage_requirements in problems:
        memo = {}
        steps = dp(0, memo, options, joltage_requirements)
        res += steps

    print(f"ANSWER: {res}")
