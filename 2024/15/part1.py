import collections


USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data2.txt"
with open(file_name, "r") as file:
    ###########################
    ### START PARSING INPUT ###
    ###########################
    lines = [line.strip() for line in file.readlines()]
    grid, moves = None, None
    for i, line in enumerate(lines):
        if line == "":
            # print("TRUE")
            # print(f"{lines[:i]=}")
            # print(f"{lines[i+1:]=}")
            grid = [collections.deque([el for el in line]) for line in lines[:i]]
            moves = "".join(lines[i+1:])
    #########################
    ### END PARSING INPUT ###
    #########################

    ROBOT, OBSTACLE, WALL, FREE_SPACE = "@", "O", "#", "."
    move_to_direction = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    M, N = len(grid), len(grid[0])

    def inBounds(x, y):
        return 0 <= x < M and 0 <= y < N

    # First, get robot's position
    robot_x, robot_y = None, None
    for i in range(M):
        if robot_x != None and robot_y != None:
            break
        for j in range(N):
            if grid[i][j] == ROBOT:
                robot_x, robot_y = i, j
                break
    assert robot_x != None and robot_y != None

    # Now, simulate all of the robots moves!
    for move in moves:
        assert grid[robot_x][robot_y] == ROBOT
        assert move in move_to_direction
        dx, dy = move_to_direction[move]
        # print(f"{move, dx, dy}")
        x, y = robot_x + dx, robot_y + dy
        assert inBounds(x, y)
        symbol = grid[x][y]
        if symbol == FREE_SPACE:
            # Change robot's position to x,y, since it's free to go to!
            assert grid[robot_x][robot_y] == ROBOT
            assert grid[x][y] == FREE_SPACE
            grid[x][y] = ROBOT
            grid[robot_x][robot_y] = FREE_SPACE
            robot_x, robot_y = x, y
            continue

        assert symbol != FREE_SPACE
        # if symbol == ROBOT:
        #     print("WEIRD GRID")
        #     print(f"{robot_x, robot_y=}, {x, y=}, {dx, dy=}")
        #     for line in grid:
        #         print("".join(line))
        assert symbol != ROBOT
        assert symbol in [OBSTACLE, WALL]
        if symbol == WALL:
            # Don't change robot's position!
            continue 
            
        assert symbol == OBSTACLE
        # Now, at this point, we want to check in the current direction, whether
        # we hit an FREE_SPACE or WALL character first (could be many obstacles
        # in between!) If a WALL character is hit first, then we cannot move the
        # obstacles, and hence we just continue. Otherwise, we have to begin moving!
        while grid[x][y] not in [FREE_SPACE, WALL]:
            x += dx
            y += dy
            assert inBounds(x, y)
        
        if grid[x][y] == WALL:
            continue

        # Now consider this. We hit a free space before we hit a wall. In between the
        # robot and this free space, there are p >= 1 obstacles in between. All we have to
        # do, is take a sequence such as "@(O){p}." --> ".@(O){p}"
        # ['@', 'O', ..., 'O', '.'] --> ['.', '@', 'O', ..., 'O']

        # Want to make grid[x][y] go from '.' to 'O'
        assert grid[x][y] == FREE_SPACE
        grid[x][y] = OBSTACLE
        # Want to make grid[robot_x][robot_y] go from '@' to '.'
        assert grid[robot_x][robot_y] == ROBOT
        grid[robot_x][robot_y] = FREE_SPACE
        # Want to make grid[robot_x + dx][robot_y + dy] go from 'O' to '@'
        assert grid[robot_x + dx][robot_y + dy] == OBSTACLE
        grid[robot_x + dx][robot_y + dy] = ROBOT
        
        # Loop Invariant
        robot_x, robot_y = robot_x + dx, robot_y + dy
        continue

    # print("NEW GRID:")
    # for line in grid:
    #     print("".join(line))
    
    res = 0
    for i in range(M):
        for j in range(N):
            if grid[i][j] == OBSTACLE:
                res += 100 * i + j
    print(f"ANSWER: {res}")
