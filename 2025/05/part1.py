USE_TEST_DATA = False
from collections import defaultdict

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    index = lines.index("")
    ranges = lines[:index]
    ingredients = lines[index + 1 :]
    ingredients = list(map(int, ingredients))

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
    sorted_ingredients = sorted(ingredients)

    index = 0
    delta = 0
    for ingredient in sorted_ingredients:
        while index < len(sorted_keys) and (key := sorted_keys[index]) < ingredient:
            delta += line_sweep[key]
            index += 1

        is_fresh = delta > 0
        if is_fresh:
            res += 1

    print(f"ANSWER: {res}")
