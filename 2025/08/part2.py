USE_TEST_DATA = False
import heapq

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    lines = list(map(lambda line: tuple(map(int, line.split(","))), lines))

    # Returns cartesian distance squared between two 3D points
    def distance(point1, point2):
        x1, y1, z1 = point1
        x2, y2, z2 = point2

        dx, dy, dz = x1 - x2, y1 - y2, z1 - z2
        return dx * dx + dy * dy + dz * dz

    points = lines
    N = len(points)
    distances = []  # (distance, point1, point2)
    for i in range(N):
        for j in range(i + 1, N):
            dist = distance(points[i], points[j])
            distances.append((dist, points[i], points[j]))
    heapq.heapify(distances)

    # This is a connected components problem, and part 2 will likely require prim's or kruskal's algorithm
    # to construct minimum spanning trees connecting all circuits with minimum total distance.
    #
    # EDIT: I was wrong, the ask is to instead keep using next shortest connection until one giant circuit
    # is formed, not to find the most optimal means of doing so. This will require keeping track of the
    # number of connected components, which we can do via union-find.
    parent = {node: node for node in points}
    rank = {node: 0 for node in points}
    size = {node: 1 for node in points}

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]  # path compression
            node = parent[node]
        return node

    def union(a, b):
        root_a, root_b = find(a), find(b)

        if root_a == root_b:
            return False

        if rank[root_a] < rank[root_b]:
            parent[root_a] = root_b
            size[root_b] += size[root_a]
        elif rank[root_a] > rank[root_b]:
            parent[root_b] = root_a
            size[root_a] += size[root_b]
        else:
            parent[root_b] = root_a
            size[root_a] += size[root_b]
            rank[root_a] += 1  # only increment when equally tall

        return True

    # Keep adding shortest connections until all points are connected
    res = None
    while len(distances) > 0:
        dist, p1, p2 = heapq.heappop(distances)
        union(p1, p2)
        if max(size[find(p1)], size[find(p2)]) == N:
            # All points are now connected
            x1, _, _ = p1
            x2, _, _ = p2
            res = x1 * x2
            break

    assert res is not None
    print(f"ANSWER: {res}")
