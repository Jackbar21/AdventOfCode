USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    # SETUP
    lines = [line.strip() for line in file.readlines()]
    assert len(lines) == 1
    ranges = lines[0].split(",")
    intervals = []
    for r in ranges:
        split_range = r.split("-")
        assert len(split_range) == 2
        start, end = split_range
        start, end = int(start), int(end)
        assert start <= end
        interval = (start, end)
        intervals.append(interval)

    # PROBLEM SOLVING
    def is_invalid(id: int) -> bool:
        str_id = str(id)
        if len(str_id) % 2 == 1:
            return False
        half = len(str_id) // 2
        return str_id[:half] == str_id[half:]

    res = 0
    for start, end in intervals:
        for id in range(start, end + 1):
            if is_invalid(id):
                res += id

    print(f"ANSWER: {res}")
