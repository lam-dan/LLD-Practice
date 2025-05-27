class Node:
    def __init__(self, val):
        self.next = None
        self.val = val

class Queue:
    def __init__(self):
        self.tail = self.head = Node(None)
        self.length = 0
     
    def enqueue(self, val):
        node = Node(val)
        self.tail.next = node
        self.tail = node
        self.length += 1
    
    def dequeue(self):
        if self.head.next is None:
            return None
        
        tmp = self.head.next
        self.head.next = tmp.next
        self.length -= 1

        if self.head.next is None:
            self.tail = self.head

        tmp.next = None
        return tmp.val
    
    def peek_front(self):
        return self.head.next.val if self.head.next else None
    
    def peek_back(self):
        return self.tail.val if self.tail != self.head else None
    

    def size(self):
        return self.length

queue = Queue()
queue.enqueue(4)
queue.enqueue(3)
queue.enqueue(2)
queue.enqueue(1)
print(queue.head.next.val)
print(queue.tail.val)
print("deque", queue.dequeue())
print(queue.head.next.val)
print(queue.tail.val)
print(queue.peek_front())
print(queue.peek_back())
print(queue.size())

