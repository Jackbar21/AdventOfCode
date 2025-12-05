USE_TEST_DATA = False

from functools import cache
import time

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [int(line.strip()) for line in file.readlines()]

    def getNextSecretNumber(secret_number):
        # Step 1
        calc = secret_number * 64
        secret_number = mix(secret_number, calc)
        secret_number = prune(secret_number)

        # Step 2
        calc = secret_number // 32
        secret_number = mix(secret_number, calc)
        secret_number = prune(secret_number)

        # Step 3
        calc = secret_number * 2048
        secret_number = mix(secret_number, calc)
        secret_number = prune(secret_number)

        # Finally, return the new secret number!
        return secret_number

    def mix(num1, num2):
        return num1 ^ num2

    def prune(num):
        return num % 16777216

    def getKthSecretNumber(secret_number, k):
        assert k >= 0
        for _ in range(k):
            secret_number = getNextSecretNumber(secret_number)
        return secret_number

    start_time = time.time()
    res = sum(getKthSecretNumber(num, 2000) for num in lines)
    print(f"ANSWER: {res}")
    print(f"TIME: {time.time() - start_time} seconds!")