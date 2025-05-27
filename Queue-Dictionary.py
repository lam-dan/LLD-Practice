from collections import defaultdict
from typing import Any

# Queue using a Dictionary
class Queue:
    def __init__(self, capacity):
        self.cache = defaultdict(dict)
        self.capacity = capacity
        self.head = 1
        self.tail = 0
    
    def dequeue(self) -> Any:
        if self.get_current_size() > 0:
            element = self.cache[self.head]
            del self.cache[self.head]
            self.head += 1
            return element
        else:
            return -1
        
    # Check the capacity
    # Add elements if there is space
    # Remove elements in the front of the queue (head) and add elements
    def enqueue(self, value: Any) -> None:
        if self.get_current_size() >= self.get_capacity():
            del self.cache[self.head]
            self.head += 1
        self.tail += 1
        self.cache[self.tail] = value
        
    def get_current_size(self) -> int:
        return len(self.cache)
    
    def get_capacity(self) -> int:
        return self.capacity

test_queue = Queue(4)
test_queue.enqueue(1)
test_queue.enqueue(2)
test_queue.enqueue(3)
test_queue.enqueue(4)
print(test_queue.cache)
print("Head pointer", test_queue.head)
print("Tail pointer", test_queue.tail)
# print("Removed elements", test_queue.dequeue())
# print(test_queue.cache)

test_queue.enqueue(5)
print(test_queue.cache)
print("Head pointer", test_queue.head)
print("Tail pointer", test_queue.tail)

print("Dequeue", test_queue.dequeue())
print(test_queue.cache)
print("Head pointer", test_queue.head)
print("Tail pointer", test_queue.tail)

test_queue.enqueue(1)
test_queue.enqueue(1)
print(test_queue.cache)
print("Head pointer", test_queue.head)
print("Tail pointer", test_queue.tail)


# print(queue.queue)
# queue.enqueue(5)
# print(queue.queue)
# print(queue.dequeue())
# print(queue.get_current_size())
# print(queue.get_capacity())