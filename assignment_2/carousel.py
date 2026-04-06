class DLinkedListNode:

    def __init__(self, data, next, previous):
        self._data = data
        self._next = next
        self._previous = previous

        if previous is not None:
            previous.setNext(self)
        if next is not None:
            next.setPrevious(self)

    def getData(self):
        return self._data

    def getNext(self):
        return self._next

    def getPrevious(self):
        return self._previous

    def setData(self, data):
        self._data = data

    def setNext(self, next):
        self._next = next

    def setPrevious(self, previous):
        self._previous = previous


class Carousel:

    def __init__(self):
        self._head = None
        self._current = None

    def add(self, data):

        if self._head is None:
            node = DLinkedListNode(data, None, None)

            node.setNext(node)
            node.setPrevious(node)

            self._head, self._current = node, node
        else:
            self._current = DLinkedListNode(data, self._current.getNext(), self._current)


    def moveNext(self):
        self._current = self._current.getNext()

    def movePrevious(self):
        self._current = self._current.getPrevious()

    def getCurrentData(self):
        return self._current.getData()

    def __str__(self):
        if self._head is None:
            return "[]"

        data = [self._head.getData()]

        current = self._head.getNext()
        while current != self._head:
            data.append(current.getData())
            current = current.getNext()

        return str(data)


def main():
    # Create a carousel
    carousel = Carousel()

    # Add some employees as strings
    carousel.add("Alice, HR, ID:101")
    carousel.add("Bob, Sales, ID:102")
    carousel.add("Charlie, IT, ID:103")
    carousel.add("Diana, Marketing, ID:104")

    # Print the carousel
    print("Full Carousel:")
    print(carousel)

    # Show the current employee
    print("\nCurrent Employee:")
    print(carousel.getCurrentData())

    # Move forward through the carousel
    carousel.moveNext()
    print("\nAfter moving next:")
    print(carousel.getCurrentData())

    # Move backward using movePrevious()
    carousel.movePrevious()
    print("Previous:", carousel.getCurrentData())

if __name__ == "__main__":
    main()