USE_TEST_DATA = False
NUM_CONNECTIONS = 10 if USE_TEST_DATA else 1000
import heapq
from collections import defaultdict, deque
from functools import reduce

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

    shortest_distances = [heapq.heappop(distances) for _ in range(NUM_CONNECTIONS)]

    # This is a connected components problem, and part 2 will likely require prim's or kruskal's algorithm
    # to construct minimum spanning trees connecting all circuits with minimum total distance.
    # For now, we'll create a graph with 'NUM_CONNECTIONS' edges based on the shorted NUM_CONNECTIONS distances.
    adj_list = defaultdict(set)
    for dist, p1, p2 in shortest_distances:
        # Not tracking edge cost, since distance can be computed in O(1) time
        adj_list[p1].add(p2)
        adj_list[p2].add(p1)
    
    # Now, lets count sizes of connected components
    components = []
    unvisited = set(points)
    while len(unvisited) > 0:
        node = unvisited.pop()
        component = []
        queue = deque([node])

        while queue:
            node = queue.popleft()
            component.append(node)
            for neigh in adj_list[node]:
                if neigh in unvisited:
                    queue.append(neigh)
                    unvisited.remove(neigh)
        components.append(component)
    
    circuit_sizes = list(map(lambda c: -len(c), components))
    heapq.heapify(circuit_sizes)
    largest_three_sizes = [-heapq.heappop(circuit_sizes) for _ in range(3)]

    getProduct = lambda nums: reduce(lambda x, y: x * y, nums, 1)
    res = getProduct(largest_three_sizes)

    print(f"ANSWER: {res}")
