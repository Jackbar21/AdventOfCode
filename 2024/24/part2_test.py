from collections import defaultdict


USE_TEST_DATA = False

file_name = "./fixed_data.txt" if not USE_TEST_DATA else "bad_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    index = lines.index("")
    inputs, old_queries = lines[:index], lines[index + 1 :]
    queries, results = [], []
    for query in old_queries:
        q, result = query.split(" -> ")
        q = tuple(q.split(" "))
        queries.append(q)
        results.append(result)
    assert len(queries) == len(results)
    N = len(queries)
    for pair in [
        (18, 64),
        (15, 139),
        (5, 55),
        (108, 115),
    ]:
        i, j = pair
        print(f"{results[i], results[j]=}")
        results[i], results[j] = results[j], results[i]

    BITS_TO_CHECK = [
        "00",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
    ]

    # HERE, WE MODIFY QUERIES UNTIL THINGS ARE CORRECT!
    def run(inputs, queries, results, bit_to_check):
        d = {}
        for input in inputs:
            wire, bit = input.split(": ")
            assert wire not in d
            d[wire] = int(bit)
            # assert wire.startswith("x") or wire.startswith("y")
            # d[wire] = int(wire.startswith("x"))
            # d[wire] = 0
        # d["x" + bit_to_check] = 1

        FIRST_WIRE, GATE, SECOND_WIRE = 0, 1, 2
        remaining = defaultdict(list)
        z_remaining = set()
        for i in range(N):
            q, result = queries[i], results[i]
            remaining[q].append(result)
            if result[0] == "z":
                assert result not in z_remaining
                z_remaining.add(result)

        # print(f"{d=}")
        # print(f"{remaining=}")
        # print(f"{z_remaining=}")
        res = sorted(z_remaining, reverse=True)
        gate_solver = {
            "AND": lambda x, y: x & y,
            "XOR": lambda x, y: x ^ y,
            "OR": lambda x, y: x | y,
        }

        MAX_TRY_LIMIT = 100
        num_tries = 0
        while len(z_remaining) > 0:
            num_tries += 1
            if num_tries == MAX_TRY_LIMIT:
                # print(f"Max Try Limit Reached...")
                return False
            remaining_set = set(remaining.keys())
            for operation in remaining_set:
                wire1, gate, wire2 = operation

                if wire1 in d and wire2 in d:
                    val1 = d[wire1]
                    val2 = d[wire2]
                    val = gate_solver[gate](val1, val2)
                    for result in remaining[operation]:
                        d[result] = val
                        z_remaining.discard(result)
                    del remaining[operation]

        X = [
            "x45",
            "x44",
            "x43",
            "x42",
            "x41",
            "x40",
            "x39",
            "x38",
            "x37",
            "x36",
            "x35",
            "x34",
            "x33",
            "x32",
            "x31",
            "x30",
            "x29",
            "x28",
            "x27",
            "x26",
            "x25",
            "x24",
            "x23",
            "x22",
            "x21",
            "x20",
            "x19",
            "x18",
            "x17",
            "x16",
            "x15",
            "x14",
            "x13",
            "x12",
            "x11",
            "x10",
            "x09",
            "x08",
            "x07",
            "x06",
            "x05",
            "x04",
            "x03",
            "x02",
            "x01",
            "x00",
        ]
        Y = [
            "y45",
            "y44",
            "y43",
            "y42",
            "y41",
            "y40",
            "y39",
            "y38",
            "y37",
            "y36",
            "y35",
            "y34",
            "y33",
            "y32",
            "y31",
            "y30",
            "y29",
            "y28",
            "y27",
            "y26",
            "y25",
            "y24",
            "y23",
            "y22",
            "y21",
            "y20",
            "y19",
            "y18",
            "y17",
            "y16",
            "y15",
            "y14",
            "y13",
            "y12",
            "y11",
            "y10",
            "y09",
            "y08",
            "y07",
            "y06",
            "y05",
            "y04",
            "y03",
            "y02",
            "y01",
            "y00",
        ]
        Z = [
            "z45",
            "z44",
            "z43",
            "z42",
            "z41",
            "z40",
            "z39",
            "z38",
            "z37",
            "z36",
            "z35",
            "z34",
            "z33",
            "z32",
            "z31",
            "z30",
            "z29",
            "z28",
            "z27",
            "z26",
            "z25",
            "z24",
            "z23",
            "z22",
            "z21",
            "z20",
            "z19",
            "z18",
            "z17",
            "z16",
            "z15",
            "z14",
            "z13",
            "z12",
            "z11",
            "z10",
            "z09",
            "z08",
            "z07",
            "z06",
            "z05",
            "z04",
            "z03",
            "z02",
            "z01",
            "z00",
        ]
        d["x45"] = 0
        d["y45"] = 0

        def bitsToBin(bits):
            return "".join(map(lambda bit: str(d[bit]), bits))

        def bitsToRes(bits):
            return int(bitsToBin(bits), 2)

        print(f"{bitsToBin(X)=}")
        print(f"{bitsToBin(Y)=}")
        print(f"{bitsToBin(Z)=}")

        print(f"{bitsToRes(X)=}")
        print(f"{bitsToRes(Y)=}")
        print(f"{bitsToRes(Z)=}")
        print(f"{bitsToRes(X) + bitsToRes(Y)=}, {bitsToRes(Z)=}")
        print(f"{bin(bitsToRes(X) & bitsToRes(Z))[2:]=}")
        print(f"{bin(bitsToRes(Y) & bitsToRes(Z))[2:]=}")
        print(f"{bitsToRes(Z) - bitsToRes(X)=}")
        print(f"{bitsToRes(Z) - bitsToRes(Y)=}")

        # print(f"{res=}")
        res = int("".join(map(lambda z: str(d[z]), res)), 2)
        # print(f"{res=}")
        # print(f"ANSWER: {res}")
        res = bitsToRes(Z) & bitsToRes(X) != 0
        # print(f"{res=}")
        return res

    run(inputs, queries, results, None)
    exit()
    # for bit_to_check in BITS_TO_CHECK:
    #     for i in range(len(queries)):
    #         for j in range(i + 1, len(queries)):
    #     while not run(inputs, queries, bit_to_check):
            
        
    #     print(f"PASSED: {bit_to_check}")
    bits_to_check = ["06", "11", "31", "38", "45"]

    # for b in bits_to_check[-1:]:
    #     found = False
    #     for i in range(N):
    #         if found:
    #             break
    #         print(f"Progress: {i}/{N}...")
    #         for j in range(i + 1, N):
    #             if found:
    #                 break
    #             else:
    #                 results[i], results[j] = results[j], results[i]
    #                 found = run(inputs, queries, results, b)
    #                 if found:
    #                     print(f"VALID SWAP: {b} --> {i=}, {j=}")
    #                 results[i], results[j] = results[j], results[i]
    #     print(f"{run(inputs, queries, results, b)=}")
    # print(f"{queries=}")

    # run(inputs, queries, "06")
    # for pair in [
    #     (18, 64),
    #     (15, 139),
    #     (5, 55),
    #     (108, 115),
    # ]:
    #     i, j = pair
    #     results[i], results[j] = results[j], results[i]
    print(f"ANSWER {[run(inputs, queries, results, bit_to_check) for bit_to_check in BITS_TO_CHECK]}")
    # 06, 11, 31, 38, 45 (irrelevant this one? I.e. caused by others...)
    # 06, 11, 31, 38

    res = []
    for pair in [
        (18, 64),
        (15, 139),
        (5, 55),
        (108, 115),
    ]:
        for i in pair:
            res.append(results[i])
    res.sort()
    res = ",".join(res)
    print(f"{res=}")