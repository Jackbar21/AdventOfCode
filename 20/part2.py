import collections
import heapq
import time


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    grid = [[c for c in line] for line in lines]
    # for line in grid:
    #     # print("".join(line))

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
            if grid[i][j] == WALL:
                continue

            if grid[i][j] == START:
                start = (i, j)
            if grid[i][j] == END:
                end = (i, j)

            for dx, dy in DIRECTIONS:
                x, y = i + dx, j + dy
                if inBounds(x, y):
                    if grid[x][y] != WALL:
                        adj_list[(i, j)].append((1, None, x, y))
                        # adj_list[(i, j)].append((None, x + M, y + N))
                        adj_list[(i + M, j + N)].append((1, None, x + M, y + N))

                    # No matter what, even if (x, y) is a wall, we can traverse THROUGH IT
                    # into "clonged graph". This is Vassos Hadzilacos trick from UofT ;)
                    if True:
                        # Add as a neighbor, every square that is at most 20 away from (i, j), and ends at a non-wall position
                        queue = collections.deque(
                            [(1, x, y)]
                        )  # (path_len, cheat_x, cheat_y)
                        vis = set()
                        vis.add((i, j))
                        vis.add((x, y))
                        while len(queue) > 0:
                            path_len, cheat_x, cheat_y = queue.popleft()
                            if path_len > 20:
                                continue  # Invalid!
                            if (
                                inBounds(cheat_x, cheat_y)
                                and grid[cheat_x][cheat_y] != WALL
                            ):  # Last picosecond of cheat can NOT be at a wall!!!
                                adj_list[(i, j)].append(
                                    (
                                        path_len,
                                        f"{i, j}-->{cheat_x, cheat_y}",
                                        cheat_x + M,
                                        cheat_y + N,
                                    )
                                )

                            for dx, dy in DIRECTIONS:
                                new_x, new_y = cheat_x + dx, cheat_y + dy
                                if inBounds(new_x, new_y) and (new_x, new_y) not in vis:
                                    vis.add((new_x, new_y))
                                    queue.append((path_len + 1, new_x, new_y))

                        # for delta_x, delta_y in DIRECTIONS:
                        #     cheat_x, cheat_y = (x + delta_x, y + delta_y)
                        #     if inBounds(cheat_x, cheat_y) and grid[cheat_x][cheat_y] != WALL and (cheat_x, cheat_y) != (i, j):
                        #         # First element is the UNIQUE cheat of this path! I.e. similar to where they place
                        #         # '1' and '2' in problem description :)
                        #         # adj_list[(i, j)].append((2, f"{x + M, y + N}-->{cheat_x + M, cheat_y + N}", cheat_x + M, cheat_y + N))
                        #         adj_list[(i, j)].append((2, f"{i, j}-->{cheat_x + M, cheat_y + N}", cheat_x + M, cheat_y + N))

    # For graph G', this will represent essentially a clone of original graph,
    # but now for every path u->v, we'll introduce an edge from u->v' of cost 1,
    # regardless of whether position v is a wall or not! For every node u with
    # coordinates (i, j), we'll denote u' with coordinates (i + M, j + N)
    # # print(f"{adj_list=}")
    # exit()
    # for i in range(M):
    #     for j in range(N):

    assert start is not None and end is not None
    GOAL_STATE = (end[0] + M, end[1] + N)
    SHORTEST_PATH = 84 if USE_TEST_DATA else 9484
    GOAL_COST = SHORTEST_PATH - (100 if not USE_TEST_DATA else 50)
    # # print(f"{adj_list=}")

    banned = set()

    res = []
    fringe = [(0, start, None)]  # (cost, node, cheat_node)
    # fringe = collections.deque(fringe)
    visited = set()
    START_TIME = time.time()
    while len(fringe) > 0:
        # print(f"{fringe=}")
        cost, node, cheat_node = heapq.heappop(fringe)
        assert cheat_node is None or len(cheat_node) > 0
        # cost, node, cheat_node = fringe.popleft()

        if node in visited:
            continue
        visited.add(node)
        # if node[0] < M:
        #     visited.add(node)

        # # print(f"{node=}")
        # # print(f"{adj_list[node]}")
        if node == GOAL_STATE:
            # # print(f"SHORTEST PATH: {cost}")
            # # print(f"{M=}, {N=}")
            if cost > GOAL_COST:
                print(f"ANSWER: {len(banned)}")
                # print(f"{banned=}")
                print(f"VASSOS TOTAL TIME: {time.time() - START_TIME}")
                exit()
            else:
                fringe = [(0, start, None)]
                visited.clear()
                assert cheat_node is not None
                assert cheat_node not in banned
                banned.add(cheat_node)
                print(f"{len(banned)=}")
                continue
            # visited.remove(GOAL_STATE)

        for edge_cost, neighbor_cheat_node, neighbor_x, neighbor_y in adj_list[node]:
            # print(f"{neighbor_cheat_node, neighbor_x, neighbor_y=}")
            neighbor = (neighbor_x, neighbor_y)
            if neighbor not in visited:
                # edge_cost = 1 + int(neighbor_cheat_node is not None)
                assert not (neighbor_cheat_node and cheat_node)
                new_cheat_node = neighbor_cheat_node if not cheat_node else cheat_node
                # new_cheat_node = cheat_node if edge_cost != 2 else neighbor
                if new_cheat_node not in banned:
                    heapq.heappush(fringe, (cost + edge_cost, neighbor, new_cheat_node))

                # if edge_cost == 2:
                #     if new_cheat_node not in banned:
                #         fringe.append((cost + edge_cost, neighbor, new_cheat_node))
                # else:
                #     fringe.appendleft((cost + edge_cost, neighbor, new_cheat_node))

    print(f"TERMINATED")
    exit()

    # fringe = [(True, 0, start[0], start[1])] # (cost, can_disable, x, y)
    # visited = set()
    # while len(fringe) > 0:
    #     can_disable, cost, x, y = heapq.heappop(fringe)

    #     if (x, y) in visited:
    #         continue
    #     if (x, y) != GOAL_STATE:
    #         visited.add((x, y))

    #     if (x, y) == GOAL_STATE and not can_disable:
    #         # print(f"SHORTEST PATH: {cost}")
    #         # exit()

    #     for dx, dy in DIRECTIONS:
    #         new_x, new_y = x + dx, y + dy
    #         if not inBounds(new_x, new_y):
    #             continue

    #         if can_disable:
    #             # heapq.heappush(fringe, (cost + 1, False, new_x, new_y))
    #             for delta_x, delta_y in DIRECTIONS:
    #                 cheat_x, cheat_y = new_x + delta_x, new_y + delta_y
    #                 if inBounds(cheat_x, cheat_y):
    #                     heapq.heappush(fringe, (False, cost + 2, cheat_x, cheat_y))

    #         if grid[new_x][new_y] != WALL:
    #             heapq.heappush(fringe, (can_disable, cost + 1, new_x, new_y))
