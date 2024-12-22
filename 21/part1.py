USE_TEST_DATA = False

# class MainRobot:


# class MiddleRobot:

# class RightRobot:

# class Myself:
    

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
        "803A": "<^^^AvvvA^>AvA",
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

    def plusOneLevelOfIndirection(sequence):
        res = []
        start_pos = "A"
        for symbol in sequence:
            path = robot_shortest_paths[(start_pos, symbol)]
            res.append(path)
            start_pos = symbol
        return "".join(res)

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
    res = 0
    for key in d:
        path = d[key] # level 1!
        for _ in range(3 - 1): # Already done first level of indirection via d!
            path = plusOneLevelOfIndirection(path)
        if USE_TEST_DATA:
            print(f"{key=}, {path == sol[key]}, {len(path)=}, {path=}")
        else:
            print(f"{key=}, {len(path)=}, {path=}")
        numeric_part = int(''.join('' if c == 'A' else c for c in key))
        # print(f"{numeric_part=}")
        res += numeric_part * len(path)
    
    print(f"ANSWER: {res}")




    def shortestPathToSymbol(goal, main_robot, left_robot, right_robot, human):
        assert main_robot == "A" or 0 <= main_robot <= 9
        for agent in [left_robot, right_robot, human]:
            assert agent in ["A", "^", "v", "<", ">"]
    
        
        

    

    def ucs(code):
        robot_pos = "A"

