
USE_TEST_DATA = True

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    res = 0

    print(f"ANSWER: {res}")
