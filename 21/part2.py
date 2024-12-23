from functools import cache

USE_TEST_DATA = False
LEVELS_OF_INDIRECTION = 25

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    keys = [line.strip() for line in file.readlines()]

    door_shortest_paths = { # (FROM, TO)
        # A (DONE!)
        ("A", "A"): ["A"],
        ("A", "0"): ["<A"],
        ("A", "1"): ["<^<A", "^<<A"],
        ("A", "2"): ["<^A", "^<A"],
        ("A", "3"): ["^A"],
        ("A", "4"): ["<^^<A", "<^<^A"] + ["^<^<A", "^<<^A", "^^<<A"],
        ("A", "5"): ["<^^A"] + ["^<^A", "^^<A"],
        ("A", "6"): ["^^A"],
        ("A", "7"): ["<^<^^A", "<^^^<A", "<^^<^A"]
        + ["^<<^^A", "^<^^<A", "^<^<^A", "^^<^<A", "^^<<^A", "^^^<<A"],
        ("A", "8"): ["<^^^A"] + ["^<^^A", "^^^<A", "^^<^A"],
        ("A", "9"): ["^^^A"],
        # 0 (DONE!)
        ("0", "A"): [">A"],
        ("0", "0"): ["A"],
        ("0", "1"): ["^<A"],
        ("0", "2"): ["^A"],
        ("0", "3"): [">^A", "^>A"],
        ("0", "4"): ["^^<A", "^<^A"],
        ("0", "5"): ["^^A"],
        ("0", "6"): ["^^>A", "^>^A", ">^^A"],
        ("0", "7"): ["^<^^A", "^^^<A", "^^<^A"],
        ("0", "8"): ["^^^A"],
        ("0", "9"): [">^^^A"] + ["^>^^A", "^^^>A", "^^>^A"],
        # 1 (DONE!)
        ("1", "A"): [">>vA", ">v>A"],
        ("1", "0"): [">vA"],
        ("1", "1"): ["A"],
        ("1", "2"): [">A"],
        ("1", "3"): [">>A"],
        ("1", "4"): ["^A"],
        ("1", "5"): ["^>A", ">^A"],
        ("1", "6"): [">^>A", ">>^A"] + ["^>>A"],
        ("1", "7"): ["^^A"],
        ("1", "8"): [">^^A"] + ["^^>A", "^>^A"],
        ("1", "9"): [">>^^A", ">^^>A", ">^>^A"] + ["^>^>A", "^>>^A", "^^>>A"],
        # 2 (DONE!)
        ("2", "A"): [">vA", "v>A"],
        ("2", "0"): ["vA"],
        ("2", "1"): ["<A"],
        ("2", "2"): ["A"],
        ("2", "3"): [">A"],
        ("2", "4"): ["^<A", "<^A"],
        ("2", "5"): ["^A"],
        ("2", "6"): ["^>A", ">^A"],
        ("2", "7"): ["<^^A"] + ["^^<A", "^<^A"],
        ("2", "8"): ["^^A"],
        ("2", "9"): [">^^A"] + ["^^>A", "^>^A"],
        # 3 (DONE!)
        ("3", "A"): ["vA"],
        ("3", "0"): ["<vA", "v<A"],
        ("3", "1"): ["<<A"],
        ("3", "2"): ["<A"],
        ("3", "3"): ["A"],
        ("3", "4"): ["<^<A", "<<^A"] + ["^<<A"],
        ("3", "5"): ["<^A", "^<A"],
        ("3", "6"): ["^A"],
        ("3", "7"): ["<<^^A", "<^^<A", "<^<^A"] + ["^<^<A", "^<<^A", "^^<<A"],
        ("3", "8"): ["<^^A"] + ["^^<A", "^<^A"],
        ("3", "9"): ["^^A"],
        # 4 (DONE!)
        ("4", "A"): [">>vvA", ">v>vA", ">vv>A"] + ["v>>vA", "v>v>A"],
        ("4", "0"): [">vvA"] + ["v>vA"],
        ("4", "1"): ["vA"],
        ("4", "2"): [">vA", "v>A"],
        ("4", "3"): [">>vA", ">v>A"] + ["v>>A"],
        ("4", "4"): ["A"],
        ("4", "5"): [">A"],
        ("4", "6"): [">>A"],
        ("4", "7"): ["^A"],
        ("4", "8"): ["^>A", ">^A"],
        ("4", "9"): [">^>A", ">>^A"] + ["^>>A"],
        # 5 (DONE!)
        ("5", "A"): [">vvA"] + ["v>vA", "vv>A"],
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
        ("6", "0"): ["<vvA"] + ["v<vA", "vv<A"],
        ("6", "1"): ["<<vA", "<v<A"] + ["v<<A"],
        ("6", "2"): ["<vA", "v<A"],
        ("6", "3"): ["vA"],
        ("6", "4"): ["<<A"],
        ("6", "5"): ["<A"],
        ("6", "6"): ["A"],
        ("6", "7"): ["<^<A", "<<^A"] + ["^<<A"],
        ("6", "8"): ["^<A", "<^A"],
        ("6", "9"): ["^A"],
        # 7 (DONE!)
        ("7", "A"): [">v>vvA", ">vv>vA", ">vvv>A", ">>vvvA"]
        + ["v>>vvA", "v>v>vA", "v>vv>A", "vv>>vA", "vv>v>A"],
        ("7", "0"): [">vvvA"] + ["v>vvA", "vv>vA"],
        ("7", "1"): ["vvA"],
        ("7", "2"): [">vvA"] + ["v>vA", "vv>A"],
        ("7", "3"): [">v>vA", ">vv>A", ">>vvA"] + ["v>>vA", "v>v>A", "vv>>A"],
        ("7", "4"): ["vA"],
        ("7", "5"): [">vA", "v>A"],
        ("7", "6"): [">v>A", ">>vA"] + ["v>>A"],
        ("7", "7"): ["A"],
        ("7", "8"): [">A"],
        ("7", "9"): [">>A"],
        # 8 (DONE!)
        ("8", "A"): ["v>vvA", "vv>vA", "vvv>A"] + [">vvvA"],
        ("8", "0"): ["vvvA"],
        ("8", "1"): ["v<vA", "vv<A"] + ["<vvA"],
        ("8", "2"): ["vvA"],
        ("8", "3"): ["v>vA", "vv>A"] + [">vvA"],
        ("8", "4"): ["<vA", "v<A"],
        ("8", "5"): ["vA"],
        ("8", "6"): ["v>A", ">vA"],
        ("8", "7"): ["<A"],
        ("8", "8"): ["A"],
        ("8", "9"): [">A"],
        # 9 (DONE!)
        ("9", "A"): ["vvvA"],
        ("9", "0"): ["<vvvA"] + ["v<vvA", "vv<vA", "vvv<A"],
        ("9", "1"): ["<v<vA", "<vv<A", "<<vvA"] + ["v<<vA", "v<v<A", "vv<<A"],
        ("9", "2"): ["<vvA"] + ["v<vA", "vv<A"],
        ("9", "3"): ["vvA"],
        ("9", "4"): ["<<vA", "<v<A"] + ["v<<A"],
        ("9", "5"): ["<vA", "v<A"],
        ("9", "6"): ["vA"],
        ("9", "7"): ["<<A"],
        ("9", "8"): ["<A"],
        ("9", "9"): ["A"],
    }

    robot_shortest_paths = { # (FROM, TO)
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
        (">", "^"): ["<^A", "^<A"],
    }


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
            start_pos = symbol
        return res

    @cache
    def addLevelsOfIndirectionToSymbol(start_symbol, dest_symbol, levels):
        assert levels >= 0
        if levels == 0:
            return 1

        return min(
            addLevelsOfIndirection(new_symbols, levels - 1)
            for new_symbols in robot_shortest_paths[(start_symbol, dest_symbol)]
        )


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

    res = 0
    for key in keys:
        min_result = float("inf")
        for sequence in getAllSequencesFromKey(key):
            min_result = min(min_result, addLevelsOfIndirection(sequence, LEVELS_OF_INDIRECTION))

        numeric_part = int("".join("" if c == "A" else c for c in key))
        res += numeric_part * min_result


    print(f"ANSWER: {res}")
