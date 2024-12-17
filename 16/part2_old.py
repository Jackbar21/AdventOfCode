USE_TEST_DATA = True

import heapq

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    grid = [[c for c in line] for line in lines]
    # for row in grid:
    #     print("".join(row))
    
    M, N = len(grid), len(grid[0])
    FREE_SPACE, WALL, START, END = ".", "#", "S", "E"

    RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    BUDGET = 93436 if USE_TEST_DATA else 11048 if "2" in file_name else 7036 # from part 1!

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
    DELIMITER = ";"
    
    optimal_visited = set()
    def ucs(best_path_cost: int, best_paths: set) -> tuple[int, set]:
        res = 0
        visited = set()
        
        fringe = [(0, start[0], start[1], RIGHT, "")] # (cost, x, y, direction, path)
        while len(fringe) > 0:
            cost, x, y, direction, path = heapq.heappop(fringe) # UCS for the fringe!
            # if (x, y, direction) in visited:
            #     continue
            visited.add((x, y, direction))

            if (x, y) == GOAL_STATE:
                if path in best_paths:
                    continue
                # best_paths.add(path)
                
                # print(f"{cost=}, {best_path_cost}")
                if cost > best_path_cost:
                    # All remaining paths won't be optimal, so draw grid & exit program!
                    # optimal_grid = grid.copy()
                    # for i in range(M):
                    #     for j in range(N):
                    #         if (i, j) in optimal_visited:
                    #             optimal_grid[i][j] = "O"
                    # print(f"OPTIMAL GRID:")
                    # for row in optimal_grid:
                    #     print(f"{''.join(row)}")
                    # print(f"{best_paths=}")
                    # print(f"{len(optimal_visited)=}")
                    # exit()
                    continue
                # if cost > best_path_cost:
                #     return None
                
                assert cost <= best_path_cost
                best_path_cost = cost
                best_paths.add(path)

                path_arr = path[1:].split(DELIMITER)
                for i in range(len(path_arr)):
                    x, y = path_arr[i].split(",")
                    optimal_visited.add((int(x), int(y)))

                print(f"ANSWER: {cost}")
                print(f"{path=}")
                # print(f"{path_arr=}")
                # print(f"{optimal_visited=}")
                # exit()
                # continue
                return (best_path_cost, best_paths)

            # Now, if we can, we should add the neighbors :) The only states
            # reachable from our current state, is by taking a step forward
            # (if doesn't reach wall), or turning clockwise, or turning counterclockwise.

            # Action 1: Take step forward (if not wall!)
            dx, dy = DIRECTIONS[direction]
            new_x, new_y = x + dx, y + dy
            if grid[new_x][new_y] != WALL and (new_x, new_y, direction) not in visited:
                heapq.heappush(fringe, (cost + 1, new_x, new_y, direction, path + f"{DELIMITER}{x},{y}"))
                visited.add((new_x, new_y, direction))
            
            # Action 2: Turn clockwise
            clockwise_direction = turnClockwise(direction)
            if (x, y, clockwise_direction) not in visited:
                heapq.heappush(fringe, (cost + 1000, x, y, clockwise_direction, path))
                visited.add((x, y, clockwise_direction))
            
            # Action 3: Turn counter-clockwise
            counter_clockwise_direction = turnCounterClockwise(direction)
            if (x, y, counter_clockwise_direction) not in visited:
                heapq.heappush(fringe, (cost + 1000, x, y, counter_clockwise_direction, path))
                visited.add((x, y, counter_clockwise_direction))


        # raise Exception("Unreachable Code - Should have found goal state!!!")
        optimal_grid = grid.copy()
        for i in range(M):
            for j in range(N):
                if (i, j) in optimal_visited:
                    optimal_grid[i][j] = "O"
        print(f"OPTIMAL GRID:")
        for row in optimal_grid:
            print(f"{''.join(row)}")
        print(f"{best_paths=}")
        print(f"{len(optimal_visited)=}")
        exit()

    best_path_cost = float("inf")
    best_paths = set()
    while True:
        best_path_cost, best_paths = ucs(best_path_cost, best_paths)