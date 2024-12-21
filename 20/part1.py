import collections
import heapq
import time

USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    grid = [[c for c in line] for line in lines]

    START, END, TRACK, WALL = "S", "E", ".", "#"
    M, N = len(grid), len(grid[0])

    def inBounds(x, y):
        return 0 <= x < M and 0 <= y < N

    RIGHT, DOWN, LEFT, UP = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

    start, end = None, None
    for i in range(M):
        for j in range(N):
            if grid[i][j] == START:
                start = (i, j)
            if grid[i][j] == END:
                end = (i, j)
    assert start is not None and end is not None
    GOAL_STATE = (end[0], end[1])

    res = 0
    def ucs(grid):
        fringe = collections.deque([(0, start[0], start[1])])  # (cost, node)
        visited = set()
        visited.add((start[0], start[1]))
        while len(fringe) > 0:
            cost, x, y = fringe.popleft()

            if (x, y) == GOAL_STATE:
                return cost

            for dx, dy in DIRECTIONS:
                new_x, new_y = x + dx, y + dy
                if (
                    inBounds(new_x, new_y)
                    and (new_x, new_y) not in visited
                    and grid[new_x][new_y] != WALL
                ):
                    fringe.append((cost + 1, new_x, new_y))
                    visited.add((new_x, new_y))
    SHORTEST_PATH = ucs(grid)
    GOAL_COST = SHORTEST_PATH - (100 if not USE_TEST_DATA else 10)

    START_TIME = time.time()
    for i in range(M):
        for j in range(N):
            if grid[i][j] != WALL:
                continue

            # Walls on the edges are useless to check!
            if i == 0 or i == M - 1 or j == 0 or j == N - 1:
                continue

            grid[i][j] = TRACK
            
            res += ucs(grid) <= GOAL_COST

            grid[i][j] = WALL # Backtrack!
    
    print(f"ANSWER: {res}")
    print(f"NAIVE TOTAL TIME: {time.time() - START_TIME}")