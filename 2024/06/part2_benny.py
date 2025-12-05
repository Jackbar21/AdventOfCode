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
                if grid[i][j] == "^":
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

    initial_pos = getGuardPosition()

    def getVisitedSpots(guard_position):
        cur_direction = UP
        cur_pos = guard_position
        r, c = cur_pos  # always the guard's current position!
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
        return visited

    res = 0
    # for i in range(m):
    #     for j in range(n):
    # Instead of looping over EVERY single index in grid, loop over only those
    # that the guard visits in the first place! Because if it does NOT visit a
    # position in the first place, then why bother checking if adding an obstacle
    # there will cause the guard to go in a loop, because we can tell for sure that
    # it won't (since again, the guard never visits that spot!!!)
    visited = getVisitedSpots(initial_pos)
    for i, j in visited:
        if grid[i][j] != ".":
            continue

        # tmp = grid[i][j]
        grid[i][j] = "#"

        ###################
        ### LOGIC START ###
        ###################
        cur_direction = UP
        r, c = initial_pos  # always the guard's current position!
        # visited = set()
        obstacles_visited = set()  # (x, y, direction)
        while True:
            # Add current position to seen set!
            # if (r, c) not in visited or True:
            #     grid[r][c] = 'X'
            # visited.add((r, c))

            # Get new position of guard
            dx, dy = DIRECTION_DELTAS[cur_direction]
            x, y = r + dx, c + dy

            # Once guard goes out of bounds, we terminate!
            if not inBounds(x, y):
                break

            # If obstacle, turn right 90 degrees instead of moving forwards!
            if isObstacle(x, y):
                if (x, y, cur_direction) in obstacles_visited:
                    res += 1
                    break
                obstacles_visited.add((x, y, cur_direction))
                cur_direction = getNextDirection(cur_direction)
                continue

            # Loop Invariant (in case no obstacle was hit!!)
            r, c = x, y
        ###################
        #### LOGIC END ####
        ###################
        # Backtrack!
        grid[i][j] = "."

    print(f"ANSWER: {res}")

    # print(f"ANSWER: {len(visited)}")
