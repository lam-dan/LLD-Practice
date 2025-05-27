
from typing import Optional
class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None


class Queue:
    def __init__(self, capacity: int):
        self.cache = {}
        self.head = Node(None, None) # Sentinel Nodes
        self.tail = Node(None, None) # Sentinel Nodes
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity
        self.length = 0
    
    # Enqueue - Insert Nodes in the tail of the DLL
    def enqueue(self, key: int, value: int) -> int:
        # Check to see if key already exists
        # return error saying key has already been used
        if key in self.cache:
            raise ValueError("Can't use the same key again")
        
        if self.length >= self.capacity:
            self.dequeue()
        
        node = Node(key, value)
        self.cache[key] = node
        # Adding to the end of the queue process:
        tmp = self.tail.prev
        self.tail.prev = node
        node.next = self.tail
        node.prev = tmp
        tmp.next = node
        self.length += 1
        return node.value

    # Returning the value of the node
    def get_node(self, key: int) -> Optional[int]:
        if key in self.cache:
            node = self.cache[key]
            return node.value
        else:
            return None

    def put_node(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update cache and also update the DLL queue
            node = self.cache[key]
            node.value = value
            self.cache[key] = node
        else:
            # Add into cache and also DLL queue
            self.enqueue(key, value)
        
    # Dequeue - Removing Nodes in the front of the DLL
    def dequeue(self) -> Optional[int]:
        # Queue isn't empty
        if self.head.next == self.tail:
            return None
        
        node = self.head.next
        if node.key in self.cache:
            del self.cache[node.key]

        # Deleting it from the front of the queue in our DLL
        self.head.next = node.next
        node.next.prev = self.head
        
        self.length -= 1
        return node.value
        

    # Size - Return the current size of the DLL
    def size(self) -> int:
        return self.length


    # Peek Front - Return the node's value at the head of DLL
    def peek_front(self) -> Optional[int]:
        return self.head.next.value


    # Peek Back - Return the node's value at the tail of the DLL
    def peek_back(self) -> Optional[int]:
        return self.tail.prev.value

# Testing
fifoCache = Queue(5)
print("Node Value Added", fifoCache.enqueue(1,1))
print("Node Value Added", fifoCache.enqueue(2,2))
print("Node Value Added", fifoCache.enqueue(3,3))
print("Node Value Added", fifoCache.enqueue(4,4))
print("Node Value Added", fifoCache.enqueue(5,5))

print("Value Removed", fifoCache.dequeue())
print("Size", fifoCache.size())
print("Peeking Front", fifoCache.peek_front())
print("Peeking Back", fifoCache.peek_back())

print("Get Node", fifoCache.get_node(1))
print("Get Node", fifoCache.get_node(3))
print("Current Cache:", fifoCache.cache)

fifoCache.put_node(2,9)
print(fifoCache.peek_front())

fifoCache.put_node(9,8)
print("Current Cache:", fifoCache.cache)
print("Peeking Back", fifoCache.peek_back())