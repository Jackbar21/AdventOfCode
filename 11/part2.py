from functools import cache


USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    # memo = {}
    # line = list(map(int, file.readline().split()))
    line = file.readline().split()
    print(f"{line=}")

    # def blinks(stone: str, num_blinks):
    #     if (stone, num_blinks)


    # KEY:
    # 0 -> 1                            | solveSingle(0) == 1 + solveSingle(1)
    # 1 -> 2024 -> 20,24 -> 2,0,2,4     | 
    # 2 -> 4048 -> 40,48 -> 4,0,4,8
    # 4 -> 8096 -> 80,96 -> 8,0,9,6
    # 6 -> 12144 -> 24579456 -> 2457,9456 -> 24,57,94,56 -> 2,4,5,7,9,4,5,6
    # 5 -> 10120 -> 20482880 -> 2048,2880 -> 20,48,28,80 -> 2,0,4,8,2,8,8,0
    # 7 -> 14168 -> 28676032 -> 2867,6032 -> 28,67,60,32 -> 2,8,6,7,6,0,3,2
    # 8 -> 16192 -> 32772608 -> 3277,2608 -> 32,77,26,08 -> 3,2,7,7,2,6,0,8
    # 9 -> 18216 -> 36869184 -> 3686,9184 -> 36,86,91,84 -> 3,6,8,6,9,1,8,4
    # 3 -> 6072 -> 60,72 -> 6,0,7,2
    @cache
    def solveSingle(stone, count):
        assert count >= 0
        assert len(stone) == 1 and stone in "0123456789"
        if count == 0:
            return 1
        
        # 0 -> 1 
        if stone == "0":
            return solveSingle("1", count - 1)
        
        return solveMulti(str(int(stone) * 2024), count - 1)
        
        # 1 -> 2024 -> 20,24 -> 2,0,2,4
        if stone == "1":
            # if count <= 3:
            #     return {1:1,2:2,3:4}[count]
            # return sum(
            #     solveSingle(str(digit), count - 3)
            #     for digit in [2,0,2,4]
            # )
            return solveMulti("2024", count - 1)
        
        # 2 -> 4048 -> 40,48 -> 4,0,4,8
        if stone == "2":
            # if count <= 3:
            #     return {1:1,2:2,3:4}[count]
            # return sum(
            #     solveSingle(str(digit), count - 3)
            #     for digit in [4,0,4,8]
            # )
            return solveMulti("4048", count - 1)
        
        # 3 -> 6072 -> 60,72 -> 6,0,7,2
        if stone == "3":
            # if count <= 3:
            #     return {1:1,2:2,3:4}[count]
            # return sum(
            #     solveSingle(str(digit), count - 3)
            #     for digit in [6,0,7,2]
            # )
            return solveMulti("6072", count - 1)

        # 4 -> 8096 -> 80,96 -> 8,0,9,6
        if stone == "4":
            if count <= 3:
                return {1:1,2:2,3:4}[count]
            return sum(
                solveSingle(str(digit), count - 3)
                for digit in [8,0,9,6]
            )

        # 5 -> 10120 -> 20482880 -> 2048,2880 -> 20,48,28,80 -> 2,0,4,8,2,8,8,0
        if stone == "5":
            if count <= 5:
                return {1:1,2:1,3:2,4:4,5:8}[count]
            return sum(
                solveSingle(str(digit), count - 5)
                for digit in [2,0,4,8,2,8,8,0]
            )
            
        # 6 -> 12144 -> 24579456 -> 2457,9456 -> 24,57,94,56 -> 2,4,5,7,9,4,5,6
        if stone == "6":
            if count <= 5:
                return {1:1,2:1,3:2,4:4,5:8}[count]
            return sum(
                solveSingle(str(digit), count - 5)
                for digit in [2,4,5,7,9,4,5,6]
            )
       
        # 7 -> 14168 -> 28676032 -> 2867,6032 -> 28,67,60,32 -> 2,8,6,7,6,0,3,2
        if stone == "7":
            if count <= 5:
                return {1:1,2:1,3:2,4:4,5:8}[count]
            return sum(
                solveSingle(str(digit), count - 5)
                for digit in [2,8,6,7,6,0,3,2]
            )
        
        # 8 -> 16192 -> 32772608 -> 3277,2608 -> 32,77,26,08 -> 3,2,7,7,2,6,0,8
        if stone == "8":
            if count <= 5:
                return {1:1,2:1,3:2,4:4,5:8}[count]
            return sum(
                solveSingle(str(digit), count - 5)
                for digit in [3,2,7,7,2,6,0,8]
            )
        
        # 9 -> 18216 -> 36869184 -> 3686,9184 -> 36,86,91,84 -> 3,6,8,6,9,1,8,4
        if stone == "9":
            if count <= 5:
                return {1:1,2:1,3:2,4:4,5:8}[count]
            return sum(
                solveSingle(str(digit), count - 5)
                for digit in [3,6,8,6,9,1,8,4]
            )

        raise Exception("stone must be between 1-to-9!")

    
    def solveMulti(stone, count):
        assert count >= 0
        assert len(stone) >= 1
        if count == 0:
            return 1

        if len(stone) == 1:
            return solveSingle(stone, count)
        
        if len(stone) % 2 == 0:
            half_index = len(stone) // 2
            left, right = stone[:half_index], stone[half_index:]
            left, right = str(int(left)), str(int(right)) # In case of trailing 0s!!!
            # print(f"{left=}, {right=}")
            return solveMulti(left, count - 1) + solveMulti(right, count - 1)

        new_stone = str(int(stone) * 2024)
        return solveMulti(new_stone, count - 1)

    res = sum(
        solveMulti(stone, 75)
        for stone in line
    )
    print(f"ANSWER: {res}")
    exit()