USE_TEST_DATA = False

import collections
import heapq

class ListNode:
    def __init__(self, val, index):
        self.val = val
        self.index = index
        self.offs = 0
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = ListNode(float("-inf"), -1) # dummy
        self.tail = ListNode(float("inf"), -1)  # dummy
        self.head.next = self.tail
        self.tail.prev = self.head

    def isEmpty(self) -> bool:
        if self.head.next == self.tail or self.tail.prev == self.head:
            assert self.head.next == self.tail and self.tail.prev == self.head
        return self.head.next == self.tail or self.tail.prev == self.head

    def deleteNode(self, node: ListNode) -> int:
        assert node not in [self.head, self.tail]
        prev_node, next_node = node.prev, node.nxt
        prev_node.next = next_node
        next_node.prev = prev_node
        return node.val
    
    def append(self, val, index) -> None:
        node = ListNode(val, index)
        last_node = self.tail.prev
        last_node.next = node
        node.next = self.tail
        self.tail.prev = node
        node.prev = last_node
    
    def appendleft(self, val, index) -> None:
        node = ListNode(val, index)
        first_node = self.head.next
        self.head.next = node
        node.next = first_node
        first_node.prev = node
        node.prev = self.head
    
    def pop(self) -> int:
        assert not self.isEmpty()
        last_node = self.tail.prev
        return self.deleteNode(last_node)
    
    def popleft(self) -> int:
        assert not self.isEmpty()
        first_node = self.head.next
        return self.deleteNode(first_node)
    
    def __str__(self):
        res = []
        node = self.head.next
        while node != self.tail:
            res.append(f"{node.val}({2 * node.index + 1}){node.offs if node.offs != 0 else ''}")
            node = node.next
        return str(res)

    def getFirstByFunc(self, func) -> ListNode | None:
        # Return first node such that func(node) returns True
        # If none exist, returns 'None'.
        # 'func' must be a function that takes a 'ListNode' as input, and returns
        # a 'bool' as output.
        node = self.head.next
        while node != self.tail:
            # print(f"{node.val=}, {func(node)=}")
            if func(node):
                return node
            node = node.next
        return None


