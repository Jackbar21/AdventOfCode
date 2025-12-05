USE_TEST_DATA = False

from collections import deque

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    ###########################
    ### START PARSING INPUT ###
    ###########################
    lines = [line.strip().split(",") for line in file.readlines()]
    for i in range(len(lines)):
        x, y = lines[i]
        lines[i] = (int(x), int(y))[::-1]
    
    NUM_BYTES = 12 if USE_TEST_DATA else 1024
    N = 6 if USE_TEST_DATA else 70
    GOAL_STATE = (N, N)
    #########################
    ### END PARSING INPUT ###
    #########################
    
    obstacles = set(lines[:NUM_BYTES])
    def isObstacle(x, y):
        assert inBounds(x, y)
        return (x, y) in obstacles
    def inBounds(x, y):
        return 0 <= x <= N and 0 <= y <= N

    RIGHT, DOWN, LEFT, UP = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

    # BFS (since each "edge" has same cost of 1!)
    visited = set()
    fringe = deque([(0, 0, 0)]) # (cost, x, y)
    while len(fringe) > 0:
        cost, x, y = fringe.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == GOAL_STATE:
            print(f"ANSWER: {cost}")
            exit()

        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if inBounds(new_x, new_y) and (new_x, new_y) not in visited and not isObstacle(new_x, new_y):
                fringe.append((cost + 1, new_x, new_y))
                # visited.add((new_x, new_y))
    
    raise Exception("Unreachable Code!!!")