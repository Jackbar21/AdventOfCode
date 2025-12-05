import re

file_name = "./data.txt"
with open(file_name, "r") as file:

    def getMulSum(text, pattern=re.compile("mul\\(\\d{1,3},\\d{1,3}\\)")):
        return sum(
            num1 * num2
            for num1, num2 in map(
                lambda match: [int(num) for num in match[4:-1].split(",")],
                re.findall(pattern, text),
            )
        )

    lines = file.readlines()
    text = "".join(lines)
    # print(f"answer={getMulSum(text)}")
    donts = text.split("don't()")
    # print(f"{donts[:1]=}")
    res = getMulSum(donts[0])
    for i in range(1, len(donts)):
        dont_text = donts[i]
        try:
            index = dont_text.index("do()")
            text = dont_text[index + len("do()"):]
            res += getMulSum(text)
        except:
            pass # do nothing (i.e. add nothing if no do()'s!)
        # except
    print(f"ANSWER: {res}")
    # exit()
    # print(f"{lines=}")

    # print(f"{pattern=}")
    # print(f"{matches}")

    # res = 0
    # for match in matches:
    #     num1, num2 = [int(num) for num in match[4:-1].split(",")]
    #     res += num1 * num2
    # print(f"{res=}")
    # print(
    #     f"ANSWER: {
    #         sum(
    #             num1 * num2 for num1, num2 in 
    #             map(
    #                 lambda match: [int(num) for num in match[4:-1].split(",")], 
    #                 re.findall(pattern, text)
    #             )
    #         )
    #     }"
    # )
