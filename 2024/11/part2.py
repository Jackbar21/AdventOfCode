from functools import cache


USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    line = file.readline().split()

    @cache
    def solve(stone, blink_count):
        if blink_count == 0:
            return 1

        if stone == "0":
            return solve("1", blink_count - 1)
        
        if len(stone) % 2 == 0:
            half_index = len(stone) // 2
            left, right = stone[:half_index], stone[half_index:]
            left, right = str(int(left)), str(int(right)) # In case of trailing 0s!!!
            return solve(left, blink_count - 1) + solve(right, blink_count - 1)

        new_stone = str(int(stone) * 2024)
        return solve(new_stone, blink_count - 1)

    res = sum(
        solve(stone, 75)
        for stone in line
    )
    print(f"ANSWER: {res}")