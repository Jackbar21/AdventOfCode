USE_TEST_DATA = False
from collections import defaultdict, deque

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
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

    # Since this is a DAG, there are no cycles, and can run DFS until no more nodes to visit
    START, GOAL = "you", "out"

    def dfs(node):
        if node == GOAL:
            return 1
        total = 0
        for neighbor in adj_list[node]:
            total += dfs(neighbor)
        return total

    res = dfs(START)
    print(f"ANSWER: {res}")
