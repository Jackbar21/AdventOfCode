USE_TEST_DATA = False

import heapq
from collections import defaultdict, deque

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data2.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    grid = [[c for c in line] for line in lines]
    # for row in grid:
    #     print("".join(row))
    
    M, N = len(grid), len(grid[0])
    FREE_SPACE, WALL, START, END = ".", "#", "S", "E"

    RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    BUDGET = 93436 if not USE_TEST_DATA else 11048 if "2" in file_name else 7036 # from part 1!
    DELIMITER = ";"


    def turnClockwise(cur_direction):
        return (cur_direction + 1) % 4

    def turnCounterClockwise(cur_direction):
        return (cur_direction - 1) % 4

    
    # Get start and end positions
    start, end = None, None
    for i in range(M):
        for j in range(N):
            if grid[i][j] == START:
                start = (i, j)
            if grid[i][j] == END:
                end = (i, j)
    assert start is not None and end is not None
    GOAL_STATE = end

    res = 0
    visited = set()
    answers = defaultdict(list)
    # fringe = [(0, start[0], start[1], RIGHT)] # (cost, x, y, direction)
    fringe = ([(0, start[0], start[1], RIGHT, "")]) # (cost, x, y, direction, path)
    while len(fringe) > 0:
        cost, x, y, direction, path = heapq.heappop(fringe) # UCS for the fringe!
        # cost, x, y, direction, path = fringe.popleft() # BFS for the fringe!
        # if (x, y, direction) in visited:
        #     continue
        # visited.add((x, y, direction))
        if cost > BUDGET:
            # Larger than optimal cost, so not worth exploring anymore
            continue

        if (x, y) == GOAL_STATE:
            # print(f"ANSWER: {cost}")
            # answers.add(cost) 
            answers[cost].append(path)
            # exit()
            continue

        visited.add((x, y, direction)) # TODO: if too slow, remove cost

        # Now, if we can, we should add the neighbors :) The only states
        # reachable from our current state, is by taking a step forward
        # (if doesn't reach wall), or turning clockwise, or turning counterclockwise.

        # Action 1: Take step forward (if not wall!)
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if grid[new_x][new_y] != WALL and (new_x, new_y, direction) not in visited:
            # heapq.heappush(fringe, (cost + 1, new_x, new_y, direction))
            # if cost + 1 <= BUDGET or True:
                # fringe.append((cost + 1, new_x, new_y, direction, path + f"{DELIMITER}{new_x},{new_y}"))
                # visited.add((new_x, new_y, direction))
            heapq.heappush(fringe, (cost + 1, new_x, new_y, direction, path + f"{DELIMITER}{new_x},{new_y}"))
        
        # Action 2: Turn clockwise
        clockwise_direction = turnClockwise(direction)
        if (x, y, clockwise_direction) not in visited:
            # heapq.heappush(fringe, (cost + 1000, x, y, clockwise_direction))
            # if cost + 1000 <= BUDGET or True:
                # fringe.append((cost + 1000, x, y, clockwise_direction, path))
                # visited.add((x, y, clockwise_direction))
            heapq.heappush(fringe, (cost + 1000, x, y, clockwise_direction, path))
        
        # Action 3: Turn counter-clockwise
        counter_clockwise_direction = turnCounterClockwise(direction)
        if (x, y, counter_clockwise_direction) not in visited:
            # heapq.heappush(fringe, (cost + 1000, x, y, counter_clockwise_direction))
            # if cost + 1000 <= BUDGET or True:
                # fringe.append((cost + 1000, x, y, clockwise_direction, path))
                # visited.add((x, y, counter_clockwise_direction))
            heapq.heappush(fringe, (cost + 1000, x, y, counter_clockwise_direction, path))

    # raise Exception("Unreachable Code - Should have found goal state!!!")
    # print(f"{answers=}")
    # print(f"{BUDGET=}")
    assert BUDGET in answers
    optimal_visited = set([start])
    for path in answers[BUDGET]:
        # All remaining paths won't be optimal, so draw grid & exit program!
        path_arr = path[1:].split(DELIMITER)
        for i in range(len(path_arr)):
            x, y = path_arr[i].split(",")
            optimal_visited.add((int(x), int(y)))
        # pass
    # optimal_grid = grid.copy()
    # for i in range(M):
    #     for j in range(N):
    #         if (i, j) in optimal_visited:
    #             optimal_grid[i][j] = "O"
    # print(f"OPTIMAL GRID:")
    # for row in optimal_grid:
    #     print(f"{''.join(row)}")
    # print(f"{best_paths=}")
    print(f"ANSWER: {len(optimal_visited)}")
    # exit()