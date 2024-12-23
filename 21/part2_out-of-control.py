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
        9: [(LEFT, 8), (DOWN, 6)]
    }

    adj_list = {
        "A": [(LEFT, '^'), (DOWN, '>')],
        "^": [(RIGHT, "A"), (DOWN, "v")],
        "v": [(LEFT, "<"), (UP, "^"), (RIGHT, ">")],
        "<": [(RIGHT, "v")],
        ">": [(LEFT, "v"), (UP, "A")]
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

    d = {
        "029A": "<A^A>^^AvvvA",
        "980A": "^^^A<AvvvA>A",
        "179A": "^<<A^^A>>AvvvA",
        "456A": "^^<<A>A>AvvA",
        "379A": "^A<<^^A>>AvvvA" # Should be <<^^, i.e. make '<' higher precendence than '^' when possible
    } if USE_TEST_DATA else {
        "140A": "^<<A^A>vvA>A",
        "170A": "^<<A^^A>vvvA>A",
        # "169A": "^<<A^>>A^AvvvA",
        "169A": "^<<A>>^A^AvvvA",
        # "803A": "^^^<AvvvA^>AvA",
        "803A": "<^^^AvvvA>^AvA",
        "129A": "^<<A>A>^^AvvvA"
    }


    # What's 
    door_shortest_paths = {
        # A
        # 0
        # 1
        # 2
        # 3
        # 4
        # 5
        # 6
        # 7
        # 8
        # 9
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
        # (">", "^"): "^<A",
        (">", "^"): "<^A",
    }

    @cache
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

    # @cache
    # def plusOneLevelOfIndirection(sequence, levels):
    #     assert levels >= 1
    #     res = []
    #     start_pos = "A"
    #     for symbol in sequence:
    #         path = robot_shortest_paths[(start_pos, symbol)]
    #         res.append(path)
    #         start_pos = symbol
    #     res = "".join(res)
    #     print(f"{len(res)=}, {addLevelsOfIndirection(sequence, 1)}")
    #     return res
        
    #     res = []
    #     start_pos = "A"

    # def plusOneLevelOfIndirectionHelper(arr)
    
    
    # def addLevelsOfIndirectionOptimized(sequence, levels):
    #     assert levels >= 1
    #     res = 0
    #     start_pos = "A"
    #     for symbol in sequence:



    def addLevelsOfIndirection(sequence, levels):
        assert levels >= 0
        if levels == 0:
            return (len(sequence), "A")

        res = 0
        start_pos = "A"
        for symbol in sequence:
            # Instead of making the path larger and larger, we need to PREDICT what is going be the price we pay
            # after applying 'levels' levels of indirection onto this symbol!
            val, new_symbol = addLevelsOfIndirectionToSymbol(start_pos, symbol, levels)
            res += val
            start_pos = new_symbol
            continue
            # res += addLevelsOfIndirectionToSymbol(start_pos, symbol, levels)
            # new_symbols = robot_shortest_paths[(start_pos, symbol)]
            # res += addLevelsOfIndirection(new_symbols, )
            start_pos = symbol
        return res
    
    @cache
    def addLevelsOfIndirectionToSymbol(start_symbol, dest_symbol, levels):
        START_FROM_A = False
        assert levels >= 0
        if levels == 0:
            return (1, dest_symbol)
        
        new_symbols = robot_shortest_paths[(start_symbol, dest_symbol)]
        res = 0
        # for symbol in new_symbols:
        #     res += addLevelsOfIndirectionToSymbol(start_symbol, symbol, levels)
        #     start_symbol = symbol
        return addLevelsOfIndirection(new_symbols, levels - 1)

        return sum(addLevelsOfIndirectionToSymbol(dest_symbol, new_symbol, levels - 1) for new_symbol in new_symbols)


        if not START_FROM_A:
            new_symbols = robot_shortest_paths[(start_symbol, dest_symbol)]
            # return sum(addLevelsOfIndirection(new_symbol, levels - 1) for new_symbol in new_symbols)
            return sum(addLevelsOfIndirection(dest_symbol, new_symbol, levels - 1) for new_symbol in new_symbols)
        else:
            new_symbols = robot_shortest_paths[("A", dest_symbol)]
            # return sum(addLevelsOfIndirection(new_symbol, levels - 1) for new_symbol in new_symbols)
            return sum(addLevelsOfIndirection("A", new_symbol, levels - 1) for new_symbol in new_symbols)
        


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
    #     for i in range(LEVELS_OF_INDIRECTION): # Already done first level of indirection via d!
    #         path = plusOneLevelOfIndirection(path)
    #         # print(f"level={i + 2}, {path[:20]=}")
    #     if USE_TEST_DATA:
    #         print(f"{key=}, {path == sol[key]}, {len(path)=}, path={path[:10]}...")
    #     else:
    #         print(f"{key=}, {len(path)=}, path={path[:10]}...")
    #     numeric_part = int(''.join('' if c == 'A' else c for c in key))
    #     # print(f"{numeric_part=}")
    #     res += numeric_part * len(path)
    
    res = 0
    for key in d:
        sequence = d[key]
        numeric_part = int(''.join('' if c == 'A' else c for c in key))
        res += numeric_part * addLevelsOfIndirection(sequence, LEVELS_OF_INDIRECTION)
    
    
    # key = "379A" if USE_TEST_DATA else "169A"
    # for key in d:
    #     sequence = d[key]
    #     cache_res = addLevelsOfIndirection(sequence, 2)
    #     print(f"{key=}, {cache_res=}")
    
    possibilities = [149684280881054, 148757066591374, 148484855140104]
    
    if res >= min(possibilities):
        print(f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!")
        print(f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!")
        print(f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!")

    print(f"ANSWER: {res}")
    
    

    if res >= min(possibilities):
        print(f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!")
        print(f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!")
        print(f"!!! WARNING: ANSWER IS WAY TOO HIGH !!!")
    # print(f"NEW ANSWER: {}")




    def shortestPathToSymbol(goal, main_robot, left_robot, right_robot, human):
        assert main_robot == "A" or 0 <= main_robot <= 9
        for agent in [left_robot, right_robot, human]:
            assert agent in ["A", "^", "v", "<", ">"]
    
        
        

    

    def ucs(code):
        robot_pos = "A"

