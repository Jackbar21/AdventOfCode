class Solution:
    def __init__(self):
        file_name = "./data.txt"
        with open(file_name, "r") as file:
            # print(f"{file.readlines()[:5]}")
            print(f"ANSWER: {sum(self.isSafeRow(row) for row in file.readlines())}")

    def isSafeRow(self, row):
        assert row[-1] == "\n"
        levels = [int(num) for num in row[:-1].split()]
        assert len(levels) >= 2

        is_increasing = levels[0] < levels[1]

        for i in range(1, len(levels)):
            prev_level = levels[i - 1]
            cur_level = levels[i]

            diff = (
                cur_level - prev_level if is_increasing else prev_level - cur_level
            )
            # Check increasing & that diff is exactly between 1 and 3 inclusive
            if not (1 <= diff <= 3):
                return False

        return True

Solution()