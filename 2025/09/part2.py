USE_TEST_DATA = False
PRINT_GRID = False # For Debugging purposes
from collections import defaultdict
import heapq

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    lines = [tuple(map(int, line.split(","))) for line in lines]

    RED_TILE, GREEN_TILE = "#", "X"
    NESTED_GREEN_TILE = GREEN_TILE

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
    
    # Now do it again to fill in gaps between green tiles
    #
    # 1. Row-by-row
    green_tiles_set = set(green_tiles)
    nested_green_tiles = []
    d = defaultdict(list)
    for x, y in green_tiles:
        d[x].append(y)
    MAX_X = max(d.keys())
    for x in d:
        min_red, max_red = min(d[x]), max(d[x])
        for y in range(min_red, max_red + 1):
            if (x, y) not in green_tiles_set:
                nested_green_tiles.append((x, y))
    # 2. Col-by-col
    d = defaultdict(list)
    for x, y in green_tiles:
        d[y].append(x)
    MAX_Y = max(d.keys())
    for y in d:
        min_red, max_red = min(d[y]), max(d[y])
        for x in range(min_red, max_red + 1):
            if (x, y) not in green_tiles_set:
                nested_green_tiles.append((x, y))

    def printGridOnScreen():
        grid = [['.' for _ in range(MAX_X + 2)] for _ in range(MAX_Y + 2)]
        for x, y in red_tiles:
            grid[y][x] = RED_TILE
        for x, y in green_tiles:
            grid[y][x] = GREEN_TILE
        for x, y in nested_green_tiles:
            grid[y][x] = NESTED_GREEN_TILE

        print()
        for row in grid:
            print(" ".join(row))
        print()
    
    if PRINT_GRID:
        printGridOnScreen()
    
    res = 0
    all_tiles = red_tiles + green_tiles + nested_green_tiles
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
            if needed1 in all_tiles_set and needed2 in all_tiles_set:
                size = getRectangleSize(tile1, tile2)
                if res < size:
                    res = size

    print(f"ANSWER: {res}")
