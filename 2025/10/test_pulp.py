# This is my first time working with pulp library, and using an Integer Linear Pogramming solver!
# So this is just a file of me experimenting with it to get the hang of it before implementing the actual solution
from pulp import *

def first_example():
    # Step 1: Create variables
    x = LpVariable("x", 0, 3) # 0 <= x <= 3
    y = LpVariable("y", cat="Binary") # y in {0, 1}

    # Step 2: Create a problem
    prob = LpProblem("myProblem", LpMinimize)

    # Step 3: Define objective (add expression, an expression doesn't have constraint like <=, ==, >=)
    prob += x + 4 * y # Minimize x + 4y

    # Step 4: Define constraints
    prob += x + y >= 2

    # Step 5: Solve
    status = prob.solve()
    return status, x.varValue, y.varValue

def second_example():
    # I'm now going to try to replicate ILP example from my CSCC73 course notes (University of Toronto)
    # Kudos to Prof. Vassos Hadzilacos!

    # c1 -> profit $3 / hectare
    # c2 -> profit $2 / hectare

    # Resources:
    # 1. Labour <= 40 hours
    # 2. Seed <= 100 kg
    # 3. Pesticide <= 10 bags

    # ______________________________________________
    # | Crop | Profit | Labour | Seed  | Pesticide |
    # |------|--------|--------|-------|-----------|
    # |  c1  |   $3   |   2hr  |  1kg  |   1bag    |
    # |  c2  |   $2   |   1hr  |  3kg  |   0bag    |
    # ----------------------------------------------

    # vars x1, x2 = hectares of c1, c2 planted
    # objective: maximize 3x1 + 2x2
    # constraints:
    # 2x1 + 1x2 <= 40 (labour)
    # 1x1 + 3x2 <= 100 (seed)
    # 1x1 + 0x2 <= 10 (pesticide)
    # x1, x2 >= 0

    # Step 1: Create variables
    x1 = LpVariable("x1", 0) # hectares of c1
    x2 = LpVariable("x2", 0) # hectares of c2

    # Step 2: Create a problem
    prob = LpProblem("Crop_Profit_Maximization", LpMaximize)

    # Step 3: Define objective
    prob += 3 * x1 + 2 * x2 # Maximize profit

    # Step 4: Define constraints
    prob += 2 * x1 + 1 * x2 <= 40  # Labour constraint
    prob += 1 * x1 + 3 * x2 <= 100  # Seed constraint
    prob += 1 * x1 + 0 * x2 <= 10   # Pesticide constraint
    prob += x1 >= 0
    prob += x2 >= 0

    # Step 5: Solve
    status = prob.solve()
    return status, x1.varValue, x2.varValue

status, x_val, y_val = first_example()
status, x1_val, x2_val = second_example()

print(f"FIRST EXAMPLE: {status=}, {x_val=}, {y_val=}, {LpStatus[status]=}")
print(f"SECOND EXAMPLE: {status=}, {x1_val=}, {x2_val=}, {LpStatus[status]=}")