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
    
    def checkExistPath(num_bytes):
        obstacles = set(lines[:num_bytes])
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
                return True # There is a path!!!

            for dx, dy in DIRECTIONS:
                new_x, new_y = x + dx, y + dy
                if inBounds(new_x, new_y) and (new_x, new_y) not in visited and not isObstacle(new_x, new_y):
                    fringe.append((cost + 1, new_x, new_y))
                    # visited.add((new_x, new_y))
        
        return False # There is no path :(
    
    # Now, just do leftmost binary search! Essentially, you can have at minimum 0 bytes
    # fallen and at maximum len(lines) bytes fallen. At the beginning, path won't be blocked,
    # and as you keep adding bytes, eventually path will be blocked, and therefore all
    # subsequent falling bytes don't matter as the path will still be blocked. 
    l, r = 0, len(lines)
    num_bytes_needed = r
    while l <= r:
        mid = (l + r) // 2
        if not checkExistPath(mid):
            # This means there is no path, as we want, so we update our current result!
            # And then, we check for smaller indices to see if there's an even EARLIER
            # solution, i.e. set r to mid - 1 :)
            num_bytes_needed = min(num_bytes_needed, mid)
            r = mid - 1
        else:
            l = mid + 1

    index = num_bytes_needed - 1
    # Backwards since we reversed all x,y pairs for convenience inside the input parsing!
    print(f"ANSWER: {lines[index][1]},{lines[index][0]}") 