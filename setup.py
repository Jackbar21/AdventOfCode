import os
from datetime import datetime

boilerplate = """
USE_TEST_DATA = True

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    res = 0

    print(f"ANSWER: {res}")
"""
YEAR = datetime.now().year

for i in range(1, 26):  # 01 → 25
    folder = f"{YEAR}/{i:02d}"
    os.makedirs(folder, exist_ok=True)

    for fname in ["part1.py", "part2.py"]:
        with open(f"{folder}/{fname}", "w") as f:
            f.write(boilerplate)

    open(f"{folder}/data.txt", "w").close()
    open(f"{folder}/test_data.txt", "w").close()

print("Done!")
