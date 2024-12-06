USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = file.readlines()
    lines = list(map(lambda line: line.strip(), lines))
    lines = list(map(lambda line: [char for char in line], lines))
    grid = lines

    m, n = len(grid), len(grid[0])
    # Find position of guard
    def getGuardPosition():
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '^':
                    return (i, j)
        raise Exception("No such position!")

    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
    DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
    DIRECTION_DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    def getNextDirection(direction):
        return DIRECTIONS[(direction + 1) % len(DIRECTIONS)]
    def inBounds(x, y):
        return 0 <= x < m and 0 <= y < n
    
    def isObstacle(x, y):
        return grid[x][y] == "#"
    
    cur_direction = UP
    cur_pos = getGuardPosition()
    r, c = cur_pos # always the guard's current position!
    visited = set()
    while True:
        # Add current position to seen set!
        # if (r, c) not in visited or True:
        #     grid[r][c] = 'X'
        visited.add((r, c))
        

        # Get new position of guard
        dx, dy = DIRECTION_DELTAS[cur_direction]
        x, y = r + dx, c + dy

        # Once guard goes out of bounds, we terminate!
        if not inBounds(x, y):
            break
        
        # If obstacle, turn right 90 degrees instead of moving forwards!
        if isObstacle(x, y):
            cur_direction = getNextDirection(cur_direction)
            continue
        
        # Loop Invariant (in case no obstacle was hit!!)
        r, c = x, y

    print(f"ANSWER: {len(visited)}")
