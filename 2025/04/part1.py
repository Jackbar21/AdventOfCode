USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    EMPTY, PAPER_ROLL = ".", "@"

    N = len(lines)
    M = len(lines[0])
    assert all(len(line) == M for line in lines)
    grid = [[pos for pos in line] for line in lines]

    inBounds = lambda i, j: 0 <= i < N and 0 <= j < M
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def countAdjacentPaperRolls(i, j):
        res = 0
        for di, dj in DIRECTIONS:
            neigh_i, neigh_j = i + di, j + dj
            if inBounds(neigh_i, neigh_j) and grid[neigh_i][neigh_j] == PAPER_ROLL:
                res += 1
        return res

    MAX_PAPER_ROLLS = 4
    res = 0
    l = []
    for i in range(N):
        for j in range(M):
            pos = grid[i][j]
            if pos != PAPER_ROLL:
                continue

            paper_rolls = countAdjacentPaperRolls(i, j)
            if paper_rolls < MAX_PAPER_ROLLS:
                res += 1

    print(f"ANSWER: {res}")
