USE_TEST_DATA = False
from collections import defaultdict

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    index = lines.index("")
    ranges = lines[:index]

    res = 0
    line_sweep = defaultdict(int)
    for r in ranges:
        split_range = r.split("-")
        assert len(split_range) == 2
        start, end = split_range
        start, end = int(start), int(end)

        line_sweep[start] += 1
        line_sweep[end + 1] -= 1

    sorted_keys = sorted(line_sweep.keys())

    prev_key = None
    delta = 0
    res = 0
    for key in sorted_keys:
        if prev_key is None:
            prev_key = key

        delta += line_sweep[key]
        if delta == 0:
            # Range of fresh ingredients: prev_key - key (for total of 'key - prev_key' fresh ingredients!)
            res += key - prev_key
            prev_key = None


    print(f"ANSWER: {res}")
