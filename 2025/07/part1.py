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

    r, c = 0, lines[0].index("S")
    queue = collections.deque([(r, c)])
    visited = set()
    res = 0  # num splits
    while queue:
        x, y = queue.popleft()

        # Base Case
        if not inBounds(x, y):
            continue

        # Base Case
        if (x, y) in visited:
            continue
        visited.add((x, y))

        below_x, below_y = x + 1, y
        if not inBounds(below_x, below_y):
            continue  # Can't go down

        if grid[below_x][below_y] == SPLITTER:
            res += 1
            queue.append((below_x, below_y - 1))
            queue.append((below_x, below_y + 1))
        else:
            queue.append((below_x, below_y))

    print(f"ANSWER: {res}")
