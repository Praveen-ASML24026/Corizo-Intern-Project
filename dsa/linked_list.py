class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self, limit=20):
        self.head = None
        self.limit = limit
        self.size = 0

    def add_first(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        self.size += 1
        # trim to limit
        if self.size > self.limit:
            # remove last
            cur = self.head
            prev = None
            for _ in range(self.limit-1):
                prev = cur
                cur = cur.next
            prev.next = None
            self.size = self.limit

    def print_all(self):
        current = self.head
        while current:
            print("->", current.data)
            current = current.next
