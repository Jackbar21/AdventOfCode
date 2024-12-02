from collections import defaultdict
file_name = "./data.txt"

d1 = defaultdict(int)
d2 = defaultdict(int)

with open(file_name, "r") as file:
    arr = file.readlines()
    for line in arr:
        num1, num2 = line.split(" " * 3)
        num1 = int(num1)
        if num2[-1] == '\n':
            num2 = int(num2[:-1])
        else:
            num2 = int(num2)

        d1[num1] += 1
        d2[num2] += 1
        # sorted_arr1.append(num1)
        # sorted_arr2.append(num2)

# sorted_arr1.sort()
# sorted_arr2.sort()
similarity_score = 0
for num in d1:
    similarity_score += num * d2.get(num, 0)
print(similarity_score)

# res = 0
# assert len(sorted_arr1) == len(sorted_arr2)
# for i in range(len(sorted_arr1)):
#     diff = sorted_arr1[i] - sorted_arr2[i]
#     res += abs(diff)

# print(f"{res=}")
