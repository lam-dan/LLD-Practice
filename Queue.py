from collections import defaultdict
from typing import Any

class Queue:
    def __init__(self, capacity):
        self.queue = defaultdict(dict)
        self.capacity = capacity
        self.head = 0
        self.tail = 0
    
    def dequeue(self) -> Any:
        if len(self.queue) > 0:
            element = self.queue[self.head]
            del self.queue[self.head]
            self.head += 1
            return element
        else:
            return -1
        
    # Check the capacity
    # Add elements if there is space
    # Remove elements in the front of the queue (head) and add elements
    def enqueue(self, value: Any) -> None:
        if len(self.queue) >= self.get_capacity():
            del self.queue[self.head]
            self.head += 1
        self.queue[self.tail] = value
        self.tail += 1

    def get_current_size(self) -> int:
        return len(self.queue)
    
    def get_capacity(self) -> int:
        return self.capacity

queue = Queue(4)
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
queue.enqueue(4)
print(queue.queue)
print(queue.dequeue())
print(queue.queue)
queue.enqueue(5)
print(queue.queue)
print(queue.dequeue())
print(queue.get_current_size())
print(queue.get_capacity())