USE_TEST_DATA = False

file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    line = file.readline()
    # print(f"{line=}")

    # Step 1: Convert into disk
    num_files = (len(line) + 1) // 2
    files = [line[i] for i in range(0, len(line), 2)]
    # print(f"FILES: {files=}, {len(files)=}, {num_files=}")

    d = {}
    for i in range(len(files)):
        d[i] = int(files[i])
    
    
    # print(f"{d=}")

    min_file_id = 0
    max_file_id = len(files) - 1

    is_file = True
    l, r = 0, len(line) - 1
    res = 0
    pos = 0
    space_index = -1
    while min_file_id <= max_file_id:
        if is_file:
            for _ in range(d[min_file_id]):
                res += min_file_id * pos
                # print(f"{res=}, case1")

                pos += 1
            
            del d[min_file_id]
            min_file_id += 1
            space_index += 2

        else:
            # space_index = d[min_file_id][INDEX] + 1
            # assert space_index < len(line) # TODO: Might need to fix this for general case...
            # TODO: optimize this obviously...
            # space_index = 2 * min_file_id + 1
            space_count = int(line[space_index])
            # print(f"{space_index=}, {space_count=}")

            while space_count > 0:
                file_count = min(space_count, d[max_file_id])
                for _ in range(file_count):
                    res += max_file_id * pos
                    # print(f"{res=}, case2")
                    pos += 1
                
                d[max_file_id] -= file_count
                if d[max_file_id] == 0:
                    del d[max_file_id]
                    max_file_id -= 1
                    assert max_file_id >= min_file_id # To check for later...
                
                space_count -= file_count
                
        
        is_file = not is_file
    
    print(f"ANSWER: {res}")
