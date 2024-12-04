file_name = "./data.txt"
with open(file_name, "r") as file:
    grid = file.readlines()
    m = len(grid)
    n = len(grid[0]) - 1 # -1 due to '\n' character!

    def inBounds(i, j):
        return 0 <= i < m and 0 <= j < n

    DIRECTIONS = [
        [-1, 0],    # up
        [1, 0],     # down
        [0, -1],    # left
        [0, 1],     # right
        # And the four diagonal directions!
        [-1, -1],
        [-1, 1],
        [1, -1],
        [1, 1]
    ]
    
    res = 0
    for i in range(m):
        for j in range(n):
            letter = grid[i][j]
            if letter != "X":
                continue
            
            # Count number of times "XMAS" substring appears at this position,
            # for a maximum of 8 (i.e. up, down, left, right, and the 4 diagonals!)
            # assert letter == "X"
            
            for dx, dy in DIRECTIONS:
                x, y = i, j
                letters = []
                for _ in range(4):        
                    if not inBounds(x, y):
                        break
                    letters.append(grid[x][y])
                    
                    # Loop Invariant
                    x += dx
                    y += dy
                
                res += "".join(letters) == "XMAS"

    print(f"ANSWER: {res}")