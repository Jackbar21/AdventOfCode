import re

file_name = "./data.txt"
with open(file_name, "r") as file:
    lines = file.readlines()
    # print(f"{lines=}")

    pattern = re.compile("mul\\(\\d{1,3},\\d{1,3}\\)")
    # print(f"{pattern=}")
    matches = re.findall(pattern, "".join(lines))
    # print(f"{matches}")

    # res = 0
    # for match in matches:
    #     num1, num2 = [int(num) for num in match[4:-1].split(",")]
    #     res += num1 * num2
    # print(f"{res=}")
    print(
        f"ANSWER: {
            sum(
                num1 * num2 for num1, num2 in 
                map(lambda match: [int(num) for num in match[4:-1].split(",")], matches)
            )
        }"
    )
