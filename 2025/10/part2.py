USE_TEST_DATA = True
from collections import deque

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

    
    res = 0
    for _, options, joltage_requirements in problems:
        # Start at 0 (all lights OFF) and run BFS to find shortest path to indicator_lights
        initial_voltages = tuple([0] * len(joltage_requirements))

        queue = deque([(0, initial_voltages)])  # (steps, cur_voltages)
        visited = set([initial_voltages])

        while queue:
            steps, cur_voltages = queue.popleft()
            if cur_voltages == joltage_requirements:
                res += steps
                print(f"Found solution in {steps} steps")
                break

            for option in options:
                next_voltages = list(cur_voltages)
                valid = True
                for idx in option:
                    next_voltages[idx] += 1
                    if next_voltages[idx] > joltage_requirements[idx]:
                        valid = False
                        break
                
                if not valid:
                    continue
                
                next_voltages = tuple(next_voltages)
                if next_voltages not in visited:
                    visited.add(next_voltages)
                    queue.append((steps + 1, next_voltages))

    print(f"ANSWER: {res}")
