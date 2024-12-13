USE_TEST_DATA = False

from collections import deque, defaultdict

file_name = "./test_data2.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    grid = [[c for c in line.strip()] for line in file.readlines()]

    LEFT, UP, RIGHT, DOWN = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    DIRECTIONS = [LEFT, UP, RIGHT, DOWN]
    CORNER_DIRECTIONS = [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)] # tl, tr, bl, br
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
            area = 0
            corners = defaultdict(int)

            queue = deque([(i, j)])
            while len(queue) > 0:
                pos_x, pos_y = queue.popleft()

                # Populate individual position's corners!
                for dx, dy in CORNER_DIRECTIONS:
                    corners[(pos_x + dx, pos_y + dy)] += 1

                area += 1
                for dx, dy in DIRECTIONS:
                    x, y = pos_x + dx, pos_y + dy
                    if not inBounds(x, y) or (x, y) in visited:
                        continue

                    if grid[x][y] == plant:
                        queue.append((x, y))
                        visited.add((x, y))

            corners_count = 0
            for key, val in corners.items():
                # Trivial case
                if val != 2:
                    corners_count += val % 2
                    continue
                
                # assert val == 2
                # This is a special case. Either it should increase count by 0,
                # or by 2! That is, either it is touching twice as corners of the
                # same fence, or twice as corners of their own fence garden corners!
                # We can verify this by checking if the positions that touched this
                # corner, for a total of two touchings, are diagonal to one another or
                # not!
                corner_x, corner_y = key 
                plants = []
                for dx, dy in CORNER_DIRECTIONS:
                    # round because paranoia moment :P
                    x, y = round(corner_x + dx), round(corner_y + dy)
                    if not inBounds(x, y):
                        # on the edge, meaning they cannot be diagonal!
                        # so don't increment count :)
                        break
                    plants.append(grid[x][y])
                if len(plants) < 4:
                    # Again, don't increment count if on the edge
                    # (since guaranteed to be same fence touching!)
                    continue
                tl, tr, bl, br = plants
                if tl == br or bl == tr:
                    corners_count += 2


            res += area * corners_count

    print(f"ANSWER: {res}")


# _ _ _ _ _ _ _
# |             |
# |              _ 
# |                 |
# |                 |
# |              _
# |             |
# _ _ _ _ _ _ _ _

# 8 sides
# 8 corners
