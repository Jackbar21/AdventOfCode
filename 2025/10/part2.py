USE_TEST_DATA = False
PRINT_OPTIMAL_SOLUTION_PER_PROBLEM = False
from collections import deque
from pulp import *

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    problems = []
    for line in lines:
        line = line.split(" ")

        indicator_lights = line[0][1:-1]

        options = [option[1:-1].split(",") for option in line[1:-1]]
        options = [tuple(int(op) for op in option) for option in options]

        joltage_requirements = tuple(map(int, line[-1][1:-1].split(",")))

        problems.append((indicator_lights, options, joltage_requirements))

    # The trick to this problem is realizing this boils down to solving a system of linear equations
    # For instance, let's take a look at the first example:
    #   [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    # We start with voltages [0,0,0,0] and want to reach [3,5,4,7]
    #
    # With each button press, we can add 1 to the voltages at the indices specified by the button
    # So we can represent this as:
    #   t0*(0,0,0,1) + t1*(0,1,0,1) + t2*(0,0,1,0) + t3*(0,0,1,1) + t4*(1,0,1,0) + t5*(1,1,0,0) = (3,5,4,7)
    # Where t0 is the number of times we press button 0, etc.
    #
    # This is a system of linear equations, where we can formulate the constraints as:
    # x0 = t4 + t5 = 3
    # x1 = t1 + t5 = 5
    # x2 = t2 + t3 + t4 = 4
    # x3 = t0 + t1 + t3 = 7
    #
    # And the objective is to minimize the sum of all ti, i.e. minimize t0 + t1 + t2 + t3 + t4 + t5

    res = 0
    for _, options, joltage_requirements in problems:
        # We want to minimize the total number of button presses, while satisfying the joltage requirements

        # Step 1: Create variables
        vars = [LpVariable(f"t{i}", 0, cat="Integer") for i in range(len(options))]

        # Step 2: Create a problem
        prob = LpProblem("Crop_Profit_Maximization", LpMinimize)

        # Step 3: Define objective
        prob += lpSum(vars)  # Minimize total button presses

        # Step 4: Define constraints
        for idx in range(len(joltage_requirements)):
            prob += (
                lpSum(vars[i] for i, option in enumerate(options) if idx in option)
                == joltage_requirements[idx]
            )

        # Step 5: Solve
        status = prob.solve(PULP_CBC_CMD(msg=False))
        presses = [int(var.varValue) for var in vars]
        total_presses = sum(presses)
        if PRINT_OPTIMAL_SOLUTION_PER_PROBLEM:
            print(f"Button presses: {presses}, Total presses: {total_presses}")
        res += total_presses

    print(f"ANSWER: {res}")
