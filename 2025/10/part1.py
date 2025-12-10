USE_TEST_DATA = False
from collections import deque

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    OFF, ON = ".", "#"
    TOGGLE = {
        OFF: ON,
        ON: OFF,
    }

    problems = []
    for line in lines:
        line = line.split(" ")

        indicator_lights = line[0][1:-1]

        options = [option[1:-1].split(",") for option in line[1:-1]]
        options = [tuple(int(op) for op in option) for option in options]

        joltage_requirements = list(map(int, line[-1][1:-1].split(",")))

        problems.append((indicator_lights, options, joltage_requirements))

    
    res = 0
    for indicator_lights, options, _ in problems:
        # Start at 0 (all lights OFF) and run BFS to find shortest path to indicator_lights
        initial_lights = OFF * len(indicator_lights)

        queue = deque([(0, initial_lights)])  # (steps, cur_lights)
        visited = set([initial_lights])

        while queue:
            steps, cur_lights = queue.popleft()
            if cur_lights == indicator_lights:
                res += steps
                break

            for option in options:
                next_lights = list(cur_lights)
                for idx in option:
                    next_lights[idx] = TOGGLE[next_lights[idx]]
                next_lights = "".join(next_lights)

                if next_lights not in visited:
                    visited.add(next_lights)
                    queue.append((steps + 1, next_lights))

    print(f"ANSWER: {res}")
