USE_TEST_DATA = True
from collections import defaultdict

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    index = lines.index("")
    ranges = lines[:index]
    fresh_ingredients = set()

    res = 0
    line_sweep = defaultdict(int)
    for r in ranges:
        split_range = r.split("-")
        assert len(split_range) == 2
        start, end = split_range
        start, end = int(start), int(end)

        fresh_ingredients.update(range(start, end + 1))

    res = len(fresh_ingredients)

    print(f"ANSWER: {res}")
