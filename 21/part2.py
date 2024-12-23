from functools import cache


USE_TEST_DATA = False
LEVELS_OF_INDIRECTION = 25


file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    print(f"{lines=}")

    # Adjacency list for main robot
    # Each neighbor is defined as (direction-to-get-to-neighbor, neighbor-value)
    RIGHT, DOWN, LEFT, UP = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
    main_robot_adj_list = {
        "A": [(LEFT, 0), (UP, 3)],
        0: [(UP, 2), (RIGHT, "A")],
        1: [(UP, 4), (RIGHT, 2)],
        2: [(LEFT, 1), (UP, 5), (RIGHT, 3), (DOWN, 0)],
        3: [(DOWN, "A"), (LEFT, 2), (UP, 6)],
        4: [(UP, 7), (RIGHT, 5), (DOWN, 1)],
        5: [(LEFT, 4), (UP, 8), (RIGHT, 6), (DOWN, 2)],
        6: [(UP, 9), (LEFT, 5), (DOWN, 3)],
        7: [(DOWN, 4), (RIGHT, 8)],
        8: [(LEFT, 7), (DOWN, 5), (RIGHT, 9)],
        9: [(LEFT, 8), (DOWN, 6)],
    }

    adj_list = {
        "A": [(LEFT, "^"), (DOWN, ">")],
        "^": [(RIGHT, "A"), (DOWN, "v")],
        "v": [(LEFT, "<"), (UP, "^"), (RIGHT, ">")],
        "<": [(RIGHT, "v")],
        ">": [(LEFT, "v"), (UP, "A")],
    }

    # def shortestPathToAction():
    #     pass

    # '<' BEFORE '^'
    # '>' BEFORE '^'
    # I think?? '<' before 'v' ?
    # So theme seems to be... go horizontal before you go vertical? But only if you can, and it doesn't interfere with
    # power moves??

    # TODO: If anything, for each one, do all combinations of a shortest path, and get smallest result :)
    # I.e. for each, do all valid permutations, and get one that is the best!
    # d = {
    #     "029A": "<A^A>^^AvvvA",
    #     "980A": "^^^A<AvvvA>A",
    #     "179A": "^<<A^^A>>AvvvA",
    #     "456A": "^^<<A>A>AvvA",
    #     "379A": "^A^^<<A>>AvvvA" # Should be <<^^, i.e. make '<' higher precendence than '^' when possible
    # } if USE_TEST_DATA else {
    #     "140A": "^<<A^A>vvA>A",
    #     "170A": "^<<A^^A>vvvA>A",
    #     "169A": "^<<A^>>A^AvvvA",
    #     "803A": "^^^<AvvvA^>AvA",
    #     "129A": "^<<A>A>^^AvvvA"
    # }

    d = (
        {
            "029A": "<A^A>^^AvvvA",
            "980A": "^^^A<AvvvA>A",
            "179A": "^<<A^^A>>AvvvA",
            "456A": "^^<<A>A>AvvA",
            "379A": "^A<<^^A>>AvvvA",  # Should be <<^^, i.e. make '<' higher precendence than '^' when possible
        }
        if USE_TEST_DATA
        else {
            "140A": "^<<A^A>vvA>A",
            "170A": "^<<A^^A>vvvA>A",
            # "169A": "^<<A^>>A^AvvvA",
            "169A": "^<<A>>^A^AvvvA",
            # "803A": "^^^<AvvvA^>AvA",
            "803A": "<^^^AvvvA^>AvA",
            "129A": "^<<A>A>^^AvvvA",
        }
    )

    # door_shortest_paths = {
    #     ("A")
    # }

    # What's
    door_shortest_paths = {
        # A (DONE!)
        ("A", "A"): ["A"],
        ("A", "0"): ["<A"],
        ("A", "1"): ["<^<A", "^<<A"],
        ("A", "2"): ["<^A", "^<A"],
        ("A", "3"): ["^A"],
        ("A", "4"): ['<^^<A', '<^<^A'] + ['^<^<A', '^<<^A', '^^<<A'],
        ("A", "5"): ['<^^A'] + ['^<^A', '^^<A'],
        ("A", "6"): ["^^A"],
        ("A", "7"): ['<^<^^A', '<^^^<A', '<^^<^A'] + ['^<<^^A', '^<^^<A', '^<^<^A', '^^<^<A', '^^<<^A', '^^^<<A'],
        ("A", "8"): ['<^^^A'] + ['^<^^A', '^^^<A', '^^<^A'],
        ("A", "9"): ["^^^A"],

        # 0 (DONE!)
        ("0", "A"): [">A"],
        ("0", "0"): ["A"],
        ("0", "1"): ["^<A"],
        ("0", "2"): ["^A"],
        ("0", "3"): [">^A", "^>A"],
        ("0", "4"): ['^^<A', '^<^A'],
        ("0", "5"): ["^^A"],
        ("0", "6"): ['^^>A', '^>^A', '>^^A'],
        ("0", "7"): ['^<^^A', '^^^<A', '^^<^A'],
        ("0", "8"): ["^^^A"],
        ("0", "9"): ['>^^^A'] + ['^>^^A', '^^^>A', '^^>^A'],

        # 1 (DONE!)
        ("1", "A"): ['>>vA', '>v>A'],
        ("1", "0"): [">vA"],
        ("1", "1"): ["A"],
        ("1", "2"): [">A"],
        ("1", "3"): [">>A"],
        ("1", "4"): ["^A"],
        ("1", "5"): ["^>A", ">^A"],
        ("1", "6"): ['>^>A', '>>^A'] + ['^>>A'],
        ("1", "7"): ["^^A"],
        ("1", "8"): ['>^^A'] + ['^^>A', '^>^A'],
        ("1", "9"): ['>>^^A', '>^^>A', '>^>^A'] + ['^>^>A', '^>>^A', '^^>>A'],

        # 2 (DONE!)
        ("2", "A"): [">vA", "v>A"],
        ("2", "0"): ["vA"],
        ("2", "1"): ["<A"],
        ("2", "2"): ["A"],
        ("2", "3"): [">A"],
        ("2", "4"): ["^<A", "<^A"],
        ("2", "5"): ["^A"],
        ("2", "6"): ["^>A", ">^A"],
        ("2", "7"): ['<^^A'] + ['^^<A', '^<^A'],
        ("2", "8"): ["^^A"],
        ("2", "9"): ['>^^A'] + ['^^>A', '^>^A'],

        # 3 (DONE!)
        ("3", "A"): ["vA"],
        ("3", "0"): ["<vA", "v<A"],
        ("3", "1"): ["<<A"],
        ("3", "2"): ["<A"],
        ("3", "3"): ["A"],
        ("3", "4"): ['<^<A', '<<^A'] + ['^<<A'],
        ("3", "5"): ["<^A", "^<A"],
        ("3", "6"): ["^A"],
        ("3", "7"): ['<<^^A', '<^^<A', '<^<^A'] + ['^<^<A', '^<<^A', '^^<<A'],
        ("3", "8"): ['<^^A'] + ['^^<A', '^<^A'],
        ("3", "9"): ["^^A"],

        # 4 (DONE!)
        ("4", "A"): ['>>vvA', '>v>vA', '>vv>A'] + ['v>>vA', 'v>v>A'],
        ("4", "0"): ['>vvA'] + ['v>vA'],
        ("4", "1"): ["vA"],
        ("4", "2"): [">vA", "v>A"],
        ("4", "3"): ['>>vA', '>v>A'] + ['v>>A'],
        ("4", "4"): ["A"],
        ("4", "5"): [">A"],
        ("4", "6"): [">>A"],
        ("4", "7"): ["^A"],
        ("4", "8"): ["^>A", ">^A"],
        ("4", "9"): ['>^>A', '>>^A'] + ['^>>A'],

        # 5 (DONE!)
        ("5", "A"): ['>vvA'] + ['v>vA', 'vv>A'],
        ("5", "0"): ["vvA"],
        ("5", "1"): ["<vA", "v<A"],
        ("5", "2"): ["vA"],
        ("5", "3"): [">vA", "v>A"],
        ("5", "4"): ["<A"],
        ("5", "5"): ["A"],
        ("5", "6"): [">A"],
        ("5", "7"): ["^<A", "<^A"],
        ("5", "8"): ["^A"],
        ("5", "9"): ["^>A", ">^A"],

        # 6 (DONE!)
        ("6", "A"): ["vvA"],
        ("6", "0"): ['<vvA'] + ['v<vA', 'vv<A'],
        ("6", "1"): ['<<vA', '<v<A'] + ['v<<A'],
        ("6", "2"): ["<vA", "v<A"],
        ("6", "3"): ["vA"],
        ("6", "4"): ["<<A"],
        ("6", "5"): ["<A"],
        ("6", "6"): ["A"],
        ("6", "7"): ['<^<A', '<<^A'] + ['^<<A'],
        ("6", "8"): ["^<A", "<^A"],
        ("6", "9"): ["^A"],

        # 7 (DONE!)
        ("7", "A"): ['>v>vvA', '>vv>vA', '>vvv>A', '>>vvvA'] + ['v>>vvA', 'v>v>vA', 'v>vv>A', 'vv>>vA', 'vv>v>A'],
        ("7", "0"): ['>vvvA'] + ['v>vvA', 'vv>vA'],
        ("7", "1"): ["vvA"],
        ("7", "2"): ['>vvA'] + ['v>vA', 'vv>A'],
        ("7", "3"): ['>v>vA', '>vv>A', '>>vvA'] + ['v>>vA', 'v>v>A', 'vv>>A'],
        ("7", "4"): ["vA"],
        ("7", "5"): [">vA", "v>A"],
        ("7", "6"): ['>v>A', '>>vA'] + ['v>>A'],
        ("7", "7"): ["A"],
        ("7", "8"): [">A"],
        ("7", "9"): [">>A"],

        # 8 (DONE!)
        ("8", "A"): ['v>vvA', 'vv>vA', 'vvv>A'] + ['>vvvA'],
        ("8", "0"): ["vvvA"],
        ("8", "1"): ['v<vA', 'vv<A'] + ['<vvA'],
        ("8", "2"): ["vvA"],
        ("8", "3"): ['v>vA', 'vv>A'] + ['>vvA'],
        ("8", "4"): ["<vA", "v<A"],
        ("8", "5"): ["vA"],
        ("8", "6"): ["v>A", ">vA"],
        ("8", "7"): ["<A"],
        ("8", "8"): ["A"],
        ("8", "9"): [">A"],

        # 9 (DONE!)
        ("9", "A"): ["vvvA"],
        ("9", "0"): ['<vvvA'] + ['v<vvA', 'vv<vA', 'vvv<A'],
        ("9", "1"): ['<v<vA', '<vv<A', '<<vvA'] + ['v<<vA', 'v<v<A', 'vv<<A'],
        ("9", "2"): ['<vvA'] + ['v<vA', 'vv<A'],
        ("9", "3"): ["vvA"],
        ("9", "4"): ['<<vA', '<v<A'] + ['v<<A'],
        ("9", "5"): ["<vA", "v<A"],
        ("9", "6"): ["vA"],
        ("9", "7"): ["<<A"],
        ("9", "8"): ["<A"],
        ("9", "9"): ["A"],
    }

    POSSIBILITIES = [
        149684280881054,
        148757066591374,
        148484855140104,
        147934623490474,
        129945784126978,
    ]
    robot_shortest_paths = {  # from, to
        # A
        ("A", "A"): ["A"],
        ("A", "^"): ["<A"],
        ("A", ">"): ["vA"],
        ("A", "v"): ["<vA", "v<A"],
        ("A", "<"): ["v<<A", "<v<A"],
        # ^
        ("^", "^"): ["A"],
        ("^", "A"): [">A"],
        ("^", "v"): ["vA"],
        ("^", ">"): ["v>A", ">vA"],
        ("^", "<"): ["v<A"],
        # <
        ("<", "<"): ["A"],
        ("<", "A"): [">>^A", ">^>A"],
        ("<", "v"): [">A"],
        ("<", ">"): [">>A"],
        ("<", "^"): [">^A"],
        # v
        ("v", "v"): ["A"],
        ("v", "A"): ["^>A", ">^A"],
        ("v", "<"): ["<A"],
        ("v", "^"): ["^A"],
        ("v", ">"): [">A"],
        # >
        (">", ">"): ["A"],
        (">", "A"): ["^A"],
        (">", "v"): ["<A"],
        (">", "<"): ["<<A"],
        # (">", "^"): "^<A",
        (">", "^"): ["<^A", "^<A"],
    }

    def plusOneLevelOfIndirection(sequence):
        res = []
        start_pos = "A"
        for symbol in sequence:
            path = robot_shortest_paths[(start_pos, symbol)]
            res.append(path)
            start_pos = symbol
        res = "".join(res)
        print(f"{len(res)=}, {addLevelsOfIndirection(sequence, 1)}")
        return res

    def addLevelsOfIndirection(sequence, levels):
        assert levels >= 0
        if levels == 0:
            return len(sequence)

        res = 0
        start_pos = "A"
        for symbol in sequence:
            # Instead of making the path larger and larger, we need to PREDICT what is going be the price we pay
            # after applying 'levels' levels of indirection onto this symbol!
            res += addLevelsOfIndirectionToSymbol(start_pos, symbol, levels)
            # new_symbols = robot_shortest_paths[(start_pos, symbol)]
            # res += addLevelsOfIndirection(new_symbols, )
            start_pos = symbol
        return res

    @cache
    def addLevelsOfIndirectionToSymbol(start_symbol, dest_symbol, levels):
        START_FROM_A = False
        assert levels >= 0
        if levels == 0:
            return 1

        return min(
            addLevelsOfIndirection(new_symbols, levels - 1)
            for new_symbols in robot_shortest_paths[(start_symbol, dest_symbol)]
        )

        new_symbols = robot_shortest_paths[(start_symbol, dest_symbol)]
        res = 0
        # for symbol in new_symbols:
        #     res += addLevelsOfIndirectionToSymbol(start_symbol, symbol, levels)
        #     start_symbol = symbol
        return addLevelsOfIndirection(new_symbols, levels - 1)

        return sum(
            addLevelsOfIndirectionToSymbol(dest_symbol, new_symbol, levels - 1)
            for new_symbol in new_symbols
        )

        if not START_FROM_A:
            new_symbols = robot_shortest_paths[(start_symbol, dest_symbol)]
            # return sum(addLevelsOfIndirection(new_symbol, levels - 1) for new_symbol in new_symbols)
            return sum(
                addLevelsOfIndirection(dest_symbol, new_symbol, levels - 1)
                for new_symbol in new_symbols
            )
        else:
            new_symbols = robot_shortest_paths[("A", dest_symbol)]
            # return sum(addLevelsOfIndirection(new_symbol, levels - 1) for new_symbol in new_symbols)
            return sum(
                addLevelsOfIndirection("A", new_symbol, levels - 1)
                for new_symbol in new_symbols
            )

    # level1 = plusOneLevelOfIndirection('<A^A>^^AvvvA')
    # print(f"{level1=}")
    # level2 = plusOneLevelOfIndirection(level1)
    # print(f"{level2=}")
    sol = {
        "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
        "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
        "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
        "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
        "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    }
    # res = 0
    # for key in d:
    #     path = d[key] # level 1!
    #     for i in range(2): # Already done first level of indirection via d!
    #         path = plusOneLevelOfIndirection(path)
    #         # print(f"level={i + 2}, {path[:20]=}")
    #     if USE_TEST_DATA:
    #         print(f"{key=}, {path == sol[key]}, {len(path)=}, path={path[:10]}...")
    #     else:
    #         print(f"{key=}, {len(path)=}, path={path[:10]}...")
    #     numeric_part = int(''.join('' if c == 'A' else c for c in key))
    #     # print(f"{numeric_part=}")
    #     res += numeric_part * len(path)

    def getAllSequencesFromKey(key):
        assert len(key) == 4
        cur_pos = "A"
        res = []
        for pos in key:
            res.append(door_shortest_paths[(cur_pos, pos)])
            cur_pos = pos
        
        assert len(res) == 4
        sequences = []
        for a in res[0]:
            for b in res[1]:
                for c in res[2]:
                    for d in res[3]:
                        sequence = "".join([a, b, c, d])
                        sequences.append(sequence)
        return sequences

    # res = 0
    # for key in d:
    #     sequence = d[key]
    #     numeric_part = int("".join("" if c == "A" else c for c in key))
    #     res += numeric_part * addLevelsOfIndirection(sequence, LEVELS_OF_INDIRECTION)

    res = 0
    for key in d:
        sequences = getAllSequencesFromKey(key)
        min_result = float("inf")
        optimal_sequence = None
        for sequence in sequences:
            new_result = addLevelsOfIndirection(sequence, LEVELS_OF_INDIRECTION)
            if new_result < min_result:
                min_result = new_result
                optimal_sequence = sequence

        print(f"{key=}, {optimal_sequence=}")
        numeric_part = int("".join("" if c == "A" else c for c in key))
        res += numeric_part * min_result

    # key = "379A" if USE_TEST_DATA else "169A"
    # for key in d:
    #     sequence = d[key]
    #     cache_res = addLevelsOfIndirection(sequence, 2)
    #     print(f"{key=}, {cache_res=}")
    

    if res >= min(POSSIBILITIES):
        string = f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!" if res > min(POSSIBILITIES) else f"!!! WARNING: ANSWER IS EQUAL !!!"
        for _ in range(3):
            print(string)

    print(f"ANSWER: {res}")

    if res >= min(POSSIBILITIES):
        string = f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!" if res > min(POSSIBILITIES) else f"!!! WARNING: ANSWER IS EQUAL !!!"
        for _ in range(3):
            print(string)
    # print(f"NEW ANSWER: {}")

    def shortestPathToSymbol(goal, main_robot, left_robot, right_robot, human):
        assert main_robot == "A" or 0 <= main_robot <= 9
        for agent in [left_robot, right_robot, human]:
            assert agent in ["A", "^", "v", "<", ">"]

    def ucs(code):
        robot_pos = "A"
