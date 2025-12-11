USE_TEST_DATA = False
from collections import defaultdict, deque

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data2.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    res = 0

    d = {
        line[0]: line[1].split(" ")
        for line in map(lambda line: line.split(": "), lines)
    }
    adj_list = defaultdict(set)
    for src, dests in d.items():
        for dest in dests:
            adj_list[src].add(dest)

    START, GOAL = "svr", "out"

    memo = {}
    def dp(node, dac, fft):
        if (node, dac, fft) in memo:
            return memo[(node, dac, fft)]

        if node == "dac":
            dac = True

        if node == "fft":
            fft = True

        if node == GOAL:
            return 1 if dac and fft else 0

        total = 0
        for neighbor in adj_list[node]:
            total += dp(neighbor, dac, fft)

        memo[(node, dac, fft)] = total
        return total

    res = dp(START, False, False)
    print(f"ANSWER: {res}")
