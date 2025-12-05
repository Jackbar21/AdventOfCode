USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    grid = [[int(digit) for digit in line.strip()] for line in file.readlines()]

    M, N = len(grid), len(grid[0])
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    START_STATE = 0
    GOAL_STATE = 9

    def inBounds(i, j):
        return 0 <= i < M and 0 <= j < N

    def dfs(grid, i, j):
        assert grid[i][j] == 0
        goal_positions = set() # i.e. (i', j') positions of 9s reached from original (i, j)!
        
        stack = [(i, j)]
        while len(stack) > 0:
            x, y = stack.pop()
            if grid[x][y] == GOAL_STATE:
                goal_positions.add((x, y))
            
            for dx, dy in DIRECTIONS:
                new_x, new_y = x + dx, y + dy
                if inBounds(new_x, new_y) and grid[new_x][new_y] == grid[x][y] + 1:
                    stack.append((new_x, new_y))
        
        return len(goal_positions)



    res = 0
    for i in range(M):
        for j in range(N):
            if grid[i][j] != START_STATE:
                continue
                
            # Count number of 9s reachable from this 0!
            res += dfs(grid, i, j)
    
    print(f"ANSWER: {res}")