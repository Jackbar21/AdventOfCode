USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    ##################################
    ### PREPARE INPUT DATA (START) ###
    ##################################
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
        prize = (int(prize[0].split("=")[1]) + 10000000000000, int(prize[1].split("=")[1]) + 10000000000000)
        data.append((a, b, prize))
    ################################
    ### PREPARE INPUT DATA (END) ###
    ################################

    def isWholeNumber(num, delta = 0.0005):
            return abs(num - round(num)) < delta

    # We now have an array 'data' which contains 2-item tuples of every A, B, prize coordinates!
    res = 0
    for a, b, prize in data: 
        a_dx, a_dy = a
        b_dx, b_dy = b
        prize_x, prize_y = prize

        # We have that:
        #   (1) a_dx * A + b_dx * B == prize_x
        #   (2) a_dy * A + b_dy * B == prize_y
        # Where A and B are unknown, and represent our number of 
        # 'A' and 'B' button presses, respectively
        # a_dx * A + b_dx * B == prize_x
        # a_dy * A + b_dy * B == prize_y
        # <--> (a_dy * A)/b_dy + B == prize_y / b_dy
        # <--> (b_dx)(a_dy * A)/b_dy + b_dx * B == (b_dx)(prize_y / b_dy)
        # <--> (b_dx)(a_dy * A)/b_dy - (a_dx * A) == (b_dx)(prize_y / b_dy) - prize_x
        # <--> A(b_dx * a_dy)/b_dy - A(a_dx) == (b_dx)(prize_y / b_dy) - prize_x
        # <--> A((b_dx * a_dy)/b_dy - a_dx) == (b_dx)(prize_y / b_dy) - prize_x
        # <--> A == [(b_dx)(prize_y / b_dy) - prize_x] / [(b_dx * a_dy)/b_dy - a_dx]
        A = ((b_dx)*(prize_y / b_dy) - prize_x) / ((b_dx * a_dy)/b_dy - a_dx)
        # Then once we know A, we know that a_dx * A + b_dx * B == prize_x, hence:
        B = (prize_x - a_dx * A) / b_dx
        
        # We know that the values of A and B we get are the ONLY possible solutions
        # (since we have the same number of unknowns as equations, from linear algebra!)
        # So if their values are not whole numbers, then it's not possible to reach
        # prize point in the context of this problem!
        if isWholeNumber(A) and isWholeNumber(B):
            cost = 3 * round(A) + round(B)
            res += cost

    print(f"ANSWER: {res}")


#########################################################################
### LEFTOVER COMMENTS FROM WHEN I WAS STRUGGLING THROUGH THIS PROBLEM ###
#########################################################################
# Would I rather spam button A, or button B?
# Well, it's going to depend on HOW LONG it's gonna take for me
# to reach that insane 10 QUADRILLION distance away, with <100 steps
# at a time! I know that for every A button press, I could have done
# 3 B button presses. I want to get to a position where I can either:
#   (1) Spam button A until I reach prize, or
#   (2) Spam button B until I reach prize

# For either case to be true, it must be that prize_x = c * b_dx, and prize_y = c * b_dy,
# for some c >= 0, and similarly for A with a_dx and a_dy. Moreover, it must be that
# b_x <= prize_x, prize_x % b_dx == 0, b_y <= prize_y, prize_y % b_dy == 0
# And then of course, something similar for the A button.

# def ucs(a, b, prize, is_goal_state): # is_goal_state(a, prize) or is_goal_state(b, prize)
#     queue = [(0, 0, 0)] # (cost, x, y)


# def ucs_a(a, b, prize):
#     queue = [(0, 0, 0)]

# def ucs_b(a, b, prize):
#     queue = [(0, 0, 0)]


# 94a + 22b = 10000000008400
# 34a + 67b = 10000000005400

# 94x + 22y = 10000000008400

# A = 


# a_dx * A + b_dx * B == prize_x
# a_dy * A + b_dy * B == prize_y
# <--> (a_dy * A)/b_dy + B == prize_y / b_dy
# <--> (b_dx)(a_dy * A)/b_dy + b_dx * B == (b_dx)(prize_y / b_dy)
# <--> (b_dx)(a_dy * A)/b_dy - (a_dx * A) == (b_dx)(prize_y / b_dy) - prize_x
# <--> A(b_dx * a_dy)/b_dy - A(a_dx) == (b_dx)(prize_y / b_dy) - prize_x
# <--> A((b_dx * a_dy)/b_dy - a_dx) == (b_dx)(prize_y / b_dy) - prize_x
# <--> A == [(b_dx)(prize_y / b_dy) - prize_x] / [(b_dx * a_dy)/b_dy - a_dx]
# Then once we know A, we know that a_dx * A + b_dx * B == prize_x, hence:
# B == (prize_x - a_dx * A) / b_dx
# BUT, this doesn't work, since we can get non integer-values of A and B!

# Let's say I want to get to the point where I can infinitely spam the B button.
# INCORRECT: Then that means I want to reach a point x, y such that x == c * b_dx, y == c * b_dy
# CORRECT: Then that means I want to reach a point x, y, such that x == (prize_x - c * b_dx), y == (prize_y - c * b_dx)
# That way, I can spam that b button as much as I like!!!

# CORRECT:
# a_dx * A + b_dx * B == (prize_x - c * b_dx), start with c == prize_x // b_dx maybe ?
# a_dy * A + b_dy * B == (prize_y - c * b_dy), start with c == prize_y // b_dy maybe ? --> or min of above two?

# We don't care what c is, as long as we achieve it, we just want to figure out A and B
# (and then spam B the rest of the way later!)

# a_dx * A + b_dx * B == (prize_x - c * b_dx)
# a_dy * A + b_dy * B == (prize_y - c * b_dy)
# <--> a_dx * A == prize_x - c * b_dx - b_dx * B
# <--> a_dx * A == prize_x - (c - B) * b_dx
# <--> a_dx * A - (c - B) * b_dx == prize_x
# <--> a_dx * A + (B - c) * b_dx == prize_x
# <--> a_dy * A + (B - c) * b_dy == prize_y [In similar fashion!]


# INCORRECT:
# a_dx * A + b_dx * B == c * b_dx
# a_dy * A + b_dy * B == c * b_dy

# We don't care what c is, as long as we achieve it, we just want to figure out A and B
# (and then spam B the rest of the way later!)

# a_dx * A + b_dx * B == c * b_dx
# a_dy * A + b_dy * B == c * b_dy
# <--> a_dx * A == c * b_dx - b_dx * B
# <--> a_dx * A == (c - B) * b_dx
# <--> a_dx * A - (c - B) * b_dx == 0
# <--> a_dx * A + (B - c) * b_dx == 0
# <--> a_dy * A + (B - c) * b_dy == 0 [In similar fashion!]