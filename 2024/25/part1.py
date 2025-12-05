USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    schematics = [[]]
    for line in lines:
        if line == "":
            schematics.append([])
        else:
            schematics[-1].append(line)

    keys, locks = [], []
    for schematic in schematics:
        if schematic[0][0] == "#":
            locks.append(schematic[1:-1])
        else:
            keys.append(schematic[1:-1])
    
    
    key_heights, lock_heights = [], []
    for key in keys:
        assert len(key) == 5 and len(key[0]) == 5
        heights = [0] * 5
        for i in range(5): # 5
            for j in range(5):
                heights[i] += key[j][i] == "#"
        key_heights.append(heights)
    for lock in locks:
        assert len(lock) == 5 and len(lock[0]) == 5
        heights = [0] * 5
        for i in range(5): # 5
            for j in range(5):
                heights[i] += lock[j][i] == "#"
        lock_heights.append(heights)
    
    def isKeyFit(key_height, lock_height):
        assert len(key_height) == len(lock_height) == 5
        for i in range(5):
            if key_height[i] + lock_height[i] > 5:
                return False
        return True

    res = sum(isKeyFit(key_height, lock_height) for key_height in key_heights for lock_height in lock_heights)
    print(f"ANSWER: {res}")
