USE_TEST_DATA = True

from collections import deque, defaultdict

file_name = "./test_data2.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    grid = [[c for c in line.strip()] for line in file.readlines()]

    DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    LEFT, UP, RIGHT, DOWN = DIRECTIONS
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
            sides = set()
            sides_extra = 0
            used = set()

            queue = deque([(i, j)])
            while len(queue) > 0:
                pos_x, pos_y = queue.popleft()
                area += 1
                for direction in DIRECTIONS:
                    dx, dy = direction
                    x, y = pos_x + dx, pos_y + dy

                    if not (inBounds(x, y) and grid[x][y] == plant):
                        # We're going in dx, dy change
                        # So check if someone has already tried going from
                        # x,y and by dx,dy, or better yet from x+dx,y+dy by -dx,-dy

                        if (pos_x, pos_y, dx, dy) in used or (pos_x+dx, pos_y+dy, -dx, -dy) in used:
                            pass
                        else:
                            perimiter += 1
                        used.add((pos_x, pos_y, dx, dy))

                        # if direction in [LEFT, RIGHT]:
                        #     # if (y, direction) in sides:
                        #     #     # add extra if uncontested!
                        #     #     can_add = True
                        #     #     for dx, dy in [UP, DOWN]:
                        #     #         new_x, new_y = x + dx, y + dy
                        #     #         if inBounds(new_x, new_y) and grid[new_x][new_y] == plant:
                        #     #             can_add = False
                        #     #             break
                        #     #     sides_extra += can_add


                        #     sides.add((y, direction))
                        # else:
                        #     sides.add((x, direction))

                    if (x, y) in visited:
                        #  perimiter += grid[x][y] != plant
                         continue
                    
                    if not inBounds(x, y):
                        #  perimiter += 1
                         continue
                    
                    if grid[x][y] == plant:
                         queue.append((x, y))
                         visited.add((x, y))
                    # else:
                    #      perimiter += 1

                
            print(f"{plant=}, {area=}, {perimiter=}, {len(sides)=}, {sides_extra=}")
            # print(f"{used=}, {len(used)=}")
            # res += area * perimiter
            print(f"{sides=}\n")
            res += area * len(sides)

    print(f"ANSWER: {res}")
