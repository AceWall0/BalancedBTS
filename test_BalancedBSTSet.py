import unittest
from BalancedBSTSet import BalancedBSTSet


class TestBalancedBSTSet(unittest.TestCase):
    def setUp(self):
        self.bst = BalancedBSTSet(False)
        self.bst.add(3)
        self.bst.add(1)
        self.bst.add(7)
        self.bst.add(6)
        self.bst.add(8)

    def test_structure(self):
        self.assertEqual(self.bst.root.data, 3)
        self.assertEqual(self.bst.root.left.data, 1)
        self.assertEqual(self.bst.root.right.left.data, 6)
        self.assertEqual(self.bst.root.right.right.data, 8)


if __name__ == '__main__':
    unittest.main()