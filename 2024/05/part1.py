from collections import defaultdict

file_name = "./data.txt"
# file_name = "./test_data.txt"
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
            # TODO: add middle book page number to result...
            assert len(nums) % 2 == 1 # must be odd length???
            res += nums[len(nums) // 2]


    # print(f"{index=}, {arr[index-1]=}, {arr[index+1]=}")
    # print(f"{rules[:5]}")
    # print(f"{updates[:5]}")
    print(f"ANSWER: {res}")