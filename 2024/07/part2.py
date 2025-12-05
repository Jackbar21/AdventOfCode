USE_TEST_DATA = False


def canBuildSolution(solution, numbers):
    # No caching, so "fake" dp lol
    def dp(i, cur_sum):
        if i >= len(numbers):
            return solution == cur_sum

        # Since only pos. numbers and only '*' and '+', can only grow number.
        # so if past solution, this branch doesn't work!
        if cur_sum > solution:
            return False

        num = numbers[i]
        return (
            dp(i + 1, cur_sum + num)
            or dp(i + 1, cur_sum * num)
            or dp(i + 1, int(str(cur_sum) + str(num)))
        )

    return dp(1, numbers[0])


file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = file.readlines()
    SOL, NUMBERS = 0, 1
    equations = []
    for line in lines:
        key, val = line.split(":")
        sol = int(key)
        numbers = [int(num) for num in val.split()]
        equations.append((sol, numbers))

    res = 0
    for sol, numbers in equations:
        if canBuildSolution(sol, numbers):
            res += sol
    print(f"ANSWER: {res}")
