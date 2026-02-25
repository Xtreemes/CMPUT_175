#----------------------------------------------------
# Lab 4: Fruit Sorter
# 
# Author: CMPUT 175 Team
#----------------------------------------------------


class Stack:
    """
    A class representing a stack Abstract Data Type (ADT).
    Modify it slightly to fit the Stack Game requirements.
    Hint:
    It needs to have a maximum capacity and can be marked as 
    completed when all items are the same and the stack is full.
    """

    def __init__(self, size: int):
        """
        Initializes an empty stack.
        """
        self.items = []
        self._size = size
        self._completed = False
    
    def push(self, item):
        """
        Adds an item to the top of the stack.
        Inputs: The item to be added to the stack.
        Returns: None
        """
        length = len(self.items)
        assert length < self._size, "Cannot push to a locked or full stack"

        self.items.append(item)

        if length + 1 == self._size:
            self._completed = True

            item = self.items[0]
            index = 1
            while index < self._size and self._completed:
                if self.items[index] != item:
                    self._completed = False
                index += 1

    
    
    def pop(self): 
        """
        Removes and returns the top item from the stack.
        Inputs: None
        Returns: The item removed from the top of the stack.

        Raises:
            Exception: If the stack is empty.
        """
        assert not self._completed, "Cannot pop from a complete stack"
        assert not self.is_empty(), "Cannot pop from an empty stack"

        return self.items.pop(-1)
    
    
    def peek(self):  
        """
        Returns the top item of the stack without removing it.
        Inputs: None
        Returns: The top item of the stack.

        Raises:
            Exception: If the stack is empty.
        """
        assert not self.is_empty(), "Cannot peek at an empty stack"

        return self.items[-1]
         
    
    def is_empty(self):
        """
        Checks if the stack is empty.
        Inputs: None
        Returns: bool - True if the stack is empty, False otherwise.
        """
        return self.items == []
    
    def size(self):
        """
        Returns the number of items in the stack.
        Inputs: None
        Returns: int - The number of items in the stack.
        """
        return len(self.items)
    
    def show(self):
        """
        Prints the items in the stack.
        Inputs: None
        Returns: None
        """
        print(self.items)
    
    def __str__(self):
        """
        Returns a string representation of the stack.
        Inputs: None
        Returns: str - A string representation of the stack.
        """
        stackAsString = ''
        for item in self.items:
            stackAsString += item + ' '
        return stackAsString
    
    def clear(self):
        """
        Removes all items from the stack. Does nothing if the stack is empty.
        Inputs: None
        Returns: None
        """
        self.items = []

    def is_completed(self):
        return self._completed



def main():
    # ----- Stack tests (formatted) -----
    print("\n=== Stack tests ===")

    # Basic usage
    print("\n-- Basic operations --")
    s = Stack(4)
    print("Initially empty:", s.is_empty())

    s.push('A')
    s.push('B')
    s.push('C')
    print("After pushing A, B, C ->")
    print("  Stack contents:", end=" ")
    s.show()
    print(f"  Size: {s.size()}")
    print(f"  Peek (top): {s.peek()}")
    popped = s.pop()
    print(f"  Popped item: {popped}")
    print("  Stack now:", end=" ")
    s.show()
    print("  Is empty?:", s.is_empty())
    print("  String repr:", str(s))

    # Additional behavioural tests
    print("\n-- Additional tests (capacity & errors) --")
    # Test completed flag when pushing identical items up to capacity
    s2 = Stack(3)
    s2.push('X')
    s2.push('X')
    s2.push('X')
    print("s2 contents:", s2.items)
    print("s2 size:", s2.size())
    print("s2 completed?:", s2.is_completed())

    # Attempting to pop from a completed stack should raise
    try:
        s2.pop()
    except Exception as e:
        print("Expected error (pop completed):", e)

    # Attempting to push to a full/completed stack should raise
    try:
        s2.push('X')
    except Exception as e:
        print("Expected error (push completed/full):", e)

    # Test pop/peek on empty stack raise
    s3 = Stack(2)
    try:
        s3.pop()
    except Exception as e:
        print("Expected error (pop empty):", e)

    try:
        s3.peek()
    except Exception as e:
        print("Expected error (peek empty):", e)

    # Test transitions: push then pop to empty
    s4 = Stack(2)
    print("s4 is_empty initially:", s4.is_empty())
    s4.push('A')
    print("s4 size after one push:", s4.size())
    popped = s4.pop()
    print("s4 popped value:", popped)
    print("s4 is_empty after pop:", s4.is_empty())

    # Test __str__ formatting for multiple items
    s5 = Stack(4)
    s5.push('p')
    s5.push('q')
    print("s5 string repr:", str(s5))

if __name__ == "__main__":
    main()