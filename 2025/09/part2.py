USE_TEST_DATA = False

# I spent two days on this problem, and eventually got frustrated and used AI help
# to get a working solution. The key insight is to use the Ray Casting Algorithm
# to determine if a point is inside the polygon formed by the red tiles.

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    lines = [tuple(map(int, line.split(","))) for line in lines]
    red_tile_coords = lines

    def is_inside(px, py, poly_coords):
        """
        Ray Casting Algorithm to determine if a point (px, py) is strictly inside
        the polygon defined by poly_coords.
        """
        n = len(poly_coords)
        is_in = False

        # Iterate over all segments (x1, y1) -> (x2, y2)
        for i in range(n):
            (x1, y1) = poly_coords[i]
            (x2, y2) = poly_coords[(i + 1) % n]

            # Check if the horizontal ray from (px, py) intersects the segment
            # Condition: The segment must straddle the ray's y-level (py)
            # We must use strict inequalities to handle boundary cases correctly.
            if (y1 <= py < y2) or (y2 <= py < y1):
                # Calculate intersection x-coordinate (based on line equation)
                x_intersect = x1 + (py - y1) / (y2 - y1) * (x2 - x1)

                # If the intersection is to the right of the point, it's a valid crossing
                if px < x_intersect:
                    is_in = not is_in
        return is_in

    # 1. Coordinate Compression
    x_coords = set(x for x, y in red_tile_coords)
    y_coords = set(y for x, y in red_tile_coords)

    sorted_x = sorted(list(x_coords))
    sorted_y = sorted(list(y_coords))

    x_map = {x: i for i, x in enumerate(sorted_x)}
    y_map = {y: i for i, y in enumerate(sorted_y)}

    # W and H are the dimensions of the compressed *region* grid (cells, not lines)
    W = len(sorted_x) - 1
    H = len(sorted_y) - 1

    compressed_red = [(x_map[x], y_map[y]) for x, y in red_tile_coords]

    # 2. Identify Interior Regions (Compressed Cells) using Ray Casting

    # region_type[i][j] stores the type of the region defined by
    # [sorted_x[i], sorted_x[i+1]) x [sorted_y[j], sorted_y[j+1])
    # 1 = Interior (Green/Allowed), 2 = Exterior (Not Allowed)
    region_type = [[0] * H for _ in range(W)]

    for i in range(W):
        for j in range(H):
            # Use a test point strictly inside the region (e.g., +1 from the lower-left corner)
            tx = sorted_x[i] + 1
            ty = sorted_y[j] + 1

            if is_inside(tx, ty, red_tile_coords):
                region_type[i][j] = 1  # Interior
            else:
                region_type[i][j] = 2  # Exterior

    # 3. Find the Largest Valid Rectangle
    res = 0
    num_red = len(compressed_red)

    # Iterate through all pairs of red tiles as opposite corners
    for i in range(num_red):
        for j in range(i + 1, num_red):
            (x1_c, y1_c) = compressed_red[i]
            (x2_c, y2_c) = compressed_red[j]

            # 3.1. Calculate Original Area
            x_min_c, x_max_c = min(x1_c, x2_c), max(x1_c, x2_c)
            y_min_c, y_max_c = min(y1_c, y2_c), max(y1_c, y2_c)

            # The rectangle spans from one coordinate to the next.
            x_start_orig = sorted_x[x_min_c]
            x_end_orig = sorted_x[x_max_c]
            y_start_orig = sorted_y[y_min_c]
            y_end_orig = sorted_y[y_max_c]

            # Width and Height are inclusive of both ends
            width = x_end_orig - x_start_orig + 1
            height = y_end_orig - y_start_orig + 1
            area = width * height

            if area <= res:
                continue

            # 3.2. Check Validity against Compressed Regions
            is_valid_rectangle = True

            # The rectangle covers compressed regions from x_min_c to x_max_c-1 and y_min_c to y_max_c-1
            # We must check all *internal* regions covered by the rectangle.
            for x_c in range(x_min_c, x_max_c):
                for y_c in range(y_min_c, y_max_c):

                    # Safety check: Ensure the region index is valid
                    if not (0 <= x_c < W and 0 <= y_c < H):
                        # If the rectangle extends beyond the polygon's bounding box
                        # in a way that includes an undefined (exterior) region, it's invalid.
                        is_valid_rectangle = False
                        break

                    # If a region covered by the rectangle is EXTERIOR (2), the rectangle is invalid.
                    if region_type[x_c][y_c] == 2:
                        is_valid_rectangle = False
                        break
                if not is_valid_rectangle:
                    break

            # 3.3. Update Max Area
            if is_valid_rectangle:
                res = max(res, area)

    print(f"ANSWER: {res}")
