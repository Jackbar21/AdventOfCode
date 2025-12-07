USE_TEST_DATA = False
import collections

# Looking at test data & input data, there's never a case of two side-by-side splitters,
# so we don't have to worry about such edge case.

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    N, M = len(lines), len(lines[0])
    EMPTY, SPLITTER = ".", "^"
    assert all(len(line) == M for line in lines)
    inBounds = lambda i, j: 0 <= i < N and 0 <= j < M
    grid = lines

    memo = {}
    
    # Computes number of ways for particle to descend from position (i, j)
    def dp(i, j):
        if (i, j) in memo:
            return memo[(i, j)]

        if not inBounds(i, j):
            return 0

        below_x, below_y = i + 1, j
        if not inBounds(below_x, below_y):
            return 1 # Final position

        res = (
            dp(below_x, below_y - 1) + dp(below_x, below_y + 1)
            if grid[below_x][below_y] == SPLITTER
            else dp(below_x, below_y)
        )

        memo[(i, j)] = res
        return res

    r, c = 0, lines[0].index("S")
    res = dp(r, c)

    print(f"ANSWER: {res}")
