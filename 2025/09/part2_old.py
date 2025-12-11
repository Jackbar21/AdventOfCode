USE_TEST_DATA = False
PRINT_GRID = True  # For Debugging purposes, makes code extremely slow
from collections import defaultdict

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    lines = [tuple(map(int, line.split(","))) for line in lines]

    EMPTY, RED_TILE, GREEN_TILE = ".", "#", "X"
    NESTED_GREEN_TILE = "X"

    def getRectangleSize(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

    red_tiles = lines
    red_tiles_set = set(red_tiles)
    green_tiles = []

    # Need to also include green tiles
    # We can do this by going row-by-row, then col-by-col
    #
    # 1. Row-by-row
    d = defaultdict(list)
    for x, y in red_tiles:
        d[x].append(y)
    MAX_X = max(d.keys())
    for x in d:
        min_red, max_red = min(d[x]), max(d[x])
        for y in range(min_red, max_red + 1):
            if (x, y) not in red_tiles_set:
                green_tiles.append((x, y))
    # 2. Col-by-col
    d = defaultdict(list)
    for x, y in red_tiles:
        d[y].append(x)
    MAX_Y = max(d.keys())
    for y in d:
        min_red, max_red = min(d[y]), max(d[y])
        for x in range(min_red, max_red + 1):
            if (x, y) not in red_tiles_set:
                green_tiles.append((x, y))

    red_and_green_tiles = red_tiles + green_tiles  # Doesn't include nested green tiles
    red_and_green_tiles_set = set(red_and_green_tiles)

    # We could now repeat the same process to find all NESTED
    # green tiles, but this is too slow for part2.
    #
    # Since we cannot populate all the nested green tiles in reasonable time, we need
    # a function that quickly tells us whether a point is indeed a nested green tile.
    # Now that we have all the red tile and non-nested green tile coordinates, we can
    # do this by tracking the min & max X values for each Y, and similarly the min & max
    # Y values for each X. Then for any point (x,y), we can simply check if x is between
    # the min & max x for Y=y, and similarly that y is between min & max y for X=x.
    #
    # We can achieve this by constructing four dictionaries:
    # 1. Two dicts to get min & max y for each x
    # 2. Two dicts to get min & max x for each y
    min_x, max_x = defaultdict(lambda: float("inf")), defaultdict(
        lambda: float("-inf")
    )  # for each y
    min_y, max_y = defaultdict(lambda: float("inf")), defaultdict(
        lambda: float("-inf")
    )  # for each x
    for x, y in red_and_green_tiles:
        min_x[y] = min(min_x[y], x)
        max_x[y] = max(max_x[y], x)

        min_y[x] = min(min_y[x], y)
        max_y[x] = max(max_y[x], y)

    def isNestedGreenTile(point):
        x, y = point
        return min_x[y] <= x <= max_x[y] and min_y[x] <= y <= max_y[x]

    def isTile(point):
        return point in red_and_green_tiles_set or isNestedGreenTile(point)

    def printGridOnScreen():
        getSymbol = lambda point: (
            RED_TILE if point in red_tiles_set
            else GREEN_TILE if point in red_and_green_tiles_set
            else NESTED_GREEN_TILE if isNestedGreenTile(point)
            else EMPTY
        )

        grid = [[getSymbol((x, y)) for x in range(MAX_X + 2)] for y in range(MAX_Y + 2)]
        for x, y in red_tiles:
            grid[y][x] = RED_TILE
        for x, y in green_tiles:
            grid[y][x] = GREEN_TILE

        print()
        for row in grid:
            print(" ".join(row))
        print()

    # Even if PRINT_GRID = True, only allow this in test mode -- since too slow otherwise
    if PRINT_GRID and USE_TEST_DATA:
        printGridOnScreen()

    res = 0
    all_tiles = red_tiles + green_tiles
    all_tiles_set = set(all_tiles)

    # Opposite corners chosen MUST be red tiles
    N = len(red_tiles)
    for i in range(N):
        tile1 = red_tiles[i]
        x1, y1 = tile1
        for j in range(i + 1, N):
            tile2 = red_tiles[j]
            x2, y2 = tile2

            needed1 = (x1, y2)
            needed2 = (x2, y1)
            if isTile(needed1) and isTile(needed2):
                size = getRectangleSize(tile1, tile2)
                if res < size:
                    res = size

    print(f"ANSWER: {res}")
