USE_TEST_DATA = False

MAGIC_NUMBER = 16777216 - 1 # &'ing with this number is <==> % 16777216 (== 2^24)

import collections
import time

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data2.txt"
with open(file_name, "r") as file:
    lines = [int(line.strip()) for line in file.readlines()]

    # More optimized version of getNextSecretNumber logic from part 1 :)
    def getNextSecretNumber(secret_number):
        secret_number = (secret_number) ^ (secret_number << 6) & MAGIC_NUMBER
        secret_number = (secret_number) ^ (secret_number >> 5) & MAGIC_NUMBER
        return (secret_number) ^ (secret_number << 11) & MAGIC_NUMBER

    def getPriceFromSecretNumber(secret_number):
        return int(str(secret_number)[-1])

    def getPricesAndDeltas(secret_number, k):
        assert k >= 0
        prices = []
        deltas = []
        for _ in range(k - 1):
            new_secret_number = getNextSecretNumber(secret_number)
            old_price, new_price = getPriceFromSecretNumber(secret_number), getPriceFromSecretNumber(new_secret_number)
            deltas.append(new_price - old_price)
            prices.append(new_price)
            secret_number = new_secret_number
        return (prices, deltas)
     
    d = collections.defaultdict(int)
    def compute(secret_number, k):
        prices, deltas = getPricesAndDeltas(secret_number, k)
        assert len(prices) == len(deltas)
        assert len(deltas) >= 4
        n = len(prices)

        visited = set()
        window = collections.deque(deltas[:3])
        window.appendleft("GARBAGE") # To be deleted immediately!
        for r in range(3, n):
            # Update the window!
            window.popleft()
            window.append(deltas[r])

            # Add current window!
            tuple_window = tuple(window)
            if tuple_window not in visited:
                visited.add(tuple_window)
                d[tuple_window] += prices[r]

    def getKthSecretNumber(secret_number, k):
        assert k >= 0
        for _ in range(k):
            secret_number = getNextSecretNumber(secret_number)
        return secret_number

    start_time = time.time()
    for secret_number in lines:
        compute(secret_number, 2000)

    print(f"ANSWER: {max(d.values())}")
    print(f"TIME: {time.time() - start_time} seconds!")