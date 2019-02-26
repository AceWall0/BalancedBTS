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
        self._size = 0
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

    def add(self, num):
        print("adicionando node")
        if self.__root is None:
            self.__root = Node(num)
            self._size += 1
            return True

        current = self.__root
        while True:

            if num > current.data:
                if current.left is None:
                    current.left = Node(num, current)
                    self._size += 1
                    return True
                else: current = current.left

            elif num < current.data:
                if current.right is None:
                    current.right = Node(num, current)
                    self._size += 1
                    return True
                else: current = current.right

            # if num == current.data, the number already exist on the tree. So, do nothing
            else: return False


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