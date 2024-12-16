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

    # print("OG GRID:")
    # for line in grid:
    #     print("".join(line))
    # print()

    ROBOT, OBSTACLE, WALL, FREE_SPACE = "@", "O", "#", "."
    OBSTACLE_LEFT, OBSTACLE_RIGHT = "[", "]"
    def getOppositeObstacle(obstacle):
        assert obstacle in [OBSTACLE_LEFT, OBSTACLE_RIGHT]
        return OBSTACLE_LEFT if obstacle != OBSTACLE_LEFT else OBSTACLE_RIGHT

    LEFT, UP, DOWN, RIGHT = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    move_to_direction = {
        '^': UP,
        'v': DOWN,
        '<': LEFT,
        '>': RIGHT
    }
    
    # Now, modify the grid as is appropriate for part 2
    for i in range(len(grid)):
        new_line = []
        for item in grid[i]:
            if item in [WALL, FREE_SPACE]:
                for _ in range(2):
                    new_line.append(item)
            elif item == OBSTACLE:
                new_line.append('[')
                new_line.append(']')
            else:
                assert item == ROBOT
                new_line.append('@')
                new_line.append('.')
        grid[i] = new_line
    
    M, N = len(grid), len(grid[0])
    def inBounds(x, y):
        return 0 <= x < M and 0 <= y < N
    
    # print("TRANSFORMED GRID:")
    # for line in grid:
    #     print("".join(line))

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
        # print(f"{robot_x, robot_y=}")
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
        # assert symbol in [OBSTACLE, WALL]
        if symbol == WALL:
            # Don't change robot's position!
            continue 

        assert symbol in [OBSTACLE_LEFT, OBSTACLE_RIGHT]
        # opposite_directions = [LEFT, RIGHT] if dx == 0 else [UP, DOWN]
        # dx1, dy1 = opposite_directions[0]
        # dx2, dy2 = opposite_directions[1]
        
        # Easy case is when we're going horizontally (i.e. dx == 0), since we can't push two boxes from one!
        # So, let's handle this case first :)
        
        if dx == 0:
            while grid[x][y] not in [FREE_SPACE, WALL]:
                assert grid[x][y] in [OBSTACLE_LEFT, OBSTACLE_RIGHT]
                x += dx
                y += dy
                assert inBounds(x, y)
            
            if grid[x][y] == WALL:
                continue
            
            # This logic will cause us to start flipping obstacle arrangements 
            # (i.e. from '[]' to '][' and vice versa). This is okay as long as we
            # recognize they are different, for the rest of the problem :)
            obstacle = grid[robot_x + dx][robot_y + dy]
            assert obstacle in [OBSTACLE_LEFT, OBSTACLE_RIGHT]
            grid[robot_x + dx][robot_y + dy] = ROBOT

            # Want to make grid[x][y] go from '.' to 'O'
            assert grid[x][y] == FREE_SPACE
            grid[x][y] = obstacle # Again, this will cause the '[]' to '][' weird flipping & vice versa
            # Want to make grid[robot_x][robot_y] go from '@' to '.'
            
            # Want to make grid[robot_x][robot_y] go from '@' to '.'
            assert grid[robot_x][robot_y] == ROBOT
            grid[robot_x][robot_y] = FREE_SPACE

            # Continue, since this is only the dx == 0 case!
            # print("NEW GRID:")
            # for line in grid:
            #     print("".join(line))
            
            # Loop Invariant
            robot_x, robot_y = robot_x + dx, robot_y + dy

            # TODO: Consider removing... FIX UP THE OBSTACLE ORIENTATIONS! -- THIS IS GOOD, BUT TAKES LINEAR TIME!!!
            tmp_x, tmp_y = robot_x + dx, robot_y + dy
            # while grid[x][y] not in [FREE_SPACE, WALL]:
            while (tmp_x, tmp_y) != (x, y):
                assert grid[tmp_x][tmp_y] in [OBSTACLE_LEFT, OBSTACLE_RIGHT]
                grid[tmp_x][tmp_y] = OBSTACLE_LEFT if grid[tmp_x][tmp_y] != OBSTACLE_LEFT else OBSTACLE_RIGHT 
                tmp_x += dx
                tmp_y += dy
                assert inBounds(tmp_x, tmp_y)
            grid[tmp_x][tmp_y] = OBSTACLE_LEFT if grid[tmp_x][tmp_y] != OBSTACLE_LEFT else OBSTACLE_RIGHT 
            # print("NEW GRID:")
            # for line in grid:
            #     print("".join(line))
            continue

        assert dx != 0
        # So now at this point, since we're moving vertically, it is quite very much possible to move 2 boxes from
        # 1 at a time, resulting into even larger chains (i.e. 1 box pushes 2, which push 4, which push 8, etc.). 
        # We can tell how many boxes are to be pushed from one by going +dy in the y coordinate, and checking that
        # it is of the OPPOSITE obstacle type. For instance:
        #   [][]
        #    [] --> the aligned obstacles (vertically) are opposite to one another!
        # And essentially, we are limited by the box that hits a wall the soonest. If any of the boxes (which we
        # can check recursively) immediately hit a wall, then we cannot move. Otherwise, we will move every such
        # obstacle :)

        # Step 1: Check if it's even possible to move a step in dx,dy direction!
        visited = set()
        def isPossible(obstacle_x, obstacle_y, dx, dy):
            if grid[obstacle_x][obstacle_y] != OBSTACLE_LEFT:
                left_x, left_y = obstacle_x, obstacle_y - 1
                assert inBounds(left_x, left_y) and grid[left_x][left_y] == OBSTACLE_LEFT
                return isPossible(left_x, left_y, dx, dy)

            left_x, left_y = obstacle_x, obstacle_y
            assert grid[left_x][left_y] == OBSTACLE_LEFT
            right_x, right_y = obstacle_x, obstacle_y + 1
            assert grid[right_x][right_y] == OBSTACLE_RIGHT

            visited.add((left_x, left_y, OBSTACLE_LEFT))
            visited.add((right_x, right_y, OBSTACLE_RIGHT))

            # Check left
            x, y = left_x + dx, left_y + dy
            if grid[x][y] == WALL:
                return False
            elif grid[x][y] in [OBSTACLE_LEFT, OBSTACLE_RIGHT]:
                if not isPossible(x, y, dx, dy):
                    return False
            else:
                assert grid[x][y] == FREE_SPACE
            
            # Check right
            x, y = right_x + dx, right_y + dy
            if grid[x][y] == WALL:
                return False
            elif grid[x][y] in [OBSTACLE_LEFT, OBSTACLE_RIGHT]:
                if not isPossible(x, y, dx, dy):
                    return False
            else:
                assert grid[x][y] == FREE_SPACE
            
            # If both of them didn't return impossible, then return True cause must be FREE_SPACE!
            return True

        obstacle_x, obstacle_y = robot_x + dx, robot_y + dy
        visited.clear()
        if not isPossible(obstacle_x, obstacle_y, dx, dy):
            continue
        
        assert len(visited) > 0
        assert (obstacle_x, obstacle_y, grid[obstacle_x][obstacle_y]) in visited
        # Now that we know it's possible to move everything up/down, we need to actually DO SO. So we'll mark
        # every "visited" obstacle character as a FREE_SPACE now, and then for each position the obstacles would
        # now end up in, i.e. by a change of dx,dy, we "re-draw" that obstacle character. And then at the end, of
        # course, we need to update the robot's position as well:
        # print("BEFORE GRID:")
        # for line in grid:
        #     print("".join(line))

        # print("SAHSJKAHSKAHKSL")
        # print(f"{visited=}")
        # for (i, j) in visited:
        #     print(f"{grid[i][j]=}, {i,j=}")
        # exit()
        # Step 1: Make all FREE_SPACE
        for (i, j, _) in visited:
            assert grid[i][j] in [OBSTACLE_LEFT, OBSTACLE_RIGHT]
            grid[i][j] = FREE_SPACE
        
        # Step 2: Redraw obstacles to new postitions
        for (i, j, obstacle_char) in visited:
            x, y = i + dx, j + dy
            grid[x][y] = obstacle_char
        
        # Step 3: Redraw robot!
        assert grid[robot_x][robot_y] == ROBOT
        assert grid[robot_x + dx][robot_y + dy] == FREE_SPACE
        grid[robot_x][robot_y] = FREE_SPACE
        grid[robot_x + dx][robot_y + dy] = ROBOT
        robot_x, robot_y = robot_x + dx, robot_y + dy

        # print("AFTER GRID:")
        # for line in grid:
        #     print("".join(line))

        # exit()
        continue
        
        # if grid[obstacle_x][obstacle_y] == OBSTACLE_RIGHT:
        #     obstacle_y -= 1
        #     assert grid[obstacle_x][obstacle_y] == OBSTACLE_LEFT
        # left_x, left_y, right_x, right_y = None, None, None, None
        # if grid[obstacle_x][obstacle_y] == OBSTACLE_LEFT:
        #     left_x, left_y = obstacle_x, obstacle_y
        #     right_x, right_y = obstacle_x, obstacle_y + 1
        # else:
        #     assert grid[obstacle_x][obstacle_y] == OBSTACLE_RIGHT
        #     left_x, left_y = obstacle_x, obstacle_y - 1
        #     right_x, right_y = obstacle_x, obstacle_y
        
        
        is_possible = True
        queue = collections.deque([(left_x, left_y), (right_x, right_y)])
        visited = set([(left_x, left_y), (right_x, right_y)])
        while len(queue) > 0:
            x, y = queue.popleft()
            new_x, new_y = x + dx, y + dy
            if grid[x][y] == getOppositeObstacle(grid[new_x][new_y]):
                is_left_obstacle = grid[x][y] == OBSTACLE_LEFT
        

        break
        exit()




        # Below is old part 1 logic, so stop!
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
            if grid[i][j] == OBSTACLE_LEFT:
                res += 100 * i + j
    print(f"ANSWER: {res}")


# . [][][] .
# . . [] . .

# .  [][]  .
# . . [] . .