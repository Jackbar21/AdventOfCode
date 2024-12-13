import heapq


USE_TEST_DATA = True

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    ### PREPARE INPUT DATA (START) ###
    lines = [line.strip() for line in file.readlines()]
    data = [] # (A_data, B_data, Prize_data), where each data object is nested 2-item tuple!
    for i in range(0, len(lines), 4):
        a = lines[i]
        b = lines[i + 1]
        prize = lines[i + 2]
        a, b, prize = a.split(": ")[1], b.split(": ")[1], prize.split(": ")[1]
        a, b, prize = a.split(", "), b.split(", "), prize.split(", ")
        a = (int(a[0].split("+")[1]), int(a[1].split("+")[1]))
        b = (int(b[0].split("+")[1]), int(b[1].split("+")[1]))
        # prize = (int(prize[0].split("=")[1]) + 10000000000000, int(prize[1].split("=")[1]) + 10000000000000)
        prize = (int(prize[0].split("=")[1]) + 0, int(prize[1].split("=")[1]) + 0)
        data.append((a, b, prize))
    ### PREPARE INPUT DATA (END) ###

    def heuristic(pos_x, pos_y, prize_x, prize_y):
        assert pos_x <= prize_x and pos_y <= prize_y
        return prize_x - pos_x, prize_y - pos_y

    # We now have an array 'data' which contains 2-item tuples of every A, B, prize coordinates!
    res = 0
    for a, b, prize in data: 
        print(f"{a=}, {b=}, {prize=}")
        a_dx, a_dy = a
        b_dx, b_dy = b
        prize_x, prize_y = prize
        continue
        
        # Just do simple UCS (might need A* search for part 2!)
        # fringe = [(prize_x + prize_y, 0, 0, 0)] # (cost + heuristic, cost x, y)
        fringe = [(0, 0, 0)] # (cost, x, y)
        visited = set()
        visited.add((0, 0))
        while len(fringe) > 0:
            # h_cost, cost, x, y = heapq.heappop(fringe)
            cost, x, y = heapq.heappop(fringe)
            # print(f"{cost=}, {x=}, {y=}")

            # if (x, y) in visited:
            #     continue
            # visited.add((x, y))

            # If reach gol state, we are finished!
            if x == prize_x and y == prize_y:
                # print(f"{cost=}")
                res += cost
                break

            # Case 1: Press A token!
            a_x, a_y = x + a_dx, y + a_dy
            # If leads away from prize, can never go backwards, so ignore!
            in_bounds = a_x <= prize_x and a_y <= prize_y
            if in_bounds and (a_x, a_y) not in visited:
                # new_cost = cost + 3
                # new_h_cost = new_cost + (prize_x - a_x) + (prize_y - a_y)
                # heapq.heappush(fringe, (new_h_cost, new_cost, a_x, a_y))
                heapq.heappush(fringe, (cost + 3, a_x, a_y))
                visited.add((a_x, a_y))
            
            # Case 2: Press B token!
            b_x, b_y = x + b_dx, y + b_dy
            # If leads away from prize, can never go backwards, so ignore!
            in_bounds = b_x <= prize_x and b_y <= prize_y
            if in_bounds and (b_x, b_y) not in visited:
                # new_cost = cost + 1
                # new_h_cost = new_cost + (prize_x - b_x) + (prize_y - b_y)
                # heapq.heappush(fringe, (new_h_cost, new_cost, b_x, b_y))
                heapq.heappush(fringe, (cost + 1, b_x, b_y))
                visited.add((b_x, b_y))
            



    print(f"ANSWER: {res}")

