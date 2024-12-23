USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    # FYI: After doing part 2, I realized I got LUCKY for my answer in part 1 hehe :P
    d = {
        "029A": "<A^A>^^AvvvA",
        "980A": "^^^A<AvvvA>A",
        "179A": "^<<A^^A>>AvvvA",
        "456A": "^^<<A>A>AvvA",
        "379A": "^A<<^^A>>AvvvA" # Should be <<^^, i.e. make '<' higher precendence than '^' when possible
    } if USE_TEST_DATA else {
        "140A": "^<<A^A>vvA>A",
        "170A": "^<<A^^A>vvvA>A",
        "169A": "^<<A>>^A^AvvvA",
        "803A": "<^^^AvvvA^>AvA",
        "129A": "^<<A>A>^^AvvvA"
    }

    robot_shortest_paths = { # from, to
        # A
        ("A", "A"): "A",
        ("A", "^"): "<A",
        ("A", ">"): "vA",
        ("A", "v"): "<vA",
        ("A", "<"): "v<<A",
        # ^
        ("^", "^"): "A",
        ("^", "A"): ">A",
        ("^", "v"): "vA",
        ("^", ">"): ">vA",
        ("^", "<"): "v<A",
        # <
        ("<", "<"): "A",
        ("<", "A"): ">>^A",
        ("<", "v"): ">A",
        ("<", ">"): ">>A",
        ("<", "^"): ">^A",
        # v
        ("v", "v"): "A",
        ("v", "A"): ">^A",
        ("v", "<"): "<A",
        ("v", "^"): "^A",
        ("v", ">"): ">A",
        # >
        (">", ">"): "A",
        (">", "A"): "^A",
        (">", "v"): "<A",
        (">", "<"): "<<A",
        (">", "^"): "<^A",
    }

    def plusOneLevelOfIndirection(sequence):
        res = []
        start_pos = "A"
        for symbol in sequence:
            path = robot_shortest_paths[(start_pos, symbol)]
            res.append(path)
            start_pos = symbol
        return "".join(res)

    res = 0
    for key in d:
        path = d[key] # level 1!
        for _ in range(3 - 1): # Already done first level of indirection via d!
            path = plusOneLevelOfIndirection(path)

        numeric_part = int(''.join('' if c == 'A' else c for c in key))
        res += numeric_part * len(path)
    
    print(f"ANSWER: {res}")

