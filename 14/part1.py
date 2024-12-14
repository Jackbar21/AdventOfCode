from collections import defaultdict


USE_TEST_DATA = False



file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    ### START OF PARSING INPUT ###
    lines = [line.split() for line in file.readlines()]
    M, N = (7, 11) if USE_TEST_DATA else (103, 101)
    NUM_SECONDS = 100
    for i in range(len(lines)):
        l = list(map(lambda item: item.split("=")[1].split(","), lines[i]))
        p = tuple(int(num) for num in l[0])
        v = tuple(int(num) for num in l[1])
        lines[i] = (p, v)
        # print(f"lines[{i}]={lines[i]}")
    robots = lines
    ### END OF PARSING INPUT ###

    Q1, Q2, Q3, Q4 = 0, 1, 2, 3
    def getQuadrant(x, y):
        # Returns -1 if not in ANY quadrant!
        ban_row_index = M // 2
        ban_col_index = N // 2
        y, x = x, y # Since problem is weird, and swaps x, y position values!
        if x == ban_row_index or y == ban_col_index:
            return -1
        
        if x < ban_row_index and y < ban_col_index:
            return Q1
        
        if x < ban_row_index and y > ban_col_index:
            return Q2
        
        assert x > ban_row_index
        if y < ban_col_index:
            return Q3
        
        assert y > ban_col_index
        return Q4

    grid = [
        [0 for _ in range(N)] for _ in range(M)
    ]

    X, Y = 0, 1
    d = defaultdict(int)
    for p, v in robots:
        new_x = (p[X] + NUM_SECONDS * v[X]) % N
        new_y = (p[Y] + NUM_SECONDS * v[Y]) % M
        # print(f"{(p[X],p[Y])=}, {(v[X],v[Y])=} {new_x,new_y=}")
        grid[new_y][new_x] += 1
        quadrant = getQuadrant(new_x, new_y)
        if quadrant != -1:
            d[quadrant] += 1
    
    # for line in grid:
    #     print("".join([str(c) if c > 0 else '.' for c in line]))
    
    res = 1
    for count in d.values():
        res *= count
    print(f"ANSWER: {res}")