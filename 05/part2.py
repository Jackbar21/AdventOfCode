from collections import defaultdict
from collections import deque

use_test_data = False

file_name = "./test_data.txt" if use_test_data else "./data.txt"
with open(file_name, "r") as file:
    arr = file.readlines()
    res = 0
    index = arr.index('\n')

    rules = arr[:index]
    updates = arr[index+1:]

    prev_rules = defaultdict(set) # num: [numbers that MUST come BEFORE it!]
    post_rules = defaultdict(set) # num: [numbers that MUST come AFTER it!]
    for e in rules:
        prev_num, post_num = [int(i) for i in e.split()[0].split('|')]
        prev_rules[post_num].add(prev_num)
        post_rules[prev_num].add(post_num)
    
    for e in updates:
        is_valid_update = True # True until proven otherwise!
        nums = [int(i) for i in e.split()[0].split(",")]
        for i in range(len(nums)):
            num = nums[i]

            # Ensure all previous nums valid!
            for j in range(i):
                prev_num = nums[j]
                if prev_num in post_rules[num]:
                    is_valid_update = False
                    break
            if not is_valid_update:
                break

            for j in range(i + 1, len(nums)):
                post_num = nums[j]
                if post_num in prev_rules[num]:
                    is_valid_update = False
                    break
            if not is_valid_update:
                break
        
        if is_valid_update:
            continue # Only consider the bad ones!
            
        # We have a bad update on our hands. Let's sort it properly,
        # which we can do by converting this into a graph problem, where the
        # page numbers are nodes and their ordering rules are the edges,
        # and then topologically sort them to build a new correct order :)
        adj_list = defaultdict(set)
        indegrees = {num: 0 for num in nums}
        for num in nums:
            neighbors = post_rules[num]
            for neighbor in neighbors:
                if neighbor in indegrees:
                    indegrees[neighbor] += 1
                    adj_list[num].add(neighbor)
        
        
        # print(f"{indegrees=}")
        # print(f"{adj_list=}")
        # Idea: Just run topological sort!

        order = []
        visited = set()
        queue = deque([node for node in indegrees if indegrees[node] == 0])
        while len(queue) > 0:
            node = queue.popleft()
            assert node not in visited
            visited.add(node)
            order.append(node)
            for neighbor in adj_list[node]:
                indegrees[neighbor] -= 1
                if indegrees[neighbor] == 0:
                    queue.append(neighbor)
        assert len(order) == len(visited) == len(nums) # i.e. actually possible to find sorting!
        # print(f"{order=}")
        # TODO: add middle book page number to result...
        assert len(order) % 2 == 1 # must be odd length???
        res += order[len(order) // 2]


    # print(f"{index=}, {arr[index-1]=}, {arr[index+1]=}")
    # print(f"{rules[:5]}")
    # print(f"{updates[:5]}")
    print(f"ANSWER: {res}")