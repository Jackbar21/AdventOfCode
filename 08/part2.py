from collections import defaultdict
USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    grid = [[c for c in line.strip()] for line in file.readlines()]

    antennas = defaultdict(list)
    antinodes = set()

    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == ".":
                continue
            
            antennas[grid[i][j]].append((i, j))
    
    def inBounds(i, j):
        return 0 <= i < m and 0 <= j < n
    
    for antenna in antennas:
        positions = antennas[antenna]
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # We need to grab the slope.
                (x1, y1), (x2, y2) = sorted([positions[i], positions[j]])

                rise = y2 - y1
                run = x2 - x1
                # slope = rise / run
                run, rise = -run, -rise
                
                # Keep adding antinodes while you can!
                x, y = x1 - run, y1 - rise
                while inBounds(x, y):
                    antinodes.add((x, y))
                    x -= run
                    y -= rise
                
                x, y = x2 + run, y2 + rise 
                while inBounds(x, y):
                    antinodes.add((x, y))
                    x += run
                    y += rise
    
    # for x, y in antinodes:
    #     grid[x][y] = "#" if grid[x][y] == "." else grid[x][y]
    # for line in grid:
    #     print(line)
    print(f"ANSWER: {len(antinodes)}")
