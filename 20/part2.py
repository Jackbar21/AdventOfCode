import collections
from functools import cache

USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    grid = [[c for c in line] for line in lines]

    START, END, TRACK, WALL = "S", "E", ".", "#"
    M, N = len(grid), len(grid[0])

    def inBounds(x, y):
        return 0 <= x < M and 0 <= y < N

    RIGHT, DOWN, LEFT, UP = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

    adj_list = collections.defaultdict(list)
    start, end = None, None
    for i in range(M):
        for j in range(N):
            if grid[i][j] == START:
                start = (i, j)
            if grid[i][j] == END:
                end = (i, j)
    # assert start is not None and end is not None

    @cache
    def bfs(i, j):
        fringe = collections.deque([(0, i, j)]) # (cost, x, y)
        visited = set()
        visited.add((i, j))
        while len(fringe) > 0:
            cost, x, y = fringe.popleft()

            if (x, y) == end:
                return cost

            for dx, dy in DIRECTIONS:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) not in visited and grid[new_x][new_y] != WALL:
                    visited.add((new_x, new_y))
                    fringe.append((cost + 1, new_x, new_y))

    SHORTEST_PATH = bfs(start[0], start[1])
    GOAL_COST = SHORTEST_PATH - (100 if not USE_TEST_DATA else 50)

    # Idea: BFS our way through EEEEEEEEEVERY track inside of the graph, keeping track of the cost it's taken to get there
    # (and marking as visited for the future). From each uniquely visited track, grab all of it's "cheatable" neighbors and
    # then dictate the cheat as valid if and only if the current cost, plus the cost of the cheat, plus the cost remaining
    # to the end node without cheating, is ALL <= GOAL_COST (i.e. shortest original path cost - 100 for real input data)
    found_cheats = set()
    fringe = collections.deque([(0, start[0], start[1])]) # (cost, x, y)
    visited = set()
    visited.add((start[0], start[1]))
    while len(fringe) > 0:
        cost, x, y = fringe.popleft()
        if cost > GOAL_COST:
            continue
        print(f"{len(found_cheats)=}")

        # No termination case, want to visit ALLLLLLLLL of the TRACKS!!!!
        for dx, dy in DIRECTIONS:
            neigh_x, neigh_y = x + dx, y + dy
            # assert inBounds(neigh_x, neigh_y)
            if (neigh_x, neigh_y) in visited or grid[neigh_x][neigh_y] == WALL:
                continue
            visited.add((neigh_x, neigh_y))
            fringe.append((cost + 1, neigh_x, neigh_y))
        
        # Now, check for ALL the cheats from this starting position! If any of them yield a valid solution, i.e. have
        # total cost <= GOAL_COST, add them to found_cheats set :) These should NOT be added to fringe for visitation,
        # the results should be immediately calculated from THIS point for efficiency sake!

        # Add as a neighbor, every square that is at most 20 away from (x, y), and ends at a non-wall position
        # assert grid[x][y] != WALL
        queue = collections.deque(
            [(0, x, y)]
        )  # (path_len, cheat_x, cheat_y)
        vis = set()
        vis.add((x, y))
        while len(queue) > 0:
            path_len, cheat_x, cheat_y = queue.popleft()
            cheat_id = f"{x, y}-->{cheat_x, cheat_y}"
            if path_len > 20:
                continue  # Invalid!
            if (
                inBounds(cheat_x, cheat_y)
                and grid[cheat_x][cheat_y] != WALL
                and (x, y) != (cheat_x, cheat_y) # Since we need to shave off >0 picoseconds!
            ):  # Last picosecond of cheat can NOT be at a wall!!!
                # assert cheat_id not in found_cheats
                full_cost = cost + path_len + bfs(cheat_x, cheat_y)
                if full_cost <= GOAL_COST:
                    found_cheats.add(cheat_id)

            for dx, dy in DIRECTIONS:
                new_x, new_y = cheat_x + dx, cheat_y + dy
                if inBounds(new_x, new_y) and (new_x, new_y) not in vis:
                    vis.add((new_x, new_y))
                    queue.append((path_len + 1, new_x, new_y))

    print(f"ANSWER: {len(found_cheats)}")
