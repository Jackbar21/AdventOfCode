USE_TEST_DATA = True
PRINT_GRID = True  # For Debugging purposes, makes code extremely slow
from collections import defaultdict, deque

# Restarting this problem on second day, since I realize I misread the problem.
# The red tiles are given in a SPECIFIC order such that they are seperated by
# straight lines the entire way through.

# I am going to CHEESE the heck out of this problem.
# First of all (let me cook here), if we can find a SINGULAR point
# inside the polygon, then we're GOLDEN. Because then we can just
# flood-fill from that point to find all the nested green tiles.
# I'm having trouble using ray-casting to find a point inside the polygon,
# although this video was helpful: https://www.youtube.com/watch?v=RSXM9bgqxJM
# So instead, I'm gonna do something that's technically incorrect but likely
# to work: which is I'm going to take the average of all the red tile coordinates
# and use that as my likely "inside" point.


file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    lines = [tuple(map(int, line.split(","))) for line in lines]

    EMPTY, RED_TILE, GREEN_TILE = ".", "#", "o"
    NESTED_GREEN_TILE = "_"

    def getRectangleSize(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

    red_tiles = lines
    red_tiles_set = set(red_tiles)
    print(f"{len(red_tiles)=}")

    # MAX_X, MAX_Y = max(x for x, y in red_tiles), max(y for x, y in red_tiles)
    # print(f"{MAX_X=}, {MAX_Y=}")

    # Coordinate compression (since flood-fill too slow otherwise)
    def compress_coordinates(tiles):
        unique_x = sorted(set(x for x, y in tiles))
        unique_y = sorted(set(y for x, y in tiles))
        x_map = {x: i for i, x in enumerate(unique_x)}
        y_map = {y: i for i, y in enumerate(unique_y)}
        compressed_tiles = [(x_map[x], y_map[y]) for x, y in tiles]
        return compressed_tiles, unique_x, unique_y

    # compressed_red_tiles, red_unique_x, red_unique_y = compress_coordinates(red_tiles)
    # compressed_red_tiles_set = set(compressed_red_tiles)

    # # Max X and Y after compression
    # MAX_X = len(red_unique_x) - 1
    # MAX_Y = len(red_unique_y) - 1

    # def inBounds(x, y):
    #     return 0 <= x <= MAX_X and 0 <= y <= MAX_Y

    green_tiles = []
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]

        assert (x1 == x2) or (y1 == y2), "Red tiles must form straight lines"
        assert (x1, y1) != (x2, y2)

        if x1 == x2:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if (x1, y) not in red_tiles_set:
                    green_tiles.append((x1, y))
        else:
            assert y1 == y2
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if (x, y1) not in red_tiles_set:
                    green_tiles.append((x, y1))

    # compressed_green_tiles, unique_green_x, unique_green_y = compress_coordinates(
    #     green_tiles
    # )
    # compressed_green_tiles_set = set(compressed_green_tiles)
    print(f"{len(green_tiles)=}")

    red_and_green_tiles = red_tiles + green_tiles  # Doesn't include nested green tiles
    print(f"{len(red_and_green_tiles)=}")
    compressed_red_and_green_tiles, unique_x, unique_y = compress_coordinates(
        red_and_green_tiles
    )
    print(f"{len(compressed_red_and_green_tiles)=}")
    compressed_red_and_green_tiles_set = set(compressed_red_and_green_tiles)
    print(f"{len(compressed_red_and_green_tiles_set)=}")

    x_map = {x: i for i, x in enumerate(unique_x)}
    y_map = {y: i for i, y in enumerate(unique_y)}
    compressed_red_tiles = [(x_map[x], y_map[y]) for x, y in red_tiles]
    compressed_green_tiles = [(x_map[x], y_map[y]) for x, y in green_tiles]
    # compressed_red_tiles = [
    #     (unique_x.index(x), unique_y.index(y)) for x, y in red_tiles
    # ]
    # print(f"{len(compressed_red_tiles)=}")
    # compressed_green_tiles = [
    #     (unique_x.index(x), unique_y.index(y)) for x, y in green_tiles
    # ]
    # print(f"{len(compressed_green_tiles)=}")
    compressed_red_tiles_set = set(compressed_red_tiles)
    compressed_green_tiles_set = set(compressed_green_tiles)

    likely_inside_x = round(
        sum(x for x, y in compressed_red_and_green_tiles)
        / len(compressed_red_and_green_tiles)
    )
    print(f"Unique x length: {len(unique_x)}")
    likely_inside_y = round(
        sum(y for x, y in compressed_red_and_green_tiles)
        / len(compressed_red_and_green_tiles)
    )
    assert (
        likely_inside_x,
        likely_inside_y,
    ) not in compressed_red_and_green_tiles_set, (
        "Likely inside point cannot be an actual red or green tile"
    )
    print(f"Likely inside point: ({likely_inside_x}, {likely_inside_y})")

    # red_and_green_tiles = red_tiles + green_tiles  # Doesn't include nested green tiles
    # red_and_green_tiles_set = set(red_and_green_tiles)

    # likely_inside_x = round(
    #     sum(x for x, y in red_and_green_tiles) / len(red_and_green_tiles)
    # )
    # likely_inside_y = round(
    #     sum(y for x, y in red_and_green_tiles) / len(red_and_green_tiles)
    # )
    # assert (
    #     likely_inside_x,
    #     likely_inside_y,
    # ) not in red_and_green_tiles_set, (
    #     "Likely inside point cannot be an actual red or green tile"
    # )
    # print(f"Likely inside point: ({likely_inside_x}, {likely_inside_y})")

    # Now, let's flood-fill from the likely inside point to find all nested green tiles
    queue = deque()
    queue.append((likely_inside_x, likely_inside_y))
    visited = set([(likely_inside_x, likely_inside_y)])
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    MAX_X = len(unique_x) - 1
    MAX_Y = len(unique_y) - 1

    def inBounds(x, y):
        return 0 <= x <= MAX_X and 0 <= y <= MAX_Y

    while queue:
        point = queue.popleft()
        assert (
            point not in compressed_red_and_green_tiles_set
        ), "Should not be visiting actual red or green tiles"

        # This will fail if likely inside point is out of bounds!
        # Which is great in verifying whether our solution is correct or not!
        assert inBounds(*point)

        x, y = point
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if (
                neighbor not in visited
                and neighbor not in compressed_red_and_green_tiles_set
            ):
                visited.add(neighbor)
                queue.append(neighbor)

    compressed_nested_green_tiles = list(visited)
    compressed_nested_green_tiles_set = set(compressed_nested_green_tiles)
    print(f"Found nested green tiles: {len(compressed_nested_green_tiles)=}")

    def isNestedGreenTile(point):
        return point in compressed_nested_green_tiles_set

    def isTile(point):
        # return point in red_and_green_tiles_set or isNestedGreenTile(point)
        return point in compressed_red_and_green_tiles_set or isNestedGreenTile(point)

    def printGridOnScreen():
        getSymbol = lambda point: (
            RED_TILE
            if point in compressed_red_tiles_set
            else (
                GREEN_TILE
                if point in compressed_green_tiles_set
                else NESTED_GREEN_TILE if isNestedGreenTile(point) else EMPTY
            )
        )

        grid = [[getSymbol((x, y)) for x in range(MAX_X + 2)] for y in range(MAX_Y + 2)]
        grid[likely_inside_y][likely_inside_x] = "!"  # Mark likely inside point
        for x, y in compressed_red_tiles:
            grid[y][x] = RED_TILE
        for x, y in compressed_green_tiles:
            grid[y][x] = GREEN_TILE

        print()
        for row in grid:
            print(" ".join(row))
        print()

    # Even if PRINT_GRID = True, only allow this in test mode -- since too slow otherwise
    if PRINT_GRID and USE_TEST_DATA:
        printGridOnScreen()

    res = 0
    # Opposite corners chosen MUST be red tiles
    for i in range(len(compressed_red_tiles)):
        tile1 = compressed_red_tiles[i]
        x1, y1 = tile1
        for j in range(i + 1, len(compressed_red_tiles)):
            tile2 = compressed_red_tiles[j]
            x2, y2 = tile2

            needed1 = (x1, y2)
            needed2 = (x2, y1)
            if isTile(needed1) and isTile(needed2):
                # size = getRectangleSize(tile1, tile2)
                width = unique_x[max(x1, x2)] - unique_x[min(x1, x2)] + 1
                height = unique_y[max(y1, y2)] - unique_y[min(y1, y2)] + 1
                size = width * height

                if res < size:
                    res = size

    print(f"ANSWER: {res}")