file_name = "./test_data.txt" if USE_TEST_DATA else "./data.txt"
with open(file_name, "r") as file:
    line = file.readline()
    # print(f"{line=}")

    # Can't really do binary search, unfortunately will have to do a linear
    # scan each and every single time :((
    ll = LinkedList()

    # Step 1: Convert into disk
    num_files = (len(line) + 1) // 2
    files = [int(line[i]) for i in range(0, len(line), 2)]
    spaces = [int(line[i]) for i in range(1, len(line), 2)]

    # Populate linked list
    for i, space in enumerate(spaces):
        ll.append(space, i)
    # print(f"{str(ll)=}")
    # exit()

    # print(f"FILES: {files=}, {len(files)=}, {num_files=}")

    d = {}
    for i in range(len(files)):
        d[i] = files[i]
    
    
    # print(f"{d=}")

    min_file_id = 0
    max_file_id = len(files) - 1

    res = 0
    min_heap = []
    for file_id in range(max_file_id, min_file_id - 1, -1): # exclude min_file_id!
        file_index = file_id * 2
        # Find smallest valid free-space block!
        node = ll.getFirstByFunc(lambda node: node.val >= d[file_id] and 2 * node.index + 1 < file_index)
        if not node:
            # print(f"not node: {file_id=}")
            # No valid spaces, so cannot move it... TODO: append value to result
            # file_index = max_file_id * 2
            # for _ in range(d[max_file_id]):
            #     res += file_index * max_file_id
            #     file_index += 1
            heapq.heappush(min_heap, (file_index, 0, file_id))
            continue
        
        # print(f"node: {file_id=}, {node.val=}, {file_id=}, {d[file_id]=}")
        index = node.index
        free_space = node.val
        assert spaces[node.index] == free_space + node.offs
        # print(f"IMPORTANT: {spaces[node.index]}")
        # print(f"{str(ll)=}")
        heapq.heappush(min_heap, (2 * node.index + 1, node.offs, file_id))
        node.val -= d[file_id]
        node.offs += d[file_id]
        # print(f"{str(ll)=}")
        # exit()
    
    
    
    # print(f"{min_heap=}")
    # min_heap_copy = min_heap.copy()
    # print(f"{[heapq.heappop(min_heap_copy) for _ in range(len(min_heap))]}")
    # print(f"{d=}")
    # print(f"{str(ll)=}")

    arr = []
    is_file = True
    file_id = 0
    for digit in line:
        digit = int(digit)
        if is_file:
            arr.append([file_id] * digit)
            assert digit == d[file_id]
            file_id += 1
        else:
            arr.append([0] * digit) # 0, since 0 * X == 0 for any X, so no effect on res!!!
        
        is_file = not is_file
    
    # print(f"{arr=}")
    while len(min_heap) > 0:
        index, offs, file_id = heapq.heappop(min_heap)
        if index % 2 == 0:
            continue
            
        # Shift from where file_id currently is, to new position!
        count = d[file_id]
        file_index = 2 * file_id
        for i in range(count):
            assert arr[file_index][i] == file_id
            arr[file_index][i] = 0

            assert arr[index][offs + i] == 0
            arr[index][offs + i] = file_id

    pos = 0
    for row in arr:
        for file_id in row:
            res += file_id * pos
            pos += 1
    # print(f"{arr=}")

    ### TERMINATION ###
    print(f"ANSWER: {res}")
    exit()

    # queue = collections.deque([int(digit) for digit in line])
    # print(f"{queue=}")

    # res = 0

    # is_file = True
    # pos = 0
    # while len(min_heap) > 0:
    #     index, offs, file_id = heapq.heappop(min_heap)
    #     if index % 2 == 0:
    #         if not is_file:
    #             # Turn into next file index!
    #             assert len(queue) > 0
    #             pos += queue.popleft()
    #         assert queue[0] == d[file_id]
    #         for _ in range(d[file_id]):
    #             res += file_id * pos
    #             pos += 1
    #             queue[0] -= 1
            
    #         # Using up the already alloted file space, so pop again from queue!
    #         assert len(queue) > 0
    #         assert 0 == queue.popleft() # yoda programming moment
    #         # We're back into free space moment, so update is_file!
    #         is_file = False
    #         continue
            
    #     assert index % 2 == 1



    #     # print(f"{queue=}")
    #     # print(f"min_heap={sorted(min_heap)}")
        




    #     assert not is_file
    #     space_available = queue[0]
    #     assert d[file_id] <= space_available
    #     for _ in range(d[file_id]):
    #         res += file_id * pos
    #         pos += 1
    #         queue[0] -= 1
    #     assert queue[0] >= 0
    #     if queue[0] == 0:
    #         queue.popleft()
    #         is_file = True
    #         assert is_file
                


        
        


    # # is_file = True
    # # l, r = 0, len(line) - 1
    # # res = 0
    # # pos = 0
    # # space_index = -1
    # # while min_file_id <= max_file_id:
    # #     if is_file:
    # #         for _ in range(d[min_file_id]):
    # #             res += min_file_id * pos
    # #             # print(f"{res=}, case1")

    # #             pos += 1
            
    # #         del d[min_file_id]
    # #         min_file_id += 1
    # #         space_index += 2

    # #     else:
    # #         # space_index = d[min_file_id][INDEX] + 1
    # #         # assert space_index < len(line) # TODO: Might need to fix this for general case...
    # #         # TODO: optimize this obviously...
    # #         # space_index = 2 * min_file_id + 1
    # #         space_count = int(line[space_index])
    # #         # print(f"{space_index=}, {space_count=}")

    # #         while space_count > 0:
    # #             file_count = min(space_count, d[max_file_id])
    # #             for _ in range(file_count):
    # #                 res += max_file_id * pos
    # #                 # print(f"{res=}, case2")
    # #                 pos += 1
                
    # #             d[max_file_id] -= file_count
    # #             if d[max_file_id] == 0:
    # #                 del d[max_file_id]
    # #                 max_file_id -= 1
    # #                 assert max_file_id >= min_file_id # To check for later...
                
    # #             space_count -= file_count
                
        
    # #     is_file = not is_file
    
    # print(f"ANSWER: {res}")
