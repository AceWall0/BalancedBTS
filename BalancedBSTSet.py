## @package BalancedBSTSet
#
#  @author Wallace Alves dos Santos
#  @date 25/02/2019
#

from __future__ import print_function
import sys
from random import randint
# raise ImportError
print("Running BalancedBSTSet")


## @author Wallace Alves dos Santos
class Node:
    def __init__(self, data, parent):
        self.data = data
        self.parent: Node = parent
        self.counter = 0
        self.left: Node = None
        self.right: Node = None

    ## Compares the data of this node to a given key.
    #
    #  @return 1 if the data of this object is greater than key's, <br>
    #         -1 if the data of this object is smaller than key's or <br>
    #          0 if it is equal
    #
    def compareTo(self, key):
        return cmp(self.data, key)

    @property
    def size(self):
        return self.counter + 1

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f"Node: {self.data}, Children: {self.counter}, Size: {sys.getsizeof(self):d}B"
        # return "Node: %s, Size: %d" % (self.data, sys.getsizeof(self))


##
# @author Wallace Alves dos Santos
#
class BalancedBSTSet:
    def __init__(self, b=False, top=2, bottom=3):
        self.__root = None
        self.__size = 0
        self.selfbalanced = b
        self.top = top
        self.bottom = bottom


    ##
    # Returns a read-only view of the root node of this tree.
    # @return root node of this tree.
    #
    def root(self):
        return self.__root


    def rebalance(self, bstnode):
        pass  # TODO!!!


    ## Return whether this tree is empty.
    def isEmpty(self):
        return self.__root is None


    ##
    #  Executes an in order traversal of the tree rooted at a given node.
    #
    #  @param node root.
    #  @param arr array for holding the node data.
    #  @return arr.
    #
    def __inOrder(self, node, arr):
        if arr is None: arr = []
        if node:
            self.__inOrder(node.left, arr)
            arr.append(node)
            self.__inOrder(node.right, arr)
        return arr


    ##
    # Returns whether the given object is in this tree.
    #
    # @param obj given object.
    # @return True if the object is in the tree, or False otherwise.
    #
    def __contains__(self, obj):
        return self.findEntry(obj) is not None


    ##
    # Adds the given object to this tree.
    #
    # @param key given object.
    # @return True if the object was found, and False otherwise.
    #
    def add(self, key):
        if self.__root is None:
            self.__root = Node(key, None)
            self.__size += 1
            return True

        current = self.__root
        output = False
        while True:
            comp = current.compareTo(key)
            if comp == 0:
                # key is already in the tree
                break

            elif comp > 0:
                if current.left:
                    current = current.left
                else:
                    current.left = Node(key, current)
                    self.__size += 1
                    self.__update_counter(current.left)
                    break

            else:
                if current.right:
                    current = current.right
                else:
                    current.right = Node(key, current)
                    self.__size += 1
                    self.__update_counter(current.right)
                    break

        if self.selfbalanced:
            unbalanced = self.__find_unbalanced(current)
            if unbalanced:
                print('unbalanced node:', unbalanced)

        return output


    ## Verify if a Node is balanced.
    #
    #  @return True if it is balanced.
    #
    def __balanced(self, x: Node):
        left_size = x.left.size if x.left else 0
        right_size = x.right.size if x.right else 0

        balan_left = left_size * self.bottom <= x.size * self.top
        balan_right = right_size * self.bottom <= x.size * self.top
        return x if (balan_left and balan_right) else None


    ## Find the highest Node in the tree that is unbalanced.
    #
    #  @returns the unbalanced Node if there is one. Returns None otherwise.
    def __find_unbalanced(self, x: Node):
        current = x
        unb = None
        while True:
            if not self.__balanced(current): unb = current
            if current.parent: current = current.parent
            else: break
        return unb


    ## Increases or decreases the counter from the parent of a Node until the root.
    #
    #  @param increase False if you want to decrease.
    #
    def __update_counter(self, node, increase=True):
        amount = 1 if increase else -1
        current = node
        if not increase:
            current.counter += amount

        while current.parent:
            current = current.parent
            current.counter += amount


    ## Adds an iterable to the tree.
    def update(self, lst):
        for i in lst:
            self.add(i)


    ## like lists.
    def append(self, n):
        return self.add(n)


    ##
    # Removes the given object from this tree.
    #
    # @param obj given object.
    # @return True if the object was found, and False otherwise.
    #
    def remove(self, obj):
        n = self.findEntry(obj)
        if n is None: return False
        self.__update_counter(n, increase=False)
        self.unlinkNode(n)
        return True


    ##
    # Returns the node containing key, or None if the key is not
    # found in the tree.
    # @param key
    # @return the node containing key, or None if not found.
    #
    def findEntry(self, key):
        current = self.__root
        while current:
            comp = current.compareTo(key)
            if comp == 0:
                return current
            elif comp > 0:
                current = current.left
            else:
                current = current.right
        return None


    ##
    # Returns the successor of the given node.
    # @param n
    # @return the successor of the given node in this tree,
    #   or None if there is no successor.
    #
    def successor(self, n):
        if n is None: return None

        elif n.right:
            # leftmost entry in right subtree
            current = n.right
            while current.left:
                current = current.left
            return current
        else:
            # we need to go up the tree to the closest ancestor that is
            # a left child its parent must be the successor
            current = n.parent
            child = n
            while current and current.right == child:
                child = current
                current = current.parent
            # either current is None, or child is left child of current
            return current


    ##
    # Removes the given node, preserving the binary search
    # tree property of the tree.
    #
    # @param n node to be removed.
    #
    def unlinkNode(self, n):
        # first deal with the two-child case copy
        # data from successor up to n, and then delete successor
        # node instead of given node n

        # startNode = None
        if n.left and n.right:
            s = self.successor(n)
            n.data = s.data
            n = s  # causes s to be deleted in code below
            # startNode = s.parent

        # n has at most one child
        replacement = None
        if n.left:
            replacement = n.left
        elif n.right:
            replacement = n.right

        # link replacement on tree in place of node n
        # (replacement may be None)
        if n.parent is None:
            self.__root = replacement
        else:
            if n == n.parent.left:
                n.parent.left = replacement
            else:
                n.parent.right = replacement

        if replacement:
            replacement.parent = n.parent

        self.__size -= 1


    ## Returns an iterator for this tree.
    def iterator(self):
        return self.BSTIterator(self)


    ## Returns the number of elements in this tree.
    def __len__(self):
        return self.__size


    ## Returns an array containing all of the elements in the subtree
    #
    # @return a list of Node objects
    #
    def subArray(self, node: Node) -> list:
        left = []
        right = []

        if node.left: left = self.subArray(node.left)
        if node.right: right = self.subArray(node.right)

        return left + [node] + right


    ## Returns an array containing all of the elements in this tree.
    # If the collection makes any guarantees as to what order its elements
    # are returned by its iterator, this method must return the elements in the same order.
    #
    # @return a list of node data (keys).
    #
    def toArray(self):
        arr = []
        for n in self.iterator():
            arr.append(n)
        return arr


    ## Indexing operator [].
    #
    # @throw IndexError.
    # @param ind index to retrieve.
    # @return ind-ith value in the tree, or an exception.
    #
    def __getitem__(self, ind):
        if ind < 0 or ind >= self.__size:
            raise IndexError

        for i, n in enumerate(self.iterator()):
            if i == ind:
                return n


    ## Iterator as a generator.
    def __iter__(self):
        for n in self.iterator():
            yield n


    ## Return the height of this tree.
    # The height of a tree is the height of its root node.
    #
    def height(self):
        return self.getHeight(self.__root)


    ## Return the height of a subtree.
    # The height of a node is the number of edges on the longest path between that node and a leaf.
    # The height of a leaf is 0.
    #
    # @param root node of the subtree.
    #
    def getHeight(self, root):
        if root:
            return 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        else:
            return -1


    ##
    # Returns a representation of this tree as a multi-line string.
    # The tree is drawn with the root at the left and children are
    # shown top-to-bottom.  Leaves are marked with a "-" and non-leaves
    # are marked with a "+".
    #
    def __repr__(self):
        sb = []
        self.__toStringRec(self.__root, sb, 0)
        return ''.join(sb)


    ## Prints the nodes of this tree in order.
    def __str__(self):
        st = ""
        for n in self:
            st += str(n) + " "
        return st


    ##
    # Preorder traversal of the tree that builds a string representation
    # in the given StringBuilder.
    #
    # @param n root of subtree to be traversed.
    # @param sb list in which to create a string representation.
    # @param depth depth of the given node in the tree.
    #
    def __toStringRec(self, n, sb, depth):
        sb.append("  " * depth)
        if n is None:
            sb.append("-\n")
            return
        if n.left or n.right:
            sb.append("+ ")
        else:
            sb.append("- ")

        sb.append(str(n))
        sb.append("\n")
        if n.left or n.right:
            self.__toStringRec(n.left, sb, depth + 1)
            self.__toStringRec(n.right, sb, depth + 1)


    ##
    # Iterator implementation for this binary search tree. The elements
    # are returned in ascending order according to their natural ordering.
    #
    class BSTIterator(object):
        ## return the smallest value of the tree.
        def getSmallestValue(self, n):
            if n:
                while n.left:
                    n = n.left
            return n


        ##
        # Constructs an iterator starting at the smallest
        # ot largest element in the tree.
        #
        def __init__(self, tree):
            ## Node returned by last call to next() and available
            #  for removal. This field is None when no node is
            #  available to be removed.
            self.__pending = None

            ## The tree to be traversed.
            self.__tree = tree

            ## Node to be returned by next call to next().
            self.__current = self.getSmallestValue(self.__tree.root())


        ## Forward iterator.
        def __iter__(self):
            # start out at smallest value
            self.__current = self.getSmallestValue(self.__tree.root())
            return self


        ##
        # Whether current is not None.
        #
        def hasNext(self):
            return self.__current is not None


        ## Return the content of the current node without advancing.
        def peek(self):
            if self.__current is None: return None
            return self.__current.data


        ##
        # Returns current node, which is saved in pending.
        # Current is set to successor(current).
        #
        def __next__(self):
            if not self.hasNext(): raise StopIteration
            self.__pending = self.__current
            self.__current = self.__tree.successor(self.__current)
            return self.__pending.data


        ## For python 2.
        def next(self):
            return self.__next__()


        ##
        # Removes the node returned by the last call to next().
        # Current pos to the successor of
        # pending, but if pending has two children, then
        # unlinkNode(pending) will copy the successor's data
        # o pending and delete the successor node.
        # So in this case, we want to end up with current
        # poing to the pending node.
        #
        def remove(self):
            if self.__pending is None: raise IndexError
            if self.__pending.left and self.__pending.right:
                self.__current = self.__pending

            # subtract the counter in the parent nodes before unlink it
            self.__tree.__update_counter(self.__pending, False)
            self.__tree.unlinkNode(self.__pending)
            self.__pending = None




## Compare two objects.
#
# @return (x > y) - (x < y)
#
def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.
    """
    return (x > y) - (x < y)


##
#  Generates an array with a random size,
#  filled with random elements.
#
#  @param n maximum array size.
#  @param vrange interval to choose the random elements from.
#  @return an array.
#
def generateRandomArray(n, vrange):
    v = []
    for i in range(randint(1, n)):
        v.append(randint(1, vrange))
    return v
