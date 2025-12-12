USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    res = 0

    presents = [[(lines[i]), (lines[i + 1]), (lines[i + 2])] for i in range(1, 29, 5)]
    problems = lines[30:]

    present_spaces = [sum(s.count("#") for s in present) for present in presents]

    for problem in problems:
        area, present_counts = problem.split(": ")

        area = area.split("x")
        area = [int(x) for x in area]
        assert len(area) == 2
        length, width = area

        present_counts = present_counts.split(" ")
        present_counts = [int(x) for x in present_counts]
        assert len(present_counts) == len(presents)

        total_space = length * width
        used_space = sum(
            present_counts[i] * present_spaces[i] for i in range(len(present_counts))
        )
        if used_space <= total_space:
            res += 1

    print(f"ANSWER: {res}")
