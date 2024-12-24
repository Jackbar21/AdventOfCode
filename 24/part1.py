from collections import defaultdict


USE_TEST_DATA = False
SMALL_DATA = False

file_name = (
    "./data.txt"
    if not USE_TEST_DATA
    else "./test_data_small.txt" if SMALL_DATA else "./test_data.txt"
)
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    index = lines.index("")
    # print(f"{lines[:index]=}")
    # print(f"{lines[index+1:]=}")
    inputs, queries = lines[:index], lines[index + 1 :]

    d = {}
    for input in inputs:
        wire, bit = input.split(": ")
        assert wire not in d
        d[wire] = int(bit)

    FIRST_WIRE, GATE, SECOND_WIRE = 0, 1, 2
    remaining = defaultdict(list)
    z_remaining = set()
    for query in queries:
        q, result = query.split(" -> ")
        q = tuple(q.split(" "))
        # if q in remaining:
        #     print(f"DUPLICATE: {q=}")
        # assert q not in remaining
        remaining[q].append(result)
        if result[0] == "z":
            assert result not in z_remaining
            z_remaining.add(result)

    # print(f"{d=}")
    # print(f"{remaining=}")
    # print(f"{z_remaining=}")
    res = sorted(z_remaining, reverse=True)
    # exit()

    gate_solver = {
        "AND": lambda x, y: x & y,
        "XOR": lambda x, y: x ^ y,
        "OR": lambda x, y: x | y,
    }

    while len(z_remaining) > 0:
        remaining_set = set(remaining.keys())
        for operation in remaining_set:
            wire1, gate, wire2 = operation

            if wire1 in d and wire2 in d:
                val1 = d[wire1]
                val2 = d[wire2]
                val = gate_solver[gate](val1, val2)
                for result in remaining[operation]:
                    d[result] = val
                    z_remaining.discard(result)
                del remaining[operation]

    res = int("".join(map(lambda z: str(d[z]), res)), 2)
    print(f"ANSWER: {res}")