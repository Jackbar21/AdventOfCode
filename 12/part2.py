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
            area, perimiter = 0, 0
            local_visited = set([(i, j)])
            fence_visited = set([])
            corners = defaultdict(int)
            corners_count = 0

            queue = deque([(i, j)])
            while len(queue) > 0:
                pos_x, pos_y = queue.popleft()

                # Populate individual position's corners!
                for dx, dy in CORNER_DIRECTIONS:
                    corners[(pos_x + dx, pos_y + dy)] += 1

                # for vert, horiz in [
                #     [DOWN, RIGHT], # bottom-right corner (br)
                #     [DOWN, LEFT],  # bottom-left  corner (bl)
                #     [UP, LEFT],    # top-left     corner (tl)
                #     [UP, RIGHT],   # top-right    corner (tr)
                # ]:
                #     dx_v, dy_v = vert
                #     dx_h, dy_h = horiz

                #     x, y = pos_x + dx_v, pos_y + dy_v
                #     if inBounds(x, y) and grid[x][y] == plant:
                #         # Irrelevant corner, ignore it!
                #         continue
                    
                #     x, y = pos_x + dx_h, pos_y + dy_h
                #     if inBounds(x, y) and grid[x][y] == plant:
                #         # Irrelevant corner, ignore it!
                #         continue
                    
                #     dx = (dx_v + dx_h) / 2
                #     dy = (dy_v + dy_h) / 2
                #     corners[(pos_x + dx, pos_y + dy)] += 1

                area += 1
                for dx, dy in DIRECTIONS:
                    x, y = pos_x + dx, pos_y + dy
                    fence_x, fence_y = pos_x + (dx / 2), pos_y + (dy / 2)
                    if (x, y) in visited:
                        perimiter += grid[x][y] != plant
                        if grid[x][y] != plant:
                            fence_visited.add((fence_x, fence_y))
                        continue

                    if not inBounds(x, y):
                        perimiter += 1
                        fence_visited.add((fence_x, fence_y))
                        continue

                    if grid[x][y] == plant:
                        queue.append((x, y))
                        local_visited.add((x, y))
                        visited.add((x, y))
                    else:
                        perimiter += 1
                        fence_visited.add((fence_x, fence_y))

            # print(f"{plant=}, {area=}, {perimiter=}")
            # print(f"{plant=}, {sorted(local_visited)=}")
            # print(f"{plant=}, {sorted(fence_visited)=}")
            # print(f"{len(fence_visited)=}, {perimiter=}\n")
            # print(f"{plant=}")
            count = 0 # valid corners!
            for key, val in corners.items():
                assert 1 <= val <= 4
                if val == 4:
                    continue
                if val == 1 or val == 3:
                    count += 1
                    continue

                assert val == 2
                # This is a special case. Either it should increase count by 0,
                # or by 2! That is, either it is touching twice as corners of the
                # same fence, or twice as corners of their own fence garden corners!
                # We can verify this by checking if the positions that touched this
                # corner, for a total of two touchings, are diagonal to one another or
                # not!
                corner_x, corner_y = key 
                # if key == (2.5, 2.5):
                #     count += 2
                plants = []
                for dx, dy in CORNER_DIRECTIONS:
                    # round because paranoia moment :P
                    x, y = round(corner_x + dx), round(corner_y + dy)
                    if not inBounds(x, y):
                        # on the edge, meaning they cannot be diagonal!
                        # so don't increment count :)
                        break
                    # positions.append((x, y))
                    plants.append(grid[x][y])
                # assert len(plants) == 4
                if len(plants) < 4:
                    # on the edge, meaning they cannot be diagonal!
                    # so don't increment count :)
                    continue
                # print(f"{plants=}")
                tl, tr, bl, br = plants
                if tl == br or bl == tr:
                    count += 2
                # else:
                #     assert tl == tr or bl == br
                


            single_corners = {key: val for key, val in corners.items() if val % 2 == 1}
            # print(f"{single_corners=}")
            # print(f"{len(single_corners)=}")
            # res += area * perimiter
            res += area * count
            # res += area * corners_count

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
