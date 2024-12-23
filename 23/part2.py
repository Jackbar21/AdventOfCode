from collections import defaultdict
import collections
import time


USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip().split("-") for line in file.readlines()]

    computers = set()
    adj_list = defaultdict(set)
    degrees = defaultdict(int)
    for computer1, computer2 in lines:
        adj_list[computer1].add(computer2)
        adj_list[computer2].add(computer1)
        computers.add(computer1)
        computers.add(computer2)
        degrees[computer1] += 1
        degrees[computer2] += 1

    # Turn everything into lists for convenience later (and sort cause why not hehe)!
    nodes = sorted(computers)
    for key in adj_list:
        adj_list[key] = sorted(adj_list[key])

    ############################################################################
    ### (START) GITHUB COPILOT GENERATED KOSARAJU'S ALGORITHM HELPER (START) ###
    ############################################################################
    def kosaraju():
        stack = []
        visited = set()
        graph = adj_list

        # Step 1: Perform DFS and push vertices onto stack
        def dfs(v):
            visited.add(v)
            for neighbor in graph[v]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(v)

        for vertex in graph:
            if vertex not in visited:
                dfs(vertex)

        # Step 2: Transpose the graph
        # TODO: Since graph is undirected, this is the SAME graph!!!
        transpose_graph = {v: [] for v in graph}
        for v in graph:
            for neighbor in graph[v]:
                transpose_graph[neighbor].append(v)

        # Step 3: Perform DFS on the transpose graph
        visited.clear()
        sccs = []

        def dfs_transpose(v, scc):
            visited.add(v)
            scc.append(v)
            for neighbor in transpose_graph[v]:
                if neighbor not in visited:
                    dfs_transpose(neighbor, scc)

        while stack:
            v = stack.pop()
            if v not in visited:
                scc = []
                dfs_transpose(v, scc)
                sccs.append(scc)

        return sccs
    ############################################################################
    ##### (END) GITHUB COPILOT GENERATED KOSARAJU'S ALGORITHM HELPER (END) #####
    ############################################################################

    # We now essentially have a graph G, where we have a list of all the unique nodes, and an
    # adjacency list for each node's unique neighbors! Obviously, something like Kosaraju's
    # algorithm can be pretty useful here, especially for whatever concoction might have been
    # cooked up by the authors over in part 2, but perhaps a little bit overkill for part 1!
    # Here we're interested in strongly-connected components of size 3 (where at least one 
    # starts with a t!).
    # So, we loop over every unique triplet in nodes, check that at least one of them starts
    # with a t, and then check if each of them have the other two as their neighbors in adj_list :)

    # NEVERMIND, SCRATCH THAT!!! Kosaraju's algorithm is completely overkill / unneeded in this example!
    # Kosaraju's algorithm uses the idea of doing a DFS from every node, as well as from the transposed-Graph,
    # to find Strongly-Connected-Components. But in this case, the Graph is undirected, so the transpose is itself!
    # So really, from any specific node, we can perform a depth-first-search FROM taht node to find all the nodes reachable
    # from it! Then we know, for each node that was reached, that node must ALSO be able to reach ALL THE OTHER nodes in
    # that visited set (since again, the graph is undirected!) Henceforth, to find the solution, we can simply run a DFS
    # from every single unvisted node, where the nodes it visits forms a CLIQUE of size k, where k == # of nodes in that set.
    # Obviously, each node in this set belongs to its own CLIQUE, so we can ignore them for the remaining nodes to search through.
    # What this means, is that in total, we will only DFS through every single node ONCE, and NOT more!!! This makes things, GIGA
    # EFFICIENT!!!!!!!!

    # NEVERMIND, SCRATCH THAT AGAIN!!! The above works in performing Kosaraju's algorith more efficiently, sure, but it only
    # finds strongly connected components... NOT CLIQUES!!! Therefore, we have to come up with another way of doing things...
    # Turns out, there are only 16 unique nodes in total, so despite finding whether a graph G has a CLIQUE of size k is an
    # NP-Complete problem (where you can #GiveMeAMillionDollarsIfIWriteAPolynomialTimeAlgoRightHere), the input size is small
    # enough to handle an exponential time algorithm. Since we want to find the largest size CLIQUE, we can check to see if
    # a CLIQUE of size 16 exists, and if not then size 15, if not then size 14, etc.... We know from part 1 there is at least
    # a CLIQUE of size 3, so we can use that as a lower bound :) Although, instead of going from 16 downwards, we can just go
    # from 3 and upwards, since we know that CLIQUE of size k ==> there's also a CLIQUE of any size smaller than k :) So, we
    # can start from 3, and work our way upwards up to 16 (inclusive), until we get a fail, for which we know the previous size
    # before the fail is the largest possible size CLIQUE :)

    # Idea: Loop through every node (computer) in nodes, and for each node find the maximal CLIQUE that includes that node
    # For now, we'll only do it with a specific node.


    # Polynomial time verifier | O(n^2)
    def isClique(vertices):
        for v1 in vertices:
            for v2 in vertices:
                if not (v1 == v2 or v1 in adj_list[v2]):
                    return False
        return True


    def getAllSubsetsOfSizeK(arr, k):
        if len(arr) <= k:
            return arr.copy() if len(arr) == k else []

        main_res = set()
        def backtrack(i, arr, res, k):
            if len(res) == k:
                new_case = tuple(sorted(res))
                if new_case not in main_res:
                    main_res.add(new_case)
                    yield new_case
                    # return

            if i >= len(arr) or len(res) > k:
                return
            
            # Case 1: Include element at index i
            element = arr[i]
            res.append(element)
            yield from backtrack(i + 1, arr, res, k)
            res.pop()

            # Case 2: Don't include element at index i
            yield from backtrack(i + 1, arr, res, k)

        yield from backtrack(0, arr, [], k)


    def CLIQUE(k):
        # If there is a CLIQUE of size k:
        #     - Returns CLIQUE as comma-separated string (alphabetically ordered!)
        # Otherwise:
        #     - Returns 'None'

        # Getting all subsets of size k, and checking them all, is an insane waste of time & resources.
        # Instead, we should loop through all of the nodes, and for each node, take every permutation of 
        # k - 1 neighbors (if any) and check if they form a clique of size k!
        for node in nodes:
            for subset in getAllSubsetsOfSizeK(adj_list[node], k - 1):
                # Don't need to append node to subset, since it already has an edge to every node in there!
                if isClique(subset):
                    # But if we do find a CLIQUE here, we do need to make sure to add the node to the result!!!
                    # This mistake cost me a single failure on AoC part 2 submission :P
                    clique = sorted(list(subset) + [node])
                    return ",".join(clique)
        return None


    # We know k must be between 3, 16 inclusive. We want to essentially
    # find the rightmost True (i.e. not 'None' CLIQUE result!). We can
    # do this via rightmost binary search :)
    # At this moment, I have discovered that EVERY SINGLE NODE has EXACTLY 13 outwards edges! This is obviously a huge thing to notice
    # that will simplify this problem A LOT... since the MAXIMUM POSSIBLE CLIQUE SIZE is now 14!!!
    start_time = time.time()
    min_degree, max_degree = min(degrees.values()), max(degrees.values())
    assert min_degree == max_degree # <-- NOT GENERALLY TRUE, just something I noticed for both test_data.txt and data.txt :)
    l, r = 3, min(degrees.values()) + 1
    res = None
    while l <= r:
        mid = (l + r) // 2
        clique = CLIQUE(mid)
        if clique != None:
            # We have found a valid case! Now keep searching to the right for potentially larger
            # but ALSO valid cliques!!!
            res = clique
            l = mid + 1
        else:
            # Uh oh... this CLIQUE size is too large! Only search for potential CLIQUEs that are smaller in size :)
            r = mid - 1
    
    print(f"ANSWER: {res} | CLIQUE-SIZE: {r}")
    print(f"TIME: {time.time() - start_time} seconds!")

# NP-Complete | O(2^n) solve | O(n^p) verify, where p is a positive integer
# CLIQUE Decision Problem: Given a Graph G = (V, E), and a positive integer k <= |V|, determine if G contains a CLIQUE of size k