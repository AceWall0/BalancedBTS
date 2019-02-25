## @package BalancedBSTSet
#
#  @author Wallace Alves dos Santos
#  @date 25/02/2019
#

## @author Wallace Alves dos Santos
class Node:
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.counter = 0
        self.left = None
        self.right = None

## @author Wallace Alves dos Santos
class BalancedBSTSet:
    def __init__(self, self_balanced=False, top=2, bottom=3):
        self._root = None
        self.top = top
        self.bottom = bottom or 3

    def root(self):
        return self._root

    def rebalance(self, bstNode):
        """TODO: Executa a operação de rebalanceamento na subárvore que está enraizada no nó dado."""
