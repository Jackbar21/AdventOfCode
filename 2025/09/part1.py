USE_TEST_DATA = False

file_name = "./data.txt" if not USE_TEST_DATA else "./test_data.txt"
with open(file_name, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    lines = [tuple(map(int, line.split(","))) for line in lines]

    def getRectangleSize(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

    res = 0
    points = lines
    N = len(points)
    for i in range(N):
        point1 = points[i]
        for j in range(i + 1, N):
            point2 = points[j]
            if res < (size := getRectangleSize(point1, point2)):
                res = size

    print(f"ANSWER: {res}")
