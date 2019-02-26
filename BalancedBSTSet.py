## @package BalancedBSTSet
#
#  @author Wallace Alves dos Santos
#  @date 25/02/2019
#

from random import randint

## @author Wallace Alves dos Santos
class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.counter = 0
        self.left = None
        self.right = None

## @author Wallace Alves dos Santos
class BalancedBSTSet:
    def __init__(self, is_self_balancing=False, top=2, bottom=3):
        self.__size = 0
        self.__root = None
        self.numerator = top
        self.denominator = bottom or 3
        self.balanced = is_self_balancing
        print("estou usando essa árvore aqui")

    def root(self):
        return self.__root

    def rebalance(self, bstNode):
        """TODO: Executa a operação de rebalanceamento na subárvore que está enraizada no nó dado."""
        pass


    ##
     # Adds the given object to this tree.
     #
     # @param key given object.
     # @return True if the object was found, and False otherwise.
     #
    def add(self, num):
        print("adicionando node")
        if self.__root is None:
            self.__root = Node(num)
            self.__size += 1
            return True

        current = self.__root
        while True:

            if num > current.data:
                if current.left is None:
                    current.left = Node(num, current)
                    self.__size += 1
                    return True
                else: current = current.left

            elif num < current.data:
                if current.right is None:
                    current.right = Node(num, current)
                    self.__size += 1
                    return True
                else: current = current.right

            # if num == current.data, the number already exist on the tree. So, do nothing.
            else: return False


    ##
     # Removes the given object from this tree.
     #
     # @param obj given object.
     # @return True if the object was found, and False otherwise.
     #
    def remove(self, obj):
        n = self.findEntry(obj)
        if n is None: return False
        self.unlinkNode(n)
        return True


    ##
     # Returns the Node object containing key, or None if the key is not
     # found in the tree.
     # @param key
     # @return the node containing key, or None if not found.
     #
    def findEntry(self, key):
        current = self.__root
        while current is not None:
            if current.data == key: return current
            elif key < current.data:
                current = current.left
            else:
                current = current.right
        return None


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
        startNode = None
        if n.left and n.right:
            s = self.successor(n)
            n.data = s.data
            n = s  # causes s to be deleted in code below
            startNode = s.parent

        # n has at most one child
        replacement = None
        if n.left is not None: replacement = n.left
        elif n.right is not None: replacement = n.right

        # link replacement on tree in place of node n
        # (replacement may be None)
        if n.parent is None: self.__root = replacement
        else:
            if n == n.parent.left:
                n.parent.left = replacement
            else:
                n.parent.right = replacement

        if replacement: replacement.parent = n.parent
        self.__size -= 1


    ##
     # Returns the successor of the given node.
     # @param n
     # @return the successor of the given node in this tree,
     #   or None if there is no successor.
     #
    def successor(self, n):
        if n is None: return None

        elif n.right is not None:
            # leftmost entry in right subtree
            current = n.right
            while current.left is not None:
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
        if root is not None:
            return 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        else:
            return -1




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