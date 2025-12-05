from functools import cache


USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    #########################
    ### START PARSE INPUT ###
    #########################
    lines = [line.strip() for line in file.readlines()]
    patterns = lines[0].split(", ")
    designs = lines[2:]
    #######################
    ### END PARSE INPUT ###
    #######################

    # TODO: Consider using full string instead
    # def dp(design, i = 0):
    #     if i >= len(design):
    #         return True
    @cache
    def dp(design: str) -> bool:
        if len(design) == 0:
            return 1
        
        count = 0
        for pattern in patterns:
            if design.startswith(pattern):
                count += dp(design[len(pattern):])

        return count
        

    res = 0
    for design in designs:
       res += dp(design)

    print(f"ANSWER: {res}")
