USE_TEST_DATA = False

from collections import deque, defaultdict

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    grid = [[c for c in line.strip()] for line in file.readlines()]

    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    M, N = len(grid), len(grid[0])
    def inBounds(i, j):
        return 0 <= i < M and 0 <= j < N

    res = 0
    visited = set()
    for i in range(M):
        for j in range(N):
            if (i, j) in visited:
                 continue
            
            plant = grid[i][j]
            visited.add((i, j))
            area, perimiter = 0, 0

            queue = deque([(i, j)])
            while len(queue) > 0:
                pos_x, pos_y = queue.popleft()
                area += 1
                for dx, dy in DIRECTIONS:
                    x, y = pos_x + dx, pos_y + dy
                    if (x, y) in visited:
                         perimiter += grid[x][y] != plant
                         continue
                    
                    if not inBounds(x, y):
                         perimiter += 1
                         continue
                    
                    if grid[x][y] == plant:
                         queue.append((x, y))
                         visited.add((x, y))
                    else:
                         perimiter += 1

                
            # print(f"{plant=}, {area=}, {perimiter=}")
            res += area * perimiter

    print(f"ANSWER: {res}")
