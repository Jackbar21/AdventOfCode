file_name = "./data.txt"
with open(file_name, "r") as file:
    grid = file.readlines()
    m = len(grid)
    n = len(grid[0]) - 1  # -1 due to '\n' character!

    def inBounds(i, j):
        return 0 <= i < m and 0 <= j < n

    DIRECTIONS = [
        [-1, 0],  # up
        [1, 0],  # down
        [0, -1],  # left
        [0, 1],  # right
        # And the four diagonal directions!
        [-1, -1],
        [-1, 1],
        [1, -1],
        [1, 1],
    ]

    res = 0
    for i in range(m):
        for j in range(n):
            letter = grid[i][j]
            if letter != "A":
                continue

            # Check if we're in a X-MAS position centered at (i, j) being the "A" character!
            pos_diag = [
                (i + 1, j - 1),
                (i - 1, j + 1),
            ]
            neg_diag = [
                (i - 1, j - 1),
                (i + 1, j + 1),
            ]

            # All positions must be in bounds of the matrix!
            if not all(
                map(
                    lambda pos: inBounds(pos[0], pos[1]),
                    pos_diag + neg_diag,
                )
            ):
                continue
                
            # If forms X-MAS shape, increment result by 1!
            pos_letters = list(map(lambda pair: grid[pair[0]][pair[1]], pos_diag))
            neg_letters = list(map(lambda pair: grid[pair[0]][pair[1]], neg_diag))
            res += sorted(pos_letters) == sorted(neg_letters) == ['M', 'S']

    print(f"ANSWER: {res}")
