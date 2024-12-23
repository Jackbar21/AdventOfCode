from collections import defaultdict


USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip().split("-") for line in file.readlines()]
    # print(f"{lines=}")

    computers = set()
    adj_list = defaultdict(set)
    for computer1, computer2 in lines:
        adj_list[computer1].add(computer2)
        adj_list[computer2].add(computer1)
        computers.add(computer1)
        computers.add(computer2)
    nodes = list(computers)
    
    # We now essentially have a graph G, where we have a list of all the unique nodes, and an
    # adjacency list for each node's unique neighbors! Obviously, something like Kosaraju's
    # algorithm can be pretty useful here, especially for whatever concoction might have been
    # cooked up by the authors over in part 2, but perhaps a little bit overkill for part 1!
    # Here we're interested in strongly-connected components of size 3 (where at least one 
    # starts with a t!).
    # So, we loop over every unique triplet in nodes, check that at least one of them starts
    # with a t, and then check if each of them have the other two as their neighbors in adj_list :)
    n = len(nodes)
    res = 0
    for i in range(n):
        print(f"Progress: {i}/{n}...")
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                
                a, b, c = nodes[i], nodes[j], nodes[k] # Computers!
                if not any(computer.startswith("t") for computer in [a, b, c]):
                    continue
                
                a_neighbors = adj_list[a]
                b_neighbors = adj_list[b]
                c_neighbors = adj_list[c]

                if b not in a_neighbors or c not in a_neighbors:
                    continue

                if a not in b_neighbors or c not in b_neighbors:
                    continue

                if a not in c_neighbors or b not in c_neighbors:
                    continue
                
                # Otherwise, at least one computer starts with a 't', and all three
                # of them are interconnected! Hence, increment result by one :)
                res += 1
    
    print(f"ANSWER: {res}")
