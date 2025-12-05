USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    # line = list(map(int, file.readline().split()))
    line = file.readline().split()
    # print(f"{line=}")

    def blink(stone: str) -> str:
        if stone == "0":
            return "1"

        n = len(stone)
        if n % 2 == 0:
            # print(f"{stone=}, {stone[:n//2]=}, {stone[n//2:]=}")
            return [str(int(stone[:n//2])), str(int(stone[n//2:]))]
        
        return str(int(stone) * 2024)
    
    def applyFunc(item, func):
        if type(item) != list:
            return func(item)
        return [
            applyFunc(sub_item, func)
            for sub_item in item
        ]
    
    for _ in range(25):
        for i, item in enumerate(line):
            line[i] = applyFunc(item, blink)

    # Now we need to count the number of stones...
    def countRec(item):
        if type(item) != list:
            assert type(item) == str
            return 1
        return sum(countRec(itm) for itm in item)

    print(f"ANSWER: {countRec(line)}")

